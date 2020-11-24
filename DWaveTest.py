from dwave.cloud import Client
from dwave.system import DWaveSampler
import dwavebinarycsp
import dwavebinarycsp.factories.constraint.gates as gates

csp = dwavebinarycsp.ConstraintSatisfactionProblem(dwavebinarycsp.BINARY)
csp.add_constraint(gates.and_gate(['x1', 'x2', 'y1']))
bqm = dwavebinarycsp.stitch(csp)
print(bqm)

# client = Client.from_config(token='DEV-32a72b08f81fd9fc8584ab76331bf18aa7913765')
# print(client.get_solvers())
# sampler = DWaveSampler(solver={'qpu': True})
# print(sampler.parameters)