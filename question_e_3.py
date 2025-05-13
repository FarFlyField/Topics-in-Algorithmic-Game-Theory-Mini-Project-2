import random
import matplotlib.pyplot as plt
from collections import deque

class DeferredAcceptance:
    def match(self, doctors_prefs, hospitals_prefs):
        hospital_rank = {
            h: {doc: idx for idx, doc in enumerate(pref_list)}
            for h, pref_list in hospitals_prefs.items()
        }
        next_proposal = {d: 0 for d in doctors_prefs}
        free = deque(doctors_prefs.keys())
        current_match = {}

        while free:
            d = free.popleft()
            if next_proposal[d] >= len(doctors_prefs[d]):
                continue
            h = doctors_prefs[d][next_proposal[d]]
            next_proposal[d] += 1
            if h not in current_match:
                current_match[h] = d
            else:
                d_current = current_match[h]
                if hospital_rank[h][d] < hospital_rank[h][d_current]:
                    free.append(d_current)
                    current_match[h] = d
                else:
                    free.append(d)
        return {d: h for h, d in current_match.items()}

def gen_weighted_prefs(n, weights):
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

def average_ranks(n_values, runs, popularity_fn=None):
    da = DeferredAcceptance()
    avg_doc = []
    avg_hosp = []
    for n in n_values:
        total_doc = 0
        total_hosp = 0
        for _ in range(runs):
            if popularity_fn is None:
                docs = {i: random.sample(range(n), n) for i in range(n)}
                hosps = {i: random.sample(range(n), n) for i in range(n)}
            else:
                base = popularity_fn(n)
                weights_h = random.sample(base, k=n)
                weights_d = random.sample(base, k=n)
                docs = gen_weighted_prefs(n, weights_h)
                hosps = gen_weighted_prefs(n, weights_d)
            matching = da.match(docs, hosps)
            hosp_inv = {
                h: {doc: idx for idx, doc in enumerate(prefs)}
                for h, prefs in hosps.items()
            }
            for d, h in matching.items():
                total_doc += docs[d].index(h) + 1
                total_hosp += hosp_inv[h][d] + 1
        avg_doc.append(total_doc / (n * runs))
        avg_hosp.append(total_hosp / (n * runs))
    return avg_doc, avg_hosp

# Parameters
n_values = [100, 200, 400]
runs = 5
pop_fn_nat = lambda n: list(range(1, n+1))

# Compute averages
doc_uni, hosp_uni = average_ranks(n_values, runs)
doc_nat, hosp_nat = average_ranks(n_values, runs, pop_fn_nat)

# Plot doctor average rank comparison
plt.figure()
plt.plot(n_values, doc_uni, marker='o', label='Uniform random')
plt.plot(n_values, doc_nat, marker='s', label='Natural weights')
plt.xlabel("n (doctors = hospitals)")
plt.ylabel("Average doctor's partner rank")
plt.title("Doctor's Avg. Rank vs n")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Plot hospital average rank comparison
plt.figure()
plt.plot(n_values, hosp_uni, marker='o', label='Uniform random')
plt.plot(n_values, hosp_nat, marker='s', label='Natural weights')
plt.xlabel("n (doctors = hospitals)")
plt.ylabel("Average hospital's partner rank")
plt.title("Hospital's Avg. Rank vs n")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
