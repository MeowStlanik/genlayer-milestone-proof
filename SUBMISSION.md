# MilestoneProof — standalone Intelligent Contract

**Category:** Intelligent Contracts

**Purpose:** A reusable acceptance-receipt primitive for text-verifiable grant and bounty milestones. It binds an agreed rubric to immutable evidence revisions and separates missing proof from explicit non-compliance.

**Why consensus matters:** The leader and each validator independently evaluate the entire rubric against the same submitted evidence. Every criterion must have a MET / NOT_MET / UNKNOWN decision. The exact ordered status vector is the equivalence key. Quotes may differ but must be real substrings. NOT_MET requires explicit contradictory evidence; absence is UNKNOWN. Weights and overall state are calculated outside the model. A partial score cannot become PASSED.

**State design:** `cases[case_id]` stores sponsor, builder, immutable rubric and rubric hash, current bounded evidence, revision and state. `receipts[case_id:revision]` preserves every completed evaluation with evidence hash, criterion decisions and deterministically calculated satisfied basis points. The creating sponsor chooses the rubric; only the named builder may accept and submit. Evaluation is permissionless.

**Reusable beyond a demo:** Conventional escrow/milestone contracts can enforce payment schedules, but cannot themselves interpret whether a report satisfies a natural-language specification. This contract exposes an interpretable, criterion-level decision vector that another protocol can consume after finality. It does not custody or release funds.

**Source:** `contract.py` (self-contained; zero-argument constructor).

**Review materials:** project README, ABI schema, `tests/test_contract.py` and `VALIDATION.md`.

**Deployment evidence:** after publication, use this repository’s `deployment.json`. It proves an observed matching transaction, not final success. Add the actual repository URL, successful deployment address and live invocation transaction IDs when submitting. Those values are intentionally not fabricated in this draft.

**Current verification scope:** local logic tests and Bradbury schema loading. Live AI consensus and production audit remain outstanding. Text sufficiency is not proof of deployment, authorship, truth, code execution or ownership. A fabricated report can fool models. Use independently authenticated artifacts upstream where those properties matter. A vague rubric can cause disagreement. This version deliberately has no expiry, arbitration admin, fund custody or cross-contract payout. Access control cannot prevent a sponsor from choosing a biased rubric; bilateral acceptance makes the rule explicit.
