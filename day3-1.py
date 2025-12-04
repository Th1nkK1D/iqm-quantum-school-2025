# Quantum School: Day 3 - Lab 1
# Original notebook - https://colab.research.google.com/drive/1nkyXz9EQD-BIYU-E3M0W5Xe0MgvRDiqv

# %%
import os

from iqm.qiskit_iqm.iqm_provider import IQMProvider
from qiskit import QuantumCircuit, transpile
from qiskit.visualization import plot_histogram
from rustworkx import spring_layout
from rustworkx.visualization import mpl_draw

from env import iqm_api_token

# %%
# Connecting to the QPU and visualizing qubits
os.environ["IQM_TOKEN"] = iqm_api_token
provider = IQMProvider("https://cocos.resonance.meetiqm.com/garnet")
backend = provider.get_backend()

mpl_draw(
    backend.coupling_map.graph,
    arrows=True,
    with_labels=True,
    node_color="#32a8a4",
    pos=spring_layout(backend.coupling_map.graph, num_iter=200),
)

# %%
# Creating a GHZ (Greenberger-Horne-Zeilinger) state
# Either |000> or |111>

num_qb = 3
qc = QuantumCircuit(num_qb)
qc.h(0)

for qb in range(1, num_qb):
    qc.cx(0, qb)

qc.measure_all()
qc.draw("mpl", style="clifford")

# %%
# Run on resonance

qc_transpiled = transpile(qc, backend=backend)
job = backend.run(qc_transpiled, shots=10000)

res = job.result()
counts = res.get_counts()

plot_histogram(counts)
