import xapp_control_ricbypass


"""
e2sm importa la libreria con il protobuf compilato
"""

from e2sm_proto import *
from time import sleep
import time 
import numpy as np 
import pandas as pd

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
    

    columns = ["RTNI", "Time", "RSRP", "BER-up", "BER-down", 
                "MCS-up", "MCS-down", "cell-load"]
    
    data = pd.DataFrame(columns)
    
    while True:

        n_requests = 10
        waiting_time = 0.5 # 500ms

        """
        # currrent_data is a dictionary
        # rtni -> { time: timestamp, 
                    rsrp : [], 
                    ber_up: [],
                    ber_down: [],
                    mcs_up: last_value
                    mcs_down:last_value
                    cell_load: []
                }
        """

        current_data = {}
        columns = ["Time", "RSRP", "BER-up", "BER-down", "MCS-up", "MCS-down", "Cell-load"]
        for _ in range(n_requests): 

            # code for recieving the indication response
            # and parsing it
            xapp_control_ricbypass.send_to_socket(buf)

            r_buf = xapp_control_ricbypass.receive_from_socket()
            ran_ind_resp = RAN_indication_response()
            ran_ind_resp.ParseFromString(r_buf)

            #timestamp
            current_time = pd.Timestamp.now()
            
            # printing the strin gto terminal
            print(ran_ind_resp)
            
            for param_map_entry in ran_ind_resp.param_map: 

                if param_map_entry.key == RAN_parameter.UE_LIST:
                    
                    # execute this only if the message contain the list
                    for ue in param_map_entry.ue_list.ue_info: 

                        if ue.rnti in current_data.keys(): 
                            
                            current_data[ue.rnti]["RSRP"].append(ue.ue_rsrp)
                            current_data[ue.rnti]["BER-up"].append(ue.ue_ber_uplink)
                            current_data[ue.rnti]["BER-dwon"].append(ue.ue_ber_downlink)
                            current_data[ue.rnti]["MCS-up"] = ue.ue_mcs_uplink
                            current_data[ue.rnti]["MCS-down"] = ue.ue_mcs_downlink
                            current_data[ue.rnti]["cell-load"].append(ue.cell_size)

                        else: 
                            current_data[ue.rnti] = {"Time": current_time, "RSRP": [ue.ue_rsrp], 
                                                    "BER-up": [ue.ue_ber_uplink], 
                                                    "BER-down": [ue.ue_ber_downlink],
                                                    "MCS-up": ue.ue_mcs_uplink,
                                                    "MCS-down": ue.ue_ber_downlink,
                                                    "cell-load": [ue.cell_size]}



            #wait 
            sleep(waiting_time/n_requests)



        
        start = time.time()

        for key in current_data.keys(): 
            

            current_data[key]["RSRP"] = sum(current_data[key]["RSRP"]) / len(current_data[key]["RSRP"])
            current_data[key]["BER-up"] = sum(current_data[key]["BER-up"]) / len(current_data[key]["BER-up"])
            current_data[key]["BER-down"] = sum(current_data[key]["BER-down"]) / len(current_data[key]["BER-down"])
            current_data[key]["cell-load"] = sum(current_data[key]["cell-load"]) / len(current_data[key]["cell-load"])


            #create row
            row = {"RNTI": key}
            row.update(current_data[key])

            #add to data 
            data = data.append(row, ignore_index = True)

        end = time.time()
        print("COMPUTING STATISTICS COMPLETED")
        print(f"Time to complete statistics: {end-start}s")
    
        
        start = time.time()
        data.to_csv("CSV_dati.csv")
        end = time.time()
        print("SAVE CHANGES TO CSV COMPLETED")
        print(f"Time to complete saving: {end-start}s")


if __name__ == '__main__':
    main()

