# -*- coding: utf-8 -*-
# Test name = Autodiag1
# Test description = Autodiag

from datetime import datetime
from time import gmtime, strftime
import time

import TEST_CREATION_API
#import shutil
#shutil.copyfile('\\\\bbtfs\\RT-Executor\\API\\NOS_API.py', 'NOS_API.py')
import NOS_API

def runTest():
    
    System_Failure = 0
    
    while(System_Failure < 2):
    
        try:   
            if(System_Failure == 1):
                ## Initialize grabber device
                TEST_CREATION_API.initialize_grabber()
                
                TEST_CREATION_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.HDMI1)
                time.sleep(2)    
                
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
                time.sleep(2)
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
                time.sleep(10)
                if not(NOS_API.is_signal_present_on_video_source()):       
                    TEST_CREATION_API.send_ir_rc_command("[POWER]")
                    time.sleep(5)
                    if not(NOS_API.is_signal_present_on_video_source()): 
                        NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.ir_nok_error_code \
                                    + "; Error message: " + NOS_API.test_cases_results_info.ir_nok_error_message)
                        NOS_API.set_error_message("IR")
                        error_codes = NOS_API.test_cases_results_info.ir_nok_error_code
                        error_messages = NOS_API.test_cases_results_info.ir_nok_error_message
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
            ## Set test result default to FAIL
            test_result = "FAIL"
            
            error_codes = ""
            error_messages = ""
            Led_result = False
            USB_result = False
            Retest = False
            counter = 0
            if(System_Failure == 0):
                ## Initialize grabber device
                TEST_CREATION_API.initialize_grabber()
                
                TEST_CREATION_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.HDMI1)
                time.sleep(2)        

            ## Enter autodiag        
            TEST_CREATION_API.send_ir_rc_command("[ENTER_AUTODIAG]")
            
            if (NOS_API.wait_for_multiple_pictures(["Led_Vermelho_Canal_ref", "Led_Vermelho_Black_ref", "Led_Vermelho_Canal_720_ref"], 45, ["[LED_Question]","[LED_Question]", "[LED_Question_720]"], [TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD, 70, TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD]) != -1):
                while(counter < 2):
                    if not(Led_result):
                        if (NOS_API.display_custom_dialog("O Led Power est\xe1 Vermelho?", 2, ["OK", "NOK"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "OK"):
                            TEST_CREATION_API.send_ir_rc_command("[OK]")
                            time.sleep(1)
                            if (NOS_API.display_custom_dialog("O Led Power est\xe1 Verde?", 2, ["OK", "NOK"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "OK"):
                                TEST_CREATION_API.send_ir_rc_command("[OK]")
                                time.sleep(1)
                                if (NOS_API.wait_for_multiple_pictures(["USB_Canal_ref", "USB_Black_ref", "USB_Canal_720_ref"], 45, ["[USB_Question]","[USB_Question]", "[USB_Question_720]" ], [TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD, 70, TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD]) != -1):                                
                                    TEST_CREATION_API.send_ir_rc_command("[OK]")
                                    time.sleep(1)
                                    if(Retest):
                                        time.sleep(15)
                                    if (NOS_API.wait_for_multiple_pictures(["OK_ref", "NOK_ref"], 45, ["[AD_RESULT]", "[AD_RESULT]"], [TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD, 70]) != -1):
                                        if not(NOS_API.grab_picture("AutoDiag_Result")):
                                            TEST_CREATION_API.write_log_to_file("HDMI NOK")
                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                            NOS_API.set_error_message("Video HDMI")
                                            error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                            error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                            
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
                        
                                        video_result1 = NOS_API.compare_pictures("OK_ref", "AutoDiag_Result", "[AD_RESULT]")
                                        video_result2 = NOS_API.compare_pictures("NOK_ref", "AutoDiag_Result", "[AD_RESULT]")
                                        if (video_result1 > TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                                            test_result = "PASS"
                                            counter = 4
                                            NOS_API.Send_Serial_Key("d", "feito")
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
                                        else: 
                                            final_result1 = NOS_API.compare_pictures("OK_ref", "AutoDiag_Result", "[LED_RESULT]")
                                            final_result2 = NOS_API.compare_pictures("OK_ref", "AutoDiag_Result", "[USB_RESULT]")
                                            final_result3 = NOS_API.compare_pictures("OK_ref", "AutoDiag_Result", "[FLASH_RESULT]")
                                            final_result4 = NOS_API.compare_pictures("OK_ref", "AutoDiag_Result", "[ETH_RESULT]")
                                            final_result5 = NOS_API.compare_pictures("OK_ref", "AutoDiag_Result", "[FR_RESULT]")
                                            
                                            if(video_result2 > TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD and Retest == False):
                                                Retest = True
                                            if(final_result1 > TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD and Led_result == False):
                                                Led_result = True
                                            if(final_result2 < TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                                                NOS_API.display_custom_dialog("Confirme o USB.", 2, ["OK", "NOK"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG)
                                            if(final_result4 < TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                                                NOS_API.display_custom_dialog("Confirme o cabo ETH.", 2, ["OK", "NOK"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG)
                                            counter += 1
                                            TEST_CREATION_API.send_ir_rc_command("[MENU]")
                                            #TEST_CREATION_API.send_ir_rc_command("[OK]")    
                                    else:
                                        TEST_CREATION_API.write_log_to_file("Image is not reproduced correctly on HDMI.")
                                        NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_720p_noise_error_code \
                                                                            + "; Error message: " + NOS_API.test_cases_results_info.hdmi_720p_noise_error_message)
                                        error_codes = NOS_API.test_cases_results_info.hdmi_720p_noise_error_code
                                        error_messages = NOS_API.test_cases_results_info.hdmi_720p_noise_error_message
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
                                else:
                                    TEST_CREATION_API.write_log_to_file("Image is not reproduced correctly on HDMI.")
                                    NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_720p_noise_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.hdmi_720p_noise_error_message)
                                    error_codes = NOS_API.test_cases_results_info.hdmi_720p_noise_error_code
                                    error_messages = NOS_API.test_cases_results_info.hdmi_720p_noise_error_message
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
                            else:
                                TEST_CREATION_API.write_log_to_file("Led Green NOK") 
                                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.led_power_green_nok_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.led_power_green_nok_error_message)
                                NOS_API.set_error_message("Led's")
                                error_codes = NOS_API.test_cases_results_info.led_power_green_nok_error_code
                                error_messages = NOS_API.test_cases_results_info.led_power_green_nok_error_message
                                counter = 4
                        else:
                            TEST_CREATION_API.write_log_to_file("Led Red NOK") 
                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.led_power_red_nok_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.led_power_red_nok_error_message)
                            NOS_API.set_error_message("Led's")
                            error_codes = NOS_API.test_cases_results_info.led_power_red_nok_error_code
                            error_messages = NOS_API.test_cases_results_info.led_power_red_nok_error_message
                            counter = 4     
                    else:
                        TEST_CREATION_API.send_ir_rc_command("[OK]")
                        time.sleep(1)
                        if (NOS_API.wait_for_multiple_pictures(["Led_Verde_Canal_ref", "Led_Verde_Black_ref"], 45, ["[LED_Question]", "[LED_Question]"], [TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD, 70]) != -1):
                            TEST_CREATION_API.send_ir_rc_command("[OK]")
                            time.sleep(1)
                            if (NOS_API.wait_for_multiple_pictures(["USB_Canal_ref", "USB_Black_ref"], 45, ["[USB_Question]", "[USB_Question]"], [TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD, 70]) != -1):
                                TEST_CREATION_API.send_ir_rc_command("[OK]")
                                time.sleep(1)
                                
                                if(Retest):
                                    time.sleep(15)
                                if (NOS_API.wait_for_multiple_pictures(["OK_ref", "NOK_ref"], 45, ["[AD_RESULT]","[AD_RESULT]"], [TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD, 70]) != -1):
                                    if not(NOS_API.grab_picture("AutoDiag_Result")):
                                        TEST_CREATION_API.write_log_to_file("HDMI NOK")
                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                        NOS_API.set_error_message("Video HDMI")
                                        error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                        error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                        
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
                    
                                    video_result1 = NOS_API.compare_pictures("OK_ref", "AutoDiag_Result", "[AD_RESULT]")
                                    video_result2 = NOS_API.compare_pictures("NOK_ref", "AutoDiag_Result", "[AD_RESULT]")
                                    if (video_result1 > TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                                        test_result = "PASS"
                                        counter = 4
                                        NOS_API.Send_Serial_Key("d", "feito")
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
                                    else: 
                                        final_result1 = NOS_API.compare_pictures("OK_ref", "AutoDiag_Result", "[LED_RESULT]")
                                        final_result2 = NOS_API.compare_pictures("OK_ref", "AutoDiag_Result", "[USB_RESULT]")
                                        final_result3 = NOS_API.compare_pictures("OK_ref", "AutoDiag_Result", "[FLASH_RESULT]")
                                        final_result4 = NOS_API.compare_pictures("OK_ref", "AutoDiag_Result", "[ETH_RESULT]")
                                        final_result5 = NOS_API.compare_pictures("OK_ref", "AutoDiag_Result", "[FR_RESULT]")
                                        if(final_result1 > TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD and Led_result == False):
                                            Led_result = True
                                        if(final_result2 > TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD and USB_result == False):
                                            USB_result = True
                                        counter += 1
                                else:
                                    TEST_CREATION_API.write_log_to_file("Image is not reproduced correctly on HDMI.")
                                    NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_720p_noise_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.hdmi_720p_noise_error_message)
                                    error_codes = NOS_API.test_cases_results_info.hdmi_720p_noise_error_code
                                    error_messages = NOS_API.test_cases_results_info.hdmi_720p_noise_error_message
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
                            else:
                                TEST_CREATION_API.write_log_to_file("Image is not reproduced correctly on HDMI.")
                                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_720p_noise_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.hdmi_720p_noise_error_message)
                                error_codes = NOS_API.test_cases_results_info.hdmi_720p_noise_error_code
                                error_messages = NOS_API.test_cases_results_info.hdmi_720p_noise_error_message
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
                        else:
                            TEST_CREATION_API.write_log_to_file("Image is not reproduced correctly on HDMI.")
                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_720p_noise_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.hdmi_720p_noise_error_message)
                            error_codes = NOS_API.test_cases_results_info.hdmi_720p_noise_error_code
                            error_messages = NOS_API.test_cases_results_info.hdmi_720p_noise_error_message
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
                if(counter == 2):
                    
                    if(final_result2 < TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD and USB_result == False):
                        TEST_CREATION_API.write_log_to_file("USB NOK") 
                        NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.usb_nok_error_code \
                                                        + "; Error message: " + NOS_API.test_cases_results_info.usb_nok_error_message)
                        NOS_API.set_error_message("USB")
                        error_codes = NOS_API.test_cases_results_info.usb_nok_error_code
                        error_messages = NOS_API.test_cases_results_info.usb_nok_error_message
                    
                    if(final_result3 < TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                        TEST_CREATION_API.write_log_to_file("Flash NOK") 
                        NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.flash_nok_error_code \
                                                        + "; Error message: " + NOS_API.test_cases_results_info.flash_nok_error_message)
                        NOS_API.set_error_message("Flash")
                        error_codes = NOS_API.test_cases_results_info.flash_nok_error_code
                        error_messages = NOS_API.test_cases_results_info.flash_nok_error_message
                        
                    if(final_result4 < TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                        TEST_CREATION_API.write_log_to_file("Ethernet NOK") 
                        NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.ethernet_nok_error_code \
                                                        + "; Error message: " + NOS_API.test_cases_results_info.ethernet_nok_error_message)
                        NOS_API.set_error_message("Eth")
                        error_codes = NOS_API.test_cases_results_info.ethernet_nok_error_code
                        error_messages = NOS_API.test_cases_results_info.ethernet_nok_error_message
                        
                    if(final_result5 < TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                        TEST_CREATION_API.write_log_to_file("Factory Reset NOK") 
                        NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.measure_boot_time_error_code \
                                                        + "; Error message: " + NOS_API.test_cases_results_info.measure_boot_time_error_message)
                        NOS_API.set_error_message("Factory Reset")
                        error_codes = NOS_API.test_cases_results_info.measure_boot_time_error_code
                        error_messages = NOS_API.test_cases_results_info.measure_boot_time_error_message
             
            else:
                TEST_CREATION_API.write_log_to_file("Image is not reproduced correctly on HDMI.")
                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_720p_noise_error_code \
                                                    + "; Error message: " + NOS_API.test_cases_results_info.hdmi_720p_noise_error_message)
                error_codes = NOS_API.test_cases_results_info.hdmi_720p_noise_error_code
                error_messages = NOS_API.test_cases_results_info.hdmi_720p_noise_error_message
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
    report_file = NOS_API.create_test_case_log_file(
                    NOS_API.test_cases_results_info.s_n_using_barcode,
                    NOS_API.test_cases_results_info.nos_sap_number,
                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                    "",
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