import dwavebinarycsp
from dwavebinarycsp.factories.csp.circuits import multiplication_circuit
import neal

csp = multiplication_circuit(10)
bqm = dwavebinarycsp.stitch(csp)
bqm.fix_variable('a0', 0);
bqm.fix_variable('a1', 0);
bqm.fix_variable('a2', 1);
bqm.fix_variable('a3', 1);
bqm.fix_variable('a4', 1);
bqm.fix_variable('a5', 1);
bqm.fix_variable('a6', 1);
bqm.fix_variable('a7', 1);
bqm.fix_variable('a8', 1);
bqm.fix_variable('a9', 1);

bqm.fix_variable('b0', 1);
bqm.fix_variable('b1', 1);
bqm.fix_variable('b2', 1);
bqm.fix_variable('b3', 1);
bqm.fix_variable('b4', 1);
bqm.fix_variable('b5', 1);
bqm.fix_variable('b6', 1);
bqm.fix_variable('b7', 1);
bqm.fix_variable('b8', 1);
bqm.fix_variable('b9', 1);

sampler = neal.SimulatedAnnealingSampler()
response = sampler.sample(bqm)
p = next(response.samples(n=1, sorted_by='energy'))
print(p['p10'], p['p9'], p['p8'], p['p7'], p['p6'], p['p5'], p['p4'], p['p3'], p['p2'], p['p1'],
      p['p0'])  # doctest: +SKIP
