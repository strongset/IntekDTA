# -*- coding: utf-8 -*-
# Test name = Software Upgrade
# Test description = Set environment, perform software upgrade and check STB state after sw upgrade

from datetime import datetime
from time import gmtime, strftime
import time
import os.path
import sys
import device

import TEST_CREATION_API
import shutil
##shutil.copyfile('\\\\bbtfs\\RT-Executor\\API\\NOS_API.py', 'NOS_API.py')

try:    
    if ((os.path.exists(os.path.join(os.path.dirname(sys.executable), "Lib\NOS_API.py")) == False) or (str(os.path.getmtime('\\\\rt-rk01\\RT-Executor\\API\\NOS_API.py')) != str(os.path.getmtime(os.path.join(os.path.dirname(sys.executable), "Lib\NOS_API.py"))))):
        shutil.copy2('\\\\rt-rk01\\RT-Executor\\API\\NOS_API.py', os.path.join(os.path.dirname(sys.executable), "Lib\NOS_API.py"))
except:
    pass

import NOS_API    
 
try:
    # Get model
    model_type = NOS_API.get_model()

    # Check if folder with thresholds exists, if not create it
    if(os.path.exists(os.path.join(os.path.dirname(sys.executable), "Thresholds")) == False):
        os.makedirs(os.path.join(os.path.dirname(sys.executable), "Thresholds"))

    # Copy file with threshold if does not exists or if it is updated
    if ((os.path.exists(os.path.join(os.path.dirname(sys.executable), "Thresholds\\" + model_type + ".txt")) == False) or (str(os.path.getmtime(NOS_API.THRESHOLDS_PATH + model_type + ".txt")) != str(os.path.getmtime(os.path.join(os.path.dirname(sys.executable), "Thresholds\\" + model_type + ".txt"))))):
        shutil.copy2(NOS_API.THRESHOLDS_PATH + model_type + ".txt", os.path.join(os.path.dirname(sys.executable), "Thresholds\\" + model_type + ".txt"))
except Exception as error_message:
    pass  
    
## Number of alphanumeric characters in SN
SN_LENGTH = 14 

WAIT_OTA_TEST = 20  

NOS_API.grabber_type()
TEST_CREATION_API.grabber_type()

def runTest():

    NOS_API.grabber_hour_reboot()
    
    System_Failure = 0
    while (System_Failure < 2):
        try:
            NOS_API.read_thresholds()
            HDMI_threshold = TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD
            NOS_API.SET_720 = False
            NOS_API.SET_576= False
            error_codes = ""
            error_messages = ""
            ## Set test result default to FAIL
            test_result = "FAIL"
            SN_LABEL = False

            Hardware_Result = False
            
            ## Reset all global variables 
            NOS_API.reset_test_cases_results_info()
            
            if(System_Failure > 0):
                NOS_API.configure_power_switch_by_inspection()
                if not(NOS_API.power_off()):
                    TEST_CREATION_API.write_log_to_file("Comunication with PowerSwitch Fails")
                    ## Update test result
                    TEST_CREATION_API.update_test_result(test_result)
                    NOS_API.set_error_message("POWER SWITCH")
                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.power_switch_error_code \
                                                        + "; Error message: " + NOS_API.test_cases_results_info.power_switch_error_message)
                    error_codes = NOS_API.test_cases_results_info.power_switch_error_code
                    error_messages = NOS_API.test_cases_results_info.power_switch_error_message
                    ## Return DUT to initial state and de-initialize grabber device
                    NOS_API.deinitialize()
                    NOS_API.add_test_case_result_to_file_report(
                            test_result,
                            "- - - - - - - - - - - - - - - - - - - -",
                            "- - - - - - - - - - - - - - - - - - - -",
                            error_codes,
                            error_messages)
                
                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    report_file = NOS_API.create_test_case_log_file(
                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                NOS_API.test_cases_results_info.nos_sap_number,
                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                NOS_API.test_cases_results_info.mac_using_barcode,
                                end_time)
                    NOS_API.upload_file_report(report_file)
                    
                    NOS_API.send_report_over_mqtt_test_plan(
                        test_result,
                        end_time,
                        error_codes,
                        report_file)
                    
                    return
        
            try:
                ## Perform scanning with barcode scanner   
                all_scanned_barcodes = NOS_API.get_all_scanned_barcodes()     
                NOS_API.test_cases_results_info.s_n_using_barcode = all_scanned_barcodes[1]       
                NOS_API.test_cases_results_info.nos_sap_number = all_scanned_barcodes[0]
            except Exception as error:   
                TEST_CREATION_API.write_log_to_file(error)
                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.scan_error_code \
                                            + "; Error message: " + NOS_API.test_cases_results_info.scan_error_message)
                NOS_API.set_error_message("Leitura de Etiquetas")
                error_codes = NOS_API.test_cases_results_info.scan_error_code
                error_messages = NOS_API.test_cases_results_info.scan_error_message
                
                NOS_API.add_test_case_result_to_file_report(
                        test_result,
                        "- - - - - - - - - - - - - - - - - - - -",
                        "- - - - - - - - - - - - - - - - - - - -",
                        error_codes,
                        error_messages)
        
                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                report_file = NOS_API.create_test_case_log_file(
                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                    NOS_API.test_cases_results_info.nos_sap_number,
                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                    end_time)
                NOS_API.upload_file_report(report_file)      
                NOS_API.test_cases_results_info.isTestOK = False
                
                ## Update test result
                TEST_CREATION_API.update_test_result(test_result)
                
                NOS_API.send_report_over_mqtt_test_plan(
                        test_result,
                        end_time,
                        error_codes,
                        report_file)
        
                return
            
            test_number = NOS_API.get_test_number(NOS_API.test_cases_results_info.s_n_using_barcode)
            device.updateUITestSlotInfo("Teste N\xb0: " + str(int(test_number)+1))
            
            if ((len(NOS_API.test_cases_results_info.s_n_using_barcode) == SN_LENGTH) and (NOS_API.test_cases_results_info.s_n_using_barcode.isalnum() or NOS_API.test_cases_results_info.s_n_using_barcode.isdigit())):
                SN_LABEL = True
            if (SN_LABEL): 
                if(System_Failure == 0):
                    if (NOS_API.display_new_dialog("Conectores?", NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "OK"): 
                        
                        if (NOS_API.display_new_dialog("Painel Traseiro?", NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "OK"):
            
                            Hardware_Result = True               
                            
                        else:
                            TEST_CREATION_API.write_log_to_file("Back Panel NOK")
                            NOS_API.set_error_message("Danos Externos")
                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.back_panel_nok_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.back_panel_nok_error_message) 
                            error_codes = NOS_API.test_cases_results_info.back_panel_nok_error_code
                            error_messages = NOS_API.test_cases_results_info.back_panel_nok_error_message 
                    else:       
                        TEST_CREATION_API.write_log_to_file("Conectores NOK")
                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.conector_nok_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.conector_nok_error_message)
                        NOS_API.set_error_message("Danos Externos")
                        error_codes = NOS_API.test_cases_results_info.conector_nok_error_code
                        error_messages = NOS_API.test_cases_results_info.conector_nok_error_message
                else:
                    Hardware_Result = True 
            else:
                TEST_CREATION_API.write_log_to_file("Labels Scaning")
                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.scan_error_code \
                                            + "; Error message: " + NOS_API.test_cases_results_info.scan_error_message)
                NOS_API.set_error_message("Leitura de Etiquetas")
                error_codes = NOS_API.test_cases_results_info.scan_error_code
                error_messages = NOS_API.test_cases_results_info.scan_error_message
            
            if(Hardware_Result):
                ## Initialize grabber device
                NOS_API.initialize_grabber()
        
                #NOS_API.reset_dut()
        
                ## Start grabber device with video on default video source
                NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.HDMI1)
                #time.sleep(1) 
                NOS_API.Send_Serial_Key("a", "feito")
                time.sleep(1)
                
                NOS_API.display_custom_dialog("Pressione bot\xe3o 'Power' at\xe9 aparecer a pr\xf3xima pergunta", 1, ["Continuar"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG)
                if (NOS_API.configure_power_switch_by_inspection()):
                    if not(NOS_API.power_on()):
                        TEST_CREATION_API.write_log_to_file("Comunication with PowerSwitch Fails")
                        ## Update test result
                        TEST_CREATION_API.update_test_result(test_result)
                        NOS_API.set_error_message("POWER SWITCH")
                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.power_switch_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.power_switch_error_message)
                        error_codes = NOS_API.test_cases_results_info.power_switch_error_code
                        error_messages = NOS_API.test_cases_results_info.power_switch_error_message
                        ## Return DUT to initial state and de-initialize grabber device
                        NOS_API.deinitialize()
                        NOS_API.add_test_case_result_to_file_report(
                                test_result,
                                "- - - - - - - - - - - - - - - - - - - -",
                                "- - - - - - - - - - - - - - - - - - - -",
                                error_codes,
                                error_messages)
                    
                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        report_file = NOS_API.create_test_case_log_file(
                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                    NOS_API.test_cases_results_info.nos_sap_number,
                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                    end_time)
                        NOS_API.upload_file_report(report_file)
                        
                        NOS_API.send_report_over_mqtt_test_plan(
                            test_result,
                            end_time,
                            error_codes,
                            report_file)
                        
                        return
                    
                    time.sleep(2)
                else:
                    TEST_CREATION_API.write_log_to_file("Incorrect test place name")
                    ## Update test result
                    TEST_CREATION_API.update_test_result(test_result)
                    NOS_API.set_error_message("POWER SWITCH")
                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.power_switch_error_code \
                                                        + "; Error message: " + NOS_API.test_cases_results_info.power_switch_error_message)
                    error_codes = NOS_API.test_cases_results_info.power_switch_error_code
                    error_messages = NOS_API.test_cases_results_info.power_switch_error_message
                    ## Return DUT to initial state and de-initialize grabber device
                    NOS_API.deinitialize()
                    NOS_API.add_test_case_result_to_file_report(
                            test_result,
                            "- - - - - - - - - - - - - - - - - - - -",
                            "- - - - - - - - - - - - - - - - - - - -",
                            error_codes,
                            error_messages)
                
                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    report_file = NOS_API.create_test_case_log_file(
                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                NOS_API.test_cases_results_info.nos_sap_number,
                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                NOS_API.test_cases_results_info.mac_using_barcode,
                                end_time)
                    NOS_API.upload_file_report(report_file)
                    
                    NOS_API.send_report_over_mqtt_test_plan(
                        test_result,
                        end_time,
                        error_codes,
                        report_file)
                
                    return              

                if not(NOS_API.display_custom_dialog("A STB est\xe1 ligada?", 2, ["OK", "NOK"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "OK"):  
                    NOS_API.display_dialog("Confirme o cabo Alimenta\xe7\xe3o e restantes cabos", NOS_API.WAIT_TIME_TO_CLOSE_DIALOG)
                    if not(NOS_API.power_off()):
                        TEST_CREATION_API.write_log_to_file("Comunication with PowerSwitch Fails")
                        ## Update test result
                        TEST_CREATION_API.update_test_result(test_result)
                        NOS_API.set_error_message("POWER SWITCH")
                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.power_switch_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.power_switch_error_message)
                        error_codes = NOS_API.test_cases_results_info.power_switch_error_code
                        error_messages = NOS_API.test_cases_results_info.power_switch_error_message
                        ## Return DUT to initial state and de-initialize grabber device
                        NOS_API.deinitialize()
                        NOS_API.add_test_case_result_to_file_report(
                                test_result,
                                "- - - - - - - - - - - - - - - - - - - -",
                                "- - - - - - - - - - - - - - - - - - - -",
                                error_codes,
                                error_messages)
                    
                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        report_file = NOS_API.create_test_case_log_file(
                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                    NOS_API.test_cases_results_info.nos_sap_number,
                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                    end_time)
                        NOS_API.upload_file_report(report_file)
                        
                        NOS_API.send_report_over_mqtt_test_plan(
                            test_result,
                            end_time,
                            error_codes,
                            report_file)
                        
                        return
                    
                    time.sleep(2)
                    NOS_API.display_custom_dialog("Pressione bot\xe3o 'Power' at\xe9 aparecer a pr\xf3xima pergunta", 1, ["Continuar"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG)
                    if not(NOS_API.power_on()):
                        TEST_CREATION_API.write_log_to_file("Comunication with PowerSwitch Fails")
                        ## Update test result
                        TEST_CREATION_API.update_test_result(test_result)
                        NOS_API.set_error_message("POWER SWITCH")
                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.power_switch_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.power_switch_error_message)
                        error_codes = NOS_API.test_cases_results_info.power_switch_error_code
                        error_messages = NOS_API.test_cases_results_info.power_switch_error_message
                        ## Return DUT to initial state and de-initialize grabber device
                        NOS_API.deinitialize()
                        NOS_API.add_test_case_result_to_file_report(
                                test_result,
                                "- - - - - - - - - - - - - - - - - - - -",
                                "- - - - - - - - - - - - - - - - - - - -",
                                error_codes,
                                error_messages)
                    
                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        report_file = NOS_API.create_test_case_log_file(
                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                    NOS_API.test_cases_results_info.nos_sap_number,
                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                    end_time)
                        NOS_API.upload_file_report(report_file)
                        
                        NOS_API.send_report_over_mqtt_test_plan(
                            test_result,
                            end_time,
                            error_codes,
                            report_file)
                        
                        return
                    if not(NOS_API.display_custom_dialog("A STB est\xe1 ligada?", 2, ["OK", "NOK"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "OK"):
                        TEST_CREATION_API.write_log_to_file("No Power")
                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.no_power_error_code \
                                                        + "; Error message: " + NOS_API.test_cases_results_info.no_power_error_message) 
                        NOS_API.set_error_message("Não Liga") 
                        error_codes =  NOS_API.test_cases_results_info.no_power_error_code
                        error_messages = NOS_API.test_cases_results_info.no_power_error_message
                        NOS_API.deinitialize()
                        
                        NOS_API.add_test_case_result_to_file_report(
                                test_result,
                                "- - - - - - - - - - - - - - - - - - - -",
                                "- - - - - - - - - - - - - - - - - - - -",
                                error_codes,
                                error_messages)
                    
                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        report_file = NOS_API.create_test_case_log_file(
                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                    NOS_API.test_cases_results_info.nos_sap_number,
                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                    end_time)
                        NOS_API.upload_file_report(report_file)
                        
                        NOS_API.send_report_over_mqtt_test_plan(
                            test_result,
                            end_time,
                            error_codes,
                            report_file)
                    
                    
                        return
    
                Comparison = NOS_API.wait_for_multiple_pictures(["OTA_Setup_ref","OTA_Setup_ref1"], WAIT_OTA_TEST, ["[OTA_SETUP]","[OTA_SETUP]"], [NOS_API.thres,NOS_API.thres])
                if(Comparison == -1):
                    if not(NOS_API.power_off()):
                        TEST_CREATION_API.write_log_to_file("Comunication with PowerSwitch Fails")
                        ## Update test result
                        TEST_CREATION_API.update_test_result(test_result)
                        NOS_API.set_error_message("POWER SWITCH")
                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.power_switch_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.power_switch_error_message)
                        error_codes = NOS_API.test_cases_results_info.power_switch_error_code
                        error_messages = NOS_API.test_cases_results_info.power_switch_error_message
                        ## Return DUT to initial state and de-initialize grabber device
                        NOS_API.deinitialize()
                        NOS_API.add_test_case_result_to_file_report(
                                test_result,
                                "- - - - - - - - - - - - - - - - - - - -",
                                "- - - - - - - - - - - - - - - - - - - -",
                                error_codes,
                                error_messages)
                    
                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        report_file = NOS_API.create_test_case_log_file(
                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                    NOS_API.test_cases_results_info.nos_sap_number,
                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                    end_time)
                        NOS_API.upload_file_report(report_file)
                        
                        NOS_API.send_report_over_mqtt_test_plan(
                            test_result,
                            end_time,
                            error_codes,
                            report_file)
                        
                        return
                    time.sleep(2)
                    NOS_API.display_custom_dialog("Pressione bot\xe3o 'Power' at\xe9 aparecer a pr\xf3xima pergunta", 1, ["Continuar"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG)
                    if not(NOS_API.power_on()):
                        TEST_CREATION_API.write_log_to_file("Comunication with PowerSwitch Fails")
                        ## Update test result
                        TEST_CREATION_API.update_test_result(test_result)
                        NOS_API.set_error_message("POWER SWITCH")
                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.power_switch_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.power_switch_error_message)
                        error_codes = NOS_API.test_cases_results_info.power_switch_error_code
                        error_messages = NOS_API.test_cases_results_info.power_switch_error_message
                        ## Return DUT to initial state and de-initialize grabber device
                        NOS_API.deinitialize()
                        NOS_API.add_test_case_result_to_file_report(
                                test_result,
                                "- - - - - - - - - - - - - - - - - - - -",
                                "- - - - - - - - - - - - - - - - - - - -",
                                error_codes,
                                error_messages)
                    
                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        report_file = NOS_API.create_test_case_log_file(
                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                    NOS_API.test_cases_results_info.nos_sap_number,
                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                    end_time)
                        NOS_API.upload_file_report(report_file)
                        
                        NOS_API.send_report_over_mqtt_test_plan(
                            test_result,
                            end_time,
                            error_codes,
                            report_file)
                        
                        return
                    if not(NOS_API.display_custom_dialog("A STB est\xe1 ligada?", 2, ["OK", "NOK"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "OK"):
                        TEST_CREATION_API.write_log_to_file("No Power")
                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.no_power_error_code \
                                                        + "; Error message: " + NOS_API.test_cases_results_info.no_power_error_message) 
                        NOS_API.set_error_message("Não Liga") 
                        error_codes =  NOS_API.test_cases_results_info.no_power_error_code
                        error_messages = NOS_API.test_cases_results_info.no_power_error_message
                        NOS_API.deinitialize()
                        
                        NOS_API.add_test_case_result_to_file_report(
                                test_result,
                                "- - - - - - - - - - - - - - - - - - - -",
                                "- - - - - - - - - - - - - - - - - - - -",
                                error_codes,
                                error_messages)
                    
                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        report_file = NOS_API.create_test_case_log_file(
                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                    NOS_API.test_cases_results_info.nos_sap_number,
                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                    end_time)
                        NOS_API.upload_file_report(report_file)
                        
                        NOS_API.send_report_over_mqtt_test_plan(
                            test_result,
                            end_time,
                            error_codes,
                            report_file)
                    
                    
                        return
                    Comparison = NOS_API.wait_for_multiple_pictures(["OTA_Setup_ref","OTA_Setup_ref1"], WAIT_OTA_TEST, ["[OTA_SETUP]","[OTA_SETUP]"], [NOS_API.thres,NOS_API.thres])
                    if(Comparison == -1):

                        TEST_CREATION_API.write_log_to_file("Doesn't upgrade")
                
                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.upgrade_nok_error_code \
                                                        + "; Error message: " + NOS_API.test_cases_results_info.upgrade_nok_error_message)                                        
                        NOS_API.set_error_message("Não Actualiza") 
                        error_codes =  NOS_API.test_cases_results_info.upgrade_nok_error_code
                        error_messages = NOS_API.test_cases_results_info.upgrade_nok_error_message                               
                        test_result = "FAIL"
                    elif(Comparison == -2):
                        NOS_API.grabber_stop_video_source()
                        time.sleep(1)
                        NOS_API.grabber_stop_audio_source()
                        time.sleep(1)
                        
                        ## Initialize input interfaces of DUT RT-AV101 device  
                        NOS_API.reset_dut()
                        #time.sleep(2)
        
                        ## Start grabber device with video on default video source
                        NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.CVBS2)
                        #time.sleep(5)
                        
                        if (NOS_API.is_signal_present_on_video_source()):
                            if not(NOS_API.grab_picture("SCART_video")):
                                TEST_CREATION_API.write_log_to_file("Image is not displayed on SCART")
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_scart_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.image_absence_scart_error_message)
                                NOS_API.set_error_message("Video SCART")
                                error_codes = NOS_API.test_cases_results_info.image_absence_scart_error_code
                                error_messages = NOS_API.test_cases_results_info.image_absence_scart_error_message
                                
                                NOS_API.add_test_case_result_to_file_report(
                                            test_result,
                                            "- - - - - - - - - - - - - - - - - - - -",
                                            "- - - - - - - - - - - - - - - - - - - -",
                                            error_codes,
                                            error_messages)
                
                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                report_file = NOS_API.create_test_case_log_file(
                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                NOS_API.test_cases_results_info.mac_using_barcode,
                                                end_time)
                            
                                NOS_API.upload_file_report(report_file)
                                NOS_API.test_cases_results_info.isTestOK = False
                                                        
                                NOS_API.send_report_over_mqtt_test_plan(
                                        test_result,
                                        end_time,
                                        error_codes,
                                        report_file)
                                        
                                ## Update test result
                                TEST_CREATION_API.update_test_result(test_result)
                                
                                ## Return DUT to initial state and de-initialize grabber device
                                NOS_API.deinitialize()
                                
                                return
                            NOS_API.display_custom_dialog("Confirme o cabo HDMI", 1, ["Continuar"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG)
                            NOS_API.grabber_stop_video_source()
                            time.sleep(1)
                            NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.HDMI1)
                            time.sleep(1)
                            Comparison = NOS_API.wait_for_multiple_pictures(["OTA_Setup_ref"], WAIT_OTA_TEST, ["[OTA_SETUP]"], [NOS_API.thres])   
                            TEST_CREATION_API.write_log_to_file(Comparison)
                            if(Comparison == -1):
                                TEST_CREATION_API.write_log_to_file("Doesn't upgrade")
                    
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.upgrade_nok_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.upgrade_nok_error_message)                                        
                                NOS_API.set_error_message("Não Actualiza") 
                                error_codes =  NOS_API.test_cases_results_info.upgrade_nok_error_code
                                error_messages = NOS_API.test_cases_results_info.upgrade_nok_error_message                               
                                test_result = "FAIL"
                            elif(Comparison == -2):
                                TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                NOS_API.set_error_message("Video HDMI(Não Retestar)")
                                error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                
                                NOS_API.add_test_case_result_to_file_report(
                                            test_result,
                                            "- - - - - - - - - - - - - - - - - - - -",
                                            "- - - - - - - - - - - - - - - - - - - -",
                                            error_codes,
                                            error_messages)
                
                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                report_file = NOS_API.create_test_case_log_file(
                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                NOS_API.test_cases_results_info.mac_using_barcode,
                                                end_time)
                            
                                NOS_API.upload_file_report(report_file)
                                NOS_API.test_cases_results_info.isTestOK = False
                                                        
                                NOS_API.send_report_over_mqtt_test_plan(
                                        test_result,
                                        end_time,
                                        error_codes,
                                        report_file)
                                        
                                ## Update test result
                                TEST_CREATION_API.update_test_result(test_result)
                                
                                ## Return DUT to initial state and de-initialize grabber device
                                NOS_API.deinitialize()
                                
                                return
                            elif(Comparison == 0):
                                time.sleep(1)
                                TEST_CREATION_API.send_ir_rc_command("[OK]")
                                time.sleep(4)
                                if(NOS_API.wait_for_no_signal_present(120)):
                                    NOS_API.test_cases_results_info.DidUpgrade = 1
                                    time.sleep(5)
                                    if(NOS_API.wait_for_signal_present(60)):
                                        boot_image = NOS_API.wait_for_multiple_pictures(["HDMI_video_1080_ref","HDMI_video_1080_ref1","HDMI_video_1080_ref2","Banner_1080_ref","No_Signal_ref","No_Signal_576_ref","No_Signal_720_ref"], 45, ["[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[BANNER_1080]","[NO_SIGNAL]","[NO_SIGNAL_576]","[NO_SIGNAL_720]"], [NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,60,NOS_API.thres])
                                        if ( boot_image == 0 or boot_image == 1 or boot_image == 2 or boot_image == 3):
                                            test_result = "PASS"
                                        elif(boot_image == 4 or boot_image == 5 or boot_image == 6):
                                            TEST_CREATION_API.send_ir_rc_command("[TV]")
                                            TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                                            boot_image = NOS_API.wait_for_multiple_pictures(["No_Signal_ref","No_Signal_576_ref","No_Signal_720_ref"], 5, ["[NO_SIGNAL]","[NO_SIGNAL_576]","[NO_SIGNAL_720]"], [NOS_API.thres,60,NOS_API.thres])
                                            if ( boot_image >= 0 and boot_image < 3):
                                                TEST_CREATION_API.send_ir_rc_command("[TV]")
                                                NOS_API.display_custom_dialog("Confirme o cabo RF", 1, ["Continuar"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG)
                                            boot_image = NOS_API.wait_for_multiple_pictures(["HDMI_video_1080_ref","HDMI_video_1080_ref1","HDMI_video_1080_ref2","Banner_1080_ref","No_Signal_ref"], 45, ["[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[BANNER_1080]","[NO_SIGNAL]"], [NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres])
                                            if ( boot_image == 0 or boot_image == 1 or boot_image == 2 or boot_image == 3):
                                                test_result = "PASS"
                                            elif(boot_image == 4):
                                                TEST_CREATION_API.write_log_to_file("Signal value is lower than threshold")                
                                                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.input_signal_error_code \
                                                                                    + "; Error message: " + NOS_API.test_cases_results_info.input_signal_error_message)
                                                NOS_API.set_error_message("Sem Sinal")
                                                error_codes = NOS_API.test_cases_results_info.input_signal_error_code
                                                error_messages = NOS_API.test_cases_results_info.input_signal_error_message
                                            elif(boot_image == -1):
                                                time.sleep(2)
                                                TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                                                boot_image = NOS_API.wait_for_multiple_pictures(["HDMI_video_1080_ref","HDMI_video_1080_ref1","HDMI_video_1080_ref2","Banner_1080_ref","No_Signal_ref","No_Signal_576_ref","No_Signal_720_ref"], 45, ["[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[BANNER_1080]","[NO_SIGNAL]","[NO_SIGNAL_576]","[NO_SIGNAL_720]"], [NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,60,NOS_API.thres])
                                                if ( boot_image == 0 or boot_image == 1 or boot_image == 2 or boot_image == 3):
                                                    test_result = "PASS"                                        
                                                elif(boot_image == 4 or boot_image == 5 or boot_image == 6):
                                                    TEST_CREATION_API.write_log_to_file("Signal value is lower than threshold")                
                                                    NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.input_signal_error_code \
                                                                                        + "; Error message: " + NOS_API.test_cases_results_info.input_signal_error_message)
                                                    NOS_API.set_error_message("Sem Sinal")
                                                    error_codes = NOS_API.test_cases_results_info.input_signal_error_code
                                                    error_messages = NOS_API.test_cases_results_info.input_signal_error_message
                                                elif(boot_image == -1):
                                                    TEST_CREATION_API.write_log_to_file("Image is not reproduced correctly on HDMI.")
                                                    NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_1080p_noise_error_code \
                                                                                        + "; Error message: " + NOS_API.test_cases_results_info.hdmi_1080p_noise_error_message)
                                                    error_codes = NOS_API.test_cases_results_info.hdmi_1080p_noise_error_code
                                                    error_messages = NOS_API.test_cases_results_info.hdmi_1080p_noise_error_message
                                                    NOS_API.set_error_message("Video HDMI")
                                                    
                                                    NOS_API.add_test_case_result_to_file_report(
                                                                test_result,
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                error_codes,
                                                                error_messages)
                                    
                                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                    report_file = NOS_API.create_test_case_log_file(
                                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                                                    end_time)
                                                
                                                    NOS_API.upload_file_report(report_file)
                                                    NOS_API.test_cases_results_info.isTestOK = False
                                                                            
                                                    NOS_API.send_report_over_mqtt_test_plan(
                                                            test_result,
                                                            end_time,
                                                            error_codes,
                                                            report_file)
                                                            
                                                    ## Update test result
                                                    TEST_CREATION_API.update_test_result(test_result)
                                                    
                                                    ## Return DUT to initial state and de-initialize grabber device
                                                    NOS_API.deinitialize()
                                                    
                                                    return                             
                                                elif(boot_image == -2):
                                                    TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                            + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                                    NOS_API.set_error_message("Reboot")
                                                    error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                                    error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                                    test_result = "FAIL"
                                                    
                                                    NOS_API.add_test_case_result_to_file_report(
                                                                    test_result,
                                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                                    error_codes,
                                                                    error_messages)
                                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                    report_file = ""
                                                    if (test_result != "PASS"):
                                                        report_file = NOS_API.create_test_case_log_file(
                                                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                        NOS_API.test_cases_results_info.nos_sap_number,
                                                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                                                        end_time)
                                                        NOS_API.upload_file_report(report_file)
                                                        NOS_API.test_cases_results_info.isTestOK = False
                                    
                                    
                                                    ## Update test result
                                                    TEST_CREATION_API.update_test_result(test_result)
                                                    
                                                    ## Return DUT to initial state and de-initialize grabber device
                                                    NOS_API.deinitialize()
                                                    
                                                    NOS_API.send_report_over_mqtt_test_plan(
                                                        test_result,
                                                        end_time,
                                                        error_codes,
                                                        report_file)
                                    
                                                    return                                       
                                            elif(boot_image == -2):
                                                TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                                NOS_API.set_error_message("Reboot")
                                                error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                                error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                                test_result = "FAIL"
                                                
                                                NOS_API.add_test_case_result_to_file_report(
                                                                test_result,
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                error_codes,
                                                                error_messages)
                                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                report_file = ""
                                                if (test_result != "PASS"):
                                                    report_file = NOS_API.create_test_case_log_file(
                                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                                                    end_time)
                                                    NOS_API.upload_file_report(report_file)
                                                    NOS_API.test_cases_results_info.isTestOK = False
                                
                                
                                                ## Update test result
                                                TEST_CREATION_API.update_test_result(test_result)
                                                
                                                ## Return DUT to initial state and de-initialize grabber device
                                                NOS_API.deinitialize()
                                                
                                                NOS_API.send_report_over_mqtt_test_plan(
                                                    test_result,
                                                    end_time,
                                                    error_codes,
                                                    report_file)
                                
                                                return
                                        elif(boot_image == -1):
                                            time.sleep(2)
                                            TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                                            boot_image = NOS_API.wait_for_multiple_pictures(["HDMI_video_1080_ref","HDMI_video_1080_ref1","HDMI_video_1080_ref2","Banner_1080_ref","No_Signal_ref","No_Signal_576_ref","No_Signal_720_ref"], 45, ["[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[BANNER_1080]","[NO_SIGNAL]","[NO_SIGNAL_576]","[NO_SIGNAL_720]"], [NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,60,NOS_API.thres])
                                            if ( boot_image == 0 or boot_image == 1 or boot_image == 2 or boot_image == 3):
                                                test_result = "PASS"    
                                            elif(boot_image == 4 or boot_image == 5 or boot_image == 6):
                                                TEST_CREATION_API.write_log_to_file("Signal value is lower than threshold")                
                                                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.input_signal_error_code \
                                                                                    + "; Error message: " + NOS_API.test_cases_results_info.input_signal_error_message)
                                                NOS_API.set_error_message("Sem Sinal")
                                                error_codes = NOS_API.test_cases_results_info.input_signal_error_code
                                                error_messages = NOS_API.test_cases_results_info.input_signal_error_message
                                            elif(boot_image == -1):
                                                TEST_CREATION_API.write_log_to_file("Image is not reproduced correctly on HDMI.")
                                                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_1080p_noise_error_code \
                                                                                    + "; Error message: " + NOS_API.test_cases_results_info.hdmi_1080p_noise_error_message)
                                                error_codes = NOS_API.test_cases_results_info.hdmi_1080p_noise_error_code
                                                error_messages = NOS_API.test_cases_results_info.hdmi_1080p_noise_error_message
                                                NOS_API.set_error_message("Video HDMI")
                                                
                                                NOS_API.add_test_case_result_to_file_report(
                                                            test_result,
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            error_codes,
                                                            error_messages)
                                
                                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                report_file = NOS_API.create_test_case_log_file(
                                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                NOS_API.test_cases_results_info.mac_using_barcode,
                                                                end_time)
                                            
                                                NOS_API.upload_file_report(report_file)
                                                NOS_API.test_cases_results_info.isTestOK = False
                                                                        
                                                NOS_API.send_report_over_mqtt_test_plan(
                                                        test_result,
                                                        end_time,
                                                        error_codes,
                                                        report_file)
                                                        
                                                ## Update test result
                                                TEST_CREATION_API.update_test_result(test_result)
                                                
                                                ## Return DUT to initial state and de-initialize grabber device
                                                NOS_API.deinitialize()
                                                
                                                return                                    
                                            elif(boot_image == -2):
                                                TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                                NOS_API.set_error_message("Reboot")
                                                error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                                error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                                test_result = "FAIL"
                                                
                                                NOS_API.add_test_case_result_to_file_report(
                                                                test_result,
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                error_codes,
                                                                error_messages)
                                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                report_file = ""
                                                if (test_result != "PASS"):
                                                    report_file = NOS_API.create_test_case_log_file(
                                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                                                    end_time)
                                                    NOS_API.upload_file_report(report_file)
                                                    NOS_API.test_cases_results_info.isTestOK = False
                                
                                
                                                ## Update test result
                                                TEST_CREATION_API.update_test_result(test_result)
                                                
                                                ## Return DUT to initial state and de-initialize grabber device
                                                NOS_API.deinitialize()
                                                
                                                NOS_API.send_report_over_mqtt_test_plan(
                                                    test_result,
                                                    end_time,
                                                    error_codes,
                                                    report_file)
                                
                                                return                                            
                                        elif(boot_image == -2):
                                            TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                            NOS_API.set_error_message("Reboot")
                                            error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                            error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                            test_result = "FAIL"
                                            
                                            NOS_API.add_test_case_result_to_file_report(
                                                            test_result,
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            error_codes,
                                                            error_messages)
                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                            report_file = ""
                                            if (test_result != "PASS"):
                                                report_file = NOS_API.create_test_case_log_file(
                                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                NOS_API.test_cases_results_info.mac_using_barcode,
                                                                end_time)
                                                NOS_API.upload_file_report(report_file)
                                                NOS_API.test_cases_results_info.isTestOK = False
                            
                            
                                            ## Update test result
                                            TEST_CREATION_API.update_test_result(test_result)
                                            
                                            ## Return DUT to initial state and de-initialize grabber device
                                            NOS_API.deinitialize()
                                            
                                            NOS_API.send_report_over_mqtt_test_plan(
                                                test_result,
                                                end_time,
                                                error_codes,
                                                report_file)
                            
                                            return                                            
                                    else:
                                        TEST_CREATION_API.send_ir_rc_command("[POWER]")
                                        time.sleep(4)
                                        if (NOS_API.is_signal_present_on_video_source()):
                                            boot_image = NOS_API.wait_for_multiple_pictures(["HDMI_video_1080_ref","HDMI_video_1080_ref1","HDMI_video_1080_ref2","Banner_1080_ref","No_Signal_ref","No_Signal_576_ref","No_Signal_720_ref"], 45, ["[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[BANNER_1080]","[NO_SIGNAL]","[NO_SIGNAL_576]","[NO_SIGNAL_720]"], [NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,60,NOS_API.thres])
                                            TEST_CREATION_API.write_log_to_file("boot image after power = " + str(boot_image))
                                            if ( boot_image == 0 or boot_image == 1 or boot_image == 2 or boot_image == 3):
                                                test_result = "PASS"
                                            elif(boot_image == 4 or boot_image == 5 or boot_image == 6):
                                                TEST_CREATION_API.send_ir_rc_command("[TV]")
                                                TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                                                boot_image = NOS_API.wait_for_multiple_pictures(["No_Signal_ref","No_Signal_576_ref","No_Signal_720_ref"], 5, ["[NO_SIGNAL]","[NO_SIGNAL_576]","[NO_SIGNAL_720]"], [NOS_API.thres,60,NOS_API.thres])
                                                if ( boot_image >= 0 and boot_image < 3):
                                                    TEST_CREATION_API.send_ir_rc_command("[TV]")
                                                    NOS_API.display_custom_dialog("Confirme o cabo RF", 1, ["Continuar"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG)
                                                boot_image = NOS_API.wait_for_multiple_pictures(["HDMI_video_1080_ref","HDMI_video_1080_ref1","HDMI_video_1080_ref2","Banner_1080_ref","No_Signal_ref","No_Signal_576_ref","No_Signal_720_ref"], 45, ["[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[BANNER_1080]","[NO_SIGNAL]","[NO_SIGNAL_576]","[NO_SIGNAL_720]"], [NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,60,NOS_API.thres])
                                                TEST_CREATION_API.write_log_to_file("boot image after rf = " + str(boot_image))
                                                if ( boot_image == 0 or boot_image == 1 or boot_image == 2 or boot_image == 3):
                                                    test_result = "PASS"   
                                                elif(boot_image == 4 or boot_image == 5 or boot_image == 6):
                                                    TEST_CREATION_API.write_log_to_file("Signal value is lower than threshold")                
                                                    NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.input_signal_error_code \
                                                                                        + "; Error message: " + NOS_API.test_cases_results_info.input_signal_error_message)
                                                    NOS_API.set_error_message("Sem Sinal")
                                                    error_codes = NOS_API.test_cases_results_info.input_signal_error_code
                                                    error_messages = NOS_API.test_cases_results_info.input_signal_error_message
                                                elif(boot_image == -1):
                                                    #time.sleep(2)
                                                    TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                                                    boot_image = NOS_API.wait_for_multiple_pictures(["HDMI_video_1080_ref","HDMI_video_1080_ref1","HDMI_video_1080_ref2","Banner_1080_ref","No_Signal_ref","No_Signal_576_ref","No_Signal_720_ref"], 45, ["[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[BANNER_1080]","[NO_SIGNAL]","[NO_SIGNAL_576]","[NO_SIGNAL_720]"], [NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,60,NOS_API.thres])
                                                    if ( boot_image == 0 or boot_image == 1 or boot_image == 2 or boot_image == 3):
                                                        test_result = "PASS"
                                                        
                                                    elif(boot_image == 4 or boot_image == 5 or boot_image == 6):
                                                        TEST_CREATION_API.write_log_to_file("Signal value is lower than threshold")                                            
                                                        NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.input_signal_error_code \
                                                                                            + "; Error message: " + NOS_API.test_cases_results_info.input_signal_error_message)
                                                        NOS_API.set_error_message("Sem Sinal")
                                                        error_codes = NOS_API.test_cases_results_info.input_signal_error_code
                                                        error_messages = NOS_API.test_cases_results_info.input_signal_error_message
                                                        
                                                    elif(boot_image == -1):
                                                        TEST_CREATION_API.write_log_to_file("Image is not reproduced correctly on HDMI.")
                                                        NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_1080p_noise_error_code \
                                                                                            + "; Error message: " + NOS_API.test_cases_results_info.hdmi_1080p_noise_error_message)
                                                        error_codes = NOS_API.test_cases_results_info.hdmi_1080p_noise_error_code
                                                        error_messages = NOS_API.test_cases_results_info.hdmi_1080p_noise_error_message
                                                        NOS_API.set_error_message("Video HDMI")
                                                        
                                                        NOS_API.add_test_case_result_to_file_report(
                                                                    test_result,
                                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                                    error_codes,
                                                                    error_messages)
                                        
                                                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                        report_file = NOS_API.create_test_case_log_file(
                                                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                        NOS_API.test_cases_results_info.nos_sap_number,
                                                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                                                        end_time)
                                                    
                                                        NOS_API.upload_file_report(report_file)
                                                        NOS_API.test_cases_results_info.isTestOK = False
                                                                                
                                                        NOS_API.send_report_over_mqtt_test_plan(
                                                                test_result,
                                                                end_time,
                                                                error_codes,
                                                                report_file)
                                                                
                                                        ## Update test result
                                                        TEST_CREATION_API.update_test_result(test_result)
                                                        
                                                        ## Return DUT to initial state and de-initialize grabber device
                                                        NOS_API.deinitialize()
                                                        
                                                        return                
                        
                                                    elif(boot_image == -2):
                                                        TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                                + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                                        NOS_API.set_error_message("Reboot")
                                                        error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                                        error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                                        test_result = "FAIL"
                                                        
                                                        NOS_API.add_test_case_result_to_file_report(
                                                                        test_result,
                                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                                        error_codes,
                                                                        error_messages)
                                                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                        report_file = ""
                                                        if (test_result != "PASS"):
                                                            report_file = NOS_API.create_test_case_log_file(
                                                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                            NOS_API.test_cases_results_info.nos_sap_number,
                                                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                                                            end_time)
                                                            NOS_API.upload_file_report(report_file)
                                                            NOS_API.test_cases_results_info.isTestOK = False
                                        
                                        
                                                        ## Update test result
                                                        TEST_CREATION_API.update_test_result(test_result)
                                                        
                                                        ## Return DUT to initial state and de-initialize grabber device
                                                        NOS_API.deinitialize()
                                                        
                                                        NOS_API.send_report_over_mqtt_test_plan(
                                                            test_result,
                                                            end_time,
                                                            error_codes,
                                                            report_file)
                                        
                                                        return
                                                elif(boot_image == -2):
                                                    TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                            + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                                    NOS_API.set_error_message("Reboot")
                                                    error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                                    error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                                    test_result = "FAIL"
                                                    
                                                    NOS_API.add_test_case_result_to_file_report(
                                                                    test_result,
                                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                                    error_codes,
                                                                    error_messages)
                                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                    report_file = ""
                                                    if (test_result != "PASS"):
                                                        report_file = NOS_API.create_test_case_log_file(
                                                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                        NOS_API.test_cases_results_info.nos_sap_number,
                                                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                                                        end_time)
                                                        NOS_API.upload_file_report(report_file)
                                                        NOS_API.test_cases_results_info.isTestOK = False
                                    
                                    
                                                    ## Update test result
                                                    TEST_CREATION_API.update_test_result(test_result)
                                                    
                                                    ## Return DUT to initial state and de-initialize grabber device
                                                    NOS_API.deinitialize()
                                                    
                                                    NOS_API.send_report_over_mqtt_test_plan(
                                                        test_result,
                                                        end_time,
                                                        error_codes,
                                                        report_file)
                                    
                                                    return                                                    
                                            elif(boot_image == -1):
                                                time.sleep(2)
                                                TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                                                boot_image = NOS_API.wait_for_multiple_pictures(["HDMI_video_1080_ref","HDMI_video_1080_ref1","HDMI_video_1080_ref2","Banner_1080_ref","No_Signal_ref","No_Signal_576_ref","No_Signal_720_ref"], 45, ["[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[BANNER_1080]","[NO_SIGNAL]","[NO_SIGNAL_576]","[NO_SIGNAL_720]"], [NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,60,NOS_API.thres])
                                                TEST_CREATION_API.write_log_to_file("boot image after not found = " + str(boot_image))
                                                if ( boot_image == 0 or boot_image == 1 or boot_image == 2 or boot_image == 3):
                                                    test_result = "PASS"
        
                                                elif(boot_image == -1):
                                                    TEST_CREATION_API.write_log_to_file("Image is not reproduced correctly on HDMI.")
                                                    NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_1080p_noise_error_code \
                                                                                        + "; Error message: " + NOS_API.test_cases_results_info.hdmi_1080p_noise_error_message)
                                                    error_codes = NOS_API.test_cases_results_info.hdmi_1080p_noise_error_code
                                                    error_messages = NOS_API.test_cases_results_info.hdmi_1080p_noise_error_message
                                                    NOS_API.set_error_message("Video HDMI")
                                                    
                                                    NOS_API.add_test_case_result_to_file_report(
                                                                test_result,
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                error_codes,
                                                                error_messages)
                                    
                                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                    report_file = NOS_API.create_test_case_log_file(
                                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                                                    end_time)
                                                
                                                    NOS_API.upload_file_report(report_file)
                                                    NOS_API.test_cases_results_info.isTestOK = False
                                                                            
                                                    NOS_API.send_report_over_mqtt_test_plan(
                                                            test_result,
                                                            end_time,
                                                            error_codes,
                                                            report_file)
                                                            
                                                    ## Update test result
                                                    TEST_CREATION_API.update_test_result(test_result)
                                                    
                                                    ## Return DUT to initial state and de-initialize grabber device
                                                    NOS_API.deinitialize()
                                                    
                                                    return                
                    
                                                elif(boot_image == -2):
                                                    TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                            + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                                    NOS_API.set_error_message("Reboot")
                                                    error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                                    error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                                    test_result = "FAIL"
                                                    
                                                    NOS_API.add_test_case_result_to_file_report(
                                                                    test_result,
                                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                                    error_codes,
                                                                    error_messages)
                                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                    report_file = ""
                                                    if (test_result != "PASS"):
                                                        report_file = NOS_API.create_test_case_log_file(
                                                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                        NOS_API.test_cases_results_info.nos_sap_number,
                                                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                                                        end_time)
                                                        NOS_API.upload_file_report(report_file)
                                                        NOS_API.test_cases_results_info.isTestOK = False
                                    
                                    
                                                    ## Update test result
                                                    TEST_CREATION_API.update_test_result(test_result)
                                                    
                                                    ## Return DUT to initial state and de-initialize grabber device
                                                    NOS_API.deinitialize()
                                                    
                                                    NOS_API.send_report_over_mqtt_test_plan(
                                                        test_result,
                                                        end_time,
                                                        error_codes,
                                                        report_file)
                                    
                                                    return
                                        
                                                elif(boot_image == 4 or boot_image == 5 or boot_image == 6):
                                                    TEST_CREATION_API.write_log_to_file("Signal value is lower than threshold")                                            
                                                    NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.input_signal_error_code \
                                                                                        + "; Error message: " + NOS_API.test_cases_results_info.input_signal_error_message)
                                                    NOS_API.set_error_message("Sem Sinal")
                                                    error_codes = NOS_API.test_cases_results_info.input_signal_error_code
                                                    error_messages = NOS_API.test_cases_results_info.input_signal_error_message                                            
                                            elif(boot_image == -2):
                                                TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                                NOS_API.set_error_message("Reboot")
                                                error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                                error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                                test_result = "FAIL"
                                                
                                                NOS_API.add_test_case_result_to_file_report(
                                                                test_result,
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                error_codes,
                                                                error_messages)
                                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                report_file = ""
                                                if (test_result != "PASS"):
                                                    report_file = NOS_API.create_test_case_log_file(
                                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                                                    end_time)
                                                    NOS_API.upload_file_report(report_file)
                                                    NOS_API.test_cases_results_info.isTestOK = False
                                
                                
                                                ## Update test result
                                                TEST_CREATION_API.update_test_result(test_result)
                                                
                                                ## Return DUT to initial state and de-initialize grabber device
                                                NOS_API.deinitialize()
                                                
                                                NOS_API.send_report_over_mqtt_test_plan(
                                                    test_result,
                                                    end_time,
                                                    error_codes,
                                                    report_file)
                                
                                                return                                                
                                        else:
                                            TEST_CREATION_API.write_log_to_file("No boot")
                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.no_boot_error_code \
                                                                                + "; Error message: " + NOS_API.test_cases_results_info.no_boot_error_message)
                                            NOS_API.set_error_message("Não arranca")
                                            error_codes =  NOS_API.test_cases_results_info.no_boot_error_code
                                            error_messages = NOS_API.test_cases_results_info.no_boot_error_message
                                            NOS_API.add_test_case_result_to_file_report(
                                                        test_result,
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        error_codes,
                                                        error_messages)
                            
                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                            report_file = NOS_API.create_test_case_log_file(
                                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                                            NOS_API.test_cases_results_info.nos_sap_number,
                                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                                            end_time)
                                        
                                            NOS_API.upload_file_report(report_file)
                                            NOS_API.test_cases_results_info.isTestOK = False
                                                                    
                                            NOS_API.send_report_over_mqtt_test_plan(
                                                    test_result,
                                                    end_time,
                                                    error_codes,
                                                    report_file)
                                                    
                                            ## Update test result
                                            TEST_CREATION_API.update_test_result(test_result)
                                            
                                            ## Return DUT to initial state and de-initialize grabber device
                                            NOS_API.deinitialize()
                                            
                                            return                                          
                        else:                       
                            TEST_CREATION_API.write_log_to_file("No boot")
                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.no_boot_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.no_boot_error_message)
                            NOS_API.set_error_message("Não arranca")
                            error_codes =  NOS_API.test_cases_results_info.no_boot_error_code
                            error_messages = NOS_API.test_cases_results_info.no_boot_error_message
                            NOS_API.add_test_case_result_to_file_report(
                                        test_result,
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        error_codes,
                                        error_messages)
            
                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                            report_file = NOS_API.create_test_case_log_file(
                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                            NOS_API.test_cases_results_info.nos_sap_number,
                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                            end_time)
                        
                            NOS_API.upload_file_report(report_file)
                            NOS_API.test_cases_results_info.isTestOK = False
                                                    
                            NOS_API.send_report_over_mqtt_test_plan(
                                    test_result,
                                    end_time,
                                    error_codes,
                                    report_file)
                                    
                            ## Update test result
                            TEST_CREATION_API.update_test_result(test_result)
                            
                            ## Return DUT to initial state and de-initialize grabber device
                            NOS_API.deinitialize()
                            
                            return                      
                    elif (Comparison == 0 or Comparison == 1):                   
                        time.sleep(1)
                        TEST_CREATION_API.send_ir_rc_command("[OK]")
                        time.sleep(2)
                        Comparison = NOS_API.wait_for_multiple_pictures(["OTA_Setup_ref","OTA_Setup_ref1"], 3, ["[OTA_SETUP]","[OTA_SETUP]"], [NOS_API.thres,NOS_API.thres])
                        if (Comparison == 0 or Comparison == 1):
                            TEST_CREATION_API.send_ir_rc_command("[OK]")
                        if(NOS_API.wait_for_no_signal_present(120)):
                            NOS_API.test_cases_results_info.DidUpgrade = 1
                            time.sleep(5)
                            if(NOS_API.wait_for_signal_present(60)):
                                TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                                boot_image = NOS_API.wait_for_multiple_pictures(["HDMI_video_1080_ref","HDMI_video_1080_ref1","HDMI_video_1080_ref2","HDMI_video_ref","HDMI_video_ref1","HDMI_video_ref2","Banner_1080_ref","HDMI_video_576_ref","No_Signal_ref","No_Signal_576_ref","No_Signal_720_ref"], 45, ["[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[HALF_SCREEN_720p]","[HALF_SCREEN_720p]","[HALF_SCREEN_720p]","[BANNER_1080]","[HALF_SCREEN_576p]","[NO_SIGNAL]","[NO_SIGNAL_576]","[NO_SIGNAL_720]"], [NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,60,NOS_API.thres,60,NOS_API.thres])
                                if ( boot_image >= 0 and boot_image <= 7):
                                    if(boot_image == 3 or boot_image == 4 or boot_image == 5):
                                        NOS_API.SET_720 = True
                                    if(boot_image == 7):
                                        NOS_API.SET_576 = True
                                    test_result = "PASS"
                                elif(boot_image >= 8 and boot_image <= 10):
                                    TEST_CREATION_API.send_ir_rc_command("[TV]")
                                    TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                                    boot_image = NOS_API.wait_for_multiple_pictures(["No_Signal_ref","No_Signal_576_ref","No_Signal_720_ref"], 5, ["[NO_SIGNAL]","[NO_SIGNAL_576]","[NO_SIGNAL_720]"], [NOS_API.thres,60,NOS_API.thres])
                                    if ( boot_image >= 0 and boot_image < 3):
                                        TEST_CREATION_API.send_ir_rc_command("[TV]")
                                        NOS_API.display_custom_dialog("Confirme o cabo RF", 1, ["Continuar"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG)
                                #  boot_image = NOS_API.wait_for_multiple_pictures(["HDMI_video_1080_ref","HDMI_video_1080_ref1","Banner_1080_ref","No_Signal_ref"], 45, ["[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[BANNER_1080]","[NO_SIGNAL]"], [HDMI_threshold,HDMI_threshold,HDMI_threshold,HDMI_threshold])
                                    boot_image = NOS_API.wait_for_multiple_pictures(["HDMI_video_1080_ref","HDMI_video_1080_ref1","HDMI_video_1080_ref2","HDMI_video_ref","HDMI_video_ref1","HDMI_video_ref2","Banner_1080_ref","HDMI_video_576_ref","No_Signal_ref","No_Signal_576_ref","No_Signal_720_ref"], 45, ["[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[HALF_SCREEN_720p]","[HALF_SCREEN_720p]","[HALF_SCREEN_720p]","[BANNER_1080]","[HALF_SCREEN_576p]","[NO_SIGNAL]","[NO_SIGNAL_576]","[NO_SIGNAL_720]"], [NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,60,NOS_API.thres,60,NOS_API.thres])
                                    if ( boot_image >= 0 and boot_image <= 7):
                                        if(boot_image == 3 or boot_image == 4 or boot_image == 5):
                                            NOS_API.SET_720 = True
                                        if(boot_image == 7):
                                            NOS_API.SET_576 = True
                                        test_result = "PASS"
                                    elif(boot_image >= 8 and boot_image <= 10):
                                        TEST_CREATION_API.write_log_to_file("Signal value is lower than threshold")                
                                        NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.input_signal_error_code \
                                                                            + "; Error message: " + NOS_API.test_cases_results_info.input_signal_error_message)
                                        NOS_API.set_error_message("Sem Sinal")
                                        error_codes = NOS_API.test_cases_results_info.input_signal_error_code
                                        error_messages = NOS_API.test_cases_results_info.input_signal_error_message
                                        time.sleep(2)
                                    elif(boot_image == -1):
                                        time.sleep(2)
                                        TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                                        boot_image = NOS_API.wait_for_multiple_pictures(["HDMI_video_1080_ref","HDMI_video_1080_ref1","HDMI_video_1080_ref2","HDMI_video_ref","HDMI_video_ref1","HDMI_video_ref2","Banner_1080_ref","HDMI_video_576_ref","No_Signal_ref","No_Signal_576_ref","No_Signal_720_ref"], 45, ["[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[HALF_SCREEN_720p]","[HALF_SCREEN_720p]","[HALF_SCREEN_720p]","[BANNER_1080]","[HALF_SCREEN_576p]","[NO_SIGNAL]","[NO_SIGNAL_576]","[NO_SIGNAL_720]"], [NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,60,NOS_API.thres,60,NOS_API.thres])
                                        if ( boot_image >= 0 and boot_image <= 7):
                                            if(boot_image == 3 or boot_image == 4 or boot_image == 5):
                                                NOS_API.SET_720 = True
                                            if(boot_image == 7):
                                                NOS_API.SET_576 = True
                                            test_result = "PASS"
                                        elif(boot_image == -1):
                                            TEST_CREATION_API.write_log_to_file("Image is not reproduced correctly on HDMI.")
                                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_1080p_noise_error_code \
                                                                                + "; Error message: " + NOS_API.test_cases_results_info.hdmi_1080p_noise_error_message)
                                            error_codes = NOS_API.test_cases_results_info.hdmi_1080p_noise_error_code
                                            error_messages = NOS_API.test_cases_results_info.hdmi_1080p_noise_error_message
                                            NOS_API.set_error_message("Video HDMI")
                                            
                                            NOS_API.add_test_case_result_to_file_report(
                                                        test_result,
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        error_codes,
                                                        error_messages)
                            
                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                            report_file = NOS_API.create_test_case_log_file(
                                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                                            NOS_API.test_cases_results_info.nos_sap_number,
                                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                                            end_time)
                                        
                                            NOS_API.upload_file_report(report_file)
                                            NOS_API.test_cases_results_info.isTestOK = False
                                                                    
                                            NOS_API.send_report_over_mqtt_test_plan(
                                                    test_result,
                                                    end_time,
                                                    error_codes,
                                                    report_file)
                                                    
                                            ## Update test result
                                            TEST_CREATION_API.update_test_result(test_result)
                                            
                                            ## Return DUT to initial state and de-initialize grabber device
                                            NOS_API.deinitialize()
                                            
                                            return                            
                                        elif(boot_image == -2):
                                            TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                            NOS_API.set_error_message("Reboot")
                                            error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                            error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                            test_result = "FAIL"
                                            
                                            NOS_API.add_test_case_result_to_file_report(
                                                            test_result,
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            error_codes,
                                                            error_messages)
                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                            report_file = ""
                                            if (test_result != "PASS"):
                                                report_file = NOS_API.create_test_case_log_file(
                                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                NOS_API.test_cases_results_info.mac_using_barcode,
                                                                end_time)
                                                NOS_API.upload_file_report(report_file)
                                                NOS_API.test_cases_results_info.isTestOK = False
                            
                            
                                            ## Update test result
                                            TEST_CREATION_API.update_test_result(test_result)
                                            
                                            ## Return DUT to initial state and de-initialize grabber device
                                            NOS_API.deinitialize()
                                            
                                            NOS_API.send_report_over_mqtt_test_plan(
                                                test_result,
                                                end_time,
                                                error_codes,
                                                report_file)
                            
                                            return                                
                                    elif(boot_image == -2):
                                        TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                        NOS_API.set_error_message("Reboot")
                                        error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                        error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                        test_result = "FAIL"
                                        
                                        NOS_API.add_test_case_result_to_file_report(
                                                        test_result,
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        error_codes,
                                                        error_messages)
                                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                        report_file = ""
                                        if (test_result != "PASS"):
                                            report_file = NOS_API.create_test_case_log_file(
                                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                                            NOS_API.test_cases_results_info.nos_sap_number,
                                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                                            end_time)
                                            NOS_API.upload_file_report(report_file)
                                            NOS_API.test_cases_results_info.isTestOK = False
                        
                        
                                        ## Update test result
                                        TEST_CREATION_API.update_test_result(test_result)
                                        
                                        ## Return DUT to initial state and de-initialize grabber device
                                        NOS_API.deinitialize()
                                        
                                        NOS_API.send_report_over_mqtt_test_plan(
                                            test_result,
                                            end_time,
                                            error_codes,
                                            report_file)
                        
                                        return                                   
                                elif(boot_image == -1):
                                        time.sleep(2)
                                        TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                                        boot_image = NOS_API.wait_for_multiple_pictures(["HDMI_video_1080_ref","HDMI_video_1080_ref1","HDMI_video_1080_ref2","HDMI_video_ref","HDMI_video_ref1","HDMI_video_ref2","Banner_1080_ref","HDMI_video_576_ref","No_Signal_ref","No_Signal_576_ref","No_Signal_720_ref"], 45, ["[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[HALF_SCREEN_720p]","[HALF_SCREEN_720p]","[HALF_SCREEN_720p]","[BANNER_1080]","[HALF_SCREEN_576p]","[NO_SIGNAL]","[NO_SIGNAL_576]","[NO_SIGNAL_720]"], [NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,60,NOS_API.thres,60,NOS_API.thres])
                                        if ( boot_image >= 0 and boot_image <= 7):
                                            if(boot_image == 3 or boot_image == 4 or boot_image == 5):
                                                NOS_API.SET_720 = True
                                            if(boot_image == 7):
                                                NOS_API.SET_576 = True
                                            test_result = "PASS"
                                        elif(boot_image >= 8 and boot_image <= 10):
                                                #perguntar e verificar Lemos
                                            time.sleep(2)
                                        elif(boot_image == -1):
                                            TEST_CREATION_API.write_log_to_file("Image is not reproduced correctly on HDMI.")
                                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_1080p_noise_error_code \
                                                                                + "; Error message: " + NOS_API.test_cases_results_info.hdmi_1080p_noise_error_message)
                                            error_codes = NOS_API.test_cases_results_info.hdmi_1080p_noise_error_code
                                            error_messages = NOS_API.test_cases_results_info.hdmi_1080p_noise_error_message
                                            NOS_API.set_error_message("Video HDMI")
                                            
                                            NOS_API.add_test_case_result_to_file_report(
                                                        test_result,
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        error_codes,
                                                        error_messages)
                            
                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                            report_file = NOS_API.create_test_case_log_file(
                                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                                            NOS_API.test_cases_results_info.nos_sap_number,
                                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                                            end_time)
                                        
                                            NOS_API.upload_file_report(report_file)
                                            NOS_API.test_cases_results_info.isTestOK = False
                                                                    
                                            NOS_API.send_report_over_mqtt_test_plan(
                                                    test_result,
                                                    end_time,
                                                    error_codes,
                                                    report_file)
                                                    
                                            ## Update test result
                                            TEST_CREATION_API.update_test_result(test_result)
                                            
                                            ## Return DUT to initial state and de-initialize grabber device
                                            NOS_API.deinitialize()
                                            
                                            return                           
                                        elif(boot_image == -2):
                                            TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                            NOS_API.set_error_message("Reboot")
                                            error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                            error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                            test_result = "FAIL"
                                            
                                            NOS_API.add_test_case_result_to_file_report(
                                                            test_result,
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            error_codes,
                                                            error_messages)
                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                            report_file = ""
                                            if (test_result != "PASS"):
                                                report_file = NOS_API.create_test_case_log_file(
                                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                NOS_API.test_cases_results_info.mac_using_barcode,
                                                                end_time)
                                                NOS_API.upload_file_report(report_file)
                                                NOS_API.test_cases_results_info.isTestOK = False
                            
                            
                                            ## Update test result
                                            TEST_CREATION_API.update_test_result(test_result)
                                            
                                            ## Return DUT to initial state and de-initialize grabber device
                                            NOS_API.deinitialize()
                                            
                                            NOS_API.send_report_over_mqtt_test_plan(
                                                test_result,
                                                end_time,
                                                error_codes,
                                                report_file)
                            
                                            return                                   
                                elif(boot_image == -2):                                                                                                                                               
                                    TEST_CREATION_API.send_ir_rc_command("[POWER]")
                                    time.sleep(4)
                                    if (NOS_API.is_signal_present_on_video_source()):
                                        TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                                        boot_image = NOS_API.wait_for_multiple_pictures(["HDMI_video_1080_ref","HDMI_video_1080_ref1","HDMI_video_1080_ref2","HDMI_video_ref","HDMI_video_ref1","HDMI_video_ref2","Banner_1080_ref","HDMI_video_576_ref","No_Signal_ref","No_Signal_576_ref","No_Signal_720_ref"], 45, ["[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[HALF_SCREEN_720p]","[HALF_SCREEN_720p]","[HALF_SCREEN_720p]","[BANNER_1080]","[HALF_SCREEN_576p]","[NO_SIGNAL]","[NO_SIGNAL_576]","[NO_SIGNAL_720]"], [NOS_API.thres,HDMI_threshold,HDMI_threshold,HDMI_threshold,HDMI_threshold,HDMI_threshold,HDMI_threshold,60,NOS_API.thres,60,NOS_API.thres])
                                        if ( boot_image >= 0 and boot_image <= 7):
                                            if(boot_image == 3 or boot_image == 4 or boot_image == 5):
                                                NOS_API.SET_720 = True
                                            if(boot_image == 7):
                                                NOS_API.SET_576 = True
                                            test_result = "PASS"
                                        elif(boot_image >= 8 and boot_image <= 10):
                                            TEST_CREATION_API.send_ir_rc_command("[TV]")
                                            TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                                            boot_image = NOS_API.wait_for_multiple_pictures(["No_Signal_ref","No_Signal_576_ref","No_Signal_720_ref"], 5, ["[NO_SIGNAL]","[NO_SIGNAL_576]","[NO_SIGNAL_720]"], [NOS_API.thres,60,NOS_API.thres])
                                            if ( boot_image >= 0 and boot_image < 3):
                                                TEST_CREATION_API.send_ir_rc_command("[TV]")
                                                NOS_API.display_custom_dialog("Confirme o cabo RF", 1, ["Continuar"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG)
                                            boot_image = NOS_API.wait_for_multiple_pictures(["HDMI_video_1080_ref","HDMI_video_1080_ref1","HDMI_video_1080_ref2","HDMI_video_ref","HDMI_video_ref1","HDMI_video_ref2","Banner_1080_ref","HDMI_video_576_ref","No_Signal_ref","No_Signal_576_ref","No_Signal_720_ref"], 45, ["[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[HALF_SCREEN_720p]","[HALF_SCREEN_720p]","[HALF_SCREEN_720p]","[BANNER_1080]","[HALF_SCREEN_576p]","[NO_SIGNAL]","[NO_SIGNAL_576]","[NO_SIGNAL_720]"], [NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,60,NOS_API.thres,60,NOS_API.thres])
                                            if ( boot_image >= 0 and boot_image <= 7):
                                                if(boot_image == 3 or boot_image == 4 or boot_image == 5):
                                                    NOS_API.SET_720 = True
                                                if(boot_image == 7):
                                                    NOS_API.SET_576 = True
                                                test_result = "PASS"
                                            elif(boot_image == 3):
                                                TEST_CREATION_API.write_log_to_file("Signal value is lower than threshold")                
                                                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.input_signal_error_code \
                                                                                    + "; Error message: " + NOS_API.test_cases_results_info.input_signal_error_message)
                                                NOS_API.set_error_message("Sem Sinal")
                                                error_codes = NOS_API.test_cases_results_info.input_signal_error_code
                                                error_messages = NOS_API.test_cases_results_info.input_signal_error_message
                                            elif(boot_image == -1):
                                                #time.sleep(2)
                                                TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                                                boot_image = NOS_API.wait_for_multiple_pictures(["HDMI_video_1080_ref","HDMI_video_1080_ref1","HDMI_video_1080_ref2","HDMI_video_ref","HDMI_video_ref1","HDMI_video_ref2","Banner_1080_ref","HDMI_video_576_ref","No_Signal_ref","No_Signal_576_ref","No_Signal_720_ref"], 45, ["[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[HALF_SCREEN_720p]","[HALF_SCREEN_720p]","[HALF_SCREEN_720p]","[BANNER_1080]","[HALF_SCREEN_576p]","[NO_SIGNAL]","[NO_SIGNAL_576]","[NO_SIGNAL_720]"], [NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,60,NOS_API.thres,60,NOS_API.thres])
                                                if ( boot_image >= 0 and boot_image <= 7):
                                                    if(boot_image == 3 or boot_image == 4 or boot_image == 5):
                                                        NOS_API.SET_720 = True
                                                    if(boot_image == 7):
                                                        NOS_API.SET_576 = True
                                                    test_result = "PASS"
                                                elif(boot_image == -1):
                                                    TEST_CREATION_API.write_log_to_file("Image is not reproduced correctly on HDMI.")
                                                    NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_1080p_noise_error_code \
                                                                                        + "; Error message: " + NOS_API.test_cases_results_info.hdmi_1080p_noise_error_message)
                                                    error_codes = NOS_API.test_cases_results_info.hdmi_1080p_noise_error_code
                                                    error_messages = NOS_API.test_cases_results_info.hdmi_1080p_noise_error_message
                                                    NOS_API.set_error_message("Video HDMI")
                                                    
                                                    NOS_API.add_test_case_result_to_file_report(
                                                                test_result,
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                error_codes,
                                                                error_messages)
                                    
                                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                    report_file = NOS_API.create_test_case_log_file(
                                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                                                    end_time)
                                                
                                                    NOS_API.upload_file_report(report_file)
                                                    NOS_API.test_cases_results_info.isTestOK = False
                                                                            
                                                    NOS_API.send_report_over_mqtt_test_plan(
                                                            test_result,
                                                            end_time,
                                                            error_codes,
                                                            report_file)
                                                            
                                                    ## Update test result
                                                    TEST_CREATION_API.update_test_result(test_result)
                                                    
                                                    ## Return DUT to initial state and de-initialize grabber device
                                                    NOS_API.deinitialize()
                                                    
                                                    return                
                    
                                                elif(boot_image == -2):
                                                    TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                            + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                                    NOS_API.set_error_message("Reboot")
                                                    error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                                    error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                                    test_result = "FAIL"
                                                    
                                                    NOS_API.add_test_case_result_to_file_report(
                                                                    test_result,
                                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                                    error_codes,
                                                                    error_messages)
                                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                    report_file = ""
                                                    if (test_result != "PASS"):
                                                        report_file = NOS_API.create_test_case_log_file(
                                                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                        NOS_API.test_cases_results_info.nos_sap_number,
                                                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                                                        end_time)
                                                        NOS_API.upload_file_report(report_file)
                                                        NOS_API.test_cases_results_info.isTestOK = False
                                    
                                    
                                                    ## Update test result
                                                    TEST_CREATION_API.update_test_result(test_result)
                                                    
                                                    ## Return DUT to initial state and de-initialize grabber device
                                                    NOS_API.deinitialize()
                                                    
                                                    NOS_API.send_report_over_mqtt_test_plan(
                                                        test_result,
                                                        end_time,
                                                        error_codes,
                                                        report_file)
                                    
                                                    return
                                            elif(boot_image == -2):
                                                TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                                NOS_API.set_error_message("Reboot")
                                                error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                                error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                                test_result = "FAIL"
                                                
                                                NOS_API.add_test_case_result_to_file_report(
                                                                test_result,
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                error_codes,
                                                                error_messages)
                                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                report_file = ""
                                                if (test_result != "PASS"):
                                                    report_file = NOS_API.create_test_case_log_file(
                                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                                                    end_time)
                                                    NOS_API.upload_file_report(report_file)
                                                    NOS_API.test_cases_results_info.isTestOK = False
                                
                                
                                                ## Update test result
                                                TEST_CREATION_API.update_test_result(test_result)
                                                
                                                ## Return DUT to initial state and de-initialize grabber device
                                                NOS_API.deinitialize()
                                                
                                                NOS_API.send_report_over_mqtt_test_plan(
                                                    test_result,
                                                    end_time,
                                                    error_codes,
                                                    report_file)
                                
                                                return
                                            elif(boot_image >= 7 and boot_image <= 9):
                                                TEST_CREATION_API.write_log_to_file("Signal value is lower than threshold")                
                                                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.input_signal_error_code \
                                                                                    + "; Error message: " + NOS_API.test_cases_results_info.input_signal_error_message)
                                                NOS_API.set_error_message("Sem Sinal")
                                                error_codes = NOS_API.test_cases_results_info.input_signal_error_code
                                                error_messages = NOS_API.test_cases_results_info.input_signal_error_message
                                                time.sleep(2)                                               
                                        elif(boot_image == -1):
                                            time.sleep(2)
                                            TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                                            boot_image = NOS_API.wait_for_multiple_pictures(["HDMI_video_1080_ref","HDMI_video_1080_ref1","HDMI_video_1080_ref2","HDMI_video_ref","HDMI_video_ref1","HDMI_video_ref2","Banner_1080_ref","HDMI_video_576_ref","No_Signal_ref","No_Signal_576_ref","No_Signal_720_ref"], 45, ["[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[HALF_SCREEN_720p]","[HALF_SCREEN_720p]","[HALF_SCREEN_720p]","[BANNER_1080]","[HALF_SCREEN_576p]","[NO_SIGNAL]","[NO_SIGNAL_576]","[NO_SIGNAL_720]"], [NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,60,NOS_API.thres,60,NOS_API.thres])
                                            if ( boot_image >= 0 and boot_image <= 7):
                                                if(boot_image == 3 or boot_image == 4 or boot_image == 5):
                                                    NOS_API.SET_720 = True
                                                if(boot_image == 7):
                                                    NOS_API.SET_576 = True
                                                test_result = "PASS"
                                            elif(boot_image >= 8 and boot_image <= 10):
                                                #perguntar e verificar Lemos
                                                time.sleep(2)
                                            elif(boot_image == -1):
                                                TEST_CREATION_API.write_log_to_file("Image is not reproduced correctly on HDMI.")
                                                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_1080p_noise_error_code \
                                                                                    + "; Error message: " + NOS_API.test_cases_results_info.hdmi_1080p_noise_error_message)
                                                error_codes = NOS_API.test_cases_results_info.hdmi_1080p_noise_error_code
                                                error_messages = NOS_API.test_cases_results_info.hdmi_1080p_noise_error_message
                                                NOS_API.set_error_message("Video HDMI")
                                                
                                                NOS_API.add_test_case_result_to_file_report(
                                                            test_result,
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            error_codes,
                                                            error_messages)
                                
                                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                report_file = NOS_API.create_test_case_log_file(
                                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                NOS_API.test_cases_results_info.mac_using_barcode,
                                                                end_time)
                                            
                                                NOS_API.upload_file_report(report_file)
                                                NOS_API.test_cases_results_info.isTestOK = False
                                                                        
                                                NOS_API.send_report_over_mqtt_test_plan(
                                                        test_result,
                                                        end_time,
                                                        error_codes,
                                                        report_file)
                                                        
                                                ## Update test result
                                                TEST_CREATION_API.update_test_result(test_result)
                                                
                                                ## Return DUT to initial state and de-initialize grabber device
                                                NOS_API.deinitialize()
                                                
                                                return                                
                                            elif(boot_image == -2):
                                                TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                                NOS_API.set_error_message("Reboot")
                                                error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                                error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                                test_result = "FAIL"
                                                
                                                NOS_API.add_test_case_result_to_file_report(
                                                                test_result,
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                error_codes,
                                                                error_messages)
                                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                report_file = ""
                                                if (test_result != "PASS"):
                                                    report_file = NOS_API.create_test_case_log_file(
                                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                                                    end_time)
                                                    NOS_API.upload_file_report(report_file)
                                                    NOS_API.test_cases_results_info.isTestOK = False
                                
                                
                                                ## Update test result
                                                TEST_CREATION_API.update_test_result(test_result)
                                                
                                                ## Return DUT to initial state and de-initialize grabber device
                                                NOS_API.deinitialize()
                                                
                                                NOS_API.send_report_over_mqtt_test_plan(
                                                    test_result,
                                                    end_time,
                                                    error_codes,
                                                    report_file)
                                
                                                return                                  
                                        elif(boot_image == -2):
                                            TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                            NOS_API.set_error_message("Reboot")
                                            error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                            error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                            test_result = "FAIL"
                                            
                                            NOS_API.add_test_case_result_to_file_report(
                                                            test_result,
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            error_codes,
                                                            error_messages)
                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                            report_file = ""
                                            if (test_result != "PASS"):
                                                report_file = NOS_API.create_test_case_log_file(
                                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                NOS_API.test_cases_results_info.mac_using_barcode,
                                                                end_time)
                                                NOS_API.upload_file_report(report_file)
                                                NOS_API.test_cases_results_info.isTestOK = False
                            
                            
                                            ## Update test result
                                            TEST_CREATION_API.update_test_result(test_result)
                                            
                                            ## Return DUT to initial state and de-initialize grabber device
                                            NOS_API.deinitialize()
                                            
                                            NOS_API.send_report_over_mqtt_test_plan(
                                                test_result,
                                                end_time,
                                                error_codes,
                                                report_file)
                            
                                            return                                           
                                    else:
                                        TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                        NOS_API.set_error_message("Reboot")
                                        error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                        error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                        test_result = "FAIL"
                                        
                                        NOS_API.add_test_case_result_to_file_report(
                                                        test_result,
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        error_codes,
                                                        error_messages)
                                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                        report_file = ""
                                        if (test_result != "PASS"):
                                            report_file = NOS_API.create_test_case_log_file(
                                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                                            NOS_API.test_cases_results_info.nos_sap_number,
                                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                                            end_time)
                                            NOS_API.upload_file_report(report_file)
                                            NOS_API.test_cases_results_info.isTestOK = False
                        
                        
                                        ## Update test result
                                        TEST_CREATION_API.update_test_result(test_result)
                                        
                                        ## Return DUT to initial state and de-initialize grabber device
                                        NOS_API.deinitialize()
                                        
                                        NOS_API.send_report_over_mqtt_test_plan(
                                            test_result,
                                            end_time,
                                            error_codes,
                                            report_file)
                        
                                        return        
                            else:
                                TEST_CREATION_API.send_ir_rc_command("[POWER]")
                                time.sleep(4)
                                if (NOS_API.is_signal_present_on_video_source()):
                                    TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                                    boot_image = NOS_API.wait_for_multiple_pictures(["HDMI_video_1080_ref","HDMI_video_1080_ref1","HDMI_video_1080_ref2","HDMI_video_ref","HDMI_video_ref1","HDMI_video_ref2","Banner_1080_ref","HDMI_video_576_ref","No_Signal_ref","No_Signal_576_ref","No_Signal_720_ref"], 45, ["[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[HALF_SCREEN_720p]","[HALF_SCREEN_720p]","[HALF_SCREEN_720p]","[BANNER_1080]","[HALF_SCREEN_576p]","[NO_SIGNAL]","[NO_SIGNAL_576]","[NO_SIGNAL_720]"], [NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,60,NOS_API.thres,60,NOS_API.thres])
                                    if ( boot_image >= 0 and boot_image <= 7):
                                        if(boot_image == 3 or boot_image == 4 or boot_image == 5):
                                            NOS_API.SET_720 = True
                                        if(boot_image == 7):
                                            NOS_API.SET_576 = True
                                        test_result = "PASS"
                                    elif(boot_image >= 8 and boot_image <= 10):
                                        TEST_CREATION_API.send_ir_rc_command("[TV]")
                                        TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                                        boot_image = NOS_API.wait_for_multiple_pictures(["No_Signal_ref","No_Signal_576_ref","No_Signal_720_ref"], 5, ["[NO_SIGNAL]","[NO_SIGNAL_576]","[NO_SIGNAL_720]"], [NOS_API.thres,60,NOS_API.thres])
                                        if ( boot_image >= 0 and boot_image < 3):
                                            TEST_CREATION_API.send_ir_rc_command("[TV]")
                                            NOS_API.display_custom_dialog("Confirme o cabo RF", 1, ["Continuar"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG)
                                        boot_image = NOS_API.wait_for_multiple_pictures(["HDMI_video_1080_ref","HDMI_video_1080_ref1","HDMI_video_1080_ref2","HDMI_video_ref","HDMI_video_ref1","HDMI_video_ref2","Banner_1080_ref","HDMI_video_576_ref","No_Signal_ref","No_Signal_576_ref","No_Signal_720_ref"], 45, ["[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[HALF_SCREEN_720p]","[HALF_SCREEN_720p]","[HALF_SCREEN_720p]","[BANNER_1080]","[HALF_SCREEN_576p]","[NO_SIGNAL]","[NO_SIGNAL_576]","[NO_SIGNAL_720]"], [NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,60,NOS_API.thres,60,NOS_API.thres])
                                        if ( boot_image >= 0 and boot_image <= 7):
                                            if(boot_image == 3 or boot_image == 4 or boot_image == 5):
                                                NOS_API.SET_720 = True
                                            if(boot_image == 7):
                                                NOS_API.SET_576 = True
                                            test_result = "PASS"
                                        elif(boot_image >= 8 and boot_image <= 10):
                                            TEST_CREATION_API.write_log_to_file("Signal value is lower than threshold")
                        
                                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.input_signal_error_code \
                                                                                + "; Error message: " + NOS_API.test_cases_results_info.input_signal_error_message)
                                            NOS_API.set_error_message("Sem Sinal")
                                            error_codes = NOS_API.test_cases_results_info.input_signal_error_code
                                            error_messages = NOS_API.test_cases_results_info.input_signal_error_message
                                        elif(boot_image == -1):
                                            #time.sleep(2)
                                            TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                                            boot_image = NOS_API.wait_for_multiple_pictures(["HDMI_video_1080_ref","HDMI_video_1080_ref1","HDMI_video_1080_ref2","HDMI_video_ref","HDMI_video_ref1","HDMI_video_ref2","Banner_1080_ref","HDMI_video_576_ref","No_Signal_ref","No_Signal_576_ref","No_Signal_720_ref"], 45, ["[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[HALF_SCREEN_720p]","[HALF_SCREEN_720p]","[HALF_SCREEN_720p]","[BANNER_1080]","[HALF_SCREEN_576p]","[NO_SIGNAL]","[NO_SIGNAL_576]","[NO_SIGNAL_720]"], [NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,60,NOS_API.thres,60,NOS_API.thres])
                                            if ( boot_image >= 0 and boot_image <= 7):
                                                if(boot_image == 3 or boot_image == 4 or boot_image == 5):
                                                    NOS_API.SET_720 = True
                                                if(boot_image == 7):
                                                    NOS_API.SET_576 = True
                                                test_result = "PASS"
                                            elif(boot_image == -1):
                                                TEST_CREATION_API.write_log_to_file("Image is not reproduced correctly on HDMI.")
                                                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_1080p_noise_error_code \
                                                                                    + "; Error message: " + NOS_API.test_cases_results_info.hdmi_1080p_noise_error_message)
                                                error_codes = NOS_API.test_cases_results_info.hdmi_1080p_noise_error_code
                                                error_messages = NOS_API.test_cases_results_info.hdmi_1080p_noise_error_message
                                                NOS_API.set_error_message("Video HDMI")
                                                
                                                NOS_API.add_test_case_result_to_file_report(
                                                            test_result,
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            error_codes,
                                                            error_messages)
                                
                                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                report_file = NOS_API.create_test_case_log_file(
                                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                NOS_API.test_cases_results_info.mac_using_barcode,
                                                                end_time)
                                            
                                                NOS_API.upload_file_report(report_file)
                                                NOS_API.test_cases_results_info.isTestOK = False
                                                                        
                                                NOS_API.send_report_over_mqtt_test_plan(
                                                        test_result,
                                                        end_time,
                                                        error_codes,
                                                        report_file)
                                                        
                                                ## Update test result
                                                TEST_CREATION_API.update_test_result(test_result)
                                                
                                                ## Return DUT to initial state and de-initialize grabber device
                                                NOS_API.deinitialize()
                                                
                                                return                
                
                                            elif(boot_image == -2):
                                                TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                                NOS_API.set_error_message("Reboot")
                                                error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                                error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                                test_result = "FAIL"
                                                
                                                NOS_API.add_test_case_result_to_file_report(
                                                                test_result,
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                error_codes,
                                                                error_messages)
                                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                report_file = ""
                                                if (test_result != "PASS"):
                                                    report_file = NOS_API.create_test_case_log_file(
                                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                                                    end_time)
                                                    NOS_API.upload_file_report(report_file)
                                                    NOS_API.test_cases_results_info.isTestOK = False
                                
                                
                                                ## Update test result
                                                TEST_CREATION_API.update_test_result(test_result)
                                                
                                                ## Return DUT to initial state and de-initialize grabber device
                                                NOS_API.deinitialize()
                                                
                                                NOS_API.send_report_over_mqtt_test_plan(
                                                    test_result,
                                                    end_time,
                                                    error_codes,
                                                    report_file)
                                
                                                return
                                        elif(boot_image == -2):
                                            TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                            NOS_API.set_error_message("Reboot")
                                            error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                            error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                            test_result = "FAIL"
                                            
                                            NOS_API.add_test_case_result_to_file_report(
                                                            test_result,
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            error_codes,
                                                            error_messages)
                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                            report_file = ""
                                            if (test_result != "PASS"):
                                                report_file = NOS_API.create_test_case_log_file(
                                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                NOS_API.test_cases_results_info.mac_using_barcode,
                                                                end_time)
                                                NOS_API.upload_file_report(report_file)
                                                NOS_API.test_cases_results_info.isTestOK = False
                            
                            
                                            ## Update test result
                                            TEST_CREATION_API.update_test_result(test_result)
                                            
                                            ## Return DUT to initial state and de-initialize grabber device
                                            NOS_API.deinitialize()
                                            
                                            NOS_API.send_report_over_mqtt_test_plan(
                                                test_result,
                                                end_time,
                                                error_codes,
                                                report_file)
                            
                                            return                                            
                                    elif(boot_image == -1):
                                        time.sleep(2)
                                        TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                                        boot_image = NOS_API.wait_for_multiple_pictures(["HDMI_video_1080_ref","HDMI_video_1080_ref1","HDMI_video_1080_ref2","HDMI_video_ref","HDMI_video_ref1","HDMI_video_ref2","Banner_1080_ref","HDMI_video_576_ref","No_Signal_ref","No_Signal_576_ref","No_Signal_720_ref"], 45, ["[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[HALF_SCREEN_720p]","[HALF_SCREEN_720p]","[HALF_SCREEN_720p]","[BANNER_1080]","[HALF_SCREEN_576p]","[NO_SIGNAL]","[NO_SIGNAL_576]","[NO_SIGNAL_720]"], [NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,60,NOS_API.thres,60,NOS_API.thres])
                                        if ( boot_image >= 0 and boot_image <= 7):
                                            if(boot_image == 3 or boot_image == 4 or boot_image == 5):
                                                NOS_API.SET_720 = True
                                            if(boot_image == 7):
                                                NOS_API.SET_576 = True
                                            test_result = "PASS"
                                        elif(boot_image == -1):
                                            TEST_CREATION_API.write_log_to_file("Image is not reproduced correctly on HDMI.")
                                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_1080p_noise_error_code \
                                                                                + "; Error message: " + NOS_API.test_cases_results_info.hdmi_1080p_noise_error_message)
                                            error_codes = NOS_API.test_cases_results_info.hdmi_1080p_noise_error_code
                                            error_messages = NOS_API.test_cases_results_info.hdmi_1080p_noise_error_message
                                            NOS_API.set_error_message("Video HDMI")
                                            
                                            NOS_API.add_test_case_result_to_file_report(
                                                        test_result,
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        error_codes,
                                                        error_messages)
                            
                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                            report_file = NOS_API.create_test_case_log_file(
                                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                                            NOS_API.test_cases_results_info.nos_sap_number,
                                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                                            end_time)
                                        
                                            NOS_API.upload_file_report(report_file)
                                            NOS_API.test_cases_results_info.isTestOK = False
                                                                    
                                            NOS_API.send_report_over_mqtt_test_plan(
                                                    test_result,
                                                    end_time,
                                                    error_codes,
                                                    report_file)
                                                    
                                            ## Update test result
                                            TEST_CREATION_API.update_test_result(test_result)
                                            
                                            ## Return DUT to initial state and de-initialize grabber device
                                            NOS_API.deinitialize()
                                            
                                            return                          
                                        elif(boot_image == -2):
                                            TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                            NOS_API.set_error_message("Reboot")
                                            error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                            error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                            test_result = "FAIL"
                                            
                                            NOS_API.add_test_case_result_to_file_report(
                                                            test_result,
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            error_codes,
                                                            error_messages)
                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                            report_file = ""
                                            if (test_result != "PASS"):
                                                report_file = NOS_API.create_test_case_log_file(
                                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                NOS_API.test_cases_results_info.mac_using_barcode,
                                                                end_time)
                                                NOS_API.upload_file_report(report_file)
                                                NOS_API.test_cases_results_info.isTestOK = False
                            
                            
                                            ## Update test result
                                            TEST_CREATION_API.update_test_result(test_result)
                                            
                                            ## Return DUT to initial state and de-initialize grabber device
                                            NOS_API.deinitialize()
                                            
                                            NOS_API.send_report_over_mqtt_test_plan(
                                                test_result,
                                                end_time,
                                                error_codes,
                                                report_file)
                            
                                            return                              
                                    elif(boot_image == -2):
                                        TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                        NOS_API.set_error_message("Reboot")
                                        error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                        error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                        test_result = "FAIL"
                                        
                                        NOS_API.add_test_case_result_to_file_report(
                                                        test_result,
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        error_codes,
                                                        error_messages)
                                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                        report_file = ""
                                        if (test_result != "PASS"):
                                            report_file = NOS_API.create_test_case_log_file(
                                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                                            NOS_API.test_cases_results_info.nos_sap_number,
                                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                                            end_time)
                                            NOS_API.upload_file_report(report_file)
                                            NOS_API.test_cases_results_info.isTestOK = False
                        
                        
                                        ## Update test result
                                        TEST_CREATION_API.update_test_result(test_result)
                                        
                                        ## Return DUT to initial state and de-initialize grabber device
                                        NOS_API.deinitialize()
                                        
                                        NOS_API.send_report_over_mqtt_test_plan(
                                            test_result,
                                            end_time,
                                            error_codes,
                                            report_file)
                        
                                        return                                      
                                else:
                                    TEST_CREATION_API.write_log_to_file("No boot")
                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.no_boot_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.no_boot_error_message)
                                    NOS_API.set_error_message("Não arranca")
                                    error_codes =  NOS_API.test_cases_results_info.no_boot_error_code
                                    error_messages = NOS_API.test_cases_results_info.no_boot_error_message
                                    NOS_API.add_test_case_result_to_file_report(
                                                test_result,
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                error_codes,
                                                error_messages)
                    
                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                    report_file = NOS_API.create_test_case_log_file(
                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                                    end_time)
                                
                                    NOS_API.upload_file_report(report_file)
                                    NOS_API.test_cases_results_info.isTestOK = False
                                                            
                                    NOS_API.send_report_over_mqtt_test_plan(
                                            test_result,
                                            end_time,
                                            error_codes,
                                            report_file)
                                            
                                    ## Update test result
                                    TEST_CREATION_API.update_test_result(test_result)
                                    
                                    ## Return DUT to initial state and de-initialize grabber device
                                    NOS_API.deinitialize()
                                    
                                    return                               
                        else: 
                            Comparison = NOS_API.wait_for_multiple_pictures(["OTA_Setup_ref"], 3, ["[OTA_SETUP]"], [NOS_API.thres])
                            if (Comparison == 0):
                                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.ir_nok_error_code \
                                            + "; Error message: " + NOS_API.test_cases_results_info.ir_nok_error_message)
                                NOS_API.set_error_message("IR")
                                error_codes = NOS_API.test_cases_results_info.ir_nok_error_code
                                error_messages = NOS_API.test_cases_results_info.ir_nok_error_message
                            else:
                                TEST_CREATION_API.write_log_to_file("Doesn't upgrade")            
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.upgrade_nok_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.upgrade_nok_error_message)                                        
                                NOS_API.set_error_message("Não Actualiza") 
                                error_codes =  NOS_API.test_cases_results_info.upgrade_nok_error_code
                                error_messages = NOS_API.test_cases_results_info.upgrade_nok_error_message                               
                                test_result = "FAIL"    
                elif(Comparison == -2):
                    NOS_API.grabber_stop_video_source()
                    time.sleep(1)
                    NOS_API.grabber_stop_audio_source()
                    time.sleep(1)
                    
                    ## Initialize input interfaces of DUT RT-AV101 device  
                    NOS_API.reset_dut()
                    #time.sleep(2)

                    ## Start grabber device with video on default video source
                    NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.CVBS2)
                    #time.sleep(5)
                    
                    if (NOS_API.is_signal_present_on_video_source()):
                        if not(NOS_API.grab_picture("SCART_video")):
                            TEST_CREATION_API.write_log_to_file("Image is not displayed on SCART")
                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_scart_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.image_absence_scart_error_message)
                            NOS_API.set_error_message("Video SCART")
                            error_codes = NOS_API.test_cases_results_info.image_absence_scart_error_code
                            error_messages = NOS_API.test_cases_results_info.image_absence_scart_error_message
                            
                            NOS_API.add_test_case_result_to_file_report(
                                        test_result,
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        error_codes,
                                        error_messages)
            
                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                            report_file = NOS_API.create_test_case_log_file(
                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                            NOS_API.test_cases_results_info.nos_sap_number,
                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                            end_time)
                        
                            NOS_API.upload_file_report(report_file)
                            NOS_API.test_cases_results_info.isTestOK = False
                                                    
                            NOS_API.send_report_over_mqtt_test_plan(
                                    test_result,
                                    end_time,
                                    error_codes,
                                    report_file)
                                    
                            ## Update test result
                            TEST_CREATION_API.update_test_result(test_result)
                            
                            ## Return DUT to initial state and de-initialize grabber device
                            NOS_API.deinitialize()
                            
                            return
                        NOS_API.display_custom_dialog("Confirme o cabo HDMI", 1, ["Continuar"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG)
                        NOS_API.grabber_stop_video_source()
                        time.sleep(1)
                        NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.HDMI1)
                        time.sleep(1)
                        Comparison = NOS_API.wait_for_multiple_pictures(["OTA_Setup_ref"], WAIT_OTA_TEST, ["[OTA_SETUP]"], [NOS_API.thres])   
                        TEST_CREATION_API.write_log_to_file(Comparison)
                        if(Comparison == -1):
                            TEST_CREATION_API.write_log_to_file("Doesn't upgrade")
                
                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.upgrade_nok_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.upgrade_nok_error_message)                                        
                            NOS_API.set_error_message("Não Actualiza") 
                            error_codes =  NOS_API.test_cases_results_info.upgrade_nok_error_code
                            error_messages = NOS_API.test_cases_results_info.upgrade_nok_error_message                               
                            test_result = "FAIL"
                        elif(Comparison == -2):                            
                            TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                            NOS_API.set_error_message("Video HDMI(Não Retestar)")
                            error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                            error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                            
                            NOS_API.add_test_case_result_to_file_report(
                                        test_result,
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        error_codes,
                                        error_messages)
            
                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                            report_file = NOS_API.create_test_case_log_file(
                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                            NOS_API.test_cases_results_info.nos_sap_number,
                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                            end_time)
                        
                            NOS_API.upload_file_report(report_file)
                            NOS_API.test_cases_results_info.isTestOK = False
                                                    
                            NOS_API.send_report_over_mqtt_test_plan(
                                    test_result,
                                    end_time,
                                    error_codes,
                                    report_file)
                                    
                            ## Update test result
                            TEST_CREATION_API.update_test_result(test_result)
                            
                            ## Return DUT to initial state and de-initialize grabber device
                            NOS_API.deinitialize()
                            
                            return
                        
                        elif(Comparison == 0):
                            time.sleep(1)
                            TEST_CREATION_API.send_ir_rc_command("[OK]")
                            time.sleep(4)
                            if(NOS_API.wait_for_no_signal_present(60)):
                                NOS_API.test_cases_results_info.DidUpgrade = 1
                                time.sleep(5)
                                if(NOS_API.wait_for_signal_present(60)):
                                    boot_image = NOS_API.wait_for_multiple_pictures(["HDMI_video_1080_ref","HDMI_video_1080_ref1","HDMI_video_1080_ref2","Banner_1080_ref","No_Signal_ref","No_Signal_576_ref","No_Signal_720_ref"], 45, ["[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[BANNER_1080]","[NO_SIGNAL]","[NO_SIGNAL_576]","[NO_SIGNAL_720]"], [NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,60,NOS_API.thres])
                                    if ( boot_image == 0 or boot_image == 1 or boot_image == 2 or boot_image == 3):
                                        test_result = "PASS"
                                    elif(boot_image == 4 or boot_image == 5 or boot_image == 6):
                                        TEST_CREATION_API.send_ir_rc_command("[TV]")
                                        TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                                        boot_image = NOS_API.wait_for_multiple_pictures(["No_Signal_ref","No_Signal_576_ref","No_Signal_720_ref"], 5, ["[NO_SIGNAL]","[NO_SIGNAL_576]","[NO_SIGNAL_720]"], [NOS_API.thres,60,NOS_API.thres])
                                        if ( boot_image >= 0 and boot_image < 3):
                                            TEST_CREATION_API.send_ir_rc_command("[TV]")
                                            NOS_API.display_custom_dialog("Confirme o cabo RF", 1, ["Continuar"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG)
                                        boot_image = NOS_API.wait_for_multiple_pictures(["HDMI_video_1080_ref","HDMI_video_1080_ref1","HDMI_video_1080_ref2","Banner_1080_ref","No_Signal_ref"], 45, ["[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[BANNER_1080]","[NO_SIGNAL]"], [NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres])
                                        if ( boot_image == 0 or boot_image == 1 or boot_image == 2 or boot_image == 3):
                                            test_result = "PASS"
                                        
                                        elif(boot_image == 3):
                                            TEST_CREATION_API.write_log_to_file("Signal value is lower than threshold")                
                                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.input_signal_error_code \
                                                                                + "; Error message: " + NOS_API.test_cases_results_info.input_signal_error_message)
                                            NOS_API.set_error_message("Sem Sinal")
                                            error_codes = NOS_API.test_cases_results_info.input_signal_error_code
                                            error_messages = NOS_API.test_cases_results_info.input_signal_error_message
                                        elif(boot_image == -1):
                                            time.sleep(2)
                                            TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                                            boot_image = NOS_API.wait_for_multiple_pictures(["HDMI_video_1080_ref","HDMI_video_1080_ref1","HDMI_video_1080_ref2","Banner_1080_ref","No_Signal_ref","No_Signal_576_ref","No_Signal_720_ref"], 45, ["[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[BANNER_1080]","[NO_SIGNAL]","[NO_SIGNAL_576]","[NO_SIGNAL_720]"], [NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,60,NOS_API.thres])
                                            if ( boot_image == 0 or boot_image == 1 or boot_image == 2 or boot_image == 3):
                                                test_result = "PASS"
                                            elif(boot_image == 4 or boot_image == 5 or boot_image == 6):
                                                TEST_CREATION_API.write_log_to_file("Signal value is lower than threshold")                
                                                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.input_signal_error_code \
                                                                                    + "; Error message: " + NOS_API.test_cases_results_info.input_signal_error_message)
                                                NOS_API.set_error_message("Sem Sinal")
                                                error_codes = NOS_API.test_cases_results_info.input_signal_error_code
                                                error_messages = NOS_API.test_cases_results_info.input_signal_error_message
                                            
                                            elif(boot_image == -1):
                                                TEST_CREATION_API.write_log_to_file("Image is not reproduced correctly on HDMI.")
                                                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_1080p_noise_error_code \
                                                                                    + "; Error message: " + NOS_API.test_cases_results_info.hdmi_1080p_noise_error_message)
                                                error_codes = NOS_API.test_cases_results_info.hdmi_1080p_noise_error_code
                                                error_messages = NOS_API.test_cases_results_info.hdmi_1080p_noise_error_message
                                                NOS_API.set_error_message("Video HDMI")
                                                
                                                NOS_API.add_test_case_result_to_file_report(
                                                            test_result,
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            error_codes,
                                                            error_messages)
                                
                                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                report_file = NOS_API.create_test_case_log_file(
                                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                NOS_API.test_cases_results_info.mac_using_barcode,
                                                                end_time)
                                            
                                                NOS_API.upload_file_report(report_file)
                                                NOS_API.test_cases_results_info.isTestOK = False
                                                                        
                                                NOS_API.send_report_over_mqtt_test_plan(
                                                        test_result,
                                                        end_time,
                                                        error_codes,
                                                        report_file)
                                                        
                                                ## Update test result
                                                TEST_CREATION_API.update_test_result(test_result)
                                                
                                                ## Return DUT to initial state and de-initialize grabber device
                                                NOS_API.deinitialize()
                                                
                                                return                
                
                                            elif(boot_image == -2):
                                                TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                                NOS_API.set_error_message("Reboot")
                                                error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                                error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                                test_result = "FAIL"
                                                
                                                NOS_API.add_test_case_result_to_file_report(
                                                                test_result,
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                error_codes,
                                                                error_messages)
                                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                report_file = ""
                                                if (test_result != "PASS"):
                                                    report_file = NOS_API.create_test_case_log_file(
                                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                                                    end_time)
                                                    NOS_API.upload_file_report(report_file)
                                                    NOS_API.test_cases_results_info.isTestOK = False
                                
                                
                                                ## Update test result
                                                TEST_CREATION_API.update_test_result(test_result)
                                                
                                                ## Return DUT to initial state and de-initialize grabber device
                                                NOS_API.deinitialize()
                                                
                                                NOS_API.send_report_over_mqtt_test_plan(
                                                    test_result,
                                                    end_time,
                                                    error_codes,
                                                    report_file)
                                
                                                return
                                    
                                        elif(boot_image == -2):
                                            TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                            NOS_API.set_error_message("Reboot")
                                            error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                            error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                            test_result = "FAIL"
                                            
                                            NOS_API.add_test_case_result_to_file_report(
                                                            test_result,
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            error_codes,
                                                            error_messages)
                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                            report_file = ""
                                            if (test_result != "PASS"):
                                                report_file = NOS_API.create_test_case_log_file(
                                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                NOS_API.test_cases_results_info.mac_using_barcode,
                                                                end_time)
                                                NOS_API.upload_file_report(report_file)
                                                NOS_API.test_cases_results_info.isTestOK = False
                            
                            
                                            ## Update test result
                                            TEST_CREATION_API.update_test_result(test_result)
                                            
                                            ## Return DUT to initial state and de-initialize grabber device
                                            NOS_API.deinitialize()
                                            
                                            NOS_API.send_report_over_mqtt_test_plan(
                                                test_result,
                                                end_time,
                                                error_codes,
                                                report_file)
                            
                                            return
                                    elif(boot_image == -1):
                                            time.sleep(2)
                                            TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                                            boot_image = NOS_API.wait_for_multiple_pictures(["HDMI_video_1080_ref","HDMI_video_1080_ref1","HDMI_video_1080_ref2","Banner_1080_ref","No_Signal_ref","No_Signal_576_ref","No_Signal_720_ref"], 45, ["[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[BANNER_1080]","[NO_SIGNAL]","[NO_SIGNAL_576]","[NO_SIGNAL_720]"], [NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,60,NOS_API.thres])
                                            if ( boot_image == 0 or boot_image == 1 or boot_image == 2 or boot_image == 3):
                                                test_result = "PASS"
                                            elif(boot_image == 4 or boot_image == 5 or boot_image == 6):
                                                TEST_CREATION_API.write_log_to_file("Signal value is lower than threshold")                
                                                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.input_signal_error_code \
                                                                                    + "; Error message: " + NOS_API.test_cases_results_info.input_signal_error_message)
                                                NOS_API.set_error_message("Sem Sinal")
                                                error_codes = NOS_API.test_cases_results_info.input_signal_error_code
                                                error_messages = NOS_API.test_cases_results_info.input_signal_error_message
                                            elif(boot_image == -1):
                                                TEST_CREATION_API.write_log_to_file("Image is not reproduced correctly on HDMI.")
                                                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_1080p_noise_error_code \
                                                                                    + "; Error message: " + NOS_API.test_cases_results_info.hdmi_1080p_noise_error_message)
                                                error_codes = NOS_API.test_cases_results_info.hdmi_1080p_noise_error_code
                                                error_messages = NOS_API.test_cases_results_info.hdmi_1080p_noise_error_message
                                                NOS_API.set_error_message("Video HDMI")
                                                
                                                NOS_API.add_test_case_result_to_file_report(
                                                            test_result,
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            error_codes,
                                                            error_messages)
                                
                                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                report_file = NOS_API.create_test_case_log_file(
                                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                NOS_API.test_cases_results_info.mac_using_barcode,
                                                                end_time)
                                            
                                                NOS_API.upload_file_report(report_file)
                                                NOS_API.test_cases_results_info.isTestOK = False
                                                                        
                                                NOS_API.send_report_over_mqtt_test_plan(
                                                        test_result,
                                                        end_time,
                                                        error_codes,
                                                        report_file)
                                                        
                                                ## Update test result
                                                TEST_CREATION_API.update_test_result(test_result)
                                                
                                                ## Return DUT to initial state and de-initialize grabber device
                                                NOS_API.deinitialize()
                                                
                                                return                
                
                                            elif(boot_image == -2):
                                                TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                                NOS_API.set_error_message("Reboot")
                                                error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                                error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                                test_result = "FAIL"
                                                
                                                NOS_API.add_test_case_result_to_file_report(
                                                                test_result,
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                error_codes,
                                                                error_messages)
                                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                report_file = ""
                                                if (test_result != "PASS"):
                                                    report_file = NOS_API.create_test_case_log_file(
                                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                                                    end_time)
                                                    NOS_API.upload_file_report(report_file)
                                                    NOS_API.test_cases_results_info.isTestOK = False
                                
                                
                                                ## Update test result
                                                TEST_CREATION_API.update_test_result(test_result)
                                                
                                                ## Return DUT to initial state and de-initialize grabber device
                                                NOS_API.deinitialize()
                                                
                                                NOS_API.send_report_over_mqtt_test_plan(
                                                    test_result,
                                                    end_time,
                                                    error_codes,
                                                    report_file)
                                
                                                return
                                        
                                    elif(boot_image == -2):
                                        TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                        NOS_API.set_error_message("Reboot")
                                        error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                        error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                        test_result = "FAIL"
                                        
                                        NOS_API.add_test_case_result_to_file_report(
                                                        test_result,
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        error_codes,
                                                        error_messages)
                                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                        report_file = ""
                                        if (test_result != "PASS"):
                                            report_file = NOS_API.create_test_case_log_file(
                                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                                            NOS_API.test_cases_results_info.nos_sap_number,
                                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                                            end_time)
                                            NOS_API.upload_file_report(report_file)
                                            NOS_API.test_cases_results_info.isTestOK = False
                        
                        
                                        ## Update test result
                                        TEST_CREATION_API.update_test_result(test_result)
                                        
                                        ## Return DUT to initial state and de-initialize grabber device
                                        NOS_API.deinitialize()
                                        
                                        NOS_API.send_report_over_mqtt_test_plan(
                                            test_result,
                                            end_time,
                                            error_codes,
                                            report_file)
                        
                                        return
                                        
                                else:
                                    TEST_CREATION_API.send_ir_rc_command("[POWER]")
                                    time.sleep(4)
                                    if (NOS_API.is_signal_present_on_video_source()):
                                        boot_image = NOS_API.wait_for_multiple_pictures(["HDMI_video_1080_ref","HDMI_video_1080_ref1","HDMI_video_1080_ref2","Banner_1080_ref","No_Signal_ref","No_Signal_576_ref","No_Signal_720_ref"], 45, ["[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[BANNER_1080]","[NO_SIGNAL]","[NO_SIGNAL_576]","[NO_SIGNAL_720]"], [NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,60,NOS_API.thres])
                                        TEST_CREATION_API.write_log_to_file("boot image after power = " + str(boot_image))
                                        if ( boot_image == 0 or boot_image == 1 or boot_image == 2 or boot_image == 3):
                                            test_result = "PASS"
                                        elif(boot_image == 4 or boot_image == 5 or boot_image == 6):
                                            TEST_CREATION_API.send_ir_rc_command("[TV]")
                                            TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                                            boot_image = NOS_API.wait_for_multiple_pictures(["No_Signal_ref","No_Signal_576_ref","No_Signal_720_ref"], 5, ["[NO_SIGNAL]","[NO_SIGNAL_576]","[NO_SIGNAL_720]"], [NOS_API.thres,60,NOS_API.thres])
                                            if ( boot_image >= 0 and boot_image < 3):
                                                TEST_CREATION_API.send_ir_rc_command("[TV]")
                                                NOS_API.display_custom_dialog("Confirme o cabo RF", 1, ["Continuar"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG)
                                            boot_image = NOS_API.wait_for_multiple_pictures(["HDMI_video_1080_ref","HDMI_video_1080_ref1","HDMI_video_1080_ref2","Banner_1080_ref","No_Signal_ref","No_Signal_576_ref","No_Signal_720_ref"], 45, ["[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[BANNER_1080]","[NO_SIGNAL]","[NO_SIGNAL_576]","[NO_SIGNAL_720]"], [NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,60,NOS_API.thres])
                                            TEST_CREATION_API.write_log_to_file("boot image after power = " + str(boot_image))
                                            if ( boot_image == 0 or boot_image == 1 or boot_image == 2 or boot_image == 3):
                                                test_result = "PASS"
                                                
                                            elif(boot_image == 4 or boot_image == 5 or boot_image == 6):
                                                TEST_CREATION_API.write_log_to_file("Signal value is lower than threshold")                
                                                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.input_signal_error_code \
                                                                                    + "; Error message: " + NOS_API.test_cases_results_info.input_signal_error_message)
                                                NOS_API.set_error_message("Sem Sinal")
                                                error_codes = NOS_API.test_cases_results_info.input_signal_error_code
                                                error_messages = NOS_API.test_cases_results_info.input_signal_error_message
                                            elif(boot_image == -1):
                                                #time.sleep(2)
                                                TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                                                boot_image = NOS_API.wait_for_multiple_pictures(["HDMI_video_1080_ref","HDMI_video_1080_ref1","HDMI_video_1080_ref2","Banner_1080_ref","No_Signal_ref","No_Signal_576_ref","No_Signal_720_ref"], 45, ["[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[BANNER_1080]","[NO_SIGNAL]","[NO_SIGNAL_576]","[NO_SIGNAL_720]"], [NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,60,NOS_API.thres])
                                                if ( boot_image == 0 or boot_image == 1 or boot_image == 2 or boot_image == 3):
                                                    test_result = "PASS"
                                                    
                                                elif(boot_image == 4 or boot_image == 5 or boot_image == 6):
                                                    TEST_CREATION_API.write_log_to_file("Signal value is lower than threshold")                                            
                                                    NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.input_signal_error_code \
                                                                                        + "; Error message: " + NOS_API.test_cases_results_info.input_signal_error_message)
                                                    NOS_API.set_error_message("Sem Sinal")
                                                    error_codes = NOS_API.test_cases_results_info.input_signal_error_code
                                                    error_messages = NOS_API.test_cases_results_info.input_signal_error_message
                                                    
                                                elif(boot_image == -1):
                                                    TEST_CREATION_API.write_log_to_file("Image is not reproduced correctly on HDMI.")
                                                    NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_1080p_noise_error_code \
                                                                                        + "; Error message: " + NOS_API.test_cases_results_info.hdmi_1080p_noise_error_message)
                                                    error_codes = NOS_API.test_cases_results_info.hdmi_1080p_noise_error_code
                                                    error_messages = NOS_API.test_cases_results_info.hdmi_1080p_noise_error_message
                                                    NOS_API.set_error_message("Video HDMI")
                                                    
                                                    NOS_API.add_test_case_result_to_file_report(
                                                                test_result,
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                error_codes,
                                                                error_messages)
                                    
                                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                    report_file = NOS_API.create_test_case_log_file(
                                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                                                    end_time)
                                                
                                                    NOS_API.upload_file_report(report_file)
                                                    NOS_API.test_cases_results_info.isTestOK = False
                                                                            
                                                    NOS_API.send_report_over_mqtt_test_plan(
                                                            test_result,
                                                            end_time,
                                                            error_codes,
                                                            report_file)
                                                            
                                                    ## Update test result
                                                    TEST_CREATION_API.update_test_result(test_result)
                                                    
                                                    ## Return DUT to initial state and de-initialize grabber device
                                                    NOS_API.deinitialize()
                                                    
                                                    return                
                    
                                                elif(boot_image == -2):
                                                    TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                            + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                                    NOS_API.set_error_message("Reboot")
                                                    error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                                    error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                                    test_result = "FAIL"
                                                    
                                                    NOS_API.add_test_case_result_to_file_report(
                                                                    test_result,
                                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                                    error_codes,
                                                                    error_messages)
                                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                    report_file = ""
                                                    if (test_result != "PASS"):
                                                        report_file = NOS_API.create_test_case_log_file(
                                                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                        NOS_API.test_cases_results_info.nos_sap_number,
                                                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                                                        end_time)
                                                        NOS_API.upload_file_report(report_file)
                                                        NOS_API.test_cases_results_info.isTestOK = False
                                    
                                    
                                                    ## Update test result
                                                    TEST_CREATION_API.update_test_result(test_result)
                                                    
                                                    ## Return DUT to initial state and de-initialize grabber device
                                                    NOS_API.deinitialize()
                                                    
                                                    NOS_API.send_report_over_mqtt_test_plan(
                                                        test_result,
                                                        end_time,
                                                        error_codes,
                                                        report_file)
                                    
                                                    return
                                            elif(boot_image == -2):
                                                TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                                NOS_API.set_error_message("Reboot")
                                                error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                                error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                                test_result = "FAIL"
                                                
                                                NOS_API.add_test_case_result_to_file_report(
                                                                test_result,
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                error_codes,
                                                                error_messages)
                                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                report_file = ""
                                                if (test_result != "PASS"):
                                                    report_file = NOS_API.create_test_case_log_file(
                                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                                                    end_time)
                                                    NOS_API.upload_file_report(report_file)
                                                    NOS_API.test_cases_results_info.isTestOK = False
                                
                                
                                                ## Update test result
                                                TEST_CREATION_API.update_test_result(test_result)
                                                
                                                ## Return DUT to initial state and de-initialize grabber device
                                                NOS_API.deinitialize()
                                                
                                                NOS_API.send_report_over_mqtt_test_plan(
                                                    test_result,
                                                    end_time,
                                                    error_codes,
                                                    report_file)
                                
                                                return
                                        
                                                
                                        elif(boot_image == -1):
                                            time.sleep(2)
                                            TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                                            boot_image = NOS_API.wait_for_multiple_pictures(["HDMI_video_1080_ref","HDMI_video_1080_ref1","HDMI_video_1080_ref2","Banner_1080_ref","No_Signal_ref","No_Signal_576_ref","No_Signal_720_ref"], 45, ["[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[BANNER_1080]","[NO_SIGNAL]","[NO_SIGNAL_576]","[NO_SIGNAL_720]"], [NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,60,NOS_API.thres])
                                            TEST_CREATION_API.write_log_to_file("boot image after power = " + str(boot_image))
                                            if ( boot_image == 0 or boot_image == 1 or boot_image == 2 or boot_image == 3):
                                                test_result = "PASS"

                                            elif(boot_image == -1):
                                                TEST_CREATION_API.write_log_to_file("Image is not reproduced correctly on HDMI.")
                                                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_1080p_noise_error_code \
                                                                                    + "; Error message: " + NOS_API.test_cases_results_info.hdmi_1080p_noise_error_message)
                                                error_codes = NOS_API.test_cases_results_info.hdmi_1080p_noise_error_code
                                                error_messages = NOS_API.test_cases_results_info.hdmi_1080p_noise_error_message
                                                NOS_API.set_error_message("Video HDMI")
                                                
                                                NOS_API.add_test_case_result_to_file_report(
                                                            test_result,
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            error_codes,
                                                            error_messages)
                                
                                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                report_file = NOS_API.create_test_case_log_file(
                                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                NOS_API.test_cases_results_info.mac_using_barcode,
                                                                end_time)
                                            
                                                NOS_API.upload_file_report(report_file)
                                                NOS_API.test_cases_results_info.isTestOK = False
                                                                        
                                                NOS_API.send_report_over_mqtt_test_plan(
                                                        test_result,
                                                        end_time,
                                                        error_codes,
                                                        report_file)
                                                        
                                                ## Update test result
                                                TEST_CREATION_API.update_test_result(test_result)
                                                
                                                ## Return DUT to initial state and de-initialize grabber device
                                                NOS_API.deinitialize()
                                                
                                                return                
                
                                            elif(boot_image == -2):
                                                TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                                NOS_API.set_error_message("Reboot")
                                                error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                                error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                                test_result = "FAIL"
                                                
                                                NOS_API.add_test_case_result_to_file_report(
                                                                test_result,
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                error_codes,
                                                                error_messages)
                                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                report_file = ""
                                                if (test_result != "PASS"):
                                                    report_file = NOS_API.create_test_case_log_file(
                                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                                                    end_time)
                                                    NOS_API.upload_file_report(report_file)
                                                    NOS_API.test_cases_results_info.isTestOK = False
                                
                                
                                                ## Update test result
                                                TEST_CREATION_API.update_test_result(test_result)
                                                
                                                ## Return DUT to initial state and de-initialize grabber device
                                                NOS_API.deinitialize()
                                                
                                                NOS_API.send_report_over_mqtt_test_plan(
                                                    test_result,
                                                    end_time,
                                                    error_codes,
                                                    report_file)
                                
                                                return
                                    
                                            elif(boot_image == 4 or boot_image == 5 or boot_image == 6):
                                                TEST_CREATION_API.write_log_to_file("Signal value is lower than threshold")                                            
                                                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.input_signal_error_code \
                                                                                    + "; Error message: " + NOS_API.test_cases_results_info.input_signal_error_message)
                                                NOS_API.set_error_message("Sem Sinal")
                                                error_codes = NOS_API.test_cases_results_info.input_signal_error_code
                                                error_messages = NOS_API.test_cases_results_info.input_signal_error_message
                                        
                                        elif(boot_image == -2):
                                            TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                            NOS_API.set_error_message("Reboot")
                                            error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                            error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                            test_result = "FAIL"
                                            
                                            NOS_API.add_test_case_result_to_file_report(
                                                            test_result,
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            error_codes,
                                                            error_messages)
                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                            report_file = ""
                                            if (test_result != "PASS"):
                                                report_file = NOS_API.create_test_case_log_file(
                                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                NOS_API.test_cases_results_info.mac_using_barcode,
                                                                end_time)
                                                NOS_API.upload_file_report(report_file)
                                                NOS_API.test_cases_results_info.isTestOK = False
                            
                            
                                            ## Update test result
                                            TEST_CREATION_API.update_test_result(test_result)
                                            
                                            ## Return DUT to initial state and de-initialize grabber device
                                            NOS_API.deinitialize()
                                            
                                            NOS_API.send_report_over_mqtt_test_plan(
                                                test_result,
                                                end_time,
                                                error_codes,
                                                report_file)
                            
                                            return
                                            
                                    else:
                                        TEST_CREATION_API.write_log_to_file("No boot")
                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.no_boot_error_code \
                                                                            + "; Error message: " + NOS_API.test_cases_results_info.no_boot_error_message)
                                        NOS_API.set_error_message("Não arranca")
                                        error_codes =  NOS_API.test_cases_results_info.no_boot_error_code
                                        error_messages = NOS_API.test_cases_results_info.no_boot_error_message
                                        NOS_API.add_test_case_result_to_file_report(
                                                    test_result,
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    error_codes,
                                                    error_messages)
                        
                                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                        report_file = NOS_API.create_test_case_log_file(
                                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                        NOS_API.test_cases_results_info.nos_sap_number,
                                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                                        end_time)
                                    
                                        NOS_API.upload_file_report(report_file)
                                        NOS_API.test_cases_results_info.isTestOK = False
                                                                
                                        NOS_API.send_report_over_mqtt_test_plan(
                                                test_result,
                                                end_time,
                                                error_codes,
                                                report_file)
                                                
                                        ## Update test result
                                        TEST_CREATION_API.update_test_result(test_result)
                                        
                                        ## Return DUT to initial state and de-initialize grabber device
                                        NOS_API.deinitialize()
                                        
                                        return         
                            else: 
                                Comparison = NOS_API.wait_for_multiple_pictures(["OTA_Setup_ref"], 3, ["[OTA_SETUP]"], [NOS_API.thres])
                                if (Comparison == 0):
                                    NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.ir_nok_error_code \
                                                + "; Error message: " + NOS_API.test_cases_results_info.ir_nok_error_message)
                                    NOS_API.set_error_message("IR")
                                    error_codes = NOS_API.test_cases_results_info.ir_nok_error_code
                                    error_messages = NOS_API.test_cases_results_info.ir_nok_error_message
                                else:
                                    TEST_CREATION_API.write_log_to_file("Doesn't upgrade")            
                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.upgrade_nok_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.upgrade_nok_error_message)                                        
                                    NOS_API.set_error_message("Não Actualiza") 
                                    error_codes =  NOS_API.test_cases_results_info.upgrade_nok_error_code
                                    error_messages = NOS_API.test_cases_results_info.upgrade_nok_error_message                               
                                    test_result = "FAIL"    
                    else:
                       
                        TEST_CREATION_API.write_log_to_file("No boot")
                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.no_boot_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.no_boot_error_message)
                        NOS_API.set_error_message("Não arranca")
                        error_codes =  NOS_API.test_cases_results_info.no_boot_error_code
                        error_messages = NOS_API.test_cases_results_info.no_boot_error_message
                        NOS_API.add_test_case_result_to_file_report(
                                    test_result,
                                    "- - - - - - - - - - - - - - - - - - - -",
                                    "- - - - - - - - - - - - - - - - - - - -",
                                    error_codes,
                                    error_messages)
        
                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                        report_file = NOS_API.create_test_case_log_file(
                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                        NOS_API.test_cases_results_info.nos_sap_number,
                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                        end_time)
                    
                        NOS_API.upload_file_report(report_file)
                        NOS_API.test_cases_results_info.isTestOK = False
                                                
                        NOS_API.send_report_over_mqtt_test_plan(
                                test_result,
                                end_time,
                                error_codes,
                                report_file)
                                
                        ## Update test result
                        TEST_CREATION_API.update_test_result(test_result)
                        
                        ## Return DUT to initial state and de-initialize grabber device
                        NOS_API.deinitialize()
                        
                        return   

                elif (Comparison == 0 or Comparison == 1):
                    
                    time.sleep(1)
                    TEST_CREATION_API.send_ir_rc_command("[OK]")
                    time.sleep(2)
                    Comparison = NOS_API.wait_for_multiple_pictures(["OTA_Setup_ref","OTA_Setup_ref1"], 3, ["[OTA_SETUP]","[OTA_SETUP]"], [NOS_API.thres,NOS_API.thres])
                    if (Comparison == 0 or Comparison == 1):
                        TEST_CREATION_API.send_ir_rc_command("[OK]")
                    if(NOS_API.wait_for_no_signal_present(120)):
                        NOS_API.test_cases_results_info.DidUpgrade = 1
                        time.sleep(5)
                        if(NOS_API.wait_for_signal_present(60)):
                            TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                            boot_image = NOS_API.wait_for_multiple_pictures(["HDMI_video_1080_ref","HDMI_video_1080_ref1","HDMI_video_1080_ref2","HDMI_video_ref","HDMI_video_ref1","HDMI_video_ref2","Banner_1080_ref","HDMI_video_576_ref","No_Signal_ref","No_Signal_576_ref","No_Signal_720_ref","LOAD_FAIL_ref"], 45, ["[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[HALF_SCREEN_720p]","[HALF_SCREEN_720p]","[HALF_SCREEN_720p]","[BANNER_1080]","[HALF_SCREEN_576p]","[NO_SIGNAL]","[NO_SIGNAL_576]","[NO_SIGNAL_720]","[FULL_SCREEN_1080]"], [NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,60,NOS_API.thres,60,NOS_API.thres,NOS_API.thres])
                            if ( boot_image >= 0 and boot_image <= 7):
                                if(boot_image == 3 or boot_image == 4 or boot_image == 5):
                                    NOS_API.SET_720 = True
                                if(boot_image == 7):
                                    NOS_API.SET_576 = True
                                test_result = "PASS"
                            elif(boot_image >= 8 and boot_image <= 10):
                                TEST_CREATION_API.send_ir_rc_command("[TV]")
                                TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                                boot_image = NOS_API.wait_for_multiple_pictures(["No_Signal_ref","No_Signal_576_ref","No_Signal_720_ref"], 5, ["[NO_SIGNAL]","[NO_SIGNAL_576]","[NO_SIGNAL_720]"], [NOS_API.thres,60,NOS_API.thres])
                                if ( boot_image >= 0 and boot_image < 3):
                                    TEST_CREATION_API.send_ir_rc_command("[TV]")
                                    NOS_API.display_custom_dialog("Confirme o cabo RF", 1, ["Continuar"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG)
                              #  boot_image = NOS_API.wait_for_multiple_pictures(["HDMI_video_1080_ref","HDMI_video_1080_ref1","Banner_1080_ref","No_Signal_ref"], 45, ["[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[BANNER_1080]","[NO_SIGNAL]"], [HDMI_threshold,HDMI_threshold,HDMI_threshold,HDMI_threshold])
                                boot_image = NOS_API.wait_for_multiple_pictures(["HDMI_video_1080_ref","HDMI_video_1080_ref1","HDMI_video_1080_ref2","HDMI_video_ref","HDMI_video_ref1","HDMI_video_ref2","Banner_1080_ref","HDMI_video_576_ref","No_Signal_ref","No_Signal_576_ref","No_Signal_720_ref","LOAD_FAIL_ref"], 45, ["[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[HALF_SCREEN_720p]","[HALF_SCREEN_720p]","[HALF_SCREEN_720p]","[BANNER_1080]","[HALF_SCREEN_576p]","[NO_SIGNAL]","[NO_SIGNAL_576]","[NO_SIGNAL_720]","[FULL_SCREEN_1080]"], [NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,60,NOS_API.thres,60,NOS_API.thres,NOS_API.thres])
                                if ( boot_image >= 0 and boot_image <= 7):
                                    if(boot_image == 3 or boot_image == 4 or boot_image == 5):
                                        NOS_API.SET_720 = True
                                    if(boot_image == 7):
                                        NOS_API.SET_576 = True
                                    test_result = "PASS"
                                elif(boot_image >= 8 and boot_image <= 10):
                                    TEST_CREATION_API.write_log_to_file("Signal value is lower than threshold")                
                                    NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.input_signal_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.input_signal_error_message)
                                    NOS_API.set_error_message("Sem Sinal")
                                    error_codes = NOS_API.test_cases_results_info.input_signal_error_code
                                    error_messages = NOS_API.test_cases_results_info.input_signal_error_message
                                    time.sleep(2)
                                elif(boot_image == -1):
                                    time.sleep(2)
                                    TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                                    boot_image = NOS_API.wait_for_multiple_pictures(["HDMI_video_1080_ref","HDMI_video_1080_ref1","HDMI_video_1080_ref2","HDMI_video_ref","HDMI_video_ref1","HDMI_video_ref2","Banner_1080_ref","HDMI_video_576_ref","No_Signal_ref","No_Signal_576_ref","No_Signal_720_ref","LOAD_FAIL_ref"], 45, ["[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[HALF_SCREEN_720p]","[HALF_SCREEN_720p]","[HALF_SCREEN_720p]","[BANNER_1080]","[HALF_SCREEN_576p]","[NO_SIGNAL]","[NO_SIGNAL_576]","[NO_SIGNAL_720]","[FULL_SCREEN_1080]"], [NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,60,NOS_API.thres,60,NOS_API.thres,NOS_API.thres])
                                    if ( boot_image >= 0 and boot_image <= 7):
                                        if(boot_image == 3 or boot_image == 4 or boot_image == 5):
                                            NOS_API.SET_720 = True
                                        if(boot_image == 7):
                                            NOS_API.SET_576 = True
                                        test_result = "PASS"
                                    elif(boot_image == -1):
                                        TEST_CREATION_API.write_log_to_file("Image is not reproduced correctly on HDMI.")
                                        NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_1080p_noise_error_code \
                                                                            + "; Error message: " + NOS_API.test_cases_results_info.hdmi_1080p_noise_error_message)
                                        error_codes = NOS_API.test_cases_results_info.hdmi_1080p_noise_error_code
                                        error_messages = NOS_API.test_cases_results_info.hdmi_1080p_noise_error_message
                                        NOS_API.set_error_message("Video HDMI")
                                        
                                        NOS_API.add_test_case_result_to_file_report(
                                                    test_result,
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    error_codes,
                                                    error_messages)
                        
                                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                        report_file = NOS_API.create_test_case_log_file(
                                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                        NOS_API.test_cases_results_info.nos_sap_number,
                                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                                        end_time)
                                    
                                        NOS_API.upload_file_report(report_file)
                                        NOS_API.test_cases_results_info.isTestOK = False
                                                                
                                        NOS_API.send_report_over_mqtt_test_plan(
                                                test_result,
                                                end_time,
                                                error_codes,
                                                report_file)
                                                
                                        ## Update test result
                                        TEST_CREATION_API.update_test_result(test_result)
                                        
                                        ## Return DUT to initial state and de-initialize grabber device
                                        NOS_API.deinitialize()
                                        
                                        return                
        
                                    elif(boot_image == -2):
                                        TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                        NOS_API.set_error_message("Reboot")
                                        error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                        error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                        test_result = "FAIL"
                                        
                                        NOS_API.add_test_case_result_to_file_report(
                                                        test_result,
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        error_codes,
                                                        error_messages)
                                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                        report_file = ""
                                        if (test_result != "PASS"):
                                            report_file = NOS_API.create_test_case_log_file(
                                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                                            NOS_API.test_cases_results_info.nos_sap_number,
                                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                                            end_time)
                                            NOS_API.upload_file_report(report_file)
                                            NOS_API.test_cases_results_info.isTestOK = False
                        
                        
                                        ## Update test result
                                        TEST_CREATION_API.update_test_result(test_result)
                                        
                                        ## Return DUT to initial state and de-initialize grabber device
                                        NOS_API.deinitialize()
                                        
                                        NOS_API.send_report_over_mqtt_test_plan(
                                            test_result,
                                            end_time,
                                            error_codes,
                                            report_file)
                        
                                        return
                               
                                elif(boot_image == -2):
                                    TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                    NOS_API.set_error_message("Reboot")
                                    error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                    error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                    test_result = "FAIL"
                                    
                                    NOS_API.add_test_case_result_to_file_report(
                                                    test_result,
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    error_codes,
                                                    error_messages)
                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                    report_file = ""
                                    if (test_result != "PASS"):
                                        report_file = NOS_API.create_test_case_log_file(
                                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                        NOS_API.test_cases_results_info.nos_sap_number,
                                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                                        end_time)
                                        NOS_API.upload_file_report(report_file)
                                        NOS_API.test_cases_results_info.isTestOK = False
                    
                    
                                    ## Update test result
                                    TEST_CREATION_API.update_test_result(test_result)
                                    
                                    ## Return DUT to initial state and de-initialize grabber device
                                    NOS_API.deinitialize()
                                    
                                    NOS_API.send_report_over_mqtt_test_plan(
                                        test_result,
                                        end_time,
                                        error_codes,
                                        report_file)
                    
                                    return
                                   
                            elif(boot_image == 11):
                                TEST_CREATION_API.write_log_to_file("Doesn't upgrade")            
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.upgrade_nok_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.upgrade_nok_error_message)                                        
                                NOS_API.set_error_message("Não Actualiza") 
                                error_codes =  NOS_API.test_cases_results_info.upgrade_nok_error_code
                                error_messages = NOS_API.test_cases_results_info.upgrade_nok_error_message                               
                                test_result = "FAIL" 
                            
                            elif(boot_image == -1):
                                    time.sleep(2)
                                    TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                                    boot_image = NOS_API.wait_for_multiple_pictures(["HDMI_video_1080_ref","HDMI_video_1080_ref1","HDMI_video_1080_ref2","HDMI_video_ref","HDMI_video_ref1","HDMI_video_ref2","Banner_1080_ref","HDMI_video_576_ref","No_Signal_ref","No_Signal_576_ref","No_Signal_720_ref","NOS_ref","Install_ref","Install_ref1","Install_ENG_ref"], 45, ["[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[HALF_SCREEN_720p]","[HALF_SCREEN_720p]","[HALF_SCREEN_720p]","[BANNER_1080]","[HALF_SCREEN_576p]","[NO_SIGNAL]","[NO_SIGNAL_576]","[NO_SIGNAL_720]","[FULL_SCREEN_1080]","[MENU_ICON_1080p]","[MENU_ICON_1080p]","[MENU_ICON_1080p]"], [NOS_API.thres,NOS_API.thres,NOS_API.thres,HDMI_threNOS_API.thresshold,NOS_API.thres,NOS_API.thres,NOS_API.thres,60,NOS_API.thres,60,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres])
                                    if ( boot_image >= 0 and boot_image <= 7):
                                        if(boot_image == 3 or boot_image == 4 or boot_image == 5):
                                            NOS_API.SET_720 = True
                                        if(boot_image == 7):
                                            NOS_API.set_576 = True
                                        test_result = "PASS"
                                        
                                    elif(boot_image >= 8 and boot_image <= 10):
                                            #perguntar e verificar Lemos
                                        time.sleep(2)
                                    elif(boot_image == -1):
                                        TEST_CREATION_API.write_log_to_file("Image is not reproduced correctly on HDMI.")
                                        NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_1080p_noise_error_code \
                                                                            + "; Error message: " + NOS_API.test_cases_results_info.hdmi_1080p_noise_error_message)
                                        error_codes = NOS_API.test_cases_results_info.hdmi_1080p_noise_error_code
                                        error_messages = NOS_API.test_cases_results_info.hdmi_1080p_noise_error_message
                                        NOS_API.set_error_message("Video HDMI")
                                        
                                        NOS_API.add_test_case_result_to_file_report(
                                                    test_result,
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    error_codes,
                                                    error_messages)
                        
                                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                        report_file = NOS_API.create_test_case_log_file(
                                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                        NOS_API.test_cases_results_info.nos_sap_number,
                                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                                        end_time)
                                    
                                        NOS_API.upload_file_report(report_file)
                                        NOS_API.test_cases_results_info.isTestOK = False
                                                                
                                        NOS_API.send_report_over_mqtt_test_plan(
                                                test_result,
                                                end_time,
                                                error_codes,
                                                report_file)
                                                
                                        ## Update test result
                                        TEST_CREATION_API.update_test_result(test_result)
                                        
                                        ## Return DUT to initial state and de-initialize grabber device
                                        NOS_API.deinitialize()
                                        
                                        return                
        
                                    elif(boot_image == -2):
                                        TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                        NOS_API.set_error_message("Reboot")
                                        error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                        error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                        test_result = "FAIL"
                                        
                                        NOS_API.add_test_case_result_to_file_report(
                                                        test_result,
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        error_codes,
                                                        error_messages)
                                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                        report_file = ""
                                        if (test_result != "PASS"):
                                            report_file = NOS_API.create_test_case_log_file(
                                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                                            NOS_API.test_cases_results_info.nos_sap_number,
                                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                                            end_time)
                                            NOS_API.upload_file_report(report_file)
                                            NOS_API.test_cases_results_info.isTestOK = False
                        
                        
                                        ## Update test result
                                        TEST_CREATION_API.update_test_result(test_result)
                                        
                                        ## Return DUT to initial state and de-initialize grabber device
                                        NOS_API.deinitialize()
                                        
                                        NOS_API.send_report_over_mqtt_test_plan(
                                            test_result,
                                            end_time,
                                            error_codes,
                                            report_file)
                        
                                        return
                                    
                                    elif(boot_image == 11):
                                        TEST_CREATION_API.send_ir_rc_command("[INSTALL_CHANNELS]")
                                        TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                                        TEST_CREATION_API.send_ir_rc_command("[BACK]")
                                        TEST_CREATION_API.send_ir_rc_command("[BACK]")
                                        boot_image = NOS_API.wait_for_multiple_pictures(["HDMI_video_1080_ref","HDMI_video_1080_ref1","HDMI_video_1080_ref2"], 45, ["[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]"], [NOS_API.thres,NOS_API.thres,NOS_API.thres])
                                        if(boot_image >= 0 and boot_image <= 2): 
                                            test_result = "PASS"
                                        elif(boot_image == -2):
                                            TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                            NOS_API.set_error_message("Reboot")
                                            error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                            error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                            test_result = "FAIL"
                                            
                                            NOS_API.add_test_case_result_to_file_report(
                                                            test_result,
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            error_codes,
                                                            error_messages)
                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                            report_file = ""
                                            if (test_result != "PASS"):
                                                report_file = NOS_API.create_test_case_log_file(
                                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                NOS_API.test_cases_results_info.mac_using_barcode,
                                                                end_time)
                                                NOS_API.upload_file_report(report_file)
                                                NOS_API.test_cases_results_info.isTestOK = False
                            
                            
                                            ## Update test result
                                            TEST_CREATION_API.update_test_result(test_result)
                                            
                                            ## Return DUT to initial state and de-initialize grabber device
                                            NOS_API.deinitialize()
                                            
                                            NOS_API.send_report_over_mqtt_test_plan(
                                                test_result,
                                                end_time,
                                                error_codes,
                                                report_file)
                            
                                            return
            
                                        elif(boot_image == -1):
                                            TEST_CREATION_API.write_log_to_file("Signal value is lower than threshold")                
                                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.input_signal_error_code \
                                                                                + "; Error message: " + NOS_API.test_cases_results_info.input_signal_error_message)
                                            NOS_API.set_error_message("Sem Sinal")
                                            error_codes = NOS_API.test_cases_results_info.input_signal_error_code
                                            error_messages = NOS_API.test_cases_results_info.input_signal_error_message
                                            time.sleep(2)
                                        
                                    elif(boot_image >= 12 and boot_image <= 14):
                                        NOS_API.display_custom_dialog("Confirme o cabo RF", 1, ["Continuar"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG)
                                        TEST_CREATION_API.send_ir_rc_command("[OK]")
                                        time.sleep(20)
                                        TEST_CREATION_API.send_ir_rc_command("[BACK]")
                                        boot_image = NOS_API.wait_for_multiple_pictures(["HDMI_video_1080_ref","HDMI_video_1080_ref1","HDMI_video_1080_ref2"], 45, ["[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]"], [NOS_API.thres,NOS_API.thres,NOS_API.thres])
                                        if(boot_image >= 0 and boot_image <= 2): 
                                            test_result = "PASS"
                
                                        elif(boot_image == -2):
                                            TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                            NOS_API.set_error_message("Reboot")
                                            error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                            error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                            test_result = "FAIL"
                                            
                                            NOS_API.add_test_case_result_to_file_report(
                                                            test_result,
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            error_codes,
                                                            error_messages)
                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                            report_file = ""
                                            if (test_result != "PASS"):
                                                report_file = NOS_API.create_test_case_log_file(
                                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                NOS_API.test_cases_results_info.mac_using_barcode,
                                                                end_time)
                                                NOS_API.upload_file_report(report_file)
                                                NOS_API.test_cases_results_info.isTestOK = False
                                
                                
                                            ## Update test result
                                            TEST_CREATION_API.update_test_result(test_result)
                                            
                                            ## Return DUT to initial state and de-initialize grabber device
                                            NOS_API.deinitialize()
                                            
                                            NOS_API.send_report_over_mqtt_test_plan(
                                                test_result,
                                                end_time,
                                                error_codes,
                                                report_file)
                                
                                            return
                
                                        elif(boot_image == -1):
                                            TEST_CREATION_API.write_log_to_file("Signal value is lower than threshold")                
                                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.input_signal_error_code \
                                                                                + "; Error message: " + NOS_API.test_cases_results_info.input_signal_error_message)
                                            NOS_API.set_error_message("Sem Sinal")
                                            error_codes = NOS_API.test_cases_results_info.input_signal_error_code
                                            error_messages = NOS_API.test_cases_results_info.input_signal_error_message
                                            time.sleep(2)

                            elif(boot_image == -2):                    
                                                                                                                          
                                TEST_CREATION_API.send_ir_rc_command("[POWER]")
                                time.sleep(4)
                                if (NOS_API.is_signal_present_on_video_source()):
                                    TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                                    boot_image = NOS_API.wait_for_multiple_pictures(["HDMI_video_1080_ref","HDMI_video_1080_ref1","HDMI_video_1080_ref2","HDMI_video_ref","HDMI_video_ref1","HDMI_video_ref2","Banner_1080_ref","HDMI_video_576_ref","No_Signal_ref","No_Signal_576_ref","No_Signal_720_ref"], 45, ["[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[HALF_SCREEN_720p]","[HALF_SCREEN_720p]","[HALF_SCREEN_720p]","[BANNER_1080]","[HALF_SCREEN_576p]","[NO_SIGNAL]","[NO_SIGNAL_576]","[NO_SIGNAL_720]"], [NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,60,NOS_API.thres,60,NOS_API.thres])
                                    if ( boot_image >= 0 and boot_image <= 7):
                                        if(boot_image == 3 or boot_image == 4 or boot_image == 5):
                                            NOS_API.SET_720 = True
                                        if(boot_image == 7):
                                            NOS_API.SET_576 = True
                                        test_result = "PASS"
                                    elif(boot_image >= 8 and boot_image <= 10):
                                        TEST_CREATION_API.send_ir_rc_command("[TV]")
                                        TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                                        boot_image = NOS_API.wait_for_multiple_pictures(["No_Signal_ref","No_Signal_576_ref","No_Signal_720_ref"], 5, ["[NO_SIGNAL]","[NO_SIGNAL_576]","[NO_SIGNAL_720]"], [NOS_API.thres,60,NOS_API.thres])
                                        if ( boot_image >= 0 and boot_image < 3):
                                            TEST_CREATION_API.send_ir_rc_command("[TV]")
                                            NOS_API.display_custom_dialog("Confirme o cabo RF", 1, ["Continuar"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG)
                                        boot_image = NOS_API.wait_for_multiple_pictures(["HDMI_video_1080_ref","HDMI_video_1080_ref1","HDMI_video_1080_ref2","HDMI_video_ref","HDMI_video_ref1","HDMI_video_ref2","Banner_1080_ref","HDMI_video_576_ref","No_Signal_ref","No_Signal_576_ref","No_Signal_720_ref"], 45, ["[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[HALF_SCREEN_720p]","[HALF_SCREEN_720p]","[HALF_SCREEN_720p]","[BANNER_1080]","[HALF_SCREEN_576p]","[NO_SIGNAL]","[NO_SIGNAL_576]","[NO_SIGNAL_720]"], [NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,60,NOS_API.thres,60,NOS_API.thres])
                                        if ( boot_image >= 0 and boot_image <= 7):
                                            if(boot_image == 3 or boot_image == 4 or boot_image == 5):
                                                NOS_API.SET_720 = True
                                            if(boot_image == 7):
                                                NOS_API.SET_576 = True
                                            test_result = "PASS"
                                        elif(boot_image == 3):
                                            TEST_CREATION_API.write_log_to_file("Signal value is lower than threshold")                
                                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.input_signal_error_code \
                                                                                + "; Error message: " + NOS_API.test_cases_results_info.input_signal_error_message)
                                            NOS_API.set_error_message("Sem Sinal")
                                            error_codes = NOS_API.test_cases_results_info.input_signal_error_code
                                            error_messages = NOS_API.test_cases_results_info.input_signal_error_message
                                        elif(boot_image == -1):
                                            #time.sleep(2)
                                            TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                                            boot_image = NOS_API.wait_for_multiple_pictures(["HDMI_video_1080_ref","HDMI_video_1080_ref1","HDMI_video_1080_ref2","HDMI_video_ref","HDMI_video_ref1","HDMI_video_ref2","Banner_1080_ref","HDMI_video_576_ref","No_Signal_ref","No_Signal_576_ref","No_Signal_720_ref"], 45, ["[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[HALF_SCREEN_720p]","[HALF_SCREEN_720p]","[HALF_SCREEN_720p]","[BANNER_1080]","[HALF_SCREEN_576p]","[NO_SIGNAL]","[NO_SIGNAL_576]","[NO_SIGNAL_720]"], [NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,60,NOS_API.thres,60,NOS_API.thres])
                                            if ( boot_image >= 0 and boot_image <= 7):
                                                if(boot_image == 3 or boot_image == 4 or boot_image == 5):
                                                    NOS_API.SET_720 = True
                                                if(boot_image == 7):
                                                    NOS_API.SET_576 = True
                                                test_result = "PASS"
                                            elif(boot_image == -1):
                                                TEST_CREATION_API.write_log_to_file("Image is not reproduced correctly on HDMI.")
                                                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_1080p_noise_error_code \
                                                                                    + "; Error message: " + NOS_API.test_cases_results_info.hdmi_1080p_noise_error_message)
                                                error_codes = NOS_API.test_cases_results_info.hdmi_1080p_noise_error_code
                                                error_messages = NOS_API.test_cases_results_info.hdmi_1080p_noise_error_message
                                                NOS_API.set_error_message("Video HDMI")
                                                
                                                NOS_API.add_test_case_result_to_file_report(
                                                            test_result,
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            error_codes,
                                                            error_messages)
                                
                                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                report_file = NOS_API.create_test_case_log_file(
                                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                NOS_API.test_cases_results_info.mac_using_barcode,
                                                                end_time)
                                            
                                                NOS_API.upload_file_report(report_file)
                                                NOS_API.test_cases_results_info.isTestOK = False
                                                                        
                                                NOS_API.send_report_over_mqtt_test_plan(
                                                        test_result,
                                                        end_time,
                                                        error_codes,
                                                        report_file)
                                                        
                                                ## Update test result
                                                TEST_CREATION_API.update_test_result(test_result)
                                                
                                                ## Return DUT to initial state and de-initialize grabber device
                                                NOS_API.deinitialize()
                                                
                                                return                
                
                                            elif(boot_image == -2):
                                                TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                                NOS_API.set_error_message("Reboot")
                                                error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                                error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                                test_result = "FAIL"
                                                
                                                NOS_API.add_test_case_result_to_file_report(
                                                                test_result,
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                error_codes,
                                                                error_messages)
                                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                report_file = ""
                                                if (test_result != "PASS"):
                                                    report_file = NOS_API.create_test_case_log_file(
                                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                                                    end_time)
                                                    NOS_API.upload_file_report(report_file)
                                                    NOS_API.test_cases_results_info.isTestOK = False
                                
                                
                                                ## Update test result
                                                TEST_CREATION_API.update_test_result(test_result)
                                                
                                                ## Return DUT to initial state and de-initialize grabber device
                                                NOS_API.deinitialize()
                                                
                                                NOS_API.send_report_over_mqtt_test_plan(
                                                    test_result,
                                                    end_time,
                                                    error_codes,
                                                    report_file)
                                
                                                return
                                        elif(boot_image == -2):
                                            TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                            NOS_API.set_error_message("Reboot")
                                            error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                            error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                            test_result = "FAIL"
                                            
                                            NOS_API.add_test_case_result_to_file_report(
                                                            test_result,
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            error_codes,
                                                            error_messages)
                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                            report_file = ""
                                            if (test_result != "PASS"):
                                                report_file = NOS_API.create_test_case_log_file(
                                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                NOS_API.test_cases_results_info.mac_using_barcode,
                                                                end_time)
                                                NOS_API.upload_file_report(report_file)
                                                NOS_API.test_cases_results_info.isTestOK = False
                            
                            
                                            ## Update test result
                                            TEST_CREATION_API.update_test_result(test_result)
                                            
                                            ## Return DUT to initial state and de-initialize grabber device
                                            NOS_API.deinitialize()
                                            
                                            NOS_API.send_report_over_mqtt_test_plan(
                                                test_result,
                                                end_time,
                                                error_codes,
                                                report_file)
                            
                                            return
                                        elif(boot_image >= 8 and boot_image <= 10):
                                            TEST_CREATION_API.write_log_to_file("Signal value is lower than threshold")                
                                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.input_signal_error_code \
                                                                                + "; Error message: " + NOS_API.test_cases_results_info.input_signal_error_message)
                                            NOS_API.set_error_message("Sem Sinal")
                                            error_codes = NOS_API.test_cases_results_info.input_signal_error_code
                                            error_messages = NOS_API.test_cases_results_info.input_signal_error_message
                                            time.sleep(2)
                                            
                                    elif(boot_image == -1):
                                        time.sleep(2)
                                        TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                                        boot_image = NOS_API.wait_for_multiple_pictures(["HDMI_video_1080_ref","HDMI_video_1080_ref1","HDMI_video_1080_ref2","HDMI_video_ref","HDMI_video_ref1","HDMI_video_ref2","Banner_1080_ref","HDMI_video_576_ref","No_Signal_ref","No_Signal_576_ref","No_Signal_720_ref","NOS_ref","Install_ref","Install_ref1","Install_ENG_ref"], 45, ["[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[HALF_SCREEN_720p]","[HALF_SCREEN_720p]","[HALF_SCREEN_720p]","[BANNER_1080]","[HALF_SCREEN_576p]","[NO_SIGNAL]","[NO_SIGNAL_576]","[NO_SIGNAL_720]","[FULL_SCREEN_1080]","[MENU_ICON_1080p]","[MENU_ICON_1080p]","[MENU_ICON_1080p]"], [NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,60,NOS_API.thres,60,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres])
                                        if ( boot_image >= 0 and boot_image <= 7):
                                            if(boot_image == 3 or boot_image == 4 or boot_image == 5):
                                                NOS_API.SET_720 = True
                                            if(boot_image == 7):
                                                NOS_API.SET_576 = True
                                            test_result = "PASS"
                                        elif(boot_image >= 8 and boot_image <= 10):
                                            #perguntar e verificar Lemos
                                            time.sleep(2)
                                        elif(boot_image == -1):
                                            TEST_CREATION_API.write_log_to_file("Image is not reproduced correctly on HDMI.")
                                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_1080p_noise_error_code \
                                                                                + "; Error message: " + NOS_API.test_cases_results_info.hdmi_1080p_noise_error_message)
                                            error_codes = NOS_API.test_cases_results_info.hdmi_1080p_noise_error_code
                                            error_messages = NOS_API.test_cases_results_info.hdmi_1080p_noise_error_message
                                            NOS_API.set_error_message("Video HDMI")
                                            
                                            NOS_API.add_test_case_result_to_file_report(
                                                        test_result,
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        error_codes,
                                                        error_messages)
                            
                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                            report_file = NOS_API.create_test_case_log_file(
                                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                                            NOS_API.test_cases_results_info.nos_sap_number,
                                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                                            end_time)
                                        
                                            NOS_API.upload_file_report(report_file)
                                            NOS_API.test_cases_results_info.isTestOK = False
                                                                    
                                            NOS_API.send_report_over_mqtt_test_plan(
                                                    test_result,
                                                    end_time,
                                                    error_codes,
                                                    report_file)
                                                    
                                            ## Update test result
                                            TEST_CREATION_API.update_test_result(test_result)
                                            
                                            ## Return DUT to initial state and de-initialize grabber device
                                            NOS_API.deinitialize()
                                            
                                            return                
            
                                        elif(boot_image == -2):
                                            TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                            NOS_API.set_error_message("Reboot")
                                            error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                            error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                            test_result = "FAIL"
                                            
                                            NOS_API.add_test_case_result_to_file_report(
                                                            test_result,
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            error_codes,
                                                            error_messages)
                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                            report_file = ""
                                            if (test_result != "PASS"):
                                                report_file = NOS_API.create_test_case_log_file(
                                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                NOS_API.test_cases_results_info.mac_using_barcode,
                                                                end_time)
                                                NOS_API.upload_file_report(report_file)
                                                NOS_API.test_cases_results_info.isTestOK = False
                            
                            
                                            ## Update test result
                                            TEST_CREATION_API.update_test_result(test_result)
                                            
                                            ## Return DUT to initial state and de-initialize grabber device
                                            NOS_API.deinitialize()
                                            
                                            NOS_API.send_report_over_mqtt_test_plan(
                                                test_result,
                                                end_time,
                                                error_codes,
                                                report_file)
                            
                                            return
                                
                                
                                        elif(boot_image == 11):
                                            TEST_CREATION_API.send_ir_rc_command("[INSTALL_CHANNELS]")
                                            TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                                            TEST_CREATION_API.send_ir_rc_command("[BACK]")
                                            TEST_CREATION_API.send_ir_rc_command("[BACK]")
                                            boot_image = NOS_API.wait_for_multiple_pictures(["HDMI_video_1080_ref","HDMI_video_1080_ref1","HDMI_video_1080_ref2"], 45, ["[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]"], [NOS_API.thres,NOS_API.thres,NOS_API.thres])
                                            if(boot_image >= 0 and boot_image <= 2): 
                                                test_result = "PASS"
                                            elif(boot_image == -2):
                                                TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                                NOS_API.set_error_message("Reboot")
                                                error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                                error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                                test_result = "FAIL"
                                                
                                                NOS_API.add_test_case_result_to_file_report(
                                                                test_result,
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                error_codes,
                                                                error_messages)
                                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                report_file = ""
                                                if (test_result != "PASS"):
                                                    report_file = NOS_API.create_test_case_log_file(
                                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                                                    end_time)
                                                    NOS_API.upload_file_report(report_file)
                                                    NOS_API.test_cases_results_info.isTestOK = False
                                
                                
                                                ## Update test result
                                                TEST_CREATION_API.update_test_result(test_result)
                                                
                                                ## Return DUT to initial state and de-initialize grabber device
                                                NOS_API.deinitialize()
                                                
                                                NOS_API.send_report_over_mqtt_test_plan(
                                                    test_result,
                                                    end_time,
                                                    error_codes,
                                                    report_file)
                                
                                                return
                
                                            elif(boot_image == -1):
                                                TEST_CREATION_API.write_log_to_file("Signal value is lower than threshold")                
                                                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.input_signal_error_code \
                                                                                    + "; Error message: " + NOS_API.test_cases_results_info.input_signal_error_message)
                                                NOS_API.set_error_message("Sem Sinal")
                                                error_codes = NOS_API.test_cases_results_info.input_signal_error_code
                                                error_messages = NOS_API.test_cases_results_info.input_signal_error_message
                                                time.sleep(2)
                                            
                                        elif(boot_image >= 12 and boot_image <= 14):
                                            NOS_API.display_custom_dialog("Confirme o cabo RF", 1, ["Continuar"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG)
                                            TEST_CREATION_API.send_ir_rc_command("[OK]")
                                            time.sleep(20)
                                            TEST_CREATION_API.send_ir_rc_command("[BACK]")
                                            boot_image = NOS_API.wait_for_multiple_pictures(["HDMI_video_1080_ref","HDMI_video_1080_ref1","HDMI_video_1080_ref2"], 45, ["[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]"], [NOS_API.thres,NOS_API.thres,NOS_API.thres])
                                            if(boot_image >= 0 and boot_image <= 2): 
                                                test_result = "PASS"
                                            elif(boot_image == -2):
                                                TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                                NOS_API.set_error_message("Reboot")
                                                error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                                error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                                test_result = "FAIL"
                                                
                                                NOS_API.add_test_case_result_to_file_report(
                                                                test_result,
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                error_codes,
                                                                error_messages)
                                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                report_file = ""
                                                if (test_result != "PASS"):
                                                    report_file = NOS_API.create_test_case_log_file(
                                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                                                    end_time)
                                                    NOS_API.upload_file_report(report_file)
                                                    NOS_API.test_cases_results_info.isTestOK = False
                                    
                                    
                                                ## Update test result
                                                TEST_CREATION_API.update_test_result(test_result)
                                                
                                                ## Return DUT to initial state and de-initialize grabber device
                                                NOS_API.deinitialize()
                                                
                                                NOS_API.send_report_over_mqtt_test_plan(
                                                    test_result,
                                                    end_time,
                                                    error_codes,
                                                    report_file)
                                    
                                                return
                    
                                            elif(boot_image == -1):
                                                TEST_CREATION_API.write_log_to_file("Signal value is lower than threshold")                
                                                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.input_signal_error_code \
                                                                                    + "; Error message: " + NOS_API.test_cases_results_info.input_signal_error_message)
                                                NOS_API.set_error_message("Sem Sinal")
                                                error_codes = NOS_API.test_cases_results_info.input_signal_error_code
                                                error_messages = NOS_API.test_cases_results_info.input_signal_error_message
                                                time.sleep(2)
                                    elif(boot_image == -2):
                                        TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                        NOS_API.set_error_message("Reboot")
                                        error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                        error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                        test_result = "FAIL"
                                        
                                        NOS_API.add_test_case_result_to_file_report(
                                                        test_result,
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        error_codes,
                                                        error_messages)
                                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                        report_file = ""
                                        if (test_result != "PASS"):
                                            report_file = NOS_API.create_test_case_log_file(
                                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                                            NOS_API.test_cases_results_info.nos_sap_number,
                                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                                            end_time)
                                            NOS_API.upload_file_report(report_file)
                                            NOS_API.test_cases_results_info.isTestOK = False
                        
                        
                                        ## Update test result
                                        TEST_CREATION_API.update_test_result(test_result)
                                        
                                        ## Return DUT to initial state and de-initialize grabber device
                                        NOS_API.deinitialize()
                                        
                                        NOS_API.send_report_over_mqtt_test_plan(
                                            test_result,
                                            end_time,
                                            error_codes,
                                            report_file)
                        
                                        return
                                        
                                else:
                                    TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                    NOS_API.set_error_message("Reboot")
                                    error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                    error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                    test_result = "FAIL"
                                    
                                    NOS_API.add_test_case_result_to_file_report(
                                                    test_result,
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    error_codes,
                                                    error_messages)
                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                    report_file = ""
                                    if (test_result != "PASS"):
                                        report_file = NOS_API.create_test_case_log_file(
                                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                        NOS_API.test_cases_results_info.nos_sap_number,
                                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                                        end_time)
                                        NOS_API.upload_file_report(report_file)
                                        NOS_API.test_cases_results_info.isTestOK = False
                    
                    
                                    ## Update test result
                                    TEST_CREATION_API.update_test_result(test_result)
                                    
                                    ## Return DUT to initial state and de-initialize grabber device
                                    NOS_API.deinitialize()
                                    
                                    NOS_API.send_report_over_mqtt_test_plan(
                                        test_result,
                                        end_time,
                                        error_codes,
                                        report_file)
                    
                                    return

                        else:
                            TEST_CREATION_API.send_ir_rc_command("[POWER]")
                            time.sleep(4)
                            if (NOS_API.is_signal_present_on_video_source()):
                                TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                                boot_image = NOS_API.wait_for_multiple_pictures(["HDMI_video_1080_ref","HDMI_video_1080_ref1","HDMI_video_1080_ref2","HDMI_video_ref","HDMI_video_ref1","HDMI_video_ref2","Banner_1080_ref","HDMI_video_576_ref","No_Signal_ref","No_Signal_576_ref","No_Signal_720_ref","LOAD_FAIL_ref"], 45, ["[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[HALF_SCREEN_720p]","[HALF_SCREEN_720p]","[HALF_SCREEN_720p]","[BANNER_1080]","[HALF_SCREEN_576p]","[NO_SIGNAL]","[NO_SIGNAL_576]","[NO_SIGNAL_720]","[FULL_SCREEN_1080]"], [NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,60,NOS_API.thres,60,NOS_API.thres,NOS_API.thres])
                                if ( boot_image >= 0 and boot_image <= 7):
                                    if(boot_image == 3 or boot_image == 4 or boot_image == 5):
                                        NOS_API.SET_720 = True
                                    if(boot_image == 7):
                                        NOS_API.SET_576 = True
                                    test_result = "PASS"
                                elif(boot_image >= 8 and boot_image <= 10):
                                    TEST_CREATION_API.send_ir_rc_command("[TV]")
                                    TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                                    boot_image = NOS_API.wait_for_multiple_pictures(["No_Signal_ref","No_Signal_576_ref","No_Signal_720_ref"], 5, ["[NO_SIGNAL]","[NO_SIGNAL_576]","[NO_SIGNAL_720]"], [NOS_API.thres,60,NOS_API.thres])
                                    if ( boot_image >= 0 and boot_image < 3):
                                        TEST_CREATION_API.send_ir_rc_command("[TV]")
                                        NOS_API.display_custom_dialog("Confirme o cabo RF", 1, ["Continuar"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG)
                                    boot_image = NOS_API.wait_for_multiple_pictures(["HDMI_video_1080_ref","HDMI_video_1080_ref1","HDMI_video_1080_ref2","HDMI_video_ref","HDMI_video_ref1","HDMI_video_ref2","Banner_1080_ref","HDMI_video_576_ref","No_Signal_ref","No_Signal_576_ref","No_Signal_720_ref"], 45, ["[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[HALF_SCREEN_720p]","[HALF_SCREEN_720p]","[HALF_SCREEN_720p]","[BANNER_1080]","[HALF_SCREEN_576p]","[NO_SIGNAL]","[NO_SIGNAL_576]","[NO_SIGNAL_720]"], [NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,60,NOS_API.thres,60,NOS_API.thres])

                                    if ( boot_image >= 0 and boot_image <= 7):
                                        if(boot_image == 3 or boot_image == 4 or boot_image == 5):
                                            NOS_API.SET_720 = True
                                        if(boot_image == 7):
                                            NOS_API.SET_576 = True
                                        test_result = "PASS"
                                        
                                    elif(boot_image >= 8 and boot_image <= 10):
                                        TEST_CREATION_API.write_log_to_file("Signal value is lower than threshold")
                    
                                        NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.input_signal_error_code \
                                                                            + "; Error message: " + NOS_API.test_cases_results_info.input_signal_error_message)
                                        NOS_API.set_error_message("Sem Sinal")
                                        error_codes = NOS_API.test_cases_results_info.input_signal_error_code
                                        error_messages = NOS_API.test_cases_results_info.input_signal_error_message
                                    elif(boot_image == -1):
                                        #time.sleep(2)
                                        TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                                        boot_image = NOS_API.wait_for_multiple_pictures(["HDMI_video_1080_ref","HDMI_video_1080_ref1","HDMI_video_1080_ref2","HDMI_video_ref","HDMI_video_ref1","HDMI_video_ref2","Banner_1080_ref","HDMI_video_576_ref","No_Signal_ref","No_Signal_576_ref","No_Signal_720_ref"], 45, ["[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[HALF_SCREEN_720p]","[HALF_SCREEN_720p]","[HALF_SCREEN_720p]","[BANNER_1080]","[HALF_SCREEN_576p]","[NO_SIGNAL]","[NO_SIGNAL_576]","[NO_SIGNAL_720]"], [NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,60,NOS_API.thres,60,NOS_API.thres])

                                        if ( boot_image >= 0 and boot_image <= 7):
                                            if(boot_image == 3 or boot_image == 4 or boot_image == 5):
                                                NOS_API.SET_720 = True
                                            if(boot_image == 7):
                                                NOS_API.SET_576 = True
                                            test_result = "PASS"
                                        elif(boot_image == -1):
                                            TEST_CREATION_API.write_log_to_file("Image is not reproduced correctly on HDMI.")
                                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_1080p_noise_error_code \
                                                                                + "; Error message: " + NOS_API.test_cases_results_info.hdmi_1080p_noise_error_message)
                                            error_codes = NOS_API.test_cases_results_info.hdmi_1080p_noise_error_code
                                            error_messages = NOS_API.test_cases_results_info.hdmi_1080p_noise_error_message
                                            NOS_API.set_error_message("Video HDMI")
                                            
                                            NOS_API.add_test_case_result_to_file_report(
                                                        test_result,
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        error_codes,
                                                        error_messages)
                            
                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                            report_file = NOS_API.create_test_case_log_file(
                                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                                            NOS_API.test_cases_results_info.nos_sap_number,
                                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                                            end_time)
                                        
                                            NOS_API.upload_file_report(report_file)
                                            NOS_API.test_cases_results_info.isTestOK = False
                                                                    
                                            NOS_API.send_report_over_mqtt_test_plan(
                                                    test_result,
                                                    end_time,
                                                    error_codes,
                                                    report_file)
                                                    
                                            ## Update test result
                                            TEST_CREATION_API.update_test_result(test_result)
                                            
                                            ## Return DUT to initial state and de-initialize grabber device
                                            NOS_API.deinitialize()
                                            
                                            return                
            
                                        elif(boot_image == -2):
                                            TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                            NOS_API.set_error_message("Reboot")
                                            error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                            error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                            test_result = "FAIL"
                                            
                                            NOS_API.add_test_case_result_to_file_report(
                                                            test_result,
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            error_codes,
                                                            error_messages)
                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                            report_file = ""
                                            if (test_result != "PASS"):
                                                report_file = NOS_API.create_test_case_log_file(
                                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                NOS_API.test_cases_results_info.mac_using_barcode,
                                                                end_time)
                                                NOS_API.upload_file_report(report_file)
                                                NOS_API.test_cases_results_info.isTestOK = False
                            
                            
                                            ## Update test result
                                            TEST_CREATION_API.update_test_result(test_result)
                                            
                                            ## Return DUT to initial state and de-initialize grabber device
                                            NOS_API.deinitialize()
                                            
                                            NOS_API.send_report_over_mqtt_test_plan(
                                                test_result,
                                                end_time,
                                                error_codes,
                                                report_file)
                            
                                            return
                                    elif(boot_image == -2):
                                        TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                        NOS_API.set_error_message("Reboot")
                                        error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                        error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                        test_result = "FAIL"
                                        
                                        NOS_API.add_test_case_result_to_file_report(
                                                        test_result,
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        error_codes,
                                                        error_messages)
                                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                        report_file = ""
                                        if (test_result != "PASS"):
                                            report_file = NOS_API.create_test_case_log_file(
                                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                                            NOS_API.test_cases_results_info.nos_sap_number,
                                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                                            end_time)
                                            NOS_API.upload_file_report(report_file)
                                            NOS_API.test_cases_results_info.isTestOK = False
                        
                        
                                        ## Update test result
                                        TEST_CREATION_API.update_test_result(test_result)
                                        
                                        ## Return DUT to initial state and de-initialize grabber device
                                        NOS_API.deinitialize()
                                        
                                        NOS_API.send_report_over_mqtt_test_plan(
                                            test_result,
                                            end_time,
                                            error_codes,
                                            report_file)
                        
                                        return
                                
                                elif(boot_image == 11):
                                    TEST_CREATION_API.write_log_to_file("Doesn't upgrade")            
                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.upgrade_nok_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.upgrade_nok_error_message)                                        
                                    NOS_API.set_error_message("Não Actualiza") 
                                    error_codes =  NOS_API.test_cases_results_info.upgrade_nok_error_code
                                    error_messages = NOS_API.test_cases_results_info.upgrade_nok_error_message                               
                                    test_result = "FAIL" 
                                elif(boot_image == -1):
                                    time.sleep(2)
                                    TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                                    boot_image = NOS_API.wait_for_multiple_pictures(["HDMI_video_1080_ref","HDMI_video_1080_ref1","HDMI_video_1080_ref2","HDMI_video_ref","HDMI_video_ref1","HDMI_video_ref2","Banner_1080_ref","HDMI_video_576_ref","No_Signal_ref","No_Signal_576_ref","No_Signal_720_ref","NOS_ref","Install_ref","Install_ref1","Install_ENG_ref"], 45, ["[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[HALF_SCREEN_720p]","[HALF_SCREEN_720p]","[HALF_SCREEN_720p]","[BANNER_1080]","[HALF_SCREEN_576p]","[NO_SIGNAL]","[NO_SIGNAL_576]","[NO_SIGNAL_720]","[FULL_SCREEN_1080]","[MENU_ICON_1080p]","[MENU_ICON_1080p]","[MENU_ICON_1080p]"], [NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,60,NOS_API.thres,60,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres,NOS_API.thres])
                                    if ( boot_image >= 0 and boot_image <= 7):
                                        if(boot_image == 3 or boot_image == 4 or boot_image == 5):
                                            NOS_API.SET_720 = True
                                        if(boot_image == 7):
                                            NOS_API.SET_576 = True
                                        test_result = "PASS"
                                    elif(boot_image == -1):
                                        TEST_CREATION_API.write_log_to_file("Image is not reproduced correctly on HDMI.")
                                        NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_1080p_noise_error_code \
                                                                            + "; Error message: " + NOS_API.test_cases_results_info.hdmi_1080p_noise_error_message)
                                        error_codes = NOS_API.test_cases_results_info.hdmi_1080p_noise_error_code
                                        error_messages = NOS_API.test_cases_results_info.hdmi_1080p_noise_error_message
                                        NOS_API.set_error_message("Video HDMI")
                                        
                                        NOS_API.add_test_case_result_to_file_report(
                                                    test_result,
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    error_codes,
                                                    error_messages)
                        
                                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                        report_file = NOS_API.create_test_case_log_file(
                                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                        NOS_API.test_cases_results_info.nos_sap_number,
                                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                                        end_time)
                                    
                                        NOS_API.upload_file_report(report_file)
                                        NOS_API.test_cases_results_info.isTestOK = False
                                                                
                                        NOS_API.send_report_over_mqtt_test_plan(
                                                test_result,
                                                end_time,
                                                error_codes,
                                                report_file)
                                                
                                        ## Update test result
                                        TEST_CREATION_API.update_test_result(test_result)
                                        
                                        ## Return DUT to initial state and de-initialize grabber device
                                        NOS_API.deinitialize()
                                        
                                        return                
        
                                    elif(boot_image == -2):
                                        TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                        NOS_API.set_error_message("Reboot")
                                        error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                        error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                        test_result = "FAIL"
                                        
                                        NOS_API.add_test_case_result_to_file_report(
                                                        test_result,
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        error_codes,
                                                        error_messages)
                                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                        report_file = ""
                                        if (test_result != "PASS"):
                                            report_file = NOS_API.create_test_case_log_file(
                                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                                            NOS_API.test_cases_results_info.nos_sap_number,
                                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                                            end_time)
                                            NOS_API.upload_file_report(report_file)
                                            NOS_API.test_cases_results_info.isTestOK = False
                        
                        
                                        ## Update test result
                                        TEST_CREATION_API.update_test_result(test_result)
                                        
                                        ## Return DUT to initial state and de-initialize grabber device
                                        NOS_API.deinitialize()
                                        
                                        NOS_API.send_report_over_mqtt_test_plan(
                                            test_result,
                                            end_time,
                                            error_codes,
                                            report_file)
                        
                                        return

                                    elif(boot_image == 11):
                                        TEST_CREATION_API.send_ir_rc_command("[INSTALL_CHANNELS]")
                                        TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                                        TEST_CREATION_API.send_ir_rc_command("[BACK]")
                                        TEST_CREATION_API.send_ir_rc_command("[BACK]")
                                        boot_image = NOS_API.wait_for_multiple_pictures(["HDMI_video_1080_ref","HDMI_video_1080_ref1","HDMI_video_1080_ref2"], 45, ["[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]"], [NOS_API.thres,NOS_API.thres,NOS_API.thres])
                                        if(boot_image >= 0 and boot_image <= 2): 
                                            test_result = "PASS"
                                        elif(boot_image == -2):
                                            TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                            NOS_API.set_error_message("Reboot")
                                            error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                            error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                            test_result = "FAIL"
                                            
                                            NOS_API.add_test_case_result_to_file_report(
                                                            test_result,
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            error_codes,
                                                            error_messages)
                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                            report_file = ""
                                            if (test_result != "PASS"):
                                                report_file = NOS_API.create_test_case_log_file(
                                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                NOS_API.test_cases_results_info.mac_using_barcode,
                                                                end_time)
                                                NOS_API.upload_file_report(report_file)
                                                NOS_API.test_cases_results_info.isTestOK = False
                            
                            
                                            ## Update test result
                                            TEST_CREATION_API.update_test_result(test_result)
                                            
                                            ## Return DUT to initial state and de-initialize grabber device
                                            NOS_API.deinitialize()
                                            
                                            NOS_API.send_report_over_mqtt_test_plan(
                                                test_result,
                                                end_time,
                                                error_codes,
                                                report_file)
                            
                                            return
            
                                        elif(boot_image == -1):
                                            TEST_CREATION_API.write_log_to_file("Signal value is lower than threshold")                
                                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.input_signal_error_code \
                                                                                + "; Error message: " + NOS_API.test_cases_results_info.input_signal_error_message)
                                            NOS_API.set_error_message("Sem Sinal")
                                            error_codes = NOS_API.test_cases_results_info.input_signal_error_code
                                            error_messages = NOS_API.test_cases_results_info.input_signal_error_message
                                            time.sleep(2)
                                        
                                    elif(boot_image >= 12 and boot_image <= 13):
                                        NOS_API.display_custom_dialog("Confirme o cabo RF", 1, ["Continuar"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG)
                                        TEST_CREATION_API.send_ir_rc_command("[OK]")
                                        boot_image = NOS_API.wait_for_multiple_pictures(["HDMI_video_1080_ref","HDMI_video_1080_ref1","HDMI_video_1080_ref2"], 45, ["[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]","[HALF_SCREEN_1080p]"], [NOS_API.thres,NOS_API.thres,NOS_API.thres])
                                        if(boot_image >= 0 and boot_image <= 2): 
                                            test_result = "PASS"
                
                                        elif(boot_image == -2):
                                            TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                            NOS_API.set_error_message("Reboot")
                                            error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                            error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                            test_result = "FAIL"
                                            
                                            NOS_API.add_test_case_result_to_file_report(
                                                            test_result,
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            error_codes,
                                                            error_messages)
                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                            report_file = ""
                                            if (test_result != "PASS"):
                                                report_file = NOS_API.create_test_case_log_file(
                                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                NOS_API.test_cases_results_info.mac_using_barcode,
                                                                end_time)
                                                NOS_API.upload_file_report(report_file)
                                                NOS_API.test_cases_results_info.isTestOK = False
                                
                                
                                            ## Update test result
                                            TEST_CREATION_API.update_test_result(test_result)
                                            
                                            ## Return DUT to initial state and de-initialize grabber device
                                            NOS_API.deinitialize()
                                            
                                            NOS_API.send_report_over_mqtt_test_plan(
                                                test_result,
                                                end_time,
                                                error_codes,
                                                report_file)
                                
                                            return
                
                                        elif(boot_image == -1):
                                            TEST_CREATION_API.write_log_to_file("Signal value is lower than threshold")                
                                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.input_signal_error_code \
                                                                                + "; Error message: " + NOS_API.test_cases_results_info.input_signal_error_message)
                                            NOS_API.set_error_message("Sem Sinal")
                                            error_codes = NOS_API.test_cases_results_info.input_signal_error_code
                                            error_messages = NOS_API.test_cases_results_info.input_signal_error_message
                                            time.sleep(2)

                                elif(boot_image == -2):
                                    TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                    NOS_API.set_error_message("Reboot")
                                    error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                    error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                    test_result = "FAIL"
                                    
                                    NOS_API.add_test_case_result_to_file_report(
                                                    test_result,
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    error_codes,
                                                    error_messages)
                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                    report_file = ""
                                    if (test_result != "PASS"):
                                        report_file = NOS_API.create_test_case_log_file(
                                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                        NOS_API.test_cases_results_info.nos_sap_number,
                                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                                        end_time)
                                        NOS_API.upload_file_report(report_file)
                                        NOS_API.test_cases_results_info.isTestOK = False
                    
                    
                                    ## Update test result
                                    TEST_CREATION_API.update_test_result(test_result)
                                    
                                    ## Return DUT to initial state and de-initialize grabber device
                                    NOS_API.deinitialize()
                                    
                                    NOS_API.send_report_over_mqtt_test_plan(
                                        test_result,
                                        end_time,
                                        error_codes,
                                        report_file)
                    
                                    return
                                    
                            else:
                                TEST_CREATION_API.write_log_to_file("No boot")
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.no_boot_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.no_boot_error_message)
                                NOS_API.set_error_message("Não arranca")
                                error_codes =  NOS_API.test_cases_results_info.no_boot_error_code
                                error_messages = NOS_API.test_cases_results_info.no_boot_error_message
                                NOS_API.add_test_case_result_to_file_report(
                                            test_result,
                                            "- - - - - - - - - - - - - - - - - - - -",
                                            "- - - - - - - - - - - - - - - - - - - -",
                                            error_codes,
                                            error_messages)
                
                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                report_file = NOS_API.create_test_case_log_file(
                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                NOS_API.test_cases_results_info.mac_using_barcode,
                                                end_time)
                            
                                NOS_API.upload_file_report(report_file)
                                NOS_API.test_cases_results_info.isTestOK = False
                                                        
                                NOS_API.send_report_over_mqtt_test_plan(
                                        test_result,
                                        end_time,
                                        error_codes,
                                        report_file)
                                        
                                ## Update test result
                                TEST_CREATION_API.update_test_result(test_result)
                                
                                ## Return DUT to initial state and de-initialize grabber device
                                NOS_API.deinitialize()
                                
                                return   
            
                    else: 
                        Comparison = NOS_API.wait_for_multiple_pictures(["OTA_Setup_ref"], 3, ["[OTA_SETUP]"], [NOS_API.thres])
                        if (Comparison == 0):
                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.ir_nok_error_code \
                                        + "; Error message: " + NOS_API.test_cases_results_info.ir_nok_error_message)
                            NOS_API.set_error_message("IR")
                            error_codes = NOS_API.test_cases_results_info.ir_nok_error_code
                            error_messages = NOS_API.test_cases_results_info.ir_nok_error_message
                        else:
                            TEST_CREATION_API.write_log_to_file("Doesn't upgrade")            
                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.upgrade_nok_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.upgrade_nok_error_message)                                        
                            NOS_API.set_error_message("Não Actualiza") 
                            error_codes =  NOS_API.test_cases_results_info.upgrade_nok_error_code
                            error_messages = NOS_API.test_cases_results_info.upgrade_nok_error_message                               
                            test_result = "FAIL"    
        
            System_Failure = 2
            
        except Exception as error:
            if(System_Failure == 0):
                System_Failure = System_Failure + 1 
                NOS_API.Inspection = True
                if(System_Failure == 1):
                    try:
                        TEST_CREATION_API.write_log_to_file(error)
                    except: 
                        pass
                    try:
                        ## Return DUT to initial state and de-initialize grabber device
                        NOS_API.deinitialize()
                        TEST_CREATION_API.write_log_to_file(error)
                    except: 
                        pass
                if (NOS_API.configure_power_switch_by_inspection()):
                    if not(NOS_API.power_off()): 
                        TEST_CREATION_API.write_log_to_file("Comunication with PowerSwitch Fails")
                        ## Update test result
                        TEST_CREATION_API.update_test_result(test_result)
                        NOS_API.set_error_message("Inspection")
                        
                        NOS_API.add_test_case_result_to_file_report(
                                        test_result,
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        error_codes,
                                        error_messages)
                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                        report_file = ""
                        if (test_result != "PASS"):
                            report_file = NOS_API.create_test_case_log_file(
                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                            NOS_API.test_cases_results_info.nos_sap_number,
                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                            "",
                                            end_time)
                            NOS_API.upload_file_report(report_file)
                            NOS_API.test_cases_results_info.isTestOK = False
                        
                        
                        ## Update test result
                        TEST_CREATION_API.update_test_result(test_result)
                    
                        ## Return DUT to initial state and de-initialize grabber device
                        NOS_API.deinitialize()
                        
                        NOS_API.send_report_over_mqtt_test_plan(
                                    test_result,
                                    end_time,
                                    error_codes,
                                    report_file)

                        return
                    time.sleep(10)
                    ## Power on STB with energenie
                    if not(NOS_API.power_on()):
                        TEST_CREATION_API.write_log_to_file("Comunication with PowerSwitch Fails")
                        ## Update test result
                        TEST_CREATION_API.update_test_result(test_result)
                        NOS_API.set_error_message("Inspection")
                        
                        NOS_API.add_test_case_result_to_file_report(
                                        test_result,
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        error_codes,
                                        error_messages)
                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                        report_file = ""
                        if (test_result != "PASS"):
                            report_file = NOS_API.create_test_case_log_file(
                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                            NOS_API.test_cases_results_info.nos_sap_number,
                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                            "",
                                            end_time)
                            NOS_API.upload_file_report(report_file)
                            NOS_API.test_cases_results_info.isTestOK = False
                        
                        test_result = "FAIL"
                        
                        ## Update test result
                        TEST_CREATION_API.update_test_result(test_result)
                    
                        ## Return DUT to initial state and de-initialize grabber device
                        NOS_API.deinitialize()
                        
                        NOS_API.send_report_over_mqtt_test_plan(
                                test_result,
                                end_time,
                                error_codes,
                                report_file)
                        
                        return
                    time.sleep(10)
                else:
                    TEST_CREATION_API.write_log_to_file("Incorrect test place name")
                    
                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.power_switch_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.power_switch_error_message)
                    NOS_API.set_error_message("Inspection")
                    
                    NOS_API.add_test_case_result_to_file_report(
                                    test_result,
                                    "- - - - - - - - - - - - - - - - - - - -",
                                    "- - - - - - - - - - - - - - - - - - - -",
                                    error_codes,
                                    error_messages)
                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  
                    report_file = ""
                    if (test_result != "PASS"):
                        report_file = NOS_API.create_test_case_log_file(
                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                        NOS_API.test_cases_results_info.nos_sap_number,
                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                        "",
                                        end_time)
                        NOS_API.upload_file_report(report_file)
                        NOS_API.test_cases_results_info.isTestOK = False
                    
                    test_result = "FAIL"
                    ## Update test result
                    TEST_CREATION_API.update_test_result(test_result)
                    
                
                    ## Return DUT to initial state and de-initialize grabber device
                    NOS_API.deinitialize()
                    
                    NOS_API.send_report_over_mqtt_test_plan(
                        test_result,
                        end_time,
                        error_codes,
                        report_file)
                    
                    return
                
                NOS_API.Inspection = False
            else:
                test_result = "FAIL"
                TEST_CREATION_API.write_log_to_file(error)
                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.grabber_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.grabber_error_message)
                error_codes = NOS_API.test_cases_results_info.grabber_error_code
                error_messages = NOS_API.test_cases_results_info.grabber_error_message
                NOS_API.set_error_message("Inspection") 
                System_Failure = 2            

    
        
    NOS_API.add_test_case_result_to_file_report(
                    test_result,
                    "- - - - - - - - - - - - - - - - - - - -",
                    "- - - - - - - - - - - - - - - - - - - -",
                    error_codes,
                    error_messages)
    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
    report_file = ""    
    if (test_result != "PASS"):
        report_file = NOS_API.create_test_case_log_file(
                        NOS_API.test_cases_results_info.s_n_using_barcode,
                        NOS_API.test_cases_results_info.nos_sap_number,
                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                        NOS_API.test_cases_results_info.mac_using_barcode,
                        end_time)
        NOS_API.upload_file_report(report_file)
        NOS_API.test_cases_results_info.isTestOK = False
        
        NOS_API.send_report_over_mqtt_test_plan(
                test_result,
                end_time,
                error_codes,
                report_file)
    
    
    ## Update test result
    TEST_CREATION_API.update_test_result(test_result)

    ## Return DUT to initial state and de-initialize grabber device
    NOS_API.deinitialize()
    