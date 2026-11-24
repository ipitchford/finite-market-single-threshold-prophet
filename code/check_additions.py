#!/usr/bin/env python3
"""Checks for the results added in revision (mpmath, 50 digits; no assert statements).

1. Boundary cases k = n or ell = n (Proposition 2.4): exact enumeration of random
   discrete product laws, every calibrated threshold, against the stated values.
2. Fixed stockout target under identical laws (Proposition 2.5): formula, optimum at
   p = b/n, and the limiting ratio of the two-point hard instance.
3. Heterogeneity gap C^iid - C (Corollary 3.3): n * gap against the coefficient.
4. Optimal stockout targets q* (Table 2) and the n^2 stockout gap at large n.
Prints a JSON summary; exits 1 on any failure.
"""
import json, random, sys
from itertools import product, permutations
from fractions import Fraction as Fr
import mpmath as mp

mp.mp.dps = 50
FAIL = []


def check(cond, msg):
    if not cond:
        FAIL.append(msg)


def binom_pmf(m, p):
    return [mp.binomial(m, j) * p**j * (1 - p)**(m - j) for j in range(m + 1)]


def low(m, p, k):
    """P(Bin(m,p) = j) for j < min(k, m+1), computed by the recursion (only k terms)."""
    p = mp.mpf(p)
    if p == 1:
        return [mp.mpf(int(j == m)) for j in range(k)]
    x = (1 - p)**m
    out = []
    for j in range(k):
        out.append(x if j <= m else mp.mpf(0))
        x = x * (m - j) * p / ((j + 1) * (1 - p)) if j < m else mp.mpf(0)
    return out


def U(m, p, k):
    """E min(Bin(m,p), k) / k."""
    return 1 - mp.fsum((k - j) * x for j, x in enumerate(low(m, p, k))) / k


def tail(m, p, k):
    return 1 - mp.fsum(low(m, p, k))


def A(m, p, k):
    """E min(1, k/(1+Bin(m,p))) via A_m(p) = k U_{m+1}(p) / ((m+1) p)."""
    p = mp.mpf(p)
    if p == 0:
        return mp.mpf(1)
    return k * U(m + 1, p, k) / ((m + 1) * p)


def bis(f, lo, hi, it=130):
    lo, hi = mp.mpf(lo), mp.mpf(hi)
    flo = f(lo)
    for _ in range(it):
        mid = (lo + hi) / 2
        fm = f(mid)
        if (fm < 0) == (flo < 0):
            lo, flo = mid, fm
        else:
            hi = mid
    return (lo + hi) / 2


def pcal(m, k, q):
    return bis(lambda p: tail(m, p, k) - q, 0, 1)


# ---------- 1. boundary cases by exact enumeration -----------------------------
def F2M(x):
    return mp.mpf(x.numerator) / x.denominator


def pb_pmf(ps):
    mass = [Fr(1)]
    for p in ps:
        new = [Fr(0)] * (len(mass) + 1)
        for j, x in enumerate(mass):
            new[j] += (1 - p) * x
            new[j + 1] += p * x
        mass = new
    return mass


def exact_ratio(laws, t, h, k, ell):
    """Direct enumeration over values, tie coins and all orders (exact rationals)."""
    n = len(laws)
    enriched = []
    for law in laws:
        e = []
        for v, w in law:
            c = Fr(1) if v > t else (h if v == t else Fr(0))
            for z, pr in ((True, c), (False, 1 - c)):
                if pr:
                    e.append((v, w * pr, z))
        enriched.append(e)
    orders = list(permutations(range(n)))
    reward = Fr(0)
    prophet = Fr(0)
    for s in product(*enriched):
        wgt = Fr(1)
        for _, pr, _ in s:
            wgt *= pr
        vals = sorted((x[0] for x in s), reverse=True)
        prophet += wgt * sum(vals[:ell])
        tot = Fr(0)
        for o in orders:
            qual = [s[i][0] for i in o if s[i][2]]
            tot += sum(qual[:k])
        reward += wgt * tot / len(orders)
    probs = [sum(w for _, w, z in e if z) for e in enriched]
    return (reward / k) / (prophet / ell), probs


def boundary_checks(trials=60, seed=20261124):
    rng = random.Random(seed)
    count = 0
    worst = {"all_static_k_eq_n": None, "fixed_q_k_eq_n": None, "fixed_q_ell_eq_n": None}
    for _ in range(trials):
        n = rng.choice([2, 3])
        laws = []
        for _ in range(n):
            a, b = sorted(rng.sample(range(0, 6), 2))
            w = Fr(rng.randint(1, 4), 5)
            laws.append([(Fr(a), w), (Fr(b), 1 - w)])
        support = sorted({v for law in laws for v, _ in law})
        for t in support:
            for h in (Fr(0), Fr(1, 3), Fr(1)):
                for k, ell in ((n, rng.randint(1, n)), (rng.randint(1, n), n)):
                    r, probs = exact_ratio(laws, t, h, k, ell)
                    D = pb_pmf(probs)
                    q = sum(D[k:])
                    if k == n:
                        # all-static: accepting all values gives ell/n; fixed q: min(q^{1/n}, ell/n)
                        if t == support[0] and h == 1:
                            check(r >= Fr(ell, n), f"accept-all below ell/n {laws}")
                        if 0 < q < 1:
                            bound = min(F2M(q) ** (mp.mpf(1) / n), mp.mpf(ell) / n)
                            check(F2M(r) >= bound - mp.mpf('1e-40'), f"k=n fixed-q {laws} {t} {h}")
                            count += 1
                    if ell == n and k < n and 0 < q < 1:
                        bound = U(n, pcal(n, k, F2M(q)), k)
                        check(F2M(r) >= bound - mp.mpf('1e-30'), f"ell=n fixed-q {laws} {t} {h}")
                        count += 1
                    if ell == n and k <= n and t == support[0] and h == 1:
                        # accept the first k in random order: ratio >= 1
                        check(r >= 1, f"ell=n accept-first-k {laws}")
    return count


# ---------- 2. fixed q under identical laws -------------------------------------
def iid_fixed_q(n, k, b, q):
    p = pcal(n, k, q)
    return min(U(n, p, k), mp.mpf(b) / k * A(n - 1, p, k)), p


def iid_instance_ratio(n, k, ell, q, eps, M):
    """Two-point iid law (1 w.p. 1-eps, M w.p. eps) at the calibrated threshold t = 1."""
    p = pcal(n, k, q)                      # qualification probability of every applicant
    W = U(n, p, k) + n * eps * (M - 1) * A(n - 1, p, k) / k
    # E top-ell sum: R ~ Bin(n, eps) rare draws
    top = mp.fsum(w * (min(r, ell) * M + (ell - min(r, ell))) for r, w in enumerate(binom_pmf(n, eps)))
    return W / (top / ell), p


def iid_checks():
    out = []
    for n, k, ell in ((3, 2, 2), (6, 2, 4), (10, 3, 3), (5, 1, 2), (8, 3, 2)):
        b = ell
        # optimum over q equals C^iid = U_n(b/n), attained at q = P(B_n(b/n) >= k)
        qstar = tail(n, mp.mpf(b) / n, k)
        val, p = iid_fixed_q(n, k, b, qstar)
        Ciid = U(n, mp.mpf(b) / n, k)
        check(abs(val - Ciid) < mp.mpf('1e-30'), f"iid optimum {n,k,ell}")
        check(abs(p - mp.mpf(b) / n) < mp.mpf('1e-30'), f"iid optimum p {n,k,ell}")
        for dq in (mp.mpf('-0.05'), mp.mpf('0.05')):
            check(iid_fixed_q(n, k, b, qstar + dq)[0] < Ciid, f"iid not max {n,k,ell}")
        # second branch is approached by the two-point instance (eps M -> infinity, eps -> 0)
        q = qstar + mp.mpf('0.1') if qstar < mp.mpf('0.85') else qstar - mp.mpf('0.1')
        branch2 = mp.mpf(b) / k * A(n - 1, pcal(n, k, q), k)
        r, _ = iid_instance_ratio(n, k, ell, q, mp.mpf('1e-12'), mp.mpf('1e18'))
        check(abs(r - branch2) < mp.mpf('1e-5'), f"iid instance branch2 {n,k,ell}")
        out.append({"n": n, "k": k, "ell": ell, "q_star_iid": float(qstar), "C_iid": float(Ciid),
                    "instance_ratio": float(r), "branch2": float(branch2)})
    return out


# ---------- 3./4. heterogeneous constants and gaps ------------------------------
def C_all(n, k, b):
    m = n - 1
    p = bis(lambda x: U(m, x, k) - mp.mpf(b) / k * A(m, x, k), 0, 1)
    return U(m, p, k), p


def F_best(n, k, b):
    m = n - 1
    def diff(pd):
        q = tail(m, pd, k)
        return U(n, pcal(n, k, q), k) - mp.mpf(b) / k * A(m, pd, k)
    pd = bis(diff, mp.mpf('1e-12'), 1 - mp.mpf('1e-12'))
    return mp.mpf(b) / k * A(m, pd, k), tail(m, pd, k)


def F2M(x):
    return mp.mpf(x.numerator) / x.denominator


def pois(lam, j):
    return mp.e**(-lam) * lam**j / mp.factorial(j)


def coeffs(k, b):
    b = mp.mpf(b)
    lo = mp.fsum(pois(b, j) for j in range(k))           # P(Z < k)
    hi = 1 - lo - pois(b, k)                              # P(Z > k)
    c = 1 - mp.fsum((k - j) * pois(b, j) for j in range(k)) / k
    first = b * lo * hi / (k * c)
    second = b * mp.fsum((k - 1 - j) * pois(b, j) for j in range(k - 1)) / (2 * k) * hi / c
    return c, first, second


def gap_checks():
    rows = []
    for k, b in ((1, 1), (2, 2), (3, 3), (2, 1), (2, 4), (4, 1.5)):
        c, first, second = coeffs(k, b)
        scaled = []
        for n in (200, 800, 3200):
            C, _ = C_all(n, k, b)
            Ciid = U(n, mp.mpf(b) / n, k)
            scaled.append(n * (Ciid - C))
        # Richardson (error O(1/n)): 2*s(2n)-s(n) with the factor-4 grid -> (4 s(4n) - s(n))/3
        rich = (4 * scaled[2] - scaled[1]) / 3
        check(abs(rich - first) < mp.mpf('2e-4') * first, f"first-order gap {k,b}")
        check(abs(scaled[2] - first) < abs(scaled[0] - first), f"first-order trend {k,b}")
        rows.append({"k": k, "b": float(b), "coefficient": float(first),
                     "n_times_gap_n200_800_3200": [float(x) for x in scaled],
                     "richardson": float(rich)})
    return rows


def stockout_gap_large_n():
    rows = []
    for k, b in ((2, 2), (3, 3)):
        _, _, second = coeffs(k, b)
        vals = []
        for n in (1000, 4000):
            C, _ = C_all(n, k, b)
            F, _ = F_best(n, k, b)
            vals.append(n * n * (C - F))
        check(abs(vals[-1] - second) < mp.mpf('2e-3') * second, f"second-order gap {k,b}")
        rows.append({"k": k, "b": b, "coefficient": float(second),
                     "n2_gap_n1000_4000": [float(v) for v in vals]})
    return rows


def qstar_table():
    rows = []
    for n, k, ell in ((3, 2, 2), (6, 2, 4), (10, 3, 3), (20, 2, 2), (50, 2, 2)):
        F, q = F_best(n, k, ell)
        C, _ = C_all(n, k, ell)
        Ciid = U(n, mp.mpf(ell) / n, k)
        rows.append({"n": n, "k": k, "ell": ell, "q_star": float(q), "best_stockout_value": float(F),
                     "all_static": float(C), "q_star_iid": float(tail(n, mp.mpf(ell) / n, k)),
                     "identical_laws": float(Ciid)})
    for k in (1, 2, 3, 5, 10):
        lam = mp.mpf(k)
        rows.append({"n": "all", "k": k, "ell": k,
                     "q_star": float(1 - mp.fsum(pois(lam, j) for j in range(k))),
                     "gamma_k": float(1 - mp.e**(-k) * mp.mpf(k)**k / mp.factorial(k))})
    return rows


if __name__ == "__main__":
    summary = {"boundary_calibrated_thresholds_checked": boundary_checks(),
               "iid_fixed_q": iid_checks(),
               "heterogeneity_gap_first_order": gap_checks(),
               "stockout_gap_second_order": stockout_gap_large_n(),
               "targets": qstar_table(),
               "failures": FAIL}
    print(json.dumps(summary, indent=1))
    if FAIL:
        sys.exit(1)
    print("ALL ADDITIONAL CHECKS PASSED", file=sys.stderr)
