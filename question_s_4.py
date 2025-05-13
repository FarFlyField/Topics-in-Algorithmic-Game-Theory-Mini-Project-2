import random
import matplotlib.pyplot as plt
from collections import deque

# Doctor-proposing Deferred Acceptance implementation
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

def compute_percentile_distributions(n, runs):
    da = DeferredAcceptance()
    doc_percentiles = []
    hosp_percentiles = []

    for _ in range(runs):
        # Uniform random preferences
        doctors_prefs = {i: random.sample(range(n), n) for i in range(n)}
        hospitals_prefs = {i: random.sample(range(n), n) for i in range(n)}
        matching = da.match(doctors_prefs, hospitals_prefs)

        # Build inverse ranking for hospitals
        hosp_inv = {
            h: {doc: idx for idx, doc in enumerate(prefs)}
            for h, prefs in hospitals_prefs.items()
        }

        for d, h in matching.items():
            doc_rank = doctors_prefs[d].index(h)
            hosp_rank = hosp_inv[h][d]
            # Convert to percentile (0 to 100)
            doc_percentiles.append(doc_rank / (n - 1) * 100)
            hosp_percentiles.append(hosp_rank / (n - 1) * 100)

    return doc_percentiles, hosp_percentiles

# Parameters
n = 100
runs = 100

# Compute distributions
doc_pct, hosp_pct = compute_percentile_distributions(n, runs)

# Plot doctor match percentiles
plt.figure()
plt.hist(doc_pct, bins=20)
plt.xlabel("Doctor match percentile")
plt.ylabel("Frequency")
plt.title(f"Doctor Match Percentile Distribution (n={n}, {runs} runs)")
plt.tight_layout()
plt.show()

# Plot hospital match percentiles
plt.figure()
plt.hist(hosp_pct, bins=20)
plt.xlabel("Hospital match percentile")
plt.ylabel("Frequency")
plt.title(f"Hospital Match Percentile Distribution (n={n}, {runs} runs)")
plt.tight_layout()
plt.show()
