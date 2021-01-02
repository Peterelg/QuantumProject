import sys
from pprint import pprint
import time
import logging
import functools
import helpers
from collections import OrderedDict
import dwavebinarycsp as dbc
from dwave.system import DWaveSampler, EmbeddingComposite
from EditedCircuit import multiplication_circuit
import neal

log = logging.getLogger(__name__)

"""This file factors numbers locally so more experimentation can occur"""


def sanitised_input(description, variable, range_):
    start = range_[0]
    stop = range_[-1]

    while True:
        ui = input("Input {:15}({:2} <= {:1} <= {:2}): ".format(description, start, variable, stop))

        try:
            ui = int(ui)
        except ValueError:
            print("Input type must be int")
            continue

        if ui not in range_:
            print("Input must be between {} and {}".format(start, stop))
            continue

        return ui


def validate_input(ui, range_):
    start = range_[0]
    stop = range_[-1]

    if not isinstance(ui, int):
        raise ValueError("Input type must be int")

    if ui not in range_:
        raise ValueError("Input must be between {} and {}".format(start, stop))


def make_array(size, string):
    return [string + str(i) for i in range(size)]


def factor(P, gap_size, max_graph_size, size_of_circuit):
    # Construct circuit
    # =================
    construction_start_time = time.time()

    validate_input(P, range(2 ** (size_of_circuit * 2)))

    """adapted simulation"""
    # csp, inputs = multiplication_circuit(size_of_circuit)

    """original simulation"""
    csp = dbc.factories.multiplication_circuit(size_of_circuit)

    # Binary quadratic model
    bqm = dbc.stitch(csp, max_graph_size=max_graph_size, min_classical_gap=gap_size)
    # for c in iter(csp.constraints):
    #     print(c)
    # multiplication_circuit() creates these variables
    p_vars = make_array(size_of_circuit * 2, 'p')
    a_vars = make_array(size_of_circuit, 'a')
    b_vars = make_array(size_of_circuit, 'b')
    binary = "{:0" + str(size_of_circuit * 2) + "b}"
    # Convert P from decimal to binary
    fixed_variables = dict(zip(reversed(p_vars), binary.format(P)))
    fixed_variables = {var: int(x) for (var, x) in fixed_variables.items()}

    # Fix product qubits
    for var, value in fixed_variables.items():
        bqm.fix_variable(var, value)
        # print(var,value)

    log.debug('bqm construction time: %s', time.time() - construction_start_time)

    # Run problem
    # ===========

    sample_time = time.time()

    # Set a QPU sampler
    sampler = neal.SimulatedAnnealingSampler()

    num_reads = 1000
    print("running localy")
    sampleset = sampler.sample(bqm, num_reads=num_reads)

    log.debug('embedding and sampling time: %s', time.time() - sample_time)

    # Output results
    # ==============

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

    # multiplication_circuit() creates these variables

    wrong_A = 0
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
            if a * b == P:
                # results_dict[(a, b, P)] = {a, b, a * b == P, num_occurrences, 100 * num_occurrences / num_reads}
                results_dict[(a, b, P)] = {"a": a,
                                           "b": b,
                                           "Valid": a * b == P,
                                           "Occurrences": num_occurrences,
                                           "Percentage of results": 100 * num_occurrences / num_reads}
            # else:
            #     wrong_A = wrong_A + 1
            # results_dict[(a, b, P)] = {"a": a,
            #                            "b": b,
            #                            "Valid": a * b == P,
            #                            "Occurrences": num_occurrences,
            #                            "Percentage of results": 100 * num_occurrences / num_reads}

    output['Results'] = list(results_dict.values())
    output['Number of reads'] = num_reads

    # output['Timing']['Actual']['QPU processing time'] = sampleset.info['timing']['qpu_access_time']
    return output, csp


if __name__ == '__main__':
    # get input from user
    number = 59989
    gap = 0.1
    graph = 8
    circuit = 8
    output, csp = factor(number, gap, graph, circuit)

    # output results
    pprint(output)
