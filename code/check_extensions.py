#!/usr/bin/env python3
"""Check the order-mixture upper examples and the finite-size expansion. No dependencies."""
from math import exp, log1p, factorial, sqrt
from itertools import product


def ensure(condition):
    """Explicit check that survives python -O (no assert statements)."""
    if not condition:
        raise SystemExit("CHECK FAILED")


def root(f, lo=0., hi=1.):
    for _ in range(58):
        x = (lo+hi)/2
        if f(x) >= 0:
            hi = x
        else:
            lo = x
    return (lo+hi)/2


def low_masses(m, p, k):
    if p == 1:
        return [float(j == m) for j in range(k)]
    mass = exp(m*log1p(-p))
    out = []
    for j in range(k):
        out.append(mass)
        mass *= (m-j)*p/((j+1)*(1-p))
    return out


def U(m, p, k):
    return 1 - sum((k-j)*z/k for j,z in enumerate(low_masses(m,p,k)))


def Q(m, p, k):
    return 1-sum(low_masses(m,p,k))


def tagged(m, p, k, rho):
    uniform = k*U(m+1,p,k)/((m+1)*p) if p > 1e-11 else 1.
    return (1-rho)*uniform + rho*(1-Q(m,p,k))


def compare_order_mixtures():
    """Enumerate possible numbers of bulk qualifiers, separately from formula (2)."""
    from math import comb
    cases = 0
    for n,k,b,rho in product(range(3,9),range(1,5),(1,1.5,2.5),(0,.4,1)):
        if n <= max(k,b):
            continue
        m = n-1
        pstar = root(lambda p: U(m,p,k)-(b/k)*tagged(m,p,k,rho))
        mass = [comb(m-1,j)*pstar**j*(1-pstar)**(m-1-j) for j in range(m)]
        up = m/k*sum(mass[:k])
        loss = m*sum(x*((1-rho)*k/((j+1)*(j+2))*(j>=k-1)
                         +rho*(j==k-1)) for j,x in enumerate(mass))
        w = up/((b/k)*loss)
        C = U(m,pstar,k)
        eps = 1e-7
        high = 1+b*w/eps
        def ratio(p):
            numerator = 0
            for j in range(m+1):
                prob = comb(m,j)*p**j*(1-p)**(m-j)
                # Absent jackpot, the exceptional applicant is below threshold.
                # Present jackpot, uniform rank or last-place rank.
                got = (1-rho)*min(1,k/(j+1)) + rho*int(j<k)
                conditional = min(k,j) + eps*(int(j<k)+(high-1)*got)
                numerator += prob*conditional/k
            return numerator/(1+w)
        worst_example_best = max(ratio(p) for p in [j/80 for j in range(81)]+[pstar])
        ensure(C-1e-10 <= worst_example_best <= C+eps/k+1e-10)
        cases += 1
    return cases


def finite_gap(n,k,b):
    m=n-1
    p=root(lambda x: U(m,x,k)-(b/k)*tagged(m,x,k,0))
    C=U(m,p,k)
    def diff(p_del):
        q=Q(m,p_del,k)
        p_all=root(lambda y: Q(n,y,k)-q)
        return U(n,p_all,k)-(b/k)*tagged(m,p_del,k,0)
    x=root(diff)
    return C-(b/k)*tagged(m,x,k,0)


def check_expansion():
    for k,b in [(2,1),(2,2),(3,3),(4,1.5),(3,5)]:
        mass=[exp(-b)*b**j/factorial(j) for j in range(k+1)]
        c=1-sum((k-j)*mass[j] for j in range(k))/k
        coeff=b*sum((k-1-j)*mass[j] for j in range(k-1))/(2*k)*(1-sum(mass))/c
        scaled=[n*n*finite_gap(n,k,b) for n in (100,500,2000)]
        ensure(abs(scaled[-1]-coeff)<.012*coeff)
        ensure(abs(scaled[-1]-coeff) < abs(scaled[0]-coeff))
        print(f'k={k}, b={b:g}: n² gap at n=100/500/2000 =',
              *(f'{v:.8f}' for v in scaled), f'; limit = {coeff:.8f}')


if __name__=='__main__':
    print('Order-mixture extremal profiles verified:', compare_order_mixtures())
    check_expansion()
