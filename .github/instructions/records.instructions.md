# Instructions for files under records/

This path contains candidate submission folders for Parameter Golf.

## Rules

- Each candidate folder should be self-contained.
- Required files:
  - `README.md`
  - `submission.json`
  - `train_gpt.py`
  - at least one training log
- Keep the explanation honest.
- If using evaluation tricks like sliding-window evaluation or legal TTT, document them explicitly.
- If using multiple seeds, report all seeds and the mean/std.
- Never hide a failing seed.
- Prefer explicit environment variable blocks in the README.

## Do not

- silently change tokenizer assumptions
- silently change dataset assumptions
- include unverifiable score claims
- add huge helper frameworks unless clearly justified
