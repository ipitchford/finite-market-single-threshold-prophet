# Review summary (public, 0.1.0-candidate)

This records the internal review of the candidate: who looked, what they raised, and what was done. It is
AI-assisted internal review, not peer review or independent reproduction.

## What ran

1. **Panel (round 1).** Five reviewer roles, editor, methodology (proof audit), domain (prophet inequalities and
   static pricing), perspective (pricing practice and statistics) and devil's advocate, run as one combined Claude
   pass, with independent recomputation of the key numbers.
2. **Lead proof audit, by hand.** Every step of Lemma 2.2, the decomposition (4), the lower and upper bounds of
   Theorem 2.1, the supporting-line inequality (7), degree elevation, the boundary cases, strictness, and
   Corollaries 3.1 and 3.2 and Section 4.
3. **Numerical checks.** A 50-digit check of the new results and a clean replay of every script, with negative controls.
4. **One revision round** with four extensions (Proposition 2.4, Corollary 3.3, Proposition 2.6, the table of optimal targets).
5. **Re-review and proof audit** of the new and rewritten material: no critical or major item; all minor items applied.

No second-model (Astra/Codex) adversarial review took place for this release.

## Main objections and dispositions

| Objection | Disposition |
|---|---|
| Correctness | No error found by the panel or the audits. The hard instance was checked to defeat every threshold (all threshold ranges, and randomisation). |
| Exposition: no plain introduction, sections open with formulas, notation collisions | Section 1 rewritten (problem, why it matters, what was known, what is new, plan); every section opens with a sentence saying what it does; notation renamed to remove collisions. |
| Novelty not argued: why did the conjecture stay open, what is the new ingredient? | Novelty paragraph added. It says plainly that Arnosti and Ma's own Lemma 1 combined with the crossing lemma already yields the conjecture, and that applying the comparison to each buyer's rival count is what makes the finite values exact. |
| Positioning against Arnosti and Ma's utilisation-calibrated rule | Proposition 2.4 added: at the target nu = C the utilisation rule attains the distribution-aware value at every n. Binomial extremality at matched utilisation credited to their Lemma 2. |
| Abstract over-reach on the extensions | Abstract and Section 4 limit the extensions to the interior range and, for order mixtures, to the distribution-aware and stockout rules. |
| Boundary cases buried | Now Proposition 2.5 with a full proof. |
| Missing citations | Ehsani et al. (2018) for k = 1, Loiseau et al. (2026) for dispersion-limited benchmarks, and the related Evidence Press release on adaptive i.i.d. limits added. |
| Practical message buried | Implications paragraph and Table 1 of optimal targets; heterogeneity cost quantified (Corollary 3.3). |
| Continuous-law remark under-specified; uniqueness of the large-n root needs a line | Both clarified. |

## Limits that remain

The open questions in Section 6 of the paper; worst-case scope; literature search of limited scope (recorded in
RESEARCH_GATES.json).
