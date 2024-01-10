import xapp_control_ricbypass


"""
e2sm importa la libreria con il protobuf compilato
"""

from e2sm_proto import *
from time import sleep

def main():    

    print("Encoding ric monitoring request")
    
    # external message
    # In questo momento lui crea il tipo di dato RAN_message
    # Questo file è stato generato da protobuf
    
    master_mess = RAN_message() # Crea un messaggio 
    '''
    Un RAN MESSAGE HA: 
    -> required RAN_message_type 
    + one payload which can be: 
    -> indication request 
    -> indication response
    -> control request
    '''
    #Si imposta che il tipo di messaggio deve essere una INDICATION REQUEST
    master_mess.msg_type = RAN_message_type.INDICATION_REQUEST

    '''
    Qui creaiamo il payload che identifichiamo come un messaggio indication request 
    -> repeated RAN_parameters target_params
    '''
    # internal message
    inner_mess = RAN_indication_request()
    # RAN indication request è definira come una lista di RAN_parameters 
    # nell'indication request 
    inner_mess.target_params.extend([
        RAN_parameter.GNB_ID,
        RAN_parameter.UE_LIST
    ])

    # assign and serialize
    master_mess.ran_indication_request.CopyFrom(inner_mess)
    buf = master_mess.SerializeToString()
    
    '''
    This is used for transmission of the protobuf data: 
    you pass the data. If the transmission is not initialized it initialize
    the transmission and then it send the data. 
    '''
    xapp_control_ricbypass.send_to_socket(buf)
    
    while True:
        r_buf = xapp_control_ricbypass.receive_from_socket()
        ran_ind_resp = RAN_indication_response()
        ran_ind_resp.ParseFromString(r_buf)
        print(ran_ind_resp)
        """
        Nel messaggio di risposta c'è un messaggio ue_list_m
        con una chiave: UE_LIST 
        e poi una ue_list_m che continet eun numero di utenti connessi
        e un repeated ue_info_m
        -> Indication Response:
            -> chiave: UE_LIST
            -> lista: UE_LIST_M -> numero utenti connessi
                                -> lista: UE_INFO_m -> messaggio con tutti i parametri 
        """
        if ran_ind_resp.param_map.key == RAN_parameter.UE_LIST:
            # Se il parametro della risposta è una ue_lista
            # apri il messaggio, vai alla lista e per tutti gli utenti ripeti 
            with open('file.txt', "a") as f: 
            
                for user in ran_ind_resp.param_map.ue_list:
                    stringa = ""
                    for j in user.ue_info:
                        stringa += str(j)
                        print(f"E' stato aggiunto: {j}")
                        print(f"Il tipo di questo dato è: {type(str)}")

                    f.write(stringa + "\n")
                
            
             
        sleep(30)
        
        xapp_control_ricbypass.send_to_socket(buf)


if __name__ == '__main__':
    main()

