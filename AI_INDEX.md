# AI index: Sharp finite-market prophet inequalities for a single threshold (v0.1.0-candidate)

Machine-oriented map of claims, evidence and limits. Human readers should start with [README.md](README.md) ("What
this is about") and the paper [manuscript.pdf](manuscript.pdf) (sources [manuscript.tex](manuscript.tex) and
[secondorder.tex](secondorder.tex); Section 1 is a plain introduction with a plan of the paper). DOI
10.5281/zenodo.24506643 (concept 10.5281/zenodo.24506642). Status: unrefereed candidate; internal AI-assisted review only.

## Normalisation

n values V_1..V_n independent, nonnegative, integrable, laws G_i (possibly different); uniformly random arrival order
independent of the values. Static threshold (t, h): values above t qualify, values equal to t qualify with probability h
(common tie coin); the first k qualifiers are accepted. W = E[sum accepted]/k; H = E[sum of the l largest]/l; b = l
(Section 4 allows non-integer b = 1/omega_1). D = number of qualifiers, D_{-i} = qualifying rivals of i; stockout
probability q = P(D >= k); utilisation E min(D,k)/k. u(d) = min(d,k)/k, a(d) = min(1, k/(1+d)); U_m(p) = E u(Bin(m,p)),
A_m(p) = E a(Bin(m,p)); p_m(q) solves P(Bin(m,p) >= k) = q; m = n-1. C_{n,k,l} = inf_G sup_{t,h} W/H (all-static value);
S_{n,k,l}(q) fixed-stockout value; R_{n,k,l}(nu) fixed-utilisation value; superscript iid: identical laws.
gamma_k = 1 - e^-k k^k/k!. AM = Arnosti and Ma, Operations Research 71(5) (2023), doi:10.1287/opre.2022.2419.
MGLP = Molina, Gast, Loiseau and Perchet, SODA 2025, doi:10.1137/1.9781611978322.38. JMZ = Jiang, Ma and Zhang, MOR 51(2) (2026).

## Claims and where they are proved

| ID | Claim | Location | Status / credit |
|---|---|---|---|
| A (main) | For n > max(k,l): S_{n,k,b}(q) = min{U_n(p_n(q)), (b/k)A_m(p_m(q))}; best stockout target is the unique intersection | Theorem 2.1(1) | written proof; new |
| B (main) | C_{n,k,b} = U_m(p_*), (b/k)A_m(p_*) = U_m(p_*); one instance defeats every threshold and every randomisation | Theorem 2.1(2), Section 2.3 | written proof; new |
| C | C^iid_{n,k,b} = U_n(b/n) | Theorem 2.1(3) | written proof; for k = l consistent with Arnosti's blog and JMZ Theorem 8/Corollary 2 |
| D | Crossing lemma: Bernoulli sum vs binomial/Poisson at a common stockout probability: distribution functions cross once at k-1 | Lemma 2.2 | written proof; relative log-concavity tools (Yu 2010) credited |
| E | Utilisation rule: R(nu) = min{nu, (b/k)A_m(U_m^{-1}(nu))}; maximum = C_{n,k,b} at nu = C_{n,k,b} | Proposition 2.4 | written proof; binomial extremality for D is AM Lemma 2 (credited) |
| F | Boundary cases k = n or l = n | Proposition 2.5 | written proof |
| G | Identical-law fixed-stockout curve; optimum equals C^iid | Proposition 2.6 | written proof |
| H | max_q S < C strictly for k >= 2 (equality for k = 1) | Section 2.6, final paragraph | written proof |
| I (main) | Over all market sizes: stockout target P(Pois(k) >= k) attains gamma_k for every k (AM conjecture, AM Section 5.2); unequal capacities give (1/k) sum_j P(Pois(b) >= j), MGLP Theorem 1.4 constant, for heterogeneous values with static thresholds | Corollary 3.1 and the paragraph after it | written proof; the paper notes that AM Lemma 1 plus Lemma 2.2 already gives the conjecture; k = 1 is Ehsani et al. 2018 |
| J | Stockout cost C - max_q S = c_2/n^2 + O(n^-3), explicit c_2 > 0 for k >= 2 (about 0.030 for k = l = 2) | Corollary 3.2 | written proof; checked numerically |
| K | Heterogeneity cost C^iid - C = b P(Z<k) P(Z>k)/(k c n) + O(n^-2), strict at every n (about 0.18/n for k = l = 2) | Corollary 3.3 | written proof; checked numerically |
| L | Weighted rank benchmarks (b = 1/omega_1) and random/adversarial order mixtures (A replaced by A^(rho); parts 1-2) | Section 4 | written proofs; interior range n > max(k,l); rho = 1, b = k recovers JMZ eq. (21) |

## Evidence

| Check | Script | Output | Scope |
|---|---|---|---|
| Crossing pattern on 585 rational Bernoulli profiles; decomposition and two-coefficient bound against direct enumeration on 12 product laws (exact Fractions); supporting slope on 650 triples (float grid); values table | [code/verify.py](code/verify.py) | [results/verify.txt](results/verify.txt) | finite cases; not a proof |
| Order-mixture hard instances at 189 profiles; scaled stockout gap vs Corollary 3.2 coefficient at five (k,b) | [code/check_extensions.py](code/check_extensions.py) | [results/extensions.txt](results/extensions.txt) | finite cases |
| 50-digit checks: boundary cases (643 calibrated thresholds), identical-law fixed-q, Corollary 3.3 coefficient by extrapolation at six (k,b), Table 1 targets | [code/check_additions.py](code/check_additions.py) | [results/additions.json](results/additions.json) | finite cases |
| Figure | [code/figure.py](code/figure.py) | [figures/frontier.pdf](figures/frontier.pdf) | illustration |

Numbers quoted on the release page: n=3, k=l=2: C = (sqrt 21 - 3)/2 = 0.79129, best stockout 0.78666 at q* = 0.64002,
C^iid = 23/27 = 0.85185; gamma_1 = 0.63212, gamma_2 = 0.72933; large-market best stockout target 0.59399 for k = 2;
c_2 = 0.0299982 (k = l = 2); heterogeneity coefficient 0.1799890 (k = l = 2). All in results/.

## Limits

One anonymous fixed threshold with a common tie coin; independent values; random order independent of values (or the
stated mixtures); worst case (infima approached, not attained); hard instances use a rare, very valuable value.
Open: exact finite value of the expected-demand rule; stockout cost under order mixtures; finite gap to adaptive policies.

## Replay and records

Replay commands and cross-platform policy: [README.md](README.md), [ENVIRONMENT.txt](ENVIRONMENT.txt),
[REPLAY_RECEIPT.md](REPLAY_RECEIPT.md), CI [.github/workflows/replay.yml](.github/workflows/replay.yml). Review:
[REVIEW_SUMMARY.md](REVIEW_SUMMARY.md). Prior art and limitation triage: [RESEARCH_GATES.json](RESEARCH_GATES.json).
Bibliography: [refs.bib](refs.bib). Licences: [LICENSE.md](LICENSE.md). Citation: [CITATION.cff](CITATION.cff).
Hashes: [MANIFEST.sha256](MANIFEST.sha256).
