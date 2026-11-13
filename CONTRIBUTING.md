# Contributing to MarketPulse

## Local workflow

1. Create a short-lived branch from `main` using the format
   `type/short-description` (for example, `feat/news-ingestion`).
2. Keep datasets, checkpoints, experiment results, local environments, and
   runtime logs out of commits; `.gitignore` covers these generated artifacts.
3. Update `readme.md` or `RUN_LOCAL.md` when a change affects the demo's setup
   or operation.
4. Before opening a pull request, run the relevant demo or visualization and
   state what was checked in the PR description.

## Pull requests

Use a focused title, describe the behaviour changed, and link the related
issue when one exists. The MarketPulse demo is analyst-review only: changes
must not introduce automatic trading or execution behaviour.
