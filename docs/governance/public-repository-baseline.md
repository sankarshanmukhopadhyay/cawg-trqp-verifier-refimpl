# Public repository baseline

This record captures the controls reviewed under issue #37. It is repository assurance evidence, not external certification.

| Control | State | Evidence | Residual risk |
|---|---|---|---|
| Purpose, maturity, adoption and authority | PASS | `README.md`, `GOVERNANCE.md`, `PROJECT-STATUS.yaml`, `AI_USAGE.md` | None identified. |
| Licensing/release provenance | PASS | repository license/release/status surfaces, `CHANGELOG.md`, `CITATION.cff` | Publication remains maintainer judgment. |
| Security reporting | PASS | `SECURITY.md` | Hosted private-vulnerability-reporting enablement remains platform evidence. |
| Contribution/community/support | PASS | `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SUPPORT.md`, issue/PR templates | None identified. |
| Dependency update management | PASS | `.github/dependabot.yml` | Hosted Dependabot enablement remains platform evidence. |
| Default-branch protection | PARTIAL | active `protect-main` observed 2026-09-05: PRs, resolved conversations, linear history, delete/non-fast-forward protection, no bypass actors | No required status check is present in the observed ruleset; tracked separately. |
| CI / evidence | PASS / bounded | repository workflows and validation/conformance surfaces | Workflow green is execution evidence, not assurance certification. |
| Authority boundary | PASS | governance + portfolio integration contract | Reference implementation does not acquire upstream specification or TRQP stack authority. |

## Completion boundary

Repository-owned public baseline gaps are closed by the associated remediation PR. Required-status enforcement remains a GitHub-hosted control tracked separately rather than represented as PASS.
