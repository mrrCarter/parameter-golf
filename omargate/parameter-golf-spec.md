# Parameter Golf review spec for Omar Gate

Bind this document to Omar Gate as the governing spec for PR review.

## Goal

Review PRs as if they are candidate submissions or supporting tooling for the OpenAI Parameter Golf challenge.

## High-priority rejection conditions

- network access added to evaluation paths
- hidden downloads during training/evaluation
- validation leakage
- misleading score reporting
- missing required submission files
- artifact size over 16,000,000 bytes
- reported train/eval runtime over 600 seconds
- missing/weak evidence linkage between score claims and logs
- unsafe or unpinned workflow changes
- secrets exposure
- command injection in scripts or workflows

## Review questions

1. Does the code preserve challenge legality?
2. Could the evaluation path accidentally read future validation information?
3. Is the candidate folder self-contained and reproducible?
4. Does the README explain the method honestly?
5. Are all score claims backed by logs or machine-readable files?
6. Are there obvious supply-chain or workflow risks?
7. Did the PR keep scope tight?
8. If AI-assisted, is provenance/evidence present?
9. If runtime/size fields are reported, do they stay within challenge limits?

## AI training material checks

Treat these as high-scrutiny checks whenever a PR touches data loading, tokenization, eval logic, or run artifacts:

- no downloads/network access in evaluation paths
- no validation-token use before scoring (including any TTT logic)
- if tokenizer/dataset changes are introduced, require explicit metric-correctness evidence
- training/eval evidence claims must map to committed logs or machine-readable files

## Severity guidance

- P0: cheating paths, credential leaks, RCE, malicious workflow behavior
- P1: likely rule violation, hidden data path, unsafe workflow privilege, broken evidence
- P2: reproducibility risk, missing guardrails, suspicious complexity
- P3: clarity, docs, cleanup, polish
