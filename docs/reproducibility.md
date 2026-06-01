# Reproducibility

The package is designed to reproduce the paper's analysis tables from released CSV artifacts. It does not rerun LLM generation or machine judging because that would require provider credentials and may produce non-identical stochastic outputs.

Use `make validate` to check artifact integrity and `make tables` to regenerate core tables under `derived/`.
