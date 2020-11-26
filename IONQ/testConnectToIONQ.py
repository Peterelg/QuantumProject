import boto3
from braket.aws import AwsDevice
from braket.circuits import Circuit

aws_account_id = boto3.client("sts").get_caller_identity()["Account"]
device = AwsDevice("arn:aws:braket:::device/qpu/ionq/ionQdevice")
s3_folder = (f"amazon-braket-52935ebbed2c", "FQI")

bell = Circuit().h(0).cnot(0, 1)
task = device.run(bell, s3_folder, shots=100)
print(task.result().measurement_counts)