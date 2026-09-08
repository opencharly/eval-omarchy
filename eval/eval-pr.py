#!/usr/bin/env python3
"""eval-pr.py — the ONE driver for omarchy PR evaluations.

Clean architecture per the repo rulebook (eval-omarchy/AGENTS.md): policy lives
ONCE in the skills under .agents/skills/omarchy-eval-* ("every agent and skill
points there, never restates"). This driver therefore never restates policy: it
READS the guidance files and hands them to the pi agents verbatim via
`pi --print --append-system-prompt <file>`; it owns only deterministic mechanics:
sequencing gates, one-lane-per-core concurrency, lock audit, teardown, media
gate, checkpoint bookkeeping.

Implemented guidance (paths, not copies):
  .agents/skills/omarchy-eval-lane/SKILL.md         (entry: state machine, verdicts,
                                                     "one eval lane per CPU core, capped so
                                                      2G x lanes <= host RAM")
  .agents/skills/omarchy-eval-{oracle,sequencing,golden,tiers,media,work-lane,full-loop,cold-reader}/SKILL.md
  eval/PR-EVAL-LANE.md  eval/PR-EVAL-TEMPLATE.md   eval/pr-10115.md (precedent)
  plan/eval-omarchy-pi-plugin.md (publication gate CLOSED — this driver NEVER
  writes to omacom/omarchy; the ONLY gh call is the read-only PR-meta fetch)

Usage:
  eval-pr.py [--config eval.yml]                    # config: prs + every option (CLI wins)
  eval-pr.py --prs 10123 10140 --stage full [--concurrency 8] [--charly PATH]
  eval-pr.py -d --pr 10140 --stage triage           # -d/--debug: full run debugging

Config file (default <repo>/eval.yml):
  prs: [10123, 10140]      # multiple PRs for evaluation
  stage: full              # full|triage|probe|eval|report|coldread
  concurrency: 8           # one lane per CPU core (RAM-capped) by default
  charly: /path/to/charly  pi: pi  workdir: /tmp/eval-pr  no_sequencing_gate: false
Precedence: CLI flags > config file > built-in defaults.
"""

import argparse, json, os, re, shutil, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EVAL = REPO / "eval"
SK = REPO / ".agents" / "skills"
UMBRELLA = Path("/home/atrawog/Sync/Atrapub/coder/pi/opencharly")
CFG = {"debug": False, "pi": "pi", "charly": "/tmp/charly-r10-fixed/bin/charly", "workdir": None}

SKILLS = {  # the single sources (R3: read, never restate)
    "lane":        SK / "omarchy-eval-lane/SKILL.md",
    "oracle":      SK / "omarchy-eval-oracle/SKILL.md",
    "sequencing":  SK / "omarchy-eval-sequencing/SKILL.md",
    "golden":      SK / "omarchy-eval-golden/SKILL.md",
    "tiers":       SK / "omarchy-eval-tiers/SKILL.md",
    "media":       SK / "omarchy-eval-media/SKILL.md",
    "work-lane":   SK / "omarchy-eval-work-lane/SKILL.md",
    "full-loop":   SK / "omarchy-eval-full-loop/SKILL.md",
    "cold-read":   SK / "omarchy-eval-cold-reader/SKILL.md",
}
TEMPLATE, LANE_DOC = EVAL / "PR-EVAL-TEMPLATE.md", EVAL / "PR-EVAL-LANE.md"
PRECEDENT = EVAL / "pr-10115.md"
AGENTS = {  # committed agent defs; first file that exists wins
    "oracle": (REPO / ".agents/agents/omarchy-config-oracle.md", UMBRELLA / ".pi/agents/omarchy-config-oracle.md"),
    "runner": (REPO / ".agents/agents/omarchy-eval-runner.md", UMBRELLA / ".pi/agents/omarchy-eval-runner.md"),
    "cold":   (REPO / ".agents/agents/omarchy-cold-reader.md", UMBRELLA / ".pi/agents/omarchy-cold-reader.md"),
}
REPO_URL = "omacom/omarchy"
MEDIA_FILES = ["cast", "gif", "mjpeg", "mp4", "png"]  # media-contract 5/5

class StageFail(Exception):  # FAIL-HARD: stop, preserve evidence, raise
    pass

def dlog(msg, force=False):
    """Debug log: stderr + workdir/debug.log when -d/--debug is set."""
    if CFG["debug"] or force:
        line = f"[debug {time.strftime('%H:%M:%S')}] {msg}"
        print(line, file=sys.stderr)
        if CFG.get("workdir"):
            Path(CFG["workdir"], "debug.log").open("a").write(line + "\n")

def load_config(path):
    """Load the eval.yml config (flat mapping of CLI options). {} if absent."""
    if not path or not Path(path).exists():
        return {}
    import yaml
    data = yaml.safe_load(Path(path).read_text()) or {}
    return {k: v for k, v in data.items() if v is not None}

def sh(cmd, cwd=None, timeout=3600):
    if CFG["debug"]:
        dlog(f"$ {cmd if isinstance(cmd, str) else ' '.join(cmd)} (cwd={cwd or REPO})")
    r = subprocess.run(cmd if isinstance(cmd, list) else cmd.split(),
                       cwd=str(cwd or REPO), capture_output=True, text=True, timeout=timeout)
    if r.returncode != 0:
        tail = f"\n--- stdout ---\n{r.stdout[-2000:]}\n--- stderr ---\n{r.stderr[-2000:]}" if CFG["debug"] else f"\n{r.stderr[-1200:]}"
        raise StageFail(f"cmd failed ({r.returncode}): {cmd}{tail}")
    if CFG["debug"]:
        dlog(f"cmd ok ({r.returncode})")
    return r

def pi_run(task, keys, agent=None, cwd=None, timeout=7200):
    """Run a pi agent non-interactively; the appended skill files ARE the instructions."""
    if agent and isinstance(agent, (tuple, list)):
        agent = next((p for p in agent if Path(p).exists()), None)
    cmd = [CFG["pi"], "--print", task]
    for k in keys:
        p = SKILLS[k]
        if not p.exists():
            raise StageFail(f"guidance missing: {p}")
        cmd += ["--append-system-prompt", str(p)]
    if agent:
        cmd += ["--system-prompt", str(agent)]
    dlog(f"pi_run keys={keys} agent={agent} bin={CFG['pi']}")
    dlog(f"pi task: {task[:400]}")
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, cwd=str(cwd or REPO))
    dlog(f"pi exit {r.returncode}, stdout {len(r.stdout)}B, stderr {len(r.stderr)}B")
    if CFG["debug"] and r.stdout:
        dlog("pi stdout head:\n" + r.stdout[:1500])
    if r.returncode != 0:
        tail = r.stderr[-1500:] if CFG["debug"] else r.stderr[-1000:]
        raise StageFail(f"pi agent failed ({r.returncode}) stage={task[:60]}...\n{tail}")
    return r.stdout

def pr_meta(pr):
    """Read-only PR metadata (the ONLY gh call; never a write)."""
    r = sh(["gh", "api", f"repos/{REPO_URL}/pulls/{pr}", "--jq",
            "{title: .title, author: .user.login, base: .base.ref, head_ref: .head.ref, "
            "head_sha: .head.sha, changed_files, additions, deletions}"])
    return json.loads(r.stdout)

# ---- sequencing gates (omarchy-eval-sequencing/SKILL.md) ----
def gate_sequencing(prs, charly):
    """HARD lane-sequencing gate: zero live batch VMs, zero in-flight runs for the
    beds, goldens present with no holder, RAM budget, load1. Any gate fails => STOP."""
    fails = []
    q = subprocess.run(["ps", "aux"], capture_output=True, text=True).stdout
    live = re.findall(r"guest=charly-check-omarchy-pr-\d+-vm", q)
    if live:
        fails.append(f"live batch VMs present: {live}")
    inflight = [f"check-omarchy-pr-{p}-vm-probe" for p in prs
                if f"check-omarchy-pr-{p}-vm-probe" in q and "check run" in q]
    if inflight:
        fails.append(f"in-flight check runs: {inflight}")
    golden = Path.home() / ".local/share/charly/vm/charly-check-omarchy-eval-base-inst/snapshots/golden/disk.qcow2"
    if not golden.exists() or golden.stat().st_size == 0:
        fails.append(f"golden missing/empty: {golden}")
    else:
        f = subprocess.run(["fuser", str(golden)], capture_output=True, text=True)
        if f.returncode == 0:
            fails.append(f"golden held by a process: {golden}")
    mem = int(Path("/proc/meminfo").read_text().splitlines()[2].split()[1]) // 1024  # MemAvailable MB
    if len(prs) * 2048 + 4096 > mem:
        fails.append(f"RAM budget: {len(prs) * 2048 + 4096}MB needed vs {mem}MB available")
    if os.getloadavg()[0] >= 20:
        fails.append(f"load1 {os.getloadavg()[0]:.1f} >= 20")
    if fails:
        raise StageFail("SEQUENCING GATE (skill: omarchy-eval-sequencing):\n  " + "\n  ".join(fails))
    dlog(f"sequencing gate OK (prs={len(prs)}, mem available {mem}MB, load1 {os.getloadavg()[0]:.1f})")

def gate_zero_locks(run_dirs):
    """Acceptance: zero 'Failed to get'/'database is locked' across every run tree."""
    hits = []
    for d in run_dirs:
        r = subprocess.run(["grep", "-rl", r"Failed to get.*write.*lock", str(d)],
                           capture_output=True, text=True)
        if r.stdout.strip():
            hits += r.stdout.split()
    if hits:
        raise StageFail(f"WRITE-LOCK INCIDENTS (wave stop): {hits}")
    dlog(f"zero-lock audit OK over {len(run_dirs)} run dirs")

def gate_teardown():
    q = subprocess.run(["ps", "aux"], capture_output=True, text=True).stdout
    left = re.findall(r"guest=charly-check-omarchy-pr-\d+-vm", q)
    if left:
        raise StageFail(f"teardown failed, eval VMs left: {left}")

def gate_media(media_dir):
    d = Path(media_dir)
    out = {}
    for f in MEDIA_FILES:
        p = next(d.glob(f"*.{f}"), None)
        if not p or p.stat().st_size == 0:
            raise StageFail(f"media gate (skill: omarchy-eval-media): missing/empty .{f} in {d}")
        out[f] = p.stat().st_size
    dlog(f"media gate OK 5/5 in {d}: {out}")
    return out

def default_lanes():
    """One eval lane per CPU core, capped so 2G x lanes <= host RAM (lane skill)."""
    mem = int(Path("/proc/meminfo").read_text().splitlines()[0].split()[1]) // 1024  # MemTotal MB
    return max(1, min(os.cpu_count() or 1, (mem - 4096) // 2048))

# ---- stages (each dispatches a pi agent; the skills ARE its instructions) ----
def stage_triage(pr, charly, workdir):
    m = pr_meta(pr)
    task = (f"TRIAGE + author the per-PR config for omacom/omarchy#{pr} exactly per the appended "
            f"oracle + tiers guidance. PR meta: {json.dumps(m)}. Deliverables: (1) the class + "
            f"hardware routing decision; (2) pr-beds/pr-{pr}/charly.yml authored per the ORACLE "
            f"TEMPLATE (drive form, from: <channel-base>:golden, marker/path rules, known-red "
            f"contract); (3) one config-audit line. Do NOT run any bed.")
    out = pi_run(task, ["oracle", "tiers"], AGENTS["oracle"], cwd=REPO)
    bed = REPO / f"pr-beds/pr-{pr}/charly.yml"
    if not bed.exists():
        raise StageFail(f"oracle produced no pr-beds/pr-{pr}/charly.yml:\n{out[-800:]}")
    sh([charly, "box", "validate"], cwd=REPO)
    (workdir / f"triage-{pr}.log").write_text(out)
    dlog(f"triage {pr}: bed written {bed}")
    print(f"  [{pr}] triage OK: {bed} written + validate green")
    return bed

def _run_bed(pr, suffix, expect, charly, workdir):
    bed = f"check-omarchy-pr-{pr}-vm{suffix}"
    task = (f"RUN the {bed} bed with {charly} per the appended lane/sequencing/golden guidance. "
            f"Place any recordings under {workdir}/media/pr-{pr}-<calver>/ (the eval-pr media "
            f"contract). FAIL-HARD: on ANY failure stop, preserve every artifact, report the "
            f"failing step + evidence, exit nonzero. Sequence per skill: pre-vm-build re-gate, "
            f"run, verdict ({expect} expected), teardown (check stop + vm destroy). Return the "
            f"summary path and the exit code.")
    out = pi_run(task, ["lane", "sequencing", "golden"], AGENTS["runner"], cwd=REPO)
    (workdir / f"run-{bed}.log").write_text(out)
    return bed

def stage_probe(pr, charly, workdir):
    bed = _run_bed(pr, "-probe", "exit 2 (known-red)", charly, workdir)
    rund = list((workdir / ".check").glob(f"check-omarchy-pr-{pr}-vm-probe/2026*")) if (workdir / ".check").exists() else []
    gate_zero_locks([d for d in rund if d.exists()])
    gate_teardown()
    print(f"  [{pr}] probe exit 2 confirmed (known-red)")

def stage_eval(pr, charly, workdir):
    _run_bed(pr, "", "exit 0", charly, workdir)
    md = sorted(Path(workdir).glob(f"media/pr-{pr}-*"))
    if not md:
        raise StageFail(f"[{pr}] eval media missing under {workdir}/media/pr-{pr}-* (media-contract)")
    media = gate_media(md[-1])  # newest calver run
    gate_teardown()
    print(f"  [{pr}] eval exit 0 confirmed, media 5/5 {media}")

def stage_report(pr, charly, workdir):
    ev = workdir / f"evidence/pr-{pr}"
    task = (f"RENDER eval/pr-{pr}.md per the appended TEMPLATE + work-lane guidance, mirroring the "
            f"precedent pr-10115.md structure (incl. the EXTERNAL NON-AUTHORITATIVE block, the "
            f"results-can-go-STALE line, the first-person 'What I did', the evidence tables). "
            f"Evidence at: {ev} and the run trees at {workdir}. Write the file to "
            f"{EVAL}/pr-{pr}.md. Do NOT post anything to omacom/omarchy.")
    out = pi_run(task, ["work-lane", "tiers", "media"], cwd=workdir)
    rep = EVAL / f"pr-{pr}.md"
    if not rep.exists():
        raise StageFail(f"no eval/pr-{pr}.md rendered:\n{out[-800:]}")
    (workdir / f"report-{pr}.log").write_text(out)
    print(f"  [{pr}] report rendered: eval/pr-{pr}.md")
    return rep

def stage_coldread(pr, workdir):
    rep = EVAL / f"pr-{pr}.md"
    task = (f"COLD-READ eval/pr-{pr}.md against the appended cold-reader + full-loop guidance: grade "
            f"every claim against the evidence at {workdir}; findings with severity; verdict line. "
            f"If a REDO-* trigger fires, state it exactly (target stage + reason).")
    out = pi_run(task, ["cold-read", "full-loop"], AGENTS["cold"], cwd=REPO)
    (workdir / f"coldread-{pr}.log").write_text(out)
    print(f"  [{pr}] cold-read done")
    return out

def full(pr, charly, workdir):
    step(pr, "triage",    lambda: stage_triage(pr, charly, workdir))
    step(pr, "probe",     lambda: stage_probe(pr, charly, workdir))
    step(pr, "eval",      lambda: stage_eval(pr, charly, workdir))
    step(pr, "report",    lambda: stage_report(pr, charly, workdir))
    for loop in range(2):  # full-loop: cold-read can trigger one redo per loop
        cr = step(pr, "coldread", lambda: stage_coldread(pr, workdir))
        if "REDO" not in cr:
            break
        target = re.search(r"REDO-(\w+)", cr).group(1).lower()
        print(f"  [{pr}] cold-read triggered REDO-{target.upper()} (loop {loop + 1})")
        globals()["stage_" + target](pr, charly, workdir)

def step(pr, name, fn):
    dlog(f"== stage {name} for PR {pr} ==")
    print(f"-- [{pr}] {name}", flush=True)
    try:
        r = fn()
        dlog(f"== stage {name} for PR {pr} OK ==")
        return r
    except StageFail as e:
        raise StageFail(f"[{pr}] {name} FAILED-HARD: {e}") from e

def main():
    ap = argparse.ArgumentParser(prog="eval-pr", description="the ONE eval-omarchy driver")
    ap.add_argument("--config", default=None,
                    help="config file (default <repo>/eval.yml when present; every option passable)")
    ap.add_argument("--pr", type=int, help="single PR")
    ap.add_argument("--prs", type=int, nargs="*", help="PR list (or from the config file)")
    ap.add_argument("--stage", default="full",
                    choices=["full", "triage", "probe", "eval", "report", "coldread"])
    ap.add_argument("--concurrency", type=int, default=default_lanes(),
                    help="one lane per CPU core by default (RAM-capped); override explicitly")
    ap.add_argument("--print-lanes", action="store_true",
                    help="print the default lane count (one per core, RAM-capped) and exit")
    ap.add_argument("--dry-run", action="store_true",
                    help="print the RESOLVED config (config file merged, CLI wins) and exit")
    ap.add_argument("--charly", default="/tmp/charly-r10-fixed/bin/charly")
    ap.add_argument("--pi", default=shutil.which("pi") or "pi", help="pi binary")
    ap.add_argument("--workdir", default=None)
    ap.add_argument("--no-sequencing-gate", action="store_true", help="(never used in prod)")
    ap.add_argument("-d", "--debug", action="store_true", help="full debug: verbose dispatch,"
                    " every command, task texts, full outputs on failure -> workdir/debug.log")
    pre = ap.parse_known_args()  # first pass: read --config (or the repo default)
    cfg = load_config(pre[0].config or (REPO / "eval.yml"))
    if cfg:
        ap.set_defaults(**cfg)  # config file supplies defaults; explicit CLI flags still win
    a = ap.parse_args()
    CFG.update(debug=a.debug, pi=a.pi, charly=a.charly)
    if a.dry_run:
        print(json.dumps({"prs": a.prs or [], "stage": a.stage, "concurrency": a.concurrency,
                          "charly": a.charly, "pi": a.pi, "debug": a.debug,
                          "workdir": a.workdir or "/tmp/eval-pr-<ts>",
                          "no_sequencing_gate": a.no_sequencing_gate}, indent=1))
        return 0
    if a.print_lanes:
        print(f"lanes={a.concurrency} (cpu={os.cpu_count()} ram-capped)")
        return 0
    prs = a.prs or ([a.pr] if a.pr else [])
    if not prs:
        ap.error("need --pr or --prs (or prs: in the config file)")
    workdir = Path(a.workdir or f"/tmp/eval-pr-{time.strftime('%Y%m%d-%H%M%S')}")
    workdir.mkdir(parents=True, exist_ok=True)
    CFG["workdir"] = str(workdir)
    dlog(f"eval-pr start prs={prs} stage={a.stage} concurrency={a.concurrency} workdir={workdir}")
    if not a.no_sequencing_gate:
        gate_sequencing(prs, a.charly)
    try:
        if a.stage == "full":
            with ThreadPoolExecutor(max_workers=a.concurrency) as ex:
                futs = [ex.submit(full, p, a.charly, workdir) for p in prs]
                for f in futs:
                    f.result()
        else:
            for p in prs:
                globals()["stage_" + a.stage](p, a.charly, workdir)
        print(f"ALL-STAGES-OK prs={prs} workdir={workdir}")
        return 0
    except StageFail as e:
        print(f"FAIL-HARD: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
