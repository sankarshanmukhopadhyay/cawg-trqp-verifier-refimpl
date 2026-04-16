# Deployment Guidance for Process-Aware Verifiers and Appraisal Services

## Deployment modes

### 1. Edge verifier
Use for constrained devices, field inspection tools, or disconnected verification. Pair with signed snapshots and local process appraisal.

### 2. Standard online verifier
Use for enterprise platforms and APIs. Enable cache-first lookups, validate shipped fixtures in CI, and export audit bundles for downstream systems.

### 3. Gateway-mediated verifier
Use where a central policy team needs to manage trust routing across multiple authorities or ecosystems and where the mediation path itself should appear in evidence.

### 4. HTTP service deployment
Use where teams want a simple network-facing reference implementation for authorization, recognition, verification, and audit bundle export.

## Appraisal service guidance

Process-aware verification can remain local for simple deployments. For larger deployments, appraisal logic can be separated into its own service so teams can evolve thresholds, signal handling, and scoring independently from verifier code.

## Operational considerations

- cache policy answers with bounded TTLs and bounded cache size
- keep gateway mediation receipts for incident analysis and interoperability review
- export audit bundles for regulated or externally reviewed workloads
- validate shipped examples and fixture packages as part of CI
- separate policy management from verifier rollout
- treat process evidence as optional unless policy requires it

## Enterprise rollout path

1. start with standard online verification
2. add audit bundle export and replay checks
3. consume canonical fixture packages to stabilize expected outcomes
4. introduce gateway mediation for central policy control and multi-authority routing
5. expose the HTTP service when the verification surface needs to be exercised as an API
