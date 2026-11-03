# Sprint 0002 retrospective

Absolute frame deadlines passed a trickle-byte regression; independent accept/receive/send bounds keep the demonstration finite. Ephemeral-port integration checks and cleanup prevented hanging test processes. Three runnable deliverables met the five-script cap.

Windows denied real symlink creation. The original test was honestly skipped; adding a real junction test verified the native reparse-point behavior without changing system privileges. This does not establish POSIX or privileged Windows symlink behavior. QA-0003 carries the remaining evidence gap.

RETRO-0001 and RETRO-0002 were applied: explicit error/resource contracts and runtime limits appear in both guides, with executable checks and stated limitations. Action RETRO-0003: Codex, Sprint 0003, keep platform-dependent tests distinguishable from ordinary assertions and report skip reasons separately. Completion measure: review lists each skipped integration check and its follow-up ID; no silent conversion to a pass.
