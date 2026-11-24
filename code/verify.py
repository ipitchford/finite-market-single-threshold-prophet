#!/usr/bin/env python3
"""Reproduce small-instance checks and sample constants. Python 3, standard library."""
from fractions import Fraction as F
from itertools import accumulate, combinations_with_replacement, permutations, product
from math import comb, exp, factorial, fsum


def ensure(condition):
    """Explicit check that survives python -O (no assert statements)."""
    if not condition:
        raise SystemExit("CHECK FAILED")


def poisson_binomial(probabilities):
    mass = [1]
    for p in probabilities:
        updated = [0] * (len(mass) + 1)
        for j, mass_j in enumerate(mass):
            updated[j] += (1-p) * mass_j
            updated[j+1] += p * mass_j
        mass = updated
    return mass


def binomial(m, p):
    return [comb(m, j) * p**j * (1-p)**(m-j) for j in range(m+1)]


def utilisation(mass, k):
    return sum(min(j, k) * v for j, v in enumerate(mass)) / k


def service(mass, k):
    return sum(min(F(1), F(k, 1+j)) * v for j, v in enumerate(mass))


def bisect_zero(increasing):
    lo, hi = 0., 1.
    for _ in range(50):
        mid = (lo+hi)/2
        if increasing(mid) < 0:
            lo = mid
        else:
            hi = mid
    return (lo+hi)/2


def calibrate(m, k, q):
    return bisect_zero(lambda p: sum(binomial(m, p)[k:]) - q)


def constants(n, k, ell):
    if n <= max(k, ell):
        raise ValueError("This table displays the interior n > max(k,ell).")
    def u(p):
        return utilisation(binomial(n-1, p), k)
    def a(p):
        return (ell/k) * service(binomial(n-1, p), k)
    p = bisect_zero(lambda x: u(x) - a(x))
    def whole_u(q):
        return utilisation(binomial(n, calibrate(n, k, q)), k)
    def deleted_a(q):
        return a(calibrate(n-1, k, q))
    q = bisect_zero(lambda q: whole_u(q)-deleted_a(q))
    iid = utilisation(binomial(n, ell/n), k)
    limit = 1 - fsum((k-j)*exp(-ell)*ell**j/factorial(j) for j in range(k))/k
    return whole_u(q), u(p), iid, limit, p


def check_crossings():
    """Certify the inequalities using rational brackets for the binomial parameter."""
    count = 0
    for m in range(2, 6):
        grid = [F(0), F(1, 5), F(1, 2), F(4, 5), F(1)]
        for probs in combinations_with_replacement(grid, m):
            if len(set(probs)) == 1:
                continue
            mass = poisson_binomial(probs)
            cdf = list(accumulate(mass))
            for k in range(1, m+1):
                q = sum(mass[k:])
                if q in (0, 1):
                    continue
                lo, hi = F(0), F(1)
                for _ in range(30):
                    mid = (lo+hi)/2
                    tail = sum(binomial(m, mid)[k:])
                    if q == tail:
                        lo = hi = mid
                        break
                    if tail < q:
                        lo = mid
                    else:
                        hi = mid
                lower = list(accumulate(binomial(m, hi)))
                upper = list(accumulate(binomial(m, lo)))
                ensure(all(cdf[j] <= lower[j] for j in range(k-1)))
                ensure(all(cdf[j] >= upper[j] for j in range(k, m)))
                count += 1
    return count


def check_welfare():
    """Compute policy and prophet directly over value outcomes, tie coins and orders."""
    laws = [
        [(F(0), F(1,3)), (F(1), F(2,3))],
        [(F(1), F(1,5)), (F(4), F(4,5))],
        [(F(0), F(2,5)), (F(1), F(3,5))],
        [(F(0), F(1,2)), (F(7), F(1,2))],
    ]
    t, rho = F(1), F(3,7)
    enriched = []
    for law in laws:
        entries = []
        for value, mass in law:
            chance = F(value > t) if value != t else rho
            for qualifies, probability in [(True, chance), (False, 1-chance)]:
                if probability:
                    entries.append((value, mass*probability, qualifies))
        enriched.append(entries)
    probs = [sum(m for _, m, z in items if z) for items in enriched]
    excesses = [sum(m * max(0, v-t) for v, m, _ in items) for items in enriched]
    orders = list(permutations(range(len(laws))))
    count = 0
    for k in [1, 2, 3]:
        reward = F(0)
        prophets = [F(0) for _ in laws]
        for sample in product(*enriched):
            weight = F(1)
            for _, probability, _ in sample:
                weight *= probability
            values = sorted((s[0] for s in sample), reverse=True)
            for ell in range(1, 5):
                prophets[ell-1] += weight * sum(values[:ell])
            for order in orders:
                qualifiers = [sample[i][0] for i in order if sample[i][2]]
                reward += weight * sum(qualifiers[:k])/len(orders)
        u = utilisation(poisson_binomial(probs), k)
        a = [service(poisson_binomial(probs[:i] + probs[i+1:]), k)
             for i in range(len(probs))]
        ensure(reward == k*t*u + sum(s*ex for s,ex in zip(a, excesses)))
        for ell, prophet in enumerate(prophets, 1):
            ensure((reward/k)/(prophet/ell) >= min(u, F(ell,k)*min(a)))
            count += 1
    return count


def check_upper_support():
    """Test the supporting slope for the finite heterogeneous extremal instance."""
    count = 0
    for n in range(2, 14):
        m = n-1
        for k in range(1, n):
            for ell in range(1, n):
                def u(x):
                    return utilisation(binomial(m, x), k)
                def a(x):
                    return service(binomial(m, x), k)
                p = bisect_zero(lambda x: u(x) - ell*a(x)/k)
                marginal = binomial(m-1, p)
                up = m/k * sum(marginal[:k])
                down = m * sum(v*k/((j+1)*(j+2))
                               for j, v in enumerate(marginal) if j >= k-1)
                weight = up/down
                optimum = u(p) + weight*a(p)
                for j in range(21):
                    x = j/20
                    ensure(u(x)+weight*a(x) <= optimum + 1.e-9 * max(1, optimum))
                count += 1
    return count


if __name__ == "__main__":
    print("Rational crossing checks:", check_crossings())
    print("Exact direct-welfare comparisons:", check_welfare())
    print("Numerical supporting-slope profiles:", check_upper_support())
    print("  n  k ell   fixed q   all static   iid       Poisson     p*")
    for n,k,ell in [(2,1,1),(3,1,1),(3,2,2),(6,2,1),(6,2,2),(6,2,4),
                    (10,1,1),(10,2,2),(10,3,3),(20,2,2),(50,2,2)]:
        print(f"{n:3d} {k:2d} {ell:3d}  " +
              "  ".join(f"{x:.8f}" for x in constants(n,k,ell)))
