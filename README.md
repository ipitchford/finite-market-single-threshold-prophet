# Sharp finite-market prophet inequalities for a single threshold

*Exact worst-case values of a fixed threshold in random-order markets, and a proof of the Arnosti-Ma stockout conjecture*

Version 0.1.0-candidate. DOI [10.5281/zenodo.24506643](https://doi.org/10.5281/zenodo.24506643) (all versions:
[10.5281/zenodo.24506642](https://doi.org/10.5281/zenodo.24506642)). Release page:
https://evidencepress.org/releases/finite-market-single-threshold-prophet/

**Status: unrefereed research candidate.** Author: Anonymous. Text CC0-1.0; code MIT (see [LICENSE.md](LICENSE.md)).

## What this is about

A seller has k identical items and faces n buyers who arrive one at a time in random order. Each buyer's value comes
from a known distribution, and different buyers may have different distributions. The seller posts **one price**,
never changes it, and sells to the first k buyers who will pay it. The same rule describes one hiring bar for k posts,
or one quality cut-off for k slots. How much of the best possible outcome can such a fixed rule guarantee? The
benchmark is a "prophet" who sees every value in advance and keeps the best l of them, compared per place filled.

**Why it matters.** One posted price is simple and fair, gives nobody a reason to wait, and can be tuned from data:
a seller can adjust the price until one market statistic, such as how often the stock sells out, hits a target.

**What was known.** Arnosti and Ma (Operations Research, 2023) found the best large-market guarantee of a fixed
threshold, 1 - e^-k k^k/k! (about 63% for one item and 73% for two), using a target for the average fraction of stock
sold. They conjectured that targeting the probability of selling out, at a particular level, works too. Exact
finite-market answers existed only for identically distributed buyers (Arnosti; Jiang, Ma and Zhang) or for
adversarial arrival order. Molina, Gast, Loiseau and Perchet (SODA 2025) found the large-market value when the seller's
and the prophet's capacities differ, for identical buyers, and asked whether it extends to different buyers.

**What is new.**
1. Exact worst-case guarantees at every finite market size n > max(k, l), for buyers with different distributions:
   for the best distribution-aware price, for a price tuned to a sell-out (stockout) probability, for a price tuned to
   the expected fraction of stock sold (utilisation), and for identical buyers; the boundary cases k = n or l = n too.
2. The Arnosti-Ma conjecture is true for every number of items and every market size. (As the paper says, Arnosti and
   Ma's own Lemma 1 combined with the crossing lemma below already yields it; the finer finite results need more.)
3. Molina et al.'s question: yes for fixed thresholds, in the large-market limit.
4. A ranking. Tuning utilisation to the right finite target loses nothing against knowing every distribution. Tuning
   the sell-out probability loses a tiny amount of order 1/n^2 (about 0.030/n^2 for two items). Different buyers cost
   of order 1/n compared with identical buyers (about 0.18/n for two items). Example: three buyers, two items: 79.1%
   guaranteed; 78.7% with the best sell-out target; 85.2% if buyers are alike.

**Idea of the proof.** Compare the number of buyers who clear the price with a binomial or Poisson count that has the
same sell-out probability: the two distribution curves cross exactly once, which bounds both the fraction sold and
each buyer's chance of being served. For the matching upper bound, one market of ordinary buyers plus one rare, very
valuable buyer defeats every possible price at once.

**Limits.** One anonymous fixed threshold; independent values; random arrival order (or the stated mixtures with an
adversarial order); worst-case guarantees, so typical markets do better; the hard cases rely on a rare, very valuable
buyer. Open: the exact finite value of the expected-demand rule, the stockout cost under order mixtures, and the gap
to adaptive policies at finite n.

## Contents

| Path | What |
|---|---|
| `manuscript.pdf`, `manuscript.tex`, `secondorder.tex` | The paper (14 pages); Section 1 is a plain introduction with a plan of the paper |
| `code/verify.py` | Exact rational checks: crossing lemma on 585 Bernoulli profiles; welfare decomposition on 12 product laws by direct enumeration; supporting-slope grid on 650 parameter triples; values table |
| `code/check_extensions.py` | Order-mixture hard instances at 189 profiles; scaled stockout gap against its coefficient at five parameter pairs |
| `code/check_additions.py` | 50-digit (mpmath) checks: boundary cases (643 calibrated thresholds), identical-law results, heterogeneity coefficient, Table 1 targets |
| `code/figure.py` | Regenerates `figures/frontier.pdf` |
| `results/` | Recorded outputs: `verify.txt`, `extensions.txt`, `additions.json` |
| `refs.bib` | The manuscript's 9 references |
| `AI_INDEX.md` | Machine-oriented map of claims, evidence and limits |
| `RESEARCH_GATES.json` | Prior-art searches, sources read, limitation triage |
| `REVIEW_SUMMARY.md` | Internal review: objections and how they were handled |
| `REPLAY_RECEIPT.md`, `ENVIRONMENT.txt` | Release replay and the cross-platform comparison policy |
| `MANIFEST.sha256` | SHA-256 of every file |

## Replay

From the package root, with CPython 3.12 and the pinned versions in `requirements.txt` (mpmath 1.3.0, matplotlib 3.10.8):

```sh
python -I -B -O code/verify.py > results/verify.txt
python -I -B -O code/check_extensions.py > results/extensions.txt
python -I -B -O code/check_additions.py > results/additions.json   # stderr: ALL ADDITIONAL CHECKS PASSED
python -E -s -B code/figure.py                                       # imports check_extensions, so not -I
```

Each script exits 1 on any failed check, also under `python -O` (no `assert` statements). On macOS arm64 under
CPython 3.12.11 the outputs are byte-identical to `results/`. **Cross-platform policy** (also in CI, ENVIRONMENT.txt and
REPLAY_RECEIPT.md): exact counts, labels and all non-numeric text compare exactly; numbers in `verify.txt` and
`extensions.txt` (printed to 8 decimals from double-precision bisection) within absolute 1e-7; floating-point numbers in
`additions.json` within relative 1e-9; the figure PDF is regenerated but not compared. The exact-rational checks are
platform independent. GitHub Actions reruns everything on Linux under this policy, with two negative controls.

## Assurance

Written proofs with exact and high-precision computational checks. Internal AI-assisted review only: five reviewer
roles (editor, methodology, domain, perspective, devil's advocate) run as one combined Claude pass, the lead's own
proof audit by hand, a 50-digit numerical check and a clean replay; one revision round with extensions; then a
re-review and proof audit of the new material. No second-model (Astra/Codex) review took place. This is not peer
review, independent reproduction or formal verification. See [REVIEW_SUMMARY.md](REVIEW_SUMMARY.md).

## Cite

Anonymous (2026). *Sharp finite-market prophet inequalities for a single threshold* (Version 0.1.0-candidate).
Evidence Press. https://doi.org/10.5281/zenodo.24506643
