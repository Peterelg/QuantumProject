# matplotlib inline
from qiskit import IBMQ

#IBMQ.save_account('f8412974401454dc09f0a2b1d4f0aa9adf75630b0a9c1b3718d88c750c124d8281382b9788531791b0d69a9d9ffb8efa5e7a20593ff43f68cbebbb9d3d31f83b')
IBMQ.load_account() # Load account from disk
IBMQ.providers()