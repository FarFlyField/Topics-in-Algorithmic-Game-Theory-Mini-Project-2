from collections import deque

class DeferredAcceptance:
    def match(self, doctors_prefs, hospitals_prefs):
        # Precompute hospital rankings of doctors
        hospital_rank = {
            h: {doc: idx for idx, doc in enumerate(pref_list)}
            for h, pref_list in hospitals_prefs.items()
        }
        # Next index to propose for each doctor
        next_proposal = {d: 0 for d in doctors_prefs}
        # Free doctors queue (doctors who haven't been matched yet)
        free = deque(doctors_prefs.keys())
        current_match = {}
        proposals = 0

        while free:
            d = free.popleft()
            prefs = doctors_prefs[d]
            if next_proposal[d] >= len(prefs):
                continue
            h = prefs[next_proposal[d]]
            next_proposal[d] += 1
            proposals += 1
            # If hospital is free, match them
            if h not in current_match:
                current_match[h] = d
            else:
                # Hospital is already matched, check if it prefers the new doctor
                d_current = current_match[h]
                if hospital_rank[h][d] < hospital_rank[h][d_current]:
                    free.append(d_current)
                    current_match[h] = d
                else:
                    free.append(d)
                    
        # Build doctor->hospital mapping
        matching = {d: h for h, d in current_match.items()}
        return matching, proposals

if __name__ == "__main__":
    doctors_prefs = {
        'd1': ['h1', 'h2', 'h3'],
        'd2': ['h1', 'h3', 'h2'],
        'd3': ['h2', 'h3', 'h1'],
    }
    hospitals_prefs = {
        'h1': ['d2', 'd1', 'd3'],
        'h2': ['d1', 'd3', 'd2'],
        'h3': ['d1', 'd2', 'd3'],
    }
    da = DeferredAcceptance()
    matching, proposals = da.match(doctors_prefs, hospitals_prefs)
    print("Matching:", matching)
    print("Proposals:", proposals)
