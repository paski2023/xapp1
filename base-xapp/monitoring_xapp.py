import xapp_control_ricbypass
"""
Non mi è ben chiaro a cosa serva importare e2sm.py
"""

from e2sm_proto import *
from time import sleep

def main():    

    print("Encoding ric monitoring request")
    
    # external message
    # In questo momento lui crea il tipo di dato RAN_message
    # Questo file è stato generato da protobuf
    
    master_mess = RAN_message()
    #Si imposta che il tipo di messaggio deve essere una INDICATION REQUEST
    master_mess.msg_type = RAN_message_type.INDICATION_REQUEST

    # internal message
    inner_mess = RAN_indication_request()
    # RAN indication request è definira come una lista di RAN_parameters 
    # nell'indication request 
    inner_mess.target_params.extend([
        RAN_parameter.GNB_ID,
        RAN_parameter.UE_LIST,
        RAN_parameter.UE_RSRP,         
        # Add the parameters you want here
        RAN_parameter.UE_BER_UPLINK,
        RAN_parameter.UE_BER_DOWNLINK,
        RAN_parameter.UE_MCS_UPLINK,
        RAN_parameter.UE_MCS_DOWNLINK,
        RAN_parameter.CELL_SIZE
    ])

    # assign and serialize
    master_mess.ran_indication_request.CopyFrom(inner_mess)
    buf = master_mess.SerializeToString()
    xapp_control_ricbypass.send_to_socket(buf)
    
    while True:
        r_buf = xapp_control_ricbypass.receive_from_socket()
        ran_ind_resp = RAN_indication_response()
        ran_ind_resp.ParseFromString(r_buf)
        print(ran_ind_resp)
        sleep(1)
        xapp_control_ricbypass.send_to_socket(buf)


if __name__ == '__main__':
    main()

