# Architecture

File: `DOCS/ARCHITECTURE.md`

Folder: `DOCS`


Domain directories hold independently usable implementations. Add a named subdirectory per implementation when development is authorized. Keep runtime configuration close to that implementation. Shared helpers require demonstrated reuse, not speculative abstraction.

TESTS contains discoverable regression checks; EXAMPLES contains synthetic usage data; BENCHMARKS records reproducible performance experiments; TOOLS holds repository maintenance utilities. DOCS contains cross-cutting standards and the catalog. TODO is the authoritative management system. Domain README files indicate planned scope, not completed capabilities.
