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
