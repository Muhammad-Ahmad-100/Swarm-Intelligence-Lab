import random

random.seed(71)  # your roll number


def f(x):
    return (x - 7) ** 2 + 4  # the function we're minimizing


positions = [random.uniform(0, 14) for _ in range(5)]
velocities = [0 for _ in range(5)]  # every particle starts still

pbest_pos = positions[:]  # each particle's own best so far

gbest_pos = min(pbest_pos, key=f)  # the swarm's best position

w, c1, c2 = 0.6, 1.5, 1.5  # inertia, personal pull, swarm pull

iterations = 40

for it in range(iterations):

    for i in range(5):

        r1, r2 = random.random(), random.random()

        # Update velocity
        velocities[i] = (
            w * velocities[i]  #  Keeps part of the previous velocity
            + c1 * r1 * (pbest_pos[i] - positions[i])    # Pull toward personal best
            + c2 * r2 * (gbest_pos - positions[i])   # Pull toward global best
        )

        # Update position
        positions[i] = positions[i] + velocities[i]

        # Update personal best
        if f(positions[i]) < f(pbest_pos[i]):
            pbest_pos[i] = positions[i]

    # Update global best
    gbest_pos = min(pbest_pos, key=f)


print("Swarm converged near x =", gbest_pos)