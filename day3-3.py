# Quantum School: Day 3 - Lab 3
# Original notebook - https://colab.research.google.com/drive/1uxolWjkyuJ_DTz3xIedd0bVXUoNXA0FK

# %%
import matplotlib.pyplot as plt
import numpy as np
from iqm.pulla.pulla import Pulla
from iqm.pulse.builder import CircuitOperation as Op
from iqm.pulse.circuit_operations import Circuit

from env import iqm_api_token

# %%
# Connect to pulla

p = Pulla(
    "https://cocos.resonance.meetiqm.com/garnet",
    get_token_callback=lambda: iqm_api_token,
)

compiler = p.get_standard_compiler()


# %%
# Measuring a qubit in different states

qubit = "QB1"
circuits = []
for name, angle in zip(["state0", "state1", "superposition"], [0.0, np.pi, np.pi / 2]):
    circuit = Circuit(
        name,
        [
            Op("prx", (qubit,), args={"angle": angle, "phase": 0.0}),
            Op("measure", (qubit,), args={"key": "M"}),
        ],
    )
    circuits.append(circuit)

compiler.print_implementations_trees(compiler.builder.op_table["measure"])

compiler.amend_calibration_for_gate_implementation(
    "measure_fidelity", "constant", (qubit,), {"acquisition_type": "complex"}
)

playlist, context = compiler.compile(circuits)
settings, context = compiler.build_settings(context, shots=1000)
job = p.execute(playlist, context, settings, verbose=False)

# %%
# Analyze the results

state_0_results = np.array(job.result[0]["M"]).squeeze()
state_1_results = np.array(job.result[1]["M"]).squeeze()
state_2_results = np.array(job.result[2]["M"]).squeeze()
plt.figure()
plt.scatter(np.real(state_0_results), np.imag(state_0_results), label="|0>", s=4)
plt.scatter(np.real(state_1_results), np.imag(state_1_results), label="|1>", s=4)
plt.scatter(
    np.real(state_2_results), np.imag(state_2_results), label="Superposition", s=4
)
plt.xlabel("Re")
plt.ylabel("Im")
plt.gca().set_aspect("equal")
plt.grid()
plt.legend()
