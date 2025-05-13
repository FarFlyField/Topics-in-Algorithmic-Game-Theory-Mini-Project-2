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
                # Hospital prefers the new proposer?
                if hospital_rank[h][d] < hospital_rank[h][d_current]:
                    free.append(d_current)
                    current_match[h] = d
                else:
                    free.append(d)
        return proposals

def run_average_proposals(n_values, runs_per_n):
    da = DeferredAcceptance()
    avg_props = []
    for n in n_values:
        total = 0
        for _ in range(runs_per_n):
            docs = {i: random.sample(range(n), n) for i in range(n)}
            hosps = {i: random.sample(range(n), n) for i in range(n)}
            total += da.match(docs, hosps)
        avg_props.append(total / runs_per_n)
    return avg_props

def run_distribution(fixed_n, runs):
    da = DeferredAcceptance()
    dist = []
    for _ in range(runs):
        docs = {i: random.sample(range(fixed_n), fixed_n) for i in range(fixed_n)}
        hosps = {i: random.sample(range(fixed_n), fixed_n) for i in range(fixed_n)}
        dist.append(da.match(docs, hosps))
    return dist

if __name__ == "__main__":
    # 1. Average proposals vs n
    n_vals = [100, 200, 400, 800, 1600]
    runs_per_n = 5
    avg_props = run_average_proposals(n_vals, runs_per_n)

    plt.figure()
    plt.plot(n_vals, avg_props, marker='o')
    plt.xlabel("n (doctors = hospitals)")
    plt.ylabel("Average total proposals")
    plt.title("Average Proposals vs n (Uniform Random Preferences)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # 2. Distribution for a fixed n
    fixed_n = 100
    runs_dist = 100
    dist = run_distribution(fixed_n, runs_dist)

    plt.figure()
    plt.hist(dist, bins=20)
    plt.xlabel("Total proposals")
    plt.ylabel("Frequency")
    plt.title(f"Proposal Count Distribution (n={fixed_n}, {runs_dist} runs)")
    plt.tight_layout()
    plt.show()
