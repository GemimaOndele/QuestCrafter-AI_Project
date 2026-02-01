## Contribution guidelines

### Branching
- Base branch: `main`
- Work on short-lived branches using prefixes:
  - `feat/` for features
  - `fix/` for bug fixes
  - `docs/` for documentation
- Example: `feat/data-pipeline`, `docs/board`

### Workflow
1) Create an issue and assign yourself
2) Create a branch from `main`
3) Push commits to your branch
4) Open a Pull Request (PR)
5) Request review from at least one teammate
6) Merge after approval

### Commit messages
Use short, action-oriented messages:
- `add data filters for reddit jokes`
- `update README with pipeline steps`

### Code style
- Keep functions small and readable
- Use explicit variable names
- Add comments only when needed to explain non-obvious logic

### Data files
- Do not commit large raw datasets
- Keep `data/raw/` and `data/processed/` ignored by git
