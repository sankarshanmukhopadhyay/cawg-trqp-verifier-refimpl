# CAWG–TRQP Verifier Reference Implementation v0.21.0

**Experimental Consent Evidence and Delegated Creator Boundaries**  
**Release date:** 11 November 2026  
**Classification:** Non-normative experimental capability release. Existing verifier APIs and operational assurance profiles remain unchanged.

## Summary

v0.21.0 adds a separate, reproducible model for classifying **caller-asserted consent evidence** alongside existing experimental delegated-creator authority evaluation. It explicitly refuses the false inference that valid organizational delegation, signature integrity, identity evidence, professional standing, or content provenance proves the consent of a person represented by a voice, face, name or likeness.

The additional evaluator is not a legal permission service, evidence authenticator, rights adjudicator, registry, issuer-verifier, consent validator or CAWG normative implementation. No real consent signatures, identity bindings, accepted registry state or trusted time were verified. Reproducible local test success does not establish factual consent.

## Changes for adopters and integrators

### Independent consent claim classification

`experimental_consent_assurance.assess_consent` accepts a normalized subject-scoped use and bounded, externally referenced consent claims. It reports evidence status (`missing`, `unverified`, `contradictory`), matching claimed action/resource/purpose, claimed historical use scope, asserted current state, and explicit untrusted evidence/time provenance.

A claim within its stated scope is reported as `claimed_in_scope`, not as independently established permission. `assured_consent` remains `indeterminate` for all caller-supplied evidence. Both input and output contracts are experimental and may evolve with separately justified versioning.

### Withdrawal and historical/current separation

The evaluator distinguishes asserted effective withdrawal from the time withdrawal was observed. A retrospective claim discovered after a requested evaluation cannot be represented as an observed state at that earlier time. Expiry and withdrawal after historical use do not silently rewrite earlier claimed scope, but historical evidence never guarantees present reuse or redistribution rights. All timestamps are caller-supplied; no trusted signing-time or authoritative historical registry state is established.

### Two integrated, reproducible creative-sector cases

- **Brand, agency and performer:** independent evidence claims about the brand's delegation and the represented performer's consent.
- **Studio, AI voice tool and performer:** bounded creative-tool delegation and independently assessed voice-use consent.

Synthetic cases exercise missing consent, wrong project/purpose, authority failure despite matching consent claims, withdrawal and uncertain evidence. The public script `python scripts/run_taskforce_consent_demo.py` emits a deterministic, privacy-minimized JSON report. A positive synthetic match remains unverified consent and indeterminate independently assured authority.

### Traceability and publication

A separate machine-readable consent traceability supplement records locally testable propositions, external evidence dependencies and upstream decisions without changing the existing twelve Delegated Creator requirements. Public documentation, the roadmap, changelog, repository status, metadata, Pages navigation, release checksums and compatibility declarations were updated for v0.21.0. Earlier v0.20.0 presentation artifacts remain deliberately and visibly version-pinned.

## Reproduction and evidence

```bash
python -m pip install -r requirements-lock.txt
python -m pip install -e .
python scripts/run_taskforce_consent_demo.py
pytest -q tests/test_experimental_consent_assurance.py tests/test_experimental_consent_temporal.py tests/test_taskforce_consent_scenarios.py tests/test_taskforce_consent_traceability.py
make validate
```

The repository release workflow runs `make validate` at the release commit, builds the wheel and source archive and publishes a checksum manifest containing consent-assurance schema and scenario identities. Evidence remains repository-local synthetic fixture and test evidence, not external conformance.

## Compatibility

There is **no intentional breaking change** to stable HTTP endpoints, CLI verifier contracts, established profiles (`standard`, `edge`, `high_assurance`), the existing five-world report schema, or external integration version pins. The new evaluator is isolated from the deployed authorization path and does not grant permission, mutate authority, or perform network fetches. Experimental interfaces are not CAWG-governed wire contracts.

## Known limitations and unfulfilled evidence gates

- No independently signed performer-consent record or established subject-to-key relationship.
- No legal adjudication of likeness, copyright, contractual enforceability, permissible use or required takedowns.
- No independently verified consent-registry state, revocation history, trusted time or binding to C2PA manifest and CAWG assertions.
- No real signed assets with accepted trust anchors, independent C2PA/TRQP interop, live governed trust registry, or verified reusable authority credential.
- Claimed evidence references and digests are supplied by the caller, not dereferenced, validated or vouched for by the evaluator.
- An unknown, missing, disputed or unavailable consent record is not evidence that consent was never given.
- Tests and release checks do not constitute independent approval, production certification or CAWG ratification.

The prior independent interoperability gate [#75](https://github.com/sankarshanmukhopadhyay/cawg-trqp-verifier-refimpl/issues/75) stays open. Upstream specification adoption and legal consent determination are outside repository authority.

## Provenance and governance

The new experiment responds to publicly discussed creator-delegation and consent questions without including or relying on nonpublic meeting material. The maintainers govern only local implementation, fixtures and release artifacts, not CAWG/C2PA/TRQP normative meaning. AI assistance was disclosed on the implementation PRs, which remain subject to ordinary review, DCO and CI.

**Compare:** [v0.20.0...v0.21.0](https://github.com/sankarshanmukhopadhyay/cawg-trqp-verifier-refimpl/compare/v0.20.0...v0.21.0)  
**Documentation:** [Experimental Consent Assurance](docs/agentic-ai/experimental-consent-assurance.md) · [Consent Traceability](conformance/delegated-creator-consent-traceability.json) · [Roadmap](ROADMAP.md)
