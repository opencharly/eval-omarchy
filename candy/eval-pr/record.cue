// record.cue — the per-PR eval record schema (the single source for the record
// shape). The `record` stage of eval-pr-plan emits this def via the `emit` stage
// (`kind: emit`, `schema: eval/pr-<N>/record.cue`), so the record is validated
// BEFORE it is written and can never be malformed YAML. A field added to the
// record MUST be added here first — an unknown or missing field fails the stage.
#EvalRecord: close({
	pr!:        string | int
	repo!:      string
	head!:      string
	generated!: string

	oracle!: {
		class!:  string
		golden!: string
		sha!:    string
		what!:   string
		drive!:  string
		files!:  [...string]
		tests!:  [...string]
		checks!: [...#EvalCheck]
	}

	control!: {
		ok!:    bool
		steps!: [...#EvalStep]
	}

	eval!: {
		verdict!:         string
		executed_checks!: int
		steps!:           [...#EvalStep]
	}

	gates!: {
		control_ok!:      bool
		executed_checks!: int
		media_ok!:        bool
	}

	validate!: {
		verdict!:   string
		security!:  string
		checklist!: [...string]
		findings!:  [...string]
	}

	media!: {
		cast!:  string
		gif!:   string
		mjpeg!: string
		mp4!:   string
		png!:   string
	}

	cold_read!: {
		verdict!:     string
		suggestions!: [...string]
	}

	report!: string
})

#EvalCheck: {
	id!:        string
	what!:      string
	assertion!: string
	knownRed!:  bool
}

// #NotTestableRecord — the record for a class "skip" (draft/WIP) PR: a plain
// disclosure, not a bed-run record (R1). Same schema-first contract: the value
// is validated before write, so the not-testable path cannot emit broken YAML
// either. `result` carries the terminal state.
#NotTestableRecord: close({
	pr!:        string | int
	repo!:      string
	head!:      string
	generated!: string
	oracle!: {
		class!:  string
		golden!: string
		sha!:    string
		what!:   string
		drive!:  string
		files!:  [...string]
		tests!:  [...string]
		checks!: [...#EvalCheck]
	}
	result!: string
	report!: string
})

#EvalStep: {
	id!:     string
	name!:   string
	status!: string
}
