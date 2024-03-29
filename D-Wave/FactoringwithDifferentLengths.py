
from collections import defaultdict

import dimod

from dwavebinarycsp.core.csp import ConstraintSatisfactionProblem
from dwavebinarycsp.factories.constraint.gates import and_gate, halfadder_gate, fulladder_gate

__all__ = ['multiplication_circuit']


def multiplication_circuit_different_factors(nbit, lenA, lenB, vartype=dimod.BINARY):


    if nbit < 1:
        raise ValueError("num_multiplier_bits, num_multiplicand_bits must be positive integers")

    num_multiplier_bits = num_multiplicand_bits = nbit

    # also checks the vartype argument
    csp = ConstraintSatisfactionProblem(vartype)

    # throughout, we will use the following convention:
    #   i to refer to the bits of the multiplier
    #   j to refer to the bits of the multiplicand
    #   k to refer to the bits of the product

    # create the variables corresponding to the input and output wires for the circuit
    a = {i: 'a%d' % i for i in range(lenA)}
    b = {j: 'b%d' % j for j in range(lenB)}
    p = {k: 'p%d' % k for k in range(nbit + nbit)}

    # we will want to store the internal variables somewhere
    AND = defaultdict(dict)  # the output of the AND gate associated with ai, bj is stored in AND[i][j]
    SUM = defaultdict(dict)  # the sum of the ADDER gate associated with ai, bj is stored in SUM[i][j]
    CARRY = defaultdict(dict)  # the carry of the ADDER gate associated with ai, bj is stored in CARRY[i][j]

    # we follow a shift adder
    for i in range(lenA):
        for j in range(lenB):

            ai = a[i]
            bj = b[j]

            if i == 0 and j == 0:
                # in this case there are no inputs from lower bits, so our only input is the AND
                # gate. And since we only have one bit to add, we don't need an adder, no have a
                # carry out
                andij = AND[i][j] = p[0]

                gate = and_gate([ai, bj, andij], vartype=vartype, name='AND(%s, %s) = %s' % (ai, bj, andij))
                csp.add_constraint(gate)

                continue

            # we always need an AND gate
            andij = AND[i][j] = 'and%s,%s' % (i, j)

            gate = and_gate([ai, bj, andij], vartype=vartype, name='AND(%s, %s) = %s' % (ai, bj, andij))
            csp.add_constraint(gate)

            # the number of inputs will determine the type of adder
            inputs = [andij]

            # determine if there is a carry in
            if i - 1 in CARRY and j in CARRY[i - 1]:
                inputs.append(CARRY[i - 1][j])

            # determine if there is a sum in
            if i - 1 in SUM and j + 1 in SUM[i - 1]:
                inputs.append(SUM[i - 1][j + 1])

            # ok, add create adders if necessary
            if len(inputs) == 1:
                # we don't need an adder and we don't have a carry
                SUM[i][j] = andij
            elif len(inputs) == 2:
                # we need a HALFADDER so we have a sum and a carry

                if j == 0:
                    sumij = SUM[i][j] = p[i]
                else:
                    sumij = SUM[i][j] = 'sum%d,%d' % (i, j)

                carryij = CARRY[i][j] = 'carry%d,%d' % (i, j)

                name = 'HALFADDER(%s, %s) = %s, %s' % (inputs[0], inputs[1], sumij, carryij)
                gate = halfadder_gate([inputs[0], inputs[1], sumij, carryij], vartype=vartype, name=name)
                csp.add_constraint(gate)
            else:
                assert len(inputs) == 3, 'unexpected number of inputs'

                # we need a FULLADDER so we have a sum and a carry

                if j == 0:
                    sumij = SUM[i][j] = p[i]
                else:
                    sumij = SUM[i][j] = 'sum%d,%d' % (i, j)

                carryij = CARRY[i][j] = 'carry%d,%d' % (i, j)

                name = 'FULLADDER(%s, %s, %s) = %s, %s' % (inputs[0], inputs[1], inputs[2], sumij, carryij)
                gate = fulladder_gate([inputs[0], inputs[1], inputs[2], sumij, carryij], vartype=vartype, name=name)
                csp.add_constraint(gate)

    # now we have a final row of full adders
    """todo need to fix this"""
    for col in range(nbit - 1):
        print(col)
        inputs = [CARRY[nbit - 1][col], SUM[nbit - 1][col + 1]]

        if col == 0:
            sumout = p[nbit + col]
            carryout = CARRY[nbit][col] = 'carry%d,%d' % (nbit, col)

            name = 'HALFADDER(%s, %s) = %s, %s' % (inputs[0], inputs[1], sumout, carryout)
            gate = halfadder_gate([inputs[0], inputs[1], sumout, carryout], vartype=vartype, name=name)
            csp.add_constraint(gate)

            continue

        inputs.append(CARRY[nbit][col - 1])

        sumout = p[nbit + col]
        if col < nbit - 2:
            carryout = CARRY[nbit][col] = 'carry%d,%d' % (nbit, col)
        else:
            carryout = p[2 * nbit - 1]

        name = 'FULLADDER(%s, %s, %s) = %s, %s' % (inputs[0], inputs[1], inputs[2], sumout, carryout)
        gate = fulladder_gate([inputs[0], inputs[1], inputs[2], sumout, carryout], vartype=vartype, name=name)
        csp.add_constraint(gate)

    return csp
