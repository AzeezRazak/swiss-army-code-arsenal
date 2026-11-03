# Sprint 0001 retrospective

Standard-library-only scope enabled all five examples and 16 tests to run without installation or network dependencies. Seeded reference comparisons covered more input combinations than a few fixed examples, while subprocess tests checked actual exit behavior.

No implementation tests failed. This is evidence of the tested cases only, not absence of defects. Testing covered one Windows runtime; portability claims remain deliberately limited.

Action RETRO-0001: owner Codex, target Sprint 0002. For each new CLI, define malformed-input, resource and timeout behavior before implementation and include a subprocess regression check. Completion measure: review links each documented error policy to an executed test. Effectiveness remains unverified until Sprint 0002.

Action RETRO-0002: owner Codex, target Sprint 0002 planning/execution. Record runtime/platform limits in every new README and avoid implying unrun platforms pass. Completion measure: review confirms explicit platform status for all new implementations. No historical corrective action has yet been verified.
