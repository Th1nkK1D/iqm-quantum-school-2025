# Quantum School: Day 2 - Lab
# Original notebook - https://colab.research.google.com/drive/1Hvdn-af2Sb3nfV_dq3bs8N95aZYqFntY

# %%
from dimod import Binary, ConstrainedQuadraticModel, quicksum
from iqm.applications.qubo import ConstrainedQuadraticInstance
from iqm.qaoa.backends import SamplerResonance, SamplerSimulation
from iqm.qaoa.qubo_qaoa import QUBOQAOA
from qrisp import QuantumVariable, cx, h, x
from qrisp.interface import IQMBackend
from toolz import pipe

from env import iqm_api_token

# %%
# Part 1: Bernstein-Vazirani algorithm

# %%
# Set up circuit

length_of_secret_code = 4
inputs = QuantumVariable(length_of_secret_code)
ans = QuantumVariable(1)

h(inputs)
pipe(ans, x, h)


def oracle(qubits, secret_code):
    for i in range(length_of_secret_code):
        if secret_code[i] == "1":
            cx(qubits[i], ans)


qubits = oracle(inputs, "1101")

h(inputs)

print(inputs.qs)

# %%
# Run measurement

print(inputs.get_measurement())

iqm_garnet = IQMBackend(api_token=iqm_api_token, device_instance="garnet")
inputs.get_measurement(backend=iqm_garnet)

# %%
# Part 2: Variational Quantum Algorithms: QAOA and MaxCut

# %%
# Formulate adjacent matrix, cost function, and problem

num_students = 6

J = [
    [0, 1, 1, 0, 0, 0],
    [0, 0, 1, 0, 0, 0],
    [0, 0, 0, 1, 1, 0],
    [0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0],
]

x = {i: Binary(i) for i in range(num_students)}

cost = quicksum(
    J[i][j] * (1 - 2 * x[i]) * (1 - 2 * x[j])
    for i in range(num_students)
    for j in range(num_students)
)

MaxCut_QUBO = ConstrainedQuadraticModel()
MaxCut_QUBO.set_objective(cost)

MaxCut_instance = ConstrainedQuadraticInstance(MaxCut_QUBO)

# %%
# Use simulation

sampler = SamplerSimulation()
# %%
# Use Resonance

sampler = SamplerResonance(
    token=iqm_api_token,
    server_url="https://cocos.resonance.meetiqm.com/garnet",
    transpiler="Default",
)

# %%
# Train and get samples

MaxCut_qaoa = QUBOQAOA(
    problem=MaxCut_instance, num_layers=2, initial_angles=[0.5, 0.5, 0.5, 0.5]
)
MaxCut_qaoa.train()

samples = MaxCut_qaoa.sample(sampler=sampler, shots=20_000)
print(samples)

most_probable = max(samples, key=lambda y: samples[y])
most_probable_cost = MaxCut_instance.quality(most_probable)

print("Cost of most probable outcome: ", most_probable_cost)
print("Most probable outcome :", most_probable)
