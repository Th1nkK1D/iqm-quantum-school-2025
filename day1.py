# Quantum School: Day 1 - Lab

# %%
from qrisp import QuantumVariable, cx, h, x
from qrisp.interface import IQMBackend
from toolz import pipe

from env import iqm_api_token

# %%
# Task 2.1: Run the code below that creates qubit states |0⟩, |1⟩, |+⟩ and |−⟩ using qrisp.
# Describe what results you get when measuring each state.

zero = QuantumVariable(1)
one = QuantumVariable(1)
plus = QuantumVariable(1)
minus = QuantumVariable(1)

pipe(one, x)
pipe(plus, h)
pipe(minus, h, x)

print(zero.qs)
print(zero.get_measurement())

print(one.qs)
print(one.get_measurement())

print(plus.qs)
print(plus.get_measurement())

print(minus.qs)
print(minus.get_measurement())

# %%
# Task 3.1: Modify the code below to evaluate some of the QuantumVariables you created in Task 2.1
# on IQM's quantum hardware (zero, one, plus, minus).

iqm_sirius = IQMBackend(api_token=iqm_api_token, device_instance="sirius")
minus.get_measurement(backend=iqm_sirius)

# %%
# Task 4.2: Modify the code above to create a GHZ state with 3 qubits instead of a Bell state with 2 qubits.

ghz = QuantumVariable(3)
h(ghz[0])
cx(ghz[0], ghz[1])
cx(ghz[1], ghz[2])

print(ghz.qs)
ghz.get_measurement()
# %%
# Simulate the modified circuit on the qrisp simulator.

iqm_garnet = IQMBackend(api_token=iqm_api_token, device_instance="garnet")
ghz.get_measurement(backend=iqm_garnet)
