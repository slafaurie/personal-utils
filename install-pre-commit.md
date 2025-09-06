Pre-commit are set of commands that run once we commit to the git history. I view them as local CI pipeline which makes sure
everything runs smoothly beforing committing changes to the main branch. To use them:

1. First, Install[[ref](https://adamj.eu/tech/2025/05/07/pre-commit-install-uv/)] precommit using uv by: 
    * `uv tool install pre-commit --with pre-commit-uv`
    * add install folder to path `$env:PATH = {path}`. You'll most likely receive the full instruction once the previous command finishes

2. Create a `.pre-commit-config.yaml` in the root directory and add your most used pre-commit. For example, here are two that:
    * Clear jupyter notebook cells output (which tends to bloat repo size)
    * Run ruff linter and format to enforce proper styling
    ```
   repos:
   -   repo: https://github.com/kynan/nbstripout
       rev: 0.7.1
       hooks:
       -   id: nbstripout
           files: ".ipynb$"
   
   - repo: https://github.com/astral-sh/ruff-pre-commit
     # Ruff version.
     rev: v0.12.12
     hooks:
       # Run the linter.
       - id: ruff-check
         types_or: [ python, pyi ]
         args: [ --fix ]
       # Run the formatter.
       - id: ruff-format
         types_or: [ python, pyi ]
   ```
