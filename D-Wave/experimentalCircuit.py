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


def run_circuit(P, gap, graph, circuit_size):


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
    csp = circuit(circuit_size)
    bqm = dbc.stitch(csp, max_graph_size=graph, min_classical_gap=gap)

    a_vars = make_array(circuit_size, 'a')
    b_vars = make_array(circuit_size, 'b')
    p_vars = make_array(circuit_size*2, 'p')
    binary = "{:0" + str(circuit_size * 2) + "b}"
    # Convert P from decimal to binary
    fixed_variables = dict(zip(reversed(p_vars), binary.format(P)))
    fixed_variables = {var: int(x) for (var, x) in fixed_variables.items()}

    # Fix product qubits
    # for var, value in fixed_variables.items():
    #     bqm.fix_variable(var, value)
    for constraint in csp.constraints:
        print(constraint)

    # results_dict = OrderedDict()
    # for sample, num_occurrences in sampleset.data(['sample', 'num_occurrences']):
    #     # Convert A and B from binary to decimal
    #     a = b = 0
    #     for lbl in reversed(a_vars):
    #         a = (a << 1) | sample[lbl]
    #     for lbl in reversed(b_vars):
    #         b = (b << 1) | sample[lbl]
    #     # Cast from numpy.int to int
    #     a, b = int(a), int(b)
    #     # Aggregate results by unique A and B values (ignoring internal circuit variables)
    #     if (a, b, P) in results_dict:
    #         results_dict[(a, b, P)]["Occurrences"] += num_occurrences
    #         results_dict[(a, b, P)]["Percentage of results"] = 100 * \
    #                                                            results_dict[(a, b, P)]["Occurrences"] / num_reads
    #     else:
    #         results_dict[(a, b, P)] = {"a": a,
    #                                    "b": b,
    #                                    # "Valid": a * b == P,
    #                                    "Occurrences": num_occurrences,
    #                                    "Percentage of results": 100 * num_occurrences / num_reads}
    # output['Results'] = list(results_dict.values())
    # output['Number of reads'] = num_reads
    # return output


# create circuit that creates constraints for 2**7 bit number
def circuit(nbit, vartype=dimod.BINARY):
    num_multiplier_bits = num_multiplicand_bits = nbit

    csp = ConstraintSatisfactionProblem(vartype)

    a = {i: 'a%d' % i for i in range(nbit)}
    b = {j: 'b%d' % j for j in range(nbit)}
    p = {k: 'p%d' % k for k in range(nbit*2)}

    AND = defaultdict(dict)  # the output of the AND gate associated with ai, bj is stored in AND[i][j]
    SUM = defaultdict(dict)  # the sum of the ADDER gate associated with ai, bj is stored in SUM[i][j]
    CARRY = defaultdict(dict)

    csp.add_constraint(operator.truth, ['a0'])
    #setting the and gates
    for i in range(1,nbit-1):
        for j in range(1,nbit-1):
            ai = a[i]
            bj = b[j]
            andij = AND[i][j] = 'and%s,%s' % (i, j)
            gate = and_gate([ai, bj, andij], vartype=vartype, name='AND(%s, %s) = %s' % (ai, bj, andij))
            csp.add_constraint(gate)
            AND[i][j] = 'and%s,%s' % (i, j)
            SUM[i][j] = 'sum%d,%d' % (i, j)
            CARRY[i][j] = 'carry%d,%d' % (i, j)

    for col in range(0,nbit*2):
        """"
            a1,b1 = 0
            a2,b2 = 1
            and(a1,b1) = 2
            and(a1,b2), and(a2,b1) = 3
            and(a2,b2) = 4 
            sum(3,3) = 5
            sum(4,4) = 6
        
        """
        #half adder
        # 1st column
        # half adder a1 and b1
        gate = halfadder_gate([col, b[1], p[1], CARRY[1][1]], vartype=vartype)
        csp.add_constraint(gate)
        # # 2nd column
        # # half adder and(a1,b1) and p2
        # gate = halfadder_gate([a[2], AND[1][1], SUM[1][2], CARRY[1][2]], vartype=vartype)
        # csp.add_constraint(gate)
        # #full adder
        # # fulladder of the sum[1][2], carry[0][0] and b2
        # gate = fulladder_gate([SUM[2][2], CARRY[0][0], b[2], p[2], CARRY[2][1]], vartype=vartype)
        # csp.add_constraint(gate)
        # # 3rd column
        # # full adder not(and[2][1]), and[1][2] and carry[1][2]
        # gate = fulladder_gate([not(AND[2][1]), AND[1][2], CARRY[1][2], SUM[3][3], CARRY[3][3]], vartype=vartype)
        # csp.add_constraint(gate)
        # # half adder
        # gate = halfadder_gate([not(SUM[3][3]), not(CARRY[2][1]), not(p[3]), CARRY[5][2]], vartype=vartype)
        # csp.add_constraint(gate)
        # # 4th column
        # # full adder and(p2,q2), q1 and not(p2,q1)
        # gate = fulladder_gate([AND[2][2], b[1], not(AND[2][1]), SUM[3][0], CARRY[3][0]], vartype=vartype)
        # csp.add_constraint(gate)
        # # full adder a1, sum, carry
        # gate = fulladder_gate([a[1], SUM[3][0], CARRY[3][3], SUM[][], CARRY[][]], vartype=vartype)
        # csp.add_constraint(gate)
        # # half adder sum and not(carry)
        # gate = halfadder_gate([SUM[][], not(CARRY[4][4]), p[4], CARRY[][]], vartype=vartype)
        # csp.add_constraint(gate)
        # #5th column
        # #full adder a2,b2, carry
        # #full adder sum, carry, carry
        # #6th column
        # #half adder carry not, carry not


    return csp


if __name__ == '__main__':
    number = 143
    gap = 0.1
    graph = 8
    circuit_size = 4
    run_circuit(number, gap,graph,circuit_size)
