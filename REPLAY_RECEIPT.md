# Replay receipt (0.1.0-candidate, 24 November 2026)

**Environment.** macOS arm64; CPython 3.12.11 (uv-managed, printed inside the run); mpmath 1.3.0, matplotlib 3.10.8.
Each run used a fresh copy of the approved candidate, cwd = package root, `PYTHONDONTWRITEBYTECODE=1`.

| Run | Command | Exit | Output vs `results/` |
|---|---|---|---|
| verify, plain and -O | `python [-O] -I -B code/verify.py` | 0, 0 | stdout byte-identical to `verify.txt` |
| extensions, plain and -O | `python [-O] -I -B code/check_extensions.py` | 0, 0 | stdout byte-identical to `extensions.txt` |
| additions, plain and -O | `python [-O] -I -B code/check_additions.py` | 0, 0 | stdout byte-identical to `additions.json`; stderr "ALL ADDITIONAL CHECKS PASSED" |
| figure | `python -E -s -B code/figure.py` | 0 | `figures/frontier.pdf` regenerated (not compared) |

**Negative controls (under -O).**
1. `check_additions.py` with the 1/n heterogeneity coefficient multiplied by 1.01: exit 1, failures listed.
2. `verify.py` with 1 added to the exact welfare-decomposition identity: "CHECK FAILED", exit 1.

**After the replay** only the title-page DOI line of `manuscript.tex`, the rebuilt PDF (three pdflatex passes, 14 pages)
and the release records changed; the code, recorded outputs, figure and requirements are byte-identical to the
replayed candidate.

**Cross-platform policy** (declared before tagging; see ENVIRONMENT.txt): text outputs token by token with decimal
numbers within absolute 1e-7; `additions.json` floats within relative 1e-9; everything else exact. The GitHub Actions
workflow `.github/workflows/replay.yml` reruns every script under `python -O` on Linux, compares under this policy and
runs both negative controls (blocking).

**Scope.** The computations check formulas and tabulated values on finite cases. The proofs carry the theorems.
