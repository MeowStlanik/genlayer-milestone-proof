# MilestoneProof

A reusable acceptance-receipt primitive for text-verifiable grant and bounty milestones. It binds an agreed rubric to immutable evidence revisions and separates missing proof from explicit non-compliance.

## Why GenLayer

Conventional escrow/milestone contracts can enforce payment schedules, but cannot themselves interpret whether a report satisfies a natural-language specification. This contract exposes an interpretable, criterion-level decision vector that another protocol can consume after finality. It does not custody or release funds.

## State and authority

`cases[case_id]` stores sponsor, builder, immutable rubric and rubric hash, current bounded evidence, revision and state. `receipts[case_id:revision]` preserves every completed evaluation with evidence hash, criterion decisions and deterministically calculated satisfied basis points. The creating sponsor chooses the rubric; only the named builder may accept and submit. Evaluation is permissionless.

## Lifecycle

`OFFERED → ACTIVE → SUBMITTED → PASSED | REWORK | UNKNOWN`. Only REWORK/UNKNOWN may receive a replacement submission, up to three total revisions. PASSED is terminal. The rubric cannot change after creation. A network consensus failure leaves SUBMITTED unchanged.

## Consensus and equivalence

The leader and each validator independently evaluate the entire rubric against the same submitted evidence. Every criterion must have a MET / NOT_MET / UNKNOWN decision. The exact ordered status vector is the equivalence key. Quotes may differ but must be real substrings. NOT_MET requires explicit contradictory evidence; absence is UNKNOWN. Weights and overall state are calculated outside the model. A partial score cannot become PASSED.

Malformed outputs, invented citations, incomplete arrays or disagreement are rejected. Each accepted receipt records the leader's validated evidence; independently produced validator explanations are not stored. The decision equivalence is substantive, not a JSON-format check.

## Public API

Constructor: no arguments. Source: [contract.py](contract.py). RPC-checked ABI: [schema.json](schema.json).

| Method | Caller | Meaning |
| --- | --- | --- |
| `create(case_id, builder: Address, rubric_json)` | Anyone creating a new case | Freeze 1–6 criteria; positive integer weights sum to 10,000 |
| `accept(case_id, rubric_hash)` | Builder | Accept exact agreed specification |
| `submit(case_id, evidence)` | Builder | Freeze next evidence revision (≤18,000 characters) |
| `evaluate(case_id)` | Anyone | Produce a receipt through consensus |
| `get_case(case_id)` | Read | Current case as JSON text |
| `get_receipt(case_id, revision)` | Read | Historical receipt as JSON text |

## Example walkthrough

1. Sponsor calls `create("docs-v1", BUILDER_ADDRESS, rubric_json)` with:

```json
[{"criterion":"The submitted API guide contains three concrete request/response examples, including one documented error response.","weight_bps":7000},{"criterion":"The guide states the authentication header and its exact syntax.","weight_bps":3000}]
```

2. Builder reads `get_case("docs-v1")`, obtains `rubric_hash`, then calls `accept` with it.
3. Builder calls `submit("docs-v1", complete_guide_text)`. Supply the actual guide, not an external URL or a promise to write it.
4. After that transaction succeeds, anyone calls `evaluate("docs-v1")`, then reads `get_receipt("docs-v1", 1)`.
5. A downstream grant controller checks the finalized receipt and its own payout rules. `satisfied_bps` is coverage of criteria, not an authorized payment amount.

Each write is a separate transaction. For this walkthrough, wait for the successful state needed by the next call. The batch deploy script skips AI confirmation only because these four constructors are independent.

## Tests and review

Run `python -m unittest discover -s tests -p 'test_*.py' -v` from this repository root. Tests load this exact source through a small fake GenVM adapter and exercise role checks, history/immutability, malicious model outputs and independent disagreement. They are logic tests, not live model consensus tests. See [VALIDATION.md](VALIDATION.md).

## Limitations

Text sufficiency is not proof of deployment, authorship, truth, code execution or ownership. A fabricated report can fool models. Use independently authenticated artifacts upstream where those properties matter. A vague rubric can cause disagreement. This version deliberately has no expiry, arbitration admin, fund custody or cross-contract payout. Access control cannot prevent a sponsor from choosing a biased rubric; bilateral acceptance makes the rule explicit.

## Deployment and integration

Deploy this file independently, with zero constructor arguments and full consensus (`leaderOnly: false`). The repository contains the contract, English documentation and tests only. Deployment tooling is maintained separately. After publication, `deployment.json` records this contract's observed Bradbury transaction. Transaction existence does not prove successful execution or finality. Consumers should read finalized successful receipts and bind them to this contract address and their own business rules.

Category: **Intelligent Contracts**. Suggested submission text: [SUBMISSION.md](SUBMISSION.md). MIT license.
