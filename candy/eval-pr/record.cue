// record.cue — the per-PR eval record schema (the SINGLE source for the record
// shape). The `record` stage of eval-pr-plan emits `#EvalRecord` and the
// `not-testable` stage emits `#NotTestableRecord`, both via the `emit` stage:
//
//   - id: record        schema: candy/eval-pr/record.cue#EvalRecord            (file#Def -> #EvalRecord)
//   - id: not-testable  schema: candy/eval-pr/record.cue#NotTestableRecord      (file#Def -> #NotTestableRecord)
//
// A `#Def` suffix selects that def explicitly; a BARE `.cue` path would select
// the file's first `#Def` (not used by this lane — both stages name their def).
// The value is validated BEFORE it is written, so
// the record can never be malformed YAML. EVERY level is `close(...)`d — the top
// def AND each nested struct — so an unknown field at any depth is a stage
// failure, not a silent drop (a bare-path schema resolving to an open top level
// would accept a record vacuously). A field added to the record MUST be added
// here first.
#EvalRecord: close({
	pr!:        string | int
	repo!:      string
	head!:      string
	generated!: string

	oracle!: #EvalOracle

	control!: close({
		ok!:    bool
		steps!: [...#EvalStep]
	})

	eval!: close({
		verdict!:         string
		executed_checks!: int
		steps!:           [...#EvalStep]
	})

	gates!: close({
		control_ok!:      bool
		executed_checks!: int
		media_ok!:        bool
	})

	validate!: close({
		verdict!:   string
		security!:  string
		checklist!: [...string]
		findings!:  [...string]
	})

	media!: close({
		cast!:  string
		gif!:   string
		mjpeg!: string
		mp4!:   string
		png!:   string
	})

	cold_read!: close({
		verdict!:     string
		suggestions!: [...string]
	})

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
	oracle!:    #EvalOracle
	result!:    string
	report!:    string
})

// #EvalOracle — the config-oracle triage block SHARED by #EvalRecord and
// #NotTestableRecord (one definition, so a field added to one record's oracle
// cannot drift from the other).
#EvalOracle: close({
	class!:  string
	golden!: string
	sha!:    string
	what!:   string
	drive!:  string
	files!:  [...string]
	tests!:  [...string]
	checks!: [...#EvalCheck]
})

#EvalStep: {
	id!:     string
	name!:   string
	status!: string
}
