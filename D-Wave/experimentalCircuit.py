import operator
from collections import defaultdict
from collections import OrderedDict
import dimod
import dwavebinarycsp as dbc
import neal
from dwavebinarycsp.core.csp import ConstraintSatisfactionProblem
from dwavebinarycsp.factories.constraint.gates import and_gate, halfadder_gate, fulladder_gate, or_gate

"""This circuit is meant for bear bone trying out a CSP circuit"""


def make_array(size, string):
    return [string + str(i) for i in range(size)]


def get_data(sampleset, P):
    output = {
        "Results": [],
        #    {
        #        "a": Number,
        #        "b": Number,
        #        "Valid": Boolean,
        #        "Occurrences": Number,
        #        "Percentage of results": Number
        #    }
        "Timing": {
            "Actual": {
                "QPU processing time": None  # microseconds
            }
        },
        "Number of reads": None
    }

    a_vars = make_array(1, 'a')
    b_vars = make_array(1, 'b')
    p_vars = make_array(1, 'p')
    results_dict = OrderedDict()
    for sample, num_occurrences in sampleset.data(['sample', 'num_occurrences']):
        # Convert A and B from binary to decimal
        a = b = 0
        for lbl in reversed(a_vars):
            a = (a << 1) | sample[lbl]
        for lbl in reversed(b_vars):
            b = (b << 1) | sample[lbl]
        # Cast from numpy.int to int
        a, b = int(a), int(b)
        # Aggregate results by unique A and B values (ignoring internal circuit variables)
        if (a, b, P) in results_dict:
            results_dict[(a, b, P)]["Occurrences"] += num_occurrences
            results_dict[(a, b, P)]["Percentage of results"] = 100 * \
                                                               results_dict[(a, b, P)]["Occurrences"] / num_reads
        else:
            results_dict[(a, b, P)] = {"a": a,
                                       "b": b,
                                       # "Valid": a * b == P,
                                       "Occurrences": num_occurrences,
                                       "Percentage of results": 100 * num_occurrences / num_reads}
    output['Results'] = list(results_dict.values())
    output['Number of reads'] = num_reads
    return output


# create circuit that creates constraints for 2**7 bit number
def circuit(vartype=dimod.BINARY):
    num_multiplier_bits = num_multiplicand_bits = nbit = 4

    csp = ConstraintSatisfactionProblem(vartype)

    a = {i: 'a%d' % i for i in range(nbit)}
    b = {j: 'b%d' % j for j in range(nbit)}
    p = {k: 'p%d' % k for k in range(nbit + nbit - 1)}

    AND = defaultdict(dict)  # the output of the AND gate associated with ai, bj is stored in AND[i][j]
    SUM = defaultdict(dict)  # the sum of the ADDER gate associated with ai, bj is stored in SUM[i][j]
    CARRY = defaultdict(dict)

    csp.add_constraint(operator.truth, ['a0'])
    #setting the and gates
    for i in range(1,2):
        for j in range(1,2):
            ai = a[i]
            bj = b[j]
            andij = AND[i][j] = 'and%s,%s' % (i, j)
            gate = and_gate([ai, bj, andij], vartype=vartype, name='AND(%s, %s) = %s' % (ai, bj, andij))
            csp.add_constraint(gate)


    #half adder
    gate = halfadder_gate([a[1], b[1], SUM[1][1], p[1]], vartype=vartype)
    csp.add_constraint(gate)
    gate = halfadder_gate([a[2], AND[1][1], SUM[1][1], CARRY[1][1]], vartype=vartype)
    csp.add_constraint(gate)

    #full adder
    gate = fulladder_gate([AND[2][2], b[1], SUM[1][2], CARRY[1][2]], vartype=vartype)
    csp.add_constraint(gate)

    return csp


if __name__ == '__main__':
    csp = circuit()

    bqm = dbc.stitch(csp)
    bqm.fix_variable('p0', 0)
    bqm.fix_variable('a0', 1)
    sampler = neal.SimulatedAnnealingSampler()
    num_reads = 1
    sampleset = sampler.sample(bqm, num_reads=num_reads)
    # output = get_data(sampleset,1)
    # print(output)
