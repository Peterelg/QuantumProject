import networkx as nx
from dimod.reference.samplers import ExactSolver
import dwave_networkx as dnx
from dwave.system import DWaveSampler, EmbeddingComposite

#creating the graph
s5 = nx.circular_ladder_graph(10)

#normal CPU
sampler = ExactSolver()
print(dnx.min_vertex_cover(s5, sampler))
#QPU
sampler = EmbeddingComposite(DWaveSampler())
print(dnx.min_vertex_cover(s5, sampler))