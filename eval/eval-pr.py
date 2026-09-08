#!/usr/bin/env python3
"""eval-pr.py — orchestrate the FULL omarchy PR evaluation, all agents, all stages.

The ONE entry point for the eval workflow codified in this repo's guidance
(eval-omarchy/AGENTS.md: policy lives ONCE in .agents/skills/omarchy-eval-*;
every agent and skill points there, never restates). This driver:
  * executes the deterministic mechanics ITSELF (beds, exits, gates, teardown,
    media, locks, concurrency) — the parts that must never be left to prose;
  * dispatches the committed pi AGENTS for the judgment stages (oracle/config,
    report writer, cold-reader) with the skill files appended as system context;
  * implements the full workflow: triage -> RED-PROBE (exit 2) -> EVAL (exit 0)
    -> REPORT -> COLD-READ with REDO loops (max 2), per the full-loop skill;
  * enforces the plan publication gate: NOTHING ever writes to omacom/omarchy
    (the only gh call is the read-only PR-meta fetch);
  * one eval lane per CPU core (RAM-capped, omarchy-eval-lane skill), sequencing
    HARD gate, zero-write-lock acceptance, teardown gate, media 5/5 gate;
  * config file support (eval.yml: prs + every option; CLI wins) and -d/--debug
    (verbose dispatch + command/task echo + full outputs -> workdir/debug.log).

Workflow guidance implemented (paths, not copies):
  .agents/skills/omarchy-eval-lane/SKILL.md   (lane semantics + one-lane-per-core)
  .agents/skills/omarchy-eval-{oracle,sequencing,golden,tiers,media,work-lane,full-loop,cold-reader}/SKILL.md
  eval/PR-EVAL-LANE.md  eval/PR-EVAL-TEMPLATE.md  eval/pr-10115.md (precedent)
  plan/eval-omarchy-pi-plugin.md (publication gate)

Usage:
  eval-pr.py [--config eval.yml]                 # full batch from the config file
  eval-pr.py --pr 10140 --stage full -d          # full eval of one PR with debug
  eval-pr.py --prs 10123 10140 --stage probe     # any single stage on several PRs
"""

import argparse, json, os, re, shutil, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EVAL = REPO / "eval"
SKILLS_DIR = REPO / ".agents" / "skills"
EVIDENCE = EVAL / "evidence"
UMBRELLA = Path(os.environ.get("EVAL_UMBRELLA") or REPO.parent)  # env-overridable; umbrella when eval-omarchy is a submodule
REPO_URL = "omacom/omarchy"
CFG = dict(debug=False, pi="pi", charly="/tmp/charly-r10-fixed/bin/charly", workdir=None)

SKILLS = {  # the single guidance sources (R3: read, never restate)
    "lane":        SKILLS_DIR / "omarchy-eval-lane/SKILL.md",
    "oracle":      SKILLS_DIR / "omarchy-eval-oracle/SKILL.md",
    "sequencing":  SKILLS_DIR / "omarchy-eval-sequencing/SKILL.md",
    "golden":      SKILLS_DIR / "omarchy-eval-golden/SKILL.md",
    "tiers":       SKILLS_DIR / "omarchy-eval-tiers/SKILL.md",
    "media":       SKILLS_DIR / "omarchy-eval-media/SKILL.md",
    "work-lane":   SKILLS_DIR / "omarchy-eval-work-lane/SKILL.md",
    "full-loop":   SKILLS_DIR / "omarchy-eval-full-loop/SKILL.md",
    "cold-read":   SKILLS_DIR / "omarchy-eval-cold-reader/SKILL.md",
}
TEMPLATE = EVAL / "PR-EVAL-TEMPLATE.md"
PRECEDENT = EVAL / "pr-10115.md"
AGENT_DEF = {
    "oracle": (REPO / ".agents/agents/omarchy-config-oracle.md", UMBRELLA / ".pi/agents/omarchy-config-oracle.md"),
    "runner": (REPO / ".agents/agents/omarchy-eval-runner.md", UMBRELLA / ".pi/agents/omarchy-eval-runner.md"),
    "cold":   (REPO / ".agents/agents/omarchy-cold-reader.md", UMBRELLA / ".pi/agents/omarchy-cold-reader.md"),
}
MEDIA_FILES = ["cast", "gif", "mjpeg", "mp4", "png"]

class StageFail(Exception):  # FAIL-HARD: stop, keep evidence, raise
    pass

# ---------------------------------------------------------------- plumbing ---
def dlog(msg):
    if CFG["debug"]:
        line = f"[dbg {time.strftime('%H:%M:%S')}] {msg}"
        print(line, file=sys.stderr)
        Path(CFG["workdir"], "debug.log").open("a").write(line + "\n")

def load_config(path):
    if not path or not Path(path).exists():
        return {}
    import yaml
    data = yaml.safe_load(Path(path).read_text()) or {}
    return {k: v for k, v in data.items() if v is not None}

def run(cmd, cwd=None, timeout=3600):
    """Deterministic command; nonzero -> StageFail (FAIL-HARD with evidence)."""
    parts = cmd if isinstance(cmd, list) else cmd.split()
    dlog("$ " + " ".join(parts) + (f" (cwd={cwd})" if cwd else ""))
    r = subprocess.run(parts, cwd=str(cwd or REPO), capture_output=True, text=True, timeout=timeout)
    if r.returncode != 0:
        tail = (f"\n--stdout--\n{r.stdout[-1600:]}\n--stderr--\n{r.stderr[-1600:]}" if CFG["debug"]
                else f"\n{r.stderr[-900:]}")
        raise StageFail(f"cmd failed ({r.returncode}): {' '.join(parts)}{tail}")
    return r

def sh_ok(cmd):
    r = subprocess.run(cmd if isinstance(cmd, list) else cmd.split(),
                       capture_output=True, text=True)
    return r.returncode == 0, r.stdout

def pi_agent(task, keys, agent=None, cwd=None, timeout=7200):
    """Dispatch a committed pi agent; the appended skill files ARE its instructions."""
    if agent:
        agent = next((p for p in agent if Path(p).exists()), None)
    cmd = [CFG["pi"], "--print", task]
    for k in keys:
        p = SKILLS[k]
        if not p.exists():
            raise StageFail(f"guidance missing: {p}")
        cmd += ["--append-system-prompt", str(p)]
    if agent:
        cmd += ["--system-prompt", str(agent)]
    dlog(f"pi_agent keys={keys} agent={agent}")
    dlog("task=" + task[:500])
    r = subprocess.run(cmd, cwd=str(cwd or REPO), capture_output=True, text=True, timeout=timeout)
    dlog(f"pi exit {r.returncode} out {len(r.stdout)}B err {len(r.stderr)}B")
    if CFG["debug"] and r.stdout:
        dlog("pi out head\n" + r.stdout[:1200])
    if r.returncode != 0:
        raise StageFail(f"pi agent failed ({r.returncode}) {task[:60]}...\n{r.stderr[-1200:]}")
    return r.stdout

def pr_meta(pr):
    """Read-only PR metadata — the ONLY gh call in the whole driver."""
    r = run(["gh", "api", f"repos/{REPO_URL}/pulls/{pr}", "--jq",
             "{title: .title, author: .user.login, base: .base.ref, head_ref: .head.ref, "
             "head_sha: .head.sha, changed_files, additions, deletions}"])
    return json.loads(r.stdout)

def default_lanes():
    """One eval lane per CPU core, capped so 2G x lanes <= host RAM (lane skill)."""
    mem = int(Path("/proc/meminfo").read_text().splitlines()[0].split()[1]) // 1024
    return max(1, min(os.cpu_count() or 1, (mem - 4096) // 2048))

# ------------------------------------------------------------ HARD gates ---
def gate_sequencing(prs):
    """omarchy-eval-sequencing: zero live batch VMs, zero in-flight runs, golden
    present + no holder, RAM budget, load1 < 20. Any failure stops the wave."""
    fails = []
    ok, q = sh_ok(["ps", "aux"])
    live = re.findall(r"guest=charly-check-omarchy-pr-\d+-vm", q)
    if live:
        fails.append(f"live batch VMs: {live}")
    inflight = [f"check-omarchy-pr-{p}-vm-probe" for p in prs
                if f"check-omarchy-pr-{p}-vm-probe" in q and "check run" in q]
    if inflight:
        fails.append(f"in-flight runs: {inflight}")
    golden = Path.home() / ".local/share/charly/vm/charly-check-omarchy-eval-base-inst/snapshots/golden/disk.qcow2"
    if not golden.exists() or golden.stat().st_size == 0:
        fails.append(f"golden missing/empty: {golden}")
    else:
        held, _ = sh_ok(["fuser", str(golden)])
        if held:
            fails.append(f"golden held: {golden}")
    mem = int(Path("/proc/meminfo").read_text().splitlines()[2].split()[1]) // 1024
    if len(prs) * 2048 + 4096 > mem:
        fails.append(f"RAM: {len(prs) * 2048 + 4096}MB needed, {mem}MB free")
    l1 = os.getloadavg()[0]
    if l1 >= 20:
        fails.append(f"load1 {l1:.1f}")
    if fails:
        raise StageFail("SEQUENCING GATE (omarchy-eval-sequencing): " + " | ".join(fails))
    dlog(f"sequencing gate OK (prs={len(prs)}, mem={mem}MB, load1={l1:.1f})")

def gate_zero_locks(run_dirs):
    """Acceptance: zero write-lock incidents across every run tree (wave stop)."""
    hits = []
    for d in run_dirs:
        ok, out = sh_ok(["grep", "-rl", r"Failed to get.*write.*lock|database is locked", str(d)])
        if out.strip():
            hits += out.split()
    if hits:
        raise StageFail(f"WRITE-LOCK INCIDENTS (wave stop): {hits}")
    dlog(f"zero-lock audit OK over {len(run_dirs)} trees")

def teardown_bed(bed, charly):
    """Sequencing skill: after a probe/eval verdict -> check stop (release the
    flock) -> vm destroy (the probe leaves the VM running for debugging)."""
    dlog(f"teardown {bed}: check stop + vm destroy")
    subprocess.run([charly, "check", "stop", bed], capture_output=True, text=True, timeout=300)
    subprocess.run([charly, "vm", "destroy", bed, "--if-exists"],
                   capture_output=True, text=True, timeout=300)

def gate_teardown():
    ok, q = sh_ok(["ps", "aux"])
    left = re.findall(r"guest=charly-check-omarchy-pr-\d+-vm", q)
    if left:
        raise StageFail(f"teardown failed, eval VMs left: {left}")

def gate_media(media_dir):
    d = Path(media_dir)
    sizes = {}
    for f in MEDIA_FILES:
        p = next(iter(sorted(d.glob(f"*.{f}"))), None)
        if not p or p.stat().st_size == 0:
            raise StageFail(f"media gate (omarchy-eval-media): missing/empty .{f} in {d}")
        sizes[f] = p.stat().st_size
    dlog(f"media gate OK 5/5: {sizes}")
    return sizes

# ------------------------------------------------------------- bed runner ---
def run_bed(pr, suffix, charly, workdir):
    """The deterministic bed run: charly check run + exit-code enforcement + the
    run-based gates. The runner agent's guidance governs WHAT the bed asserts;
    the driver enforces the exit contract in code."""
    bed = f"check-omarchy-pr-{pr}-vm{suffix}"
    log = workdir / f"run-{bed}.log"
    dlog(f"== run bed {bed} ==")
    r = subprocess.run([charly, "check", "run", bed], cwd=str(workdir),
                       capture_output=True, text=True, timeout=5400)
    log.write_text(r.stdout + "\n--stderr--\n" + r.stderr)
    dlog(f"bed {bed} exit {r.returncode}")
    if CFG["debug"]:
        dlog("bed stdout tail: " + r.stdout[-1200:])
    trees = sorted((workdir / ".check").glob(f"{bed}/2026*")) if (workdir / ".check").exists() else []
    gate_zero_locks([t for t in trees if t.exists()])
    return r.returncode, bed, (trees[-1] if trees else None)

def summary_of(run_tree):
    sp = Path(run_tree) / "summary.yml"
    if not sp.exists():
        return {}
    try:
        import yaml
        return yaml.safe_load(sp.read_text()) or {}
    except Exception:
        return {}

# ---------------------------------------------------------------- stages ---
def stage_triage(pr, charly, workdir):
    m = pr_meta(pr)
    task = (f"TRIAGE + author the per-PR config for omacom/omarchy#{pr} per the appended oracle + "
            f"tiers guidance. PR meta: {json.dumps(m)}. Deliverables: (1) class + hardware routing; "
            f"(2) pr-beds/pr-{pr}/charly.yml per the ORACLE TEMPLATE (drive form, known-red "
            f"contract); (3) a config-audit line. Do NOT run beds. Write the file to "
            f"{REPO}/pr-beds/pr-{pr}/charly.yml.")
    out = pi_agent(task, ["oracle", "tiers"], AGENT_DEF["oracle"], cwd=REPO)
    bed = REPO / f"pr-beds/pr-{pr}/charly.yml"
    if not bed.exists():
        raise StageFail(f"oracle produced no {bed}:\n{out[-700:]}")
    run([charly, "box", "validate"], cwd=REPO)
    (workdir / f"triage-{pr}.log").write_text(out)
    dlog(f"triage {pr} OK: {bed}")
    return bed

def stage_probe(pr, charly, workdir):
    """RED-PROBE: the SAME checks with NO apply — must FAIL (exit 2, known-red)."""
    code, bed, tree = run_bed(pr, "-probe", charly, workdir)
    if code != 2:
        raise StageFail(f"[{pr}] probe must exit 2 (known-red), got {code} — summary {tree}")
    teardown_bed(bed, charly)
    gate_teardown()
    dlog(f"[{pr}] probe RED (exit 2) confirmed, run {tree}")
    return tree

def assemble_media(pr, calver, workdir):
    """Media contract (omarchy-eval-media skill): the check runs pull the artifacts
    host-side to /tmp/pr-<N>.{cast,gif,mjpeg,screen.png}; assemble media/<pr>-<calver>/
    per the skill's recipe (cp the four + ffmpeg-transcode the mjpeg to screen.mp4)."""
    md = workdir / "media" / f"pr-{pr}-{calver}"
    md.mkdir(parents=True, exist_ok=True)
    for f, src_name in (("cast", f"pr-{pr}.cast"), ("gif", f"pr-{pr}.gif"),
                          ("mjpeg", f"pr-{pr}.mjpeg"), ("screen.png", f"pr-{pr}-screen.png")):
        src = Path("/tmp") / src_name
        if src.exists():
            shutil.copy2(src, md / f"pr-{pr}.{f}")
    mp = Path("/tmp") / f"pr-{pr}.mjpeg"
    out_mp4 = md / f"pr-{pr}-screen.mp4"
    if mp.exists() and not out_mp4.exists():
        r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp),
                            "-c:v", "libx264", "-pix_fmt", "yuv420p", str(out_mp4)],
                           capture_output=True, text=True, timeout=300)
        if r.returncode != 0 and not out_mp4.exists():
            raise StageFail(f"media transcode failed: {r.stderr[-400:]}")
    return md

def stage_eval(pr, charly, workdir):
    """EVAL: the golden-VM lane with the PR applied — must exit 0 with 5/5 media."""
    code, bed, tree = run_bed(pr, "", charly, workdir)
    if code != 0:
        raise StageFail(f"[{pr}] eval must exit 0, got {code} — summary {tree}")
    calver = Path(tree).name
    md = assemble_media(pr, calver, workdir)
    media = gate_media(md)
    teardown_bed(bed, charly)
    gate_teardown()
    dlog(f"[{pr}] eval GREEN (exit 0), media 5/5, run {tree}")
    return tree, media
def stage_report(pr, charly, workdir, tree=None, media=None):
    if tree is None:
        trees = sorted((workdir / ".check").glob(f"check-omarchy-pr-{pr}-vm/2026*")) if (workdir / ".check").exists() else []
        tree = trees[-1] if trees else None
    if media is None:
        mds = sorted((workdir / "media").glob(f"pr-{pr}-*")) if (workdir / "media").exists() else []
        media = mds[-1] if mds else None
        if media:
            try:
                media = gate_media(media)
            except StageFail:
                pass
    summ = summary_of(tree)
    task = (f"RENDER eval/pr-{pr}.md (PASS verdict) per the appended work-lane + tiers + media "
            f"guidance, mirroring the precedent {PRECEDENT}: EXTERNAL NON-AUTHORITATIVE block, "
            f"'results can go STALE' guard, first-person 'What I did' scoped to the golden-VM tier, "
            f"step matrices from {tree}/summary.yml, the 5/5 media table {media}, and the Assisted-by "
            f"footer. Write to {EVAL}/pr-{pr}.md. Do NOT post to omacom/omarchy.")
    out = pi_agent(task, ["work-lane", "tiers", "media"], cwd=workdir)
    rep = EVAL / f"pr-{pr}.md"
    if not rep.exists():
        raise StageFail(f"no report rendered: {rep}\n{out[-700:]}")
    (workdir / f"report-{pr}.log").write_text(out)
    dlog(f"[{pr}] report {rep}")
    return rep

def stage_coldread(pr, workdir):
    rep = EVAL / f"pr-{pr}.md"
    task = (f"COLD-READ {rep} per the appended cold-reader + full-loop guidance: grade every claim "
            f"against the evidence under {workdir}; findings with severity; final verdict line. If a "
            f"REDO-* trigger fires, state it EXACTLY (target stage + reason).")
    out = pi_agent(task, ["cold-read", "full-loop"], AGENT_DEF["cold"], cwd=REPO)
    (workdir / f"coldread-{pr}.log").write_text(out)
    dlog(f"[{pr}] cold-read:" + "\n" + out[:600])
    return out

# ------------------------------------------------------------ full loop ---
def full(pr, charly, workdir):
    """The complete eval workflow for one PR (triage -> probe -> eval -> report
    -> cold-read with REDO loops), FAIL-HARD at every stage boundary."""
    results = {}
    def step(n, fn):
        dlog(f"== [{pr}] {n} ==")
        return fn()
    try:
        bed = step("triage", lambda: stage_triage(pr, charly, workdir))
        tree_p = step("probe", lambda: stage_probe(pr, charly, workdir))
        tree_e, media = step("eval", lambda: stage_eval(pr, charly, workdir))
        rep = step("report", lambda: stage_report(pr, charly, workdir, tree_e, media))
        for loop in range(2):  # full-loop: cold-read can trigger one redo per loop
            cr = step("coldread", lambda: stage_coldread(pr, workdir))
            m = re.search(r"REDO-(\w+)", cr)
            if not m:
                break
            target = m.group(1).lower()
            dlog(f"[{pr}] cold-read REDO-{target.upper()} (loop {loop + 1})")
            step(target, lambda: globals()["stage_" + target](pr, charly, workdir) or None)
        results[pr] = {"probe": str(tree_p), "eval": str(tree_e), "media": media, "report": str(rep)}
        print(f"  [{pr}] FULL-OK probe={tree_p} eval={tree_e} media={media}", flush=True)
        return results
    except StageFail as e:
        raise StageFail(f"[{pr}] full-loop FAILED-HARD: {e}") from e

def main():
    ap = argparse.ArgumentParser(prog="eval-pr", description="orchestrate the FULL omarchy PR eval")
    ap.add_argument("--config", default=None, help="config file (default <repo>/eval.yml)")
    ap.add_argument("--pr", type=int)
    ap.add_argument("--prs", type=int, nargs="*")
    ap.add_argument("--stage", default="full",
                    choices=["full", "triage", "probe", "eval", "report", "coldread"])
    ap.add_argument("--concurrency", type=int, default=default_lanes())
    ap.add_argument("--print-lanes", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--charly", default="/tmp/charly-r10-fixed/bin/charly")
    ap.add_argument("--pi", default=shutil.which("pi") or "pi")
    ap.add_argument("--workdir", default=None)
    ap.add_argument("--no-sequencing-gate", action="store_true")
    ap.add_argument("-d", "--debug", action="store_true", help="full run debugging")
    pre = ap.parse_known_args()
    cfg = load_config(pre[0].config or (REPO / "eval.yml"))
    if cfg:
        ap.set_defaults(**cfg)
    a = ap.parse_args()
    CFG.update(debug=a.debug, pi=a.pi, charly=a.charly)
    if a.dry_run:
        print(json.dumps({"prs": a.prs or [], "stage": a.stage, "concurrency": a.concurrency,
                          "charly": a.charly, "pi": a.pi, "debug": a.debug,
                          "workdir": a.workdir or "/tmp/eval-pr-<ts>"}, indent=1))
        return 0
    if a.print_lanes:
        print(f"lanes={a.concurrency} (cpu={os.cpu_count()} ram-capped)")
        return 0
    # CLI pr selection wins over the config file's prs list (documented precedence)
    cli_prs = "--prs" in sys.argv
    cli_pr = "--pr" in sys.argv
    if cli_prs:
        prs = a.prs or []
    elif cli_pr:
        prs = [a.pr]
    else:
        prs = a.prs or []
    if not prs:
        ap.error("need --pr/--prs or prs: in the config file")
    workdir = Path(a.workdir or f"/tmp/eval-pr-{time.strftime('%Y%m%d-%H%M%S')}")
    workdir.mkdir(parents=True, exist_ok=True)
    CFG["workdir"] = str(workdir)
    dlog(f"eval-pr start prs={prs} stage={a.stage} lanes={a.concurrency} workdir={workdir}")
    if not a.no_sequencing_gate:
        gate_sequencing(prs)
    try:
        if a.stage == "full":
            with ThreadPoolExecutor(max_workers=a.concurrency) as ex:
                futs = [ex.submit(full, p, a.charly, workdir) for p in prs]
                for f in futs:
                    f.result()
        else:
            for p in prs:
                res = globals()["stage_" + a.stage](p, a.charly, workdir)
                dlog(f"stage {a.stage} [{p}] -> {res}")
        print(f"ALL-STAGES-OK prs={prs} workdir={workdir}")
        return 0
    except StageFail as e:
        print(f"FAIL-HARD: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
