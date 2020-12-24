import sys
from pprint import pprint
import time
import logging
import functools
from collections import OrderedDict
from saveData import save_data
import dwavebinarycsp as dbc
from dwave.system import DWaveSampler, EmbeddingComposite

log = logging.getLogger(__name__)


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

    # Constraint satisfaction problem
    # where the number of
    csp = dbc.factories.multiplication_circuit(size_of_circuit)

    # Binary quadratic model
    bqm = dbc.stitch(csp, min_classical_gap=gap_size, max_graph_size=max_graph_size)

    # multiplication_circuit() creates these variables
    p_vars = make_array(size_of_circuit * 2, 'p')
    binary = "{:0" + str(size_of_circuit * 2) + "b}"
    # Convert P from decimal to binary
    fixed_variables = dict(zip(reversed(p_vars), binary.format(P)))
    fixed_variables = {var: int(x) for (var, x) in fixed_variables.items()}

    # Fix product qubits
    for var, value in fixed_variables.items():
        bqm.fix_variable(var, value)

    log.debug('bqm construction time: %s', time.time() - construction_start_time)

    # Run problem
    # ===========

    sample_time = time.time()

    # Set a QPU sampler
    sampler = EmbeddingComposite(DWaveSampler())

    num_reads = 1000
    print("Sent to D-Wave")
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
    a_vars = make_array(size_of_circuit, 'a')
    b_vars = make_array(size_of_circuit, 'b')
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
            # if a * b == P:
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

    output['Timing']['Actual']['QPU processing time'] = sampleset.info['timing']['qpu_access_time']
    save_data(P, 'Advantage_system1.1', size_of_circuit, gap_size, max_graph_size, output)
    return output


if __name__ == '__main__':
    # get input from user
    print("Enter a number to be factored:")
    #
    # # send problem to QPU
    print("Running on QPU")
    # numbers = [143,1000,403,901]
    numbers = [299]
    gaps = [0.01, 0.03, 0.05, 0.08, 0.1]
    for n in numbers:
        for gap in gaps:
            for graph in range(5, 20, 5):
                for circuit in range(5, 8):
                    output = factor(n, gap, graph, circuit)
                    print('done:', gap, graph, circuit)

    # output results
    # pprint(output)
