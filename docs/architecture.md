# Architecture

## v0.9.0 architecture

CAWG/C2PA manifest
  -> signal extraction
  -> verifier
     -> direct TRQP service or trust gateway
     -> process appraisal
     -> verification result
     -> optional audit bundle export

The trust gateway is optional. Process evidence is optional unless policy requires it.


## Bundle attestation and reproducibility

The evidence plane now distinguishes between a bundle digest and an optional bundle attestation. The digest answers whether the exported bundle content is internally deterministic. The attestation answers whether an identified signer vouches for that exported artifact.

Replay inputs now also carry pinned policy feed metadata. This keeps replay portable without forcing the bundle to embed mutable policy state. In practice, this creates a cleaner separation between the evidence artifact, the signer, and the policy source used to reproduce the decision.
