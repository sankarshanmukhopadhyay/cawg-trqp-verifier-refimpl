# CAWG-TRQP Verifier Reference Implementation v0.19.2

## Decision isolation and assurance hardening

Published **1 September 2026**. This patch release closes the v0.19.x hardening tranche.

### Fixed
- Isolated transient transport, revocation, descriptor and cache evidence per verification execution context.
- Rejected malformed process evidence at the typed request boundary, including non-numeric, non-finite and out-of-range confidence values.

### Assurance
- Made `make validate` the authoritative repository completion gate.
- Added machine-readable adversarial vectors for delegated-authority misuse, gateway substitution, revoked issuer recognition, provenance stripping and replay-root confusion.
- Generated and attached checksum evidence to the published release.

### Authority and limitations

No CAWG/C2PA or TRQP normative authority is asserted. The release does not establish independent certification or external interoperability. The experimental Delegated Creator and external C2PA validation adapter merged onto `main` later and are **not** part of v0.19.2.

[Published GitHub release and assets](https://github.com/sankarshanmukhopadhyay/cawg-trqp-verifier-refimpl/releases/tag/v0.19.2)
