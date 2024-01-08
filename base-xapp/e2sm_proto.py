from sys import path
from os import getcwd

cwd = getcwd()
path.append('{}/Protolib1/builds'.format(cwd))

tmp = __import__('ran_messages_pb2')
print("rannando e2sm_proto.py")
print(tmp)
globals().update(vars(tmp))
print("finito di rannare e2sm_proto.py")
