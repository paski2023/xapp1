from sys import path
from os import getcwd


cwd = getcwd() #restituisce la directory corrente 
"""
sys.path è una lista di directories dove l'interprete python cerca moduli
"""
# Si aggiunge il percorso alla cartella Protolib1/builds

path.append('{}/Protolib1/builds'.format(cwd)) 


# Infatti il file ran_messages pb2.py si trova in quella cartella
tmp = __import__('ran_messages_pb2')
# L'import effettuato in questo modo permette di rinominare la libreria


globals().update(vars(tmp))
#Aggiorna le variabili globali con le variabili della libreria ran_messages_pb2
