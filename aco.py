import random
random.seed(71)

paths = {'Path A': 10, 'Path B': 15, 'Path C': 8, 'Path D':12}
pheromone = {p: 1.0 for p in paths}
evaporation_rate = 0.5
Q = 100
iterations = 50
ants_per_iteration = 5
for it in range(iterations):
  for ant in range(ants_per_iteration):
    total = sum(pheromone[p] / paths[p] for p in paths)

    weights = {p: (pheromone[p] / paths[p]) / total for p in paths}

    chosen = random.choices(list(paths.keys()), weights=list(weights.values()) )[0]  # randomly chooses a path according to those probabilities.

    pheromone[chosen] += Q / paths[chosen] #selected path gets extra pheromone
  for p in pheromone:
    pheromone[p] =  pheromone[p] * (1 - evaporation_rate) # pheromone becomes half

best =  max(pheromone, key=pheromone.get) # path having the highest pheromone
print("Colony converged on:", best)