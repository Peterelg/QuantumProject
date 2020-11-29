from coreapi.auth import BasicAuthentication
from quantuminspire.api import QuantumInspireAPI


qi = QuantumInspireAPI()


qasm = '''
version 1.0

qubits 3

# start writing your code here

prep_x q[0]
Rx q[0], 3.142
Ry q[0], 1.57
measure_z q[0]
prep_x q[1]
Rx q[1], 3.142
Ry q[1], 1.57
measure_x q[1]
prep_x q[2]
Rx q[2], 3.142
Ry q[2], 1.57
measure_y q[2]
'''
#test test#

backend_type = qi.get_backend_type_by_name('QX single-node simulator')
result = qi.execute_qasm(qasm, backend_type=backend_type, number_of_shots=1024)

if result.get('histogram', {}):
    print(result['histogram'])
else:
    reason = result.get('raw_text', 'No reason in result structure.')
    print(f'Result structure does not contain proper histogram data. {reason}')