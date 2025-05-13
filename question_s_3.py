import random
import matplotlib.pyplot as plt
from collections import deque

# Doctor-proposing Deferred Acceptance
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

da = DeferredAcceptance()

# n values and runs
n_values = [100, 200, 400, 800, 1600]
runs_per_n = 5

avg_doc_ranks = []
avg_hosp_ranks = []

for n in n_values:
    total_doc_rank = 0
    total_hosp_rank = 0
    for _ in range(runs_per_n):
        # generate uniform random preferences
        doctors_prefs = {i: random.sample(range(n), n) for i in range(n)}
        hospitals_prefs = {i: random.sample(range(n), n) for i in range(n)}
        matching = da.match(doctors_prefs, hospitals_prefs)

        # build inverse ranking for hospitals
        hosp_inverse = {
            h: {doc: idx for idx, doc in enumerate(prefs)}
            for h, prefs in hospitals_prefs.items()
        }

        # sum ranks over all matched pairs
        for d, h in matching.items():
            total_doc_rank += doctors_prefs[d].index(h) + 1
            total_hosp_rank += hosp_inverse[h][d] + 1

    avg_doc_ranks.append(total_doc_rank / (n * runs_per_n))
    avg_hosp_ranks.append(total_hosp_rank / (n * runs_per_n))

# Plot average doctor rank vs n
plt.figure()
plt.plot(n_values, avg_doc_ranks, marker='o')
plt.xlabel("n")
plt.ylabel("Average doctor's partner rank")
plt.title("Average Doctor Rank vs n")
plt.grid(True)
plt.tight_layout()
plt.show()

# Plot average hospital rank vs n
plt.figure()
plt.plot(n_values, avg_hosp_ranks, marker='o')
plt.xlabel("n")
plt.ylabel("Average hospital's partner rank")
plt.title("Average Hospital Rank vs n")
plt.grid(True)
plt.tight_layout()
plt.show()
