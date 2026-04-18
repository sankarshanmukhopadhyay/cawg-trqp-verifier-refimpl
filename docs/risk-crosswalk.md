---
title: Risk Crosswalk
description: Maps trust risks to verifier controls, TRQP queries, enforcement mechanisms, evidence artifacts, conformance tests, and assurance frameworks.
---

# Risk Crosswalk

This document maps key trust risks to:

- verifier controls
- TRQP queries
- enforcement points
- evidence artifacts such as decision receipts and audit bundles
- conformance tests
- adversarial test vectors
- assurance frameworks including NIST AI RMF and ISO/IEC 42001

It answers a practical question:

> What risks does this system mitigate, how are they enforced, and how can that be verified?

The intent of this document is to make the repository legible to technical, assurance, procurement, and governance audiences at the same time. The verifier does not merely check whether an input is valid. It applies runtime controls against specific failure modes and produces evidence that those controls were actually enforced.

---

# How to read this document

Each row in the crosswalk describes:

- **Risk**: what can go wrong
- **Failure Mode**: how the risk appears in practice
- **Control**: what the verifier enforces
- **TRQP Dependency**: what query or trust-state dependency is involved
- **Enforcement Point**: where the control is applied
- **Evidence Produced**: what artifact proves the control was applied
- **Severity**: the impact if the risk is exploited
- **Likelihood**: how plausible the failure mode is in realistic deployments
- **Conformance Test**: how the repository can validate the control
- **Adversarial Vector**: how an attacker or faulty environment could trigger the failure mode
- **Standards Mapping**: indicative alignment to broader assurance frameworks

This is therefore both a narrative and an operational map. It explains the trust model while also making it easier to expand the conformance surface over time.

---

# Risk Crosswalk Table

| ID | Risk | Failure Mode | Control | TRQP Dependency | Enforcement Point | Evidence Produced | Severity | Likelihood | Conformance Test | Adversarial Vector | Standards Mapping |
|----|------|-------------|---------|-----------------|------------------|------------------|----------|------------|------------------|-------------------|------------------|
| R1 | Unauthorized Actor | An actor submits or acts without permission in the relevant authority context | Authorization check against actor, action, and resource context | Authorization query | Policy evaluation | Decision receipt: `authorization`; audit bundle policy evidence | High | High | `test_authorization_denied` | Credential reuse, actor spoofing, delegated authority misuse | NIST AI RMF GOV-1, GOV-2; ISO/IEC 42001 access control |
| R2 | Unrecognized Issuer | A credential or trust assertion is issued by an entity not recognized by the required authority | Issuer recognition check | Recognition query | Policy evaluation | Decision receipt: `recognition`; audit bundle policy evidence | High | Medium | `test_unrecognized_issuer` | Rogue issuer injection, mis-bound issuer metadata | NIST AI RMF GOV-2; ISO/IEC 42001 supply chain and trust source governance |
| R3 | Stale Revocation | A revoked entity continues to appear valid because revocation state is not fresh enough | Revocation freshness enforcement with profile-driven thresholds | Revocation query | Profile enforcement | Decision receipt: `revocation_freshness`; replay inputs revocation status | Critical | High | `test_revocation_stale_fail`, `test_revocation_stale_warn` | Revocation lag exploitation, stale cache reuse | NIST AI RMF MAP-3, MEA-1; ISO/IEC 42001 lifecycle control |
| R4 | Integrity Tampering | The asset or supporting data has been altered or corrupted | Integrity signal validation | None for local signal evaluation | Asset validation | Decision receipt: `integrity`; verification result block | High | Medium | `test_integrity_failure` | Hash mismatch, tampering in transit, modified content | NIST AI RMF MEA-1 |
| R5 | Missing Provenance | The asset has no credible origin or process evidence attached | Provenance requirement and validation | None for local signal evaluation | Asset validation | Decision receipt: `provenance`; verification result block | Medium | High | `test_missing_provenance` | Metadata stripping, provenance envelope removal | NIST AI RMF GOV-3 |
| R6 | Process Manipulation | The asset was created or transformed outside an allowed workflow | Process evidence validation and policy comparison | Policy constraints, potentially tied to recognition or authorization context | Policy evaluation | Decision receipt: `process_evidence`; process appraisal notes | High | Medium | `test_invalid_process` | Pipeline bypass, unauthorized transformation stage | ISO/IEC 42001 operational control |
| R7 | Transport Bypass | Policy or trust-state queries travel over an untrusted or disallowed route | Transport validation based on profile constraints | TRQP transport mode and route metadata | Transport enforcement | Decision receipt: `transport_mode`; transport metadata in audit bundle | High | Medium | `test_transport_policy_violation` | Proxy injection, man-in-the-middle path, unexpected downgrade | NIST AI RMF SEC-2 |
| R8 | Gateway Misrouting | A gateway routes a trust query to the wrong authority or policy source | Route validation and gateway metadata checks | Gateway metadata and mediated TRQP path | Transport enforcement | Decision receipt: `gateway_route`; gateway mediation evidence | High | Low | `test_gateway_route_mismatch` | Route spoofing, stale route map, misconfigured gateway | ISO/IEC 42001 network and control-plane management |
| R9 | Snapshot Staleness | Offline verification relies on an outdated or invalid snapshot of trust state | Snapshot verification plus freshness and signature policy | Snapshot metadata and trust anchors | Profile enforcement | Decision receipt: `snapshot_reference`; snapshot verification evidence | High | Medium | `test_snapshot_expired`, `test_edge_snapshot_authorized` | Replay of expired snapshot, old signed state reuse | NIST AI RMF MAP-3; ISO/IEC 42001 lifecycle and change control |
| R10 | Authority Fragmentation | Different authority sources provide conflicting or incomplete state | Multi-authority composition rules and reconciliation logic | Multiple TRQP queries across authority contexts | Policy evaluation | Decision receipt: `authority_sources`; interoperability vectors and audit evidence | Medium | Medium | `test_multi_authority_conflict` | Split-authority attack, inconsistent federation state | NIST AI RMF GOV-4 |
| R11 | Non-Reproducible Decision | A decision cannot be replayed because key inputs or responses are missing | Replay enforcement and captured replay inputs | Captured TRQP responses, resolved profile, and transport metadata | Evidence generation | Audit bundle; reproducibility bundle; decision receipt references | Critical | Medium | `test_replay_determinism` | Missing inputs, mutable references, non-deterministic runtime behavior | NIST AI RMF MEA-2 |
| R12 | Opaque Decision Logic | A result is produced without enough explanation to inspect or dispute it | Structured policy evaluation and receipt generation | TRQP responses plus profile rules | Decision construction | Decision receipt: `policy_evaluation`; verification explanations | Medium | High | `test_decision_explainability` | Black-box output without traceable rationale | NIST AI RMF GOV-1 |
| R13 | Policy Drift | Different environments or configurations produce inconsistent outcomes | Profile enforcement and schema-governed configuration | Profile definition and resolved profile content | Verification execution | Decision receipt: `profile`; resolved profile in replay inputs | Medium | Medium | `test_profile_consistency` | Configuration drift, undocumented overrides, stale profiles | ISO/IEC 42001 governance and change control |
| R14 | Silent Degradation | The system continues under degraded conditions without making that visible | Explicit degraded mode handling and result signaling | TRQP availability and profile rules | Decision construction | Decision receipt: `result=degraded`; transport and freshness annotations | High | Medium | `test_degraded_mode_flag` | Forced fallback, partial outage hiding, suppressed warning path | NIST AI RMF SEC-1 |
| R15 | Trust Injection | A malicious or unauthorized trust source is treated as authoritative | Trust anchor validation and trusted source pinning | Trust anchors and source metadata | Transport and snapshot enforcement | Decision receipt evidence and trust anchor references | Critical | Low | `test_invalid_trust_anchor` | Fake registry, malicious snapshot signer, compromised source metadata | ISO/IEC 42001 trust management and key material governance |

---

# Risk scoring model

## Severity levels

- **Critical**: Breaks core trust guarantees or can cause materially incorrect decisions to be accepted as valid.
- **High**: Enables unauthorized, misleading, or materially unsafe outcomes.
- **Medium**: Weakens assurance, auditability, or consistency in ways that matter operationally.
- **Low**: Limited operational impact or strongly constrained by other controls.

## Likelihood levels

- **High**: Common or expected in distributed and federated systems.
- **Medium**: Plausible under realistic deployment or integration conditions.
- **Low**: Requires specialized attack capability, unusual conditions, or multiple failures.

These scores are indicative rather than normative. They are meant to help readers understand why certain controls matter and where the repository currently focuses its enforcement effort.

---

# Conformance integration

Each risk maps to a **testable condition**.

The purpose of the crosswalk is not only to describe the system, but to support the following chain:

> Risk → Control → Test → Evidence

The Conformance Suite or any downstream validation harness can use this document to determine:

- which controls should be tested
- what negative and positive outcomes should be expected
- what evidence should appear in decision receipts or audit bundles

This also helps distinguish a strong implementation from one that merely produces the correct output in happy-path conditions.

---

# Adversarial testing model

Each risk includes a realistic adversarial path. These are not abstract thought experiments. They are meant to be converted into executable test vectors over time.

Examples include:

- delaying revocation propagation to test stale acceptance or fail/warn handling
- injecting a proxy or alternative route to test transport enforcement
- replaying an expired snapshot to test signature and freshness policy
- supplying split authority responses to test multi-authority reconciliation

These adversarial vectors are especially useful when positioning the repository as an assurance artifact rather than a simple demo.

---

# Standards mapping

## NIST AI RMF (indicative)

The mappings in this document use a lightweight shorthand:

- **GOV**: governance, accountability, and oversight
- **MAP**: risk identification and tracking
- **MEA**: measurement, monitoring, and validation
- **SEC**: security and resilience

These mappings are indicative rather than authoritative. Their purpose is to provide a practical alignment surface for enterprise and public-sector readers.

## ISO/IEC 42001 (indicative)

The ISO references are also indicative and center on areas such as:

- access control
- operational control
- lifecycle management
- trust source governance
- supply chain and dependency management
- change control and assurance traceability

---

# Assurance level interpretation

The crosswalk can also support a lightweight assurance-level interpretation model.

## AL1: Basic runtime trust

Covers foundational controls required to avoid obviously unsafe operation:

- R1 Unauthorized Actor
- R2 Unrecognized Issuer
- R4 Integrity Tampering
- R5 Missing Provenance

## AL2: Operational trust

Adds controls needed for production-grade runtime handling:

- AL1 plus R3 Stale Revocation
- AL1 plus R6 Process Manipulation
- AL1 plus R7 Transport Bypass

## AL3: High-assurance and mediated operation

Adds controls required for more demanding and more distributed environments:

- AL2 plus R8 Gateway Misrouting
- AL2 plus R9 Snapshot Staleness
- AL2 plus R10 Authority Fragmentation

## AL4: Critical, auditable, and adversarially aware operation

Adds controls required for the strongest assurance posture:

- AL3 plus R11 Non-Reproducible Decision
- AL3 plus R12 Opaque Decision Logic
- AL3 plus R13 Policy Drift
- AL3 plus R14 Silent Degradation
- AL3 plus R15 Trust Injection

This interpretation is intentionally practical. It can be used later as an input to a fuller assurance-hub or conformance-suite mapping without overstating the current repository scope.

---

# Relationship to decision receipts

Every control in this table should produce **observable evidence**.

Decision receipts are the most concise place where that evidence becomes inspectable. A receipt can show:

- which profile was used
- which TRQP responses were relied on
- how freshness or transport conditions were evaluated
- which outcome was produced
- why the outcome was produced

Audit bundles and replay bundles extend this by providing richer replay and verification context.

---

# Example: video verification

For the repository walkthrough scenario built around `city-bridge-inspection.mp4`, the crosswalk becomes concrete:

- **R1**: the actor must be authorized to submit the inspection video
- **R2**: the issuer behind the trust assertion must be recognized
- **R3**: revocation information must be fresh enough for the selected profile
- **R4–R6**: integrity, provenance, and process evidence must all satisfy policy
- **R7–R9**: transport route, gateway mediation, or snapshot usage must match profile expectations
- **R11–R12**: the final decision must be replayable and explainable

This is the practical difference between “a file looks valid” and “a file was accepted under a governed, auditable trust process.”

---

# What this enables

This crosswalk turns the repository into a more legible assurance artifact.

It makes it easier to answer:

- what risks the system covers
- what runtime controls exist
- what evidence is produced
- what should be tested next
- how the repository aligns with larger governance and assurance programs

It therefore bridges:

> implementation → governance → assurance

---

# Future evolution

This document can grow further by:

- linking each risk to concrete file paths and existing tests as they mature
- introducing weighted scoring or deployment-specific profiles
- adding challenge and dispute workflows for decision receipts
- connecting directly to external control catalogs in the TRQP ecosystem

---

# Summary

This repository does not just verify inputs.

It mitigates defined risks, enforces controls at runtime, and produces evidence that those controls were applied.

The risk crosswalk makes that control model explicit, testable, and auditable.
