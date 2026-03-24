# Deployment Guidance for Process-Aware Verifiers and Appraisal Services

## Deployment modes

### 1. Edge verifier
Use for constrained devices, field inspection tools, or disconnected verification. Pair with signed snapshots and local process appraisal.

### 2. Standard online verifier
Use for enterprise platforms and APIs. Enable cache-first lookups and export audit bundles for downstream systems.

### 3. Gateway-mediated verifier
Use where a central policy team needs to manage trust routing across multiple authorities or ecosystems.

## Appraisal service guidance

Process-aware verification can remain local for simple deployments. For larger deployments, appraisal logic can be separated into its own service so teams can evolve thresholds, signal handling, and scoring independently from verifier code.

## Operational considerations

- Cache policy answers with bounded TTLs.
- Keep gateway mediation receipts for incident analysis.
- Export audit bundles for regulated workloads.
- Separate policy management from verifier rollout.
- Treat process evidence as optional unless policy requires it.

## Enterprise rollout path

1. Start with standard online verification.
2. Add audit bundle export.
3. Introduce gateway mediation for central policy control.
4. Add process-aware appraisal for higher assurance cases.
