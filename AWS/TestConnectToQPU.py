
# general imports
import numpy as np
import matplotlib.pyplot as plt
# magic word for producing visualizations in notebook
import string
import time

# AWS imports: Import Braket SDK modules
from braket.circuits import Circuit, Gate, Instruction, circuit, Observable
from braket.devices import LocalSimulator
from braket.aws import AwsDevice, AwsQuantumTask


my_bucket = f"amazon-braket-52935ebbed2c" # the name of the bucket
my_prefix = "FQI" # the name of the folder in the bucket
s3_folder = (my_bucket, my_prefix)


# print all (the usual suspects) available gates currently available within SDK
gate_set = [attr for attr in dir(Gate) if attr[0] in string.ascii_uppercase]
print('Gate set supported by SDK:\n', gate_set)
print('\n')

# the Rigetti device
device = AwsDevice("arn:aws:braket:::device/quantum-simulator/amazon/sv1")
# supported_gates = device.properties.action['braket.ir.jaqcd.program'].supportedOperations
# # print the supported gate set
# print('Gate set supported by the Rigetti device:\n', supported_gates)
# print('\n')
#
#
# bell = Circuit().h(0).cnot(0, 1)
# print(bell)
#
# # set up device
# rigetti = AwsDevice("arn:aws:braket:::device/qpu/rigetti/Aspen-8")
#
# # create a clean circuit with no result type attached.(This is because some result types are only supported when shots=0)
# bell = Circuit().h(0).cnot(0, 1)
#
# # add the Z \otimes Z expectation value
# bell.expectation(Observable.Z() @ Observable.Z(), target=[0,1])
#
# # run circuit with a polling time of 5 days
# rigetti_task = rigetti.run(bell, s3_folder, shots=1000, poll_timeout_seconds=5*24*60*60)
#
# # get id and status of submitted task
# rigetti_task_id = rigetti_task.id
# rigetti_status = rigetti_task.state()
# # print('ID of task:', rigetti_task_id)
# print('Status of task:', rigetti_status)
#
# task_load = AwsQuantumTask(arn=rigetti_task_id)
#
# # print status
# status = task_load.state()
# print('Status of (reconstructed) task:', status)
# print('\n')
# # wait for job to complete
# # terminal_states = ['COMPLETED', 'FAILED', 'CANCELLED']
# if status == 'COMPLETED':
#     # get results
#     rigetti_results = task_load.result()
#     # print(rigetti_results)
#
#     # get all metadata of submitted task
#     metadata = task_load.metadata()
#     # example for metadata
#     shots = metadata['shots']
#     machine = metadata['deviceArn']
#     # print example metadata
#     print("{} shots taken on machine {}.\n".format(shots, machine))
#
#     # get the compiled circuit
#     print("The compiled circuit is:\n", rigetti_results.additional_metadata.rigettiMetadata.compiledProgram)
#
#     # get measurement counts
#     rigetti_counts = rigetti_results.measurement_counts
#     print('Measurement counts:', rigetti_counts)
#
#     # plot results: see effects of noise
#     plt.bar(rigetti_counts.keys(), rigetti_counts.values());
#     plt.xlabel('bitstrings');
#     plt.ylabel('counts');
#     plt.tight_layout();
#     plt.savefig('rigetti.png', dpi=700);
#
# elif status in ['FAILED', 'CANCELLED']:
#     # print terminal message
#     print('Your task is in terminal status, but has not completed.')
#
# else:
#     # print current status
#     print('Sorry, your task is still being processed and has not been finalized yet.')
