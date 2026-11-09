# Offline request budget planner

File: `SCRIPTS/09-automation-scripting/request-budget-plan/README.md`

Folder: `SCRIPTS/09-automation-scripting/request-budget-plan`

`build_rate_plan.py` creates a reviewable schedule from request, interval, concurrency and body-size limits. It does not send requests, create workers or contact targets.

Example: `python SCRIPTS/09-automation-scripting/request-budget-plan/build_rate_plan.py --requests 5 --interval 2 --concurrency 2 --body-bytes 4096`
