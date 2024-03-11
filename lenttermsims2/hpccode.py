import numpy as np
import networkx as nx

class Counter(dict):
    largest_non_zero = 0
    def increment(self, item, delta = 1):
        new_val = delta + self.pop(item, 0)
        if new_val > 0:
            self[item] = new_val
            if (item != 0) and (new_val > self.largest_non_zero):
                self.largest_non_zero = new_val

def y(x):
    return 2**x

def find_tranformation_matrix(b, E, N, Tmax):

    M = np.shape(E)[0]
    n = np.random.poisson(lam = Tmax*(N+b*M))
    times = np.sort(np.random.uniform(0, Tmax, n))
    R = np.zeros(n, dtype = int)
    X = [2**i for i in range(N)][::-1]
    pmixed= False

    counts = Counter()
    for element in X:
        counts.increment(element, 1)

    for t in range(n):
        
        if np.random.random() < N/(N + b*M):

            i = np.random.randint(N)

            if X[i] != 0:
                
                counts.increment(X[i], -1)

                X[i] = 0

                counts.increment(0, 1)
        else:

            i,j = E[np.random.randint(M)]

            if X[i] != X[j]:
                    
                new = X[i] | X[j]
                counts.increment(X[i], -1)
                counts.increment(X[j], -1)
                counts.increment(new, 2)
                X[i] = X[j] = new
                
        R[t] = non_zero_distinct_rows = len(counts) - (0 in counts)

        if (not pmixed) and (non_zero_distinct_rows == 1):
            pmixing = times[t]
            pmixed = True

        if pmixed:
            if (non_zero_distinct_rows == 0) or (times[t] > 4 * pmixing):
                times = times[:t]
                R = R[:t]
                break

    return times, R, counts.largest_non_zero, pmixing


N = 2000
d = 3
G = nx.random_regular_graph(d, N)
E = list(G.edges)
Tmax = 1e3
num_trials = 100

b = np.linspace(0.002, 5, 30)
s1starvar = []
s1starav = []
pmixinglist = []
for i in range(len(b)):
    s1 = []
    pm = []
    for j in range(num_trials):
        times, R, spatial, pmixing = find_tranformation_matrix(b[i], E, N, Tmax)
        s1.append(spatial)
        pm.append(pmixing)
    s1starav.append(np.mean(s1))
    s1starvar.append(np.var(s1))
    pmixinglist.append(np.mean(pm))
print(s1starav)
print(s1starvar)
print(pmixinglist)
