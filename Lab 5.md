import random
import matplotlib.pyplot as plt

# Use your roll number as the random seed (e.g., 21)
random.seed(71)

def f(x):
    # The objective function to minimize (true minimum at x = 7)
    return (x - 7) ** 2 + 4

def fitness(x):
    # Fitness function: higher values mean closer to the minimum
    return 1 / (1 + f(x))

# Initialize 5 food sources randomly between 3 and 10
sources = [random.uniform(3, 10) for _ in range(5)]
trials = [0 for _ in range(5)]       # Trial counters for stagnation
limit = 2                            # Abandonment limit
iterations = 30                      # Total generations/iterations

# History logging for convergence visualization
history = [[] for _ in range(5)]
best_history = []

print("=== Initial Food Sources ===")
for idx, val in enumerate(sources):
    print(f"Source {idx+1}: x = {val:.4f} | f(x) = {f(val):.4f}")
print("=" * 45)

# --- Main Optimization Loop ---
for it in range(iterations):
    # Log trajectories for plotting
    for i in range(5):
        history[i].append(sources[i])
    
    current_best = min(sources, key=f)
    best_history.append(current_best)

    # 1. Employed Bee Phase (Exploitation)
    for i in range(5):        
        k = random.choice([j for j in range(5) if j != i])
        candidate = sources[i] + random.uniform(-1, 1) * (sources[i] - sources[k])        
        
        if fitness(candidate) > fitness(sources[i]):
            sources[i], trials[i] = candidate, 0      
        else:
            trials[i] = trials[i] + 1                     

    # 2. Scout Bee Phase (Exploration / Escape Hatch)
    for i in range(5):                          
        if trials[i] > limit:
            sources[i] = random.uniform(0, 14)    # Abandon stale source, explore fresh ground
            trials[i] = 0                         # Reset trial counter

    # Find the best source in the current iteration
    best_source = min(sources, key=f)
    print(f"Iteration {it+1:02d} | Best x: {best_source:.4f} | Best f(x): {f(best_source):.4f}")

print("=" * 45)
final_best = min(sources, key=f)
print(f"Optimization Complete!")
print(f"Best solution found: x = {final_best:.4f} with f(x) = {f(final_best):.4f}")







import random
import matplotlib.pyplot as plt

# -------------------------------------------------------------
# 1. SETUP & INITIALIZATION
# -------------------------------------------------------------

# Seed ensures deterministic runs and personalizes results to roll number 79
random.seed(79)

# Target objective function to minimize: minimum is at x = 7 where f(7) = 4
def f(x):
    return (x - 7) ** 2 + 4

# Fitness function: maps lower function values to higher fitness scores
def fitness(x):
    return 1 / (1 + f(x))

# Algorithm configuration parameters
num_sources = 5
limit = 8           # Abandonment limit: maximum failed attempts before discarding a source
iterations = 40     # Total search iterations

# Initialize 5 random food source positions across the domain [0, 14]
sources = [random.uniform(0, 14) for _ in range(num_sources)]

# Dedicated stagnation counter for each food source to track failure counts independently
trials = [0 for _ in range(num_sources)]

# History logging for convergence visualization
history = [[] for _ in range(num_sources)]
best_history = []

# -------------------------------------------------------------
# 2. OPTIMIZATION CYCLE
# -------------------------------------------------------------
for it in range(iterations):
    # Log trajectories for plotting
    for i in range(num_sources):
        history[i].append(sources[i])
    
    # Store the leading source at iteration 'it'
    current_best = max(sources, key=fitness)
    best_history.append(current_best)

    # --- Phase 1: Employed Bee Phase (Exploitation) ---
    for i in range(num_sources):
        # Pick another distinct food source k (k != i) to provide a search direction
        k = random.choice([j for j in range(num_sources) if j != i])
        
        # Perturbation step: search along the vector connecting sources i and k
        phi = random.uniform(-1, 1)
        candidate = sources[i] + phi * (sources[i] - sources[k])
        
        # Greedy selection: adopt new candidate position only if fitness improves
        if fitness(candidate) > fitness(sources[i]):
            sources[i], trials[i] = candidate, 0   # Accept position and reset counter
        else:
            trials[i] = trials[i] + 1              # Increment failure count

    # --- Phase 2: Scout Bee Phase (Exploration) ---
    for i in range(num_sources):
        # Trigger scout behavior if a food source exceeds the abandonment threshold
        if trials[i] > limit:
            # Discard stagnant position and sample a new uniform point across [0, 14]
            sources[i] = random.uniform(0, 14)
            trials[i] = 0                          # Reset stagnation count for new food source

# -------------------------------------------------------------
# 3. RESULTS & VISUALIZATION
# -------------------------------------------------------------
best_solution = max(sources, key=fitness)
print(f"Optimal x found: {best_solution:.4f}")
print(f"Objective value f(x): {f(best_solution):.4f}")

plt.figure(figsize=(12, 6))
colors = ['#c45d69', '#9d7685', '#dbba7a', '#7982a6', '#9c9c9c']

for i in range(num_sources):
    plt.plot(range(iterations), history[i], label=f'Food source {i+1}', color=colors[i], alpha=0.85, linewidth=1.8)

plt.plot(range(iterations), best_history, label='Best source x', color='black', linewidth=2.5)
plt.axhline(y=7, color='#c99738', linestyle='--', linewidth=2, label='true minimum, x = 7')

plt.title("Artificial Bee Colony Search Trajectory (Seed = 79)", fontsize=14)
plt.xlabel("Iteration", fontsize=12)
plt.ylabel("x position", fontsize=12)
plt.legend(frameon=False, loc='upper right')
plt.grid(True, linestyle=':', alpha=0.5)
plt.ylim(0, 15)
plt.show()









def run_abc(num_sources=5, limit=8, seed=79):
    random.seed(seed)
    sources = [random.uniform(0, 14) for _ in range(num_sources)]
    trials = [0 for _ in range(num_sources)]
    
    for it in range(40):
        for i in range(num_sources):
            k = random.choice([j for j in range(num_sources) if j != i])
            candidate = sources[i] + random.uniform(-1, 1) * (sources[i] - sources[k])
            if fitness(candidate) > fitness(sources[i]):
                sources[i], trials[i] = candidate, 0
            else:
                trials[i] += 1
        for i in range(num_sources):
            if trials[i] > limit:
                sources[i] = random.uniform(0, 14)
                trials[i] = 0
                
    best = max(sources, key=fitness)
    return best, f(best)

print("--- 1. Testing Abandonment Limit (num_sources=5, seed=79) ---")
for lim in [2, 8, 20]:
    sol, score = run_abc(num_sources=5, limit=lim, seed=79)
    print(f"Limit = {lim:2d} -> Best x: {sol:.4f}, f(x): {score:.4f}")

print("\n--- 2. Testing Number of Sources (limit=8, seed=79) ---")
for pop in [3, 5, 10]:
    sol, score = run_abc(num_sources=pop, limit=8, seed=79)
    print(f"Sources = {pop:2d} -> Best x: {sol:.4f}, f(x): {score:.4f}")
