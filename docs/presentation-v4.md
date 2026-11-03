---
layout: default
title: "Presentation v4 (v0.20.0)"
description: "Current reference explainer for the experimental v0.20.0 release; v3 preserved as a historical snapshot."
nav_order: 3
permalink: /presentation-v4/
---
# CAWG–TRQP Explainer Presentation v4
{: .fs-9 }

A 20-slide, **non-normative** reference explainer aligned to the
[v0.20.0 release](https://github.com/sankarshanmukhopadhyay/cawg-trqp-verifier-refimpl/releases/tag/v0.20.0)
(3 November 2026). The presentation covers existing verifier profiles,
evidence and audit paths, experimental Delegated Creator scenarios,
and the distinction between local test results and independent assurance.
{: .fs-6 .fw-300 }

[Open v4 PDF](../assets/presentations/cawg-trqp-explainer-v4.pdf){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View historical v3](presentation.md){: .btn .fs-5 .mb-4 .mb-md-0 .mr-2 }
[Release notes](../RELEASE_NOTES_v0.20.0.md){: .btn .fs-5 .mb-4 .mb-md-0 }

## Artifact status

| Field | Value |
|---|---|
| Explainer version | **v4** |
| Implementation baseline | **v0.20.0**, released 3 November 2026 |
| Slides | 20 |
| Status | Explanatory and non-normative |
| PDF | `assets/presentations/cawg-trqp-explainer-v4.pdf` |
| Integrity evidence | [v4 manifest](../assets/presentations/manifest-v4.json), containing the uploaded PDF's SHA-256 |
| Previous explainer | [v3 (v0.19.2)](presentation.md), retained without replacement |

**Authority boundary.** The PDF explains repository behavior but does not
define CAWG, C2PA, or TRQP requirements. The implementation, JSON Schemas,
OpenAPI contract, profiles, and authoritative upstream specifications govern
where any wording differs. The Delegated Creator work in v0.20.0 remains
experimental: synthetic scenarios, locally pinned Ed25519 keys and
mock-driven adapter tests do **not** demonstrate adopted CAWG assertions,
independently verified signer identity, organizational authority, trusted
signing time, or C2PA/TRQP interoperability. The remaining independent evidence
gate is [issue #75](https://github.com/sankarshanmukhopadhyay/cawg-trqp-verifier-refimpl/issues/75).

## What is new compared with v3?

The earlier v3 presentation describes the historical v0.19.2 repository
snapshot. V4 adds the v0.20.0 experimental Delegated Creator and assurance
boundaries (slides 11–13), updates the walkthrough overview (slide 14) and
provides a test-evidence snapshot for 3 November 2026 (slide 17). These
counts are **point-in-time observations from the deck**, not automatically
updated statistics or independent certification.

For current, executable detail, use the
[Delegated Creator traceability](agentic-ai/delegated-creator-trqp-traceability.md),
[five-world demonstration](agentic-ai/taskforce-five-world-demo.md),
[current walkthrough catalogue](sections/walkthroughs-index.md), and
[release notes](../RELEASE_NOTES_v0.20.0.md).

## Embedded v4 presentation

Some browsers can display the PDF below; use **Open v4 PDF** above if the
embedded viewer is unavailable.

<div class="pdf-container">
  <iframe
    src="{{ '/assets/presentations/cawg-trqp-explainer-v4.pdf' | relative_url }}"
    title="CAWG-TRQP verifier explainer v4, pinned to v0.20.0"
    width="100%"
    height="720"
    loading="lazy">
  </iframe>
</div>

## Historical presentations

The [v3 explainer](presentation.md) remains accessible through its existing
page and original PDF path. Its 17 slides, original metadata and hash continue
to describe the v0.19.2 snapshot. No silent substitution or overwrite occurs.

If a newer presentation is published later, preserve this document and v4 PDF
as historical artifacts and publish a new versioned file and integrity record.
