# CAWG-TRQP Verifier Reference Implementation v0.19.0

## Semantic Assurance and Downgrade Resistance

v0.19.0 strengthens the boundary between CAWG/C2PA evidence extraction and TRQP trust decisions. It makes expected evidence, unperformed checks, and contradictory assertions explicit and machine-verifiable rather than allowing them to collapse into a generic success state.

## Added

- Profile controls for required and supported CAWG/C2PA assertion labels.
- Explicit `assertion_evaluation` evidence covering expected, present, missing, unsupported, and unknown assertion labels.
- Profile-local deterministic conflict rules with `unresolved` and `precedence` strategies.
- `conflict_evaluation` evidence exposing contradictions and any configured resolution.
- Proposition-level verification outcomes separating asset integrity, assertion expectation, assertion conflict, issuer recognition, actor authorization, and process integrity.
- `semantic_guardrail` fail-closed behavior before TRQP authority lookup when required semantic evidence fails.
- `degraded` trust outcome when warning-level semantic gaps accompany an otherwise successful trust decision.
- External assurance traceability from RAHP Toolkit CAWG/C2PA findings to implementation controls, tests, and evidence.

## Fixed

- Repaired `conformance/risk-to-test-map.yaml`, which previously contained supplemental feed-descriptor risks outside the top-level YAML mapping and could not be parsed as valid YAML.

## Assurance references

The release uses the separately maintained **RAHP Toolkit** as non-normative reference work. In particular, implementation changes are traceable to the CAWG/C2PA risk and security-review items `CRK-23` / `SEC-CW-004`, `CRK-28` / `SEC-CW-005`, `CRK-04` / `SEC-CW-006`, and `CRK-12`.

RAHP remains external assurance evidence. It is not a runtime dependency, does not define CAWG/C2PA normative semantics, and does not determine relying-party legal or editorial outcomes.

## Compatibility

Existing built-in profiles preserve prior behavior because semantic controls default to observation with no required assertion labels or conflict rules. Deployments can opt into stricter semantic assurance through inline or repository profiles without changing the TRQP service interface.

## Validation

The release is validated through the repository gate:

```bash
make validate
```

Targeted semantic assurance tests are in `tests/test_semantic_assurance.py`.
