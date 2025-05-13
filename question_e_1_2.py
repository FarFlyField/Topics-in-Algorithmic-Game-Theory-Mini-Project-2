import random
import matplotlib.pyplot as plt
from collections import deque

class DeferredAcceptance:
    def match(self, doctors_prefs, hospitals_prefs):
        # Precompute hospital rankings of doctors
        hospital_rank = {
            h: {doc: idx for idx, doc in enumerate(pref_list)}
            for h, pref_list in hospitals_prefs.items()
        }
        next_proposal = {d: 0 for d in doctors_prefs}
        free = deque(doctors_prefs.keys())
        current_match = {}
        proposals = 0

        while free:
            d = free.popleft()
            if next_proposal[d] >= len(doctors_prefs[d]):
                continue
            h = doctors_prefs[d][next_proposal[d]]
            next_proposal[d] += 1
            proposals += 1

            if h not in current_match:
                current_match[h] = d
            else:
                d_current = current_match[h]
                if hospital_rank[h][d] < hospital_rank[h][d_current]:
                    free.append(d_current)
                    current_match[h] = d
                else:
                    free.append(d)
        return proposals

def gen_weighted_prefs(n, weights):
    """
    Generate preference lists by sampling without replacement,
    probability ∝ weights.
    """
    prefs = {}
    for agent in range(n):
        remaining = list(range(n))
        w = weights.copy()
        order = []
        for _ in range(n):
            choice = random.choices(remaining, weights=w, k=1)[0]
            idx = remaining.index(choice)
            order.append(choice)
            remaining.pop(idx)
            w.pop(idx)
        prefs[agent] = order
    return prefs

def run_average_proposals_popularity(n_values, runs_per_n, popularity_fn):
    da = DeferredAcceptance()
    avg_props = []
    for n in n_values:
        base_weights = popularity_fn(n)
        total = 0
        for _ in range(runs_per_n):
            weights_h = random.sample(base_weights, k=n)
            weights_d = random.sample(base_weights, k=n)
            docs = gen_weighted_prefs(n, weights_h)
            hosps = gen_weighted_prefs(n, weights_d)
            total += da.match(docs, hosps)
        avg_props.append(total / runs_per_n)
    return avg_props

def run_distribution_popularity(fixed_n, runs, popularity_fn):
    da = DeferredAcceptance()
    dist = []
    base_weights = popularity_fn(fixed_n)
    for _ in range(runs):
        weights_h = random.sample(base_weights, k=fixed_n)
        weights_d = random.sample(base_weights, k=fixed_n)
        docs = gen_weighted_prefs(fixed_n, weights_h)
        hosps = gen_weighted_prefs(fixed_n, weights_d)
        dist.append(da.match(docs, hosps))
    return dist

if __name__ == "__main__":
    print("In main")
    # Natural number weights: 1, 2, 3, ..., n
    pop_fn_nat = lambda n: list(range(1, n+1))
    # Uniform weights for comparison
    pop_fn_unif = lambda n: [1] * n

    n_vals = [100, 200, 400]
    runs = 5

    # 1. Average proposals vs n for natural numbers

    print("avg_nat")
    avg_nat = run_average_proposals_popularity(n_vals, runs, pop_fn_nat)
    #  Uniform for baseline
    print("avg_uni")
    avg_uni = run_average_proposals_popularity(n_vals, runs, pop_fn_unif)

    print("Plotting")
    plt.figure()
    plt.plot(n_vals, avg_nat, marker='o', label="Natural weights 1..n")
    plt.plot(n_vals, avg_uni, marker='x', label="Uniform weights")
    plt.xlabel("n (doctors = hospitals)")
    plt.ylabel("Average total proposals")
    plt.title("Popularity Model: Avg Proposals vs n")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # 2. Distribution at fixed n for natural numbers

    fixed_n = 100
    runs_dist = 100
    print("dist_nat")
    dist_nat = run_distribution_popularity(fixed_n, runs_dist, pop_fn_nat)
    print("dist_uni")
    dist_uni = run_distribution_popularity(fixed_n, runs_dist, pop_fn_unif)

    print("Plotting distribution")
    plt.figure()
    plt.hist(dist_nat, bins=20, alpha=0.7, label="Natural weights")
    plt.hist(dist_uni, bins=20, alpha=0.7, label="Uniform weights")
    plt.xlabel("Total proposals")
    plt.ylabel("Frequency")
    plt.title(f"Proposal Distribution at n={fixed_n}")
    plt.legend()
    plt.tight_layout()
    plt.show()
