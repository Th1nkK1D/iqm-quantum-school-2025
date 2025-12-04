# Quantum School: Day 3 - Lab 2
# Original notebook - https://colab.research.google.com/drive/1Q3FSXw488hl8FAf_SFmgwsT6WSAfW6OJ

# %%
from IPython.core.display import HTML
from iqm.iqm_client import Circuit
from iqm.pulla.pulla import Pulla
from iqm.pulse.playlist.visualisation.base import inspect_playlist
from iqm.qiskit_iqm.iqm_provider import IQMProvider
from iqm.qiskit_iqm.qiskit_to_iqm import serialize_instructions
from qrisp import QuantumCircuit

from env import iqm_api_token

# %%
# Connect to pulla

p = Pulla(
    "https://cocos.resonance.meetiqm.com/garnet",
    get_token_callback=lambda: iqm_api_token,
)

compiler = p.get_standard_compiler()

# %%
# Create GHZ state circuit

qc_0 = QuantumCircuit(3)

qc_0.h(0)
qc_0.cx(0, 1)
qc_0.cx(0, 2)
qc_0.measure([0, 1, 2])

print(qc_0)

# %%
# Transpile to selected hardware backend

provider = IQMProvider(
    "https://cocos.resonance.meetiqm.com/garnet", token=iqm_api_token
)
transpiled_qc = qc_0.transpile(backend=provider.get_backend())

print(transpiled_qc)

qiskit_circuit = transpiled_qc.to_qiskit()

# %%
# Compile into pulses

iqm_instructions = serialize_instructions(
    qiskit_circuit, {i: "QB" + str(i + 1) for i in range(qiskit_circuit.num_qubits)}
)
iqm_circuit = Circuit(name="my_circuit", instructions=iqm_instructions)

playlist, context = compiler.compile([iqm_circuit])

HTML(inspect_playlist(playlist))
