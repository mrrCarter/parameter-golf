# Instructions for GitHub workflow files

This repo uses workflows for:
- Omar Gate security review
- challenge-specific validation
- optional GPU/nightly runs

## Requirements

- pin major actions to stable versions
- upload artifacts when checks fail
- fail closed on required checks
- keep PR workflow cheap
- keep heavyweight GPU work in manual or self-hosted workflows
