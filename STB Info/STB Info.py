# Test name = Serial Number
# Test description = Check S/N from menu with scanned S/N, log nagraguide version and sw version
from datetime import datetime
import time

import TEST_CREATION_API
#import shutil
#shutil.copyfile('\\\\bbtfs\\RT-Executor\\API\\NOS_API.py', 'NOS_API.py')
import NOS_API

SNR_VALUE_THRESHOLD_LOW = 55
SNR_VALUE_THRESHOLD_HIGH = 75

def runTest():
    
    System_Failure = 0
    
    while (System_Failure < 2):
        try:
            ## Set test result default to FAIL
            test_result = "FAIL"
            test_result_sn = False        
            SW_Version = "-"
            Bootloader = "-"
            Signal_Power = 0
            Signal_Quality = "-"

            error_codes = ""
            error_messages = ""
            counter = 0
            FIRMWARE_VERSION_PROD = NOS_API.Firmware_Version_Intek_DTA
            Bootloader_Version = NOS_API.Bootloader_Version_Intek_DTA
            ## Get scanned STB Barcode
            scanned_serial_number = NOS_API.test_cases_results_info.s_n_using_barcode
            scanned_serial_number = NOS_API.remove_whitespaces(NOS_API.test_cases_results_info.s_n_using_barcode)

            ## Initialize grabber device
            TEST_CREATION_API.initialize_grabber()

            ## Start grabber device with video on default video source
            TEST_CREATION_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.HDMI1)
            time.sleep(3)
            if(System_Failure > 0):
                TEST_CREATION_API.send_ir_rc_command("[EXIT]")
                TEST_CREATION_API.send_ir_rc_command("[EXIT]")
                TEST_CREATION_API.send_ir_rc_command("[EXIT]")
            
            video_height = NOS_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
            if(video_height == "720"):
                NOS_API.SET_720 = True
                NOS_API.SET_576 = False
            elif(video_height == "576"):
                NOS_API.SET_720 = False
                NOS_API.SET_576 = True   
            elif(video_height == "1080"):
                NOS_API.SET_720 = False
                NOS_API.SET_576 = False   
                
                
            if (NOS_API.is_signal_present_on_video_source()):
                TEST_CREATION_API.send_ir_rc_command("[MENU]")
                time.sleep(1)
                if not(NOS_API.grab_picture("Menu")):
                    TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
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
                 
                if(NOS_API.SET_576):
                    video_result_Install = NOS_API.compare_pictures("Install_Menu_576_ref", "Menu", "[MENU_ICON_576p]")
                    video_result_Install1 = NOS_API.compare_pictures("Install_Menu_576_ref1", "Menu", "[MENU_ICON_576p]")
                    video_result_Install_Eng = NOS_API.compare_pictures("Install_Menu_576_ENG_ref", "Menu", "[MENU_ICON_576p]")
                    video_result_Channel = NOS_API.compare_pictures("Channel_Menu_576_ref", "Menu", "[MENU_ICON_576p]")
                    video_result_Channel_ENG = NOS_API.compare_pictures("Channel_Menu_576_ENG_ref", "Menu", "[MENU_ICON_576p]")
                    video_result_Config = NOS_API.compare_pictures("Config_menu_576_ref", "Menu", "[MENU_ICON_576p]")
                    video_result_Config_ENG = NOS_API.compare_pictures("Config_menu_576_ENG_ref", "Menu", "[MENU_ICON_576p]")
                elif(NOS_API.SET_720):
                    video_result_Install = NOS_API.compare_pictures("Install_Menu_720_ref", "Menu", "[MENU_ICON_720p]")
                    video_result_Install1 = NOS_API.compare_pictures("Install_Menu_720_ref1", "Menu", "[MENU_ICON_720p]")
                    video_result_Install_Eng = NOS_API.compare_pictures("Install_Menu_720_ENG_ref", "Menu", "[MENU_ICON_720p]")
                    video_result_Channel = NOS_API.compare_pictures("Channel_Menu_720_ref", "Menu", "[MENU_ICON_720p]")
                    video_result_Channel_ENG = NOS_API.compare_pictures("Channel_Menu_720_ENG_ref", "Menu", "[MENU_ICON_720p]")
                    video_result_Config = NOS_API.compare_pictures("Config_menu_720_ref", "Menu", "[MENU_ICON_720p]")
                    video_result_Config_ENG = NOS_API.compare_pictures("Config_menu_720_ENG_ref", "Menu", "[MENU_ICON_720p]")
                else:
                    video_result_Install = NOS_API.compare_pictures("Install_Menu_1080_ref", "Menu", "[MENU_ICON_1080p]")
                    video_result_Install1 = NOS_API.compare_pictures("Install_Menu_1080_ref1", "Menu", "[MENU_ICON_1080p]")
                    video_result_Install_Eng = NOS_API.compare_pictures("Install_Menu_1080_ENG_ref", "Menu", "[MENU_ICON_1080p]")
                    video_result_Install_Eng1 = NOS_API.compare_pictures("Install_Menu_1080_ENG_ref1", "Menu", "[MENU_ICON_1080p]")
                    video_result_Channel = NOS_API.compare_pictures("Channel_Menu_1080_ref", "Menu", "[MENU_ICON_1080p]")
                    video_result_Channel_ENG = NOS_API.compare_pictures("Channel_Menu_1080_ENG_ref", "Menu", "[MENU_ICON_1080p]")
                    video_result_Config = NOS_API.compare_pictures("Config_menu_1080_ref", "Menu", "[MENU_ICON_1080p]")
                    video_result_Config_ENG = NOS_API.compare_pictures("Config_menu_1080_ENG_ref", "Menu", "[MENU_ICON_1080p]")
                
                
                
                if(video_result_Install >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD or video_result_Install1 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD or video_result_Install_Eng >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD or video_result_Install_Eng1 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                    if(NOS_API.SET_720):
                        TEST_CREATION_API.send_ir_rc_command("[LEFT]")
                        
                        TEST_CREATION_API.send_ir_rc_command("[SET_RESOLUTION_1080i]")
                        video_height = TEST_CREATION_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                        if (video_height != "1080"):    
                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.resolution_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.resolution_error_message)
                            error_codes = NOS_API.test_cases_results_info.resolution_error_code
                            error_messages = NOS_API.test_cases_results_info.resolution_error_message
                            NOS_API.set_error_message("Resolução")
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

                        TEST_CREATION_API.send_ir_rc_command("[RIGHT]")
                    if(NOS_API.SET_576):
                        TEST_CREATION_API.send_ir_rc_command("[LEFT]")
                        
                        TEST_CREATION_API.send_ir_rc_command("[SET_RESOLUTION_1080_from_576p]")
                        video_height = TEST_CREATION_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                        if (video_height != "1080"):    
                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.resolution_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.resolution_error_message)
                            error_codes = NOS_API.test_cases_results_info.resolution_error_code
                            error_messages = NOS_API.test_cases_results_info.resolution_error_message
                            NOS_API.set_error_message("Resolução")
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

                        TEST_CREATION_API.send_ir_rc_command("[RIGHT]")
                    
                    TEST_CREATION_API.send_ir_rc_command("[SIGNAL_MENU]")
                    if not(NOS_API.grab_picture("Signal_Menu")):
                        TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
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

                    try:          
                        ## Get SSignal values from menu
                        Signal_Power_line = fix_Signal_values(TEST_CREATION_API.OCR_recognize_text("Signal_Menu", "[SIGNAL]", "[DTA_FILTER]","Signal_Power"))
                        Signal_Quality_line = fix_Signal_values(TEST_CREATION_API.OCR_recognize_text("Signal_Menu", "[SIGNAL_QUALITY]", "[DTA_FILTER]","Signal_Quality"))
                        Signal_Power = float(Get_Values(Signal_Power_line, True))
                        Signal_Quality = Get_Values(Signal_Quality_line, False)
                        TEST_CREATION_API.write_log_to_file("Signal Power: " + str(Signal_Power))
                        TEST_CREATION_API.write_log_to_file("Signal Quality: " + str(Signal_Quality))
                        
                    except Exception as error:
                        ## Set test result to INCONCLUSIVE
                        TEST_CREATION_API.write_log_to_file(str(error))
                        Signal_Quality = ""
                        Signal_Power = 0
                        
                    if (Signal_Power < SNR_VALUE_THRESHOLD_LOW and Signal_Power > SNR_VALUE_THRESHOLD_HIGH):
                        TEST_CREATION_API.write_log_to_file("SNR value is out of the threshold")
                        NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.snr_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.snr_error_message)
                        NOS_API.set_error_message("SNR")
                        error_codes = NOS_API.test_cases_results_info.snr_error_code
                        error_messages = NOS_API.test_cases_results_info.snr_error_message
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

                    TEST_CREATION_API.send_ir_rc_command("[BACK]")
                    TEST_CREATION_API.send_ir_rc_command("[UP]")
                    TEST_CREATION_API.send_ir_rc_command("[UP]")
                    TEST_CREATION_API.send_ir_rc_command("[LEFT]")
                    
                    TEST_CREATION_API.send_ir_rc_command("[SW_MENU]")
                    if not(NOS_API.grab_picture("SW_Menu")):
                        TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
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

                    try:          
                        ## Get SW from menu
                        SW_Version = TEST_CREATION_API.OCR_recognize_text("SW_Menu", "[SW_VERSION]", "[DTA_FILTER]","SW_Version")
                        Bootloader = TEST_CREATION_API.OCR_recognize_text("SW_Menu", "[BOOTLOADER]", "[DTA_FILTER]","Bootloader")

                        TEST_CREATION_API.write_log_to_file("SW Version: " + SW_Version)
                        TEST_CREATION_API.write_log_to_file("Bootloader Version: " + Bootloader)
                        
                    except Exception as error:
                        ## Set test result to INCONCLUSIVE
                        TEST_CREATION_API.write_log_to_file(str(error))
                        SW_Version = ""
                        Bootloader = ""
    
                    if not(SW_Version == FIRMWARE_VERSION_PROD):
                        TEST_CREATION_API.write_log_to_file("Doesn't upgrade")
            
                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.upgrade_nok_error_code \
                                                        + "; Error message: " + NOS_API.test_cases_results_info.upgrade_nok_error_message)                                        
                        NOS_API.set_error_message("Não Actualiza") 
                        error_codes =  NOS_API.test_cases_results_info.upgrade_nok_error_code
                        error_messages = NOS_API.test_cases_results_info.upgrade_nok_error_message                               
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

                    else:
                        test_result = "PASS"
                    
                    TEST_CREATION_API.send_ir_rc_command("[BACK]")
                    TEST_CREATION_API.send_ir_rc_command("[UP]")
                    TEST_CREATION_API.send_ir_rc_command("[UP]")
                    TEST_CREATION_API.send_ir_rc_command("[UP]")
                    TEST_CREATION_API.send_ir_rc_command("[RIGHT]")
                    
                    TEST_CREATION_API.send_ir_rc_command("[EXIT]")
                elif(video_result_Channel >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD or video_result_Channel_ENG >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                    if(NOS_API.SET_720):
                        TEST_CREATION_API.send_ir_rc_command("[RIGHT]")
                        
                        TEST_CREATION_API.send_ir_rc_command("[SET_RESOLUTION_1080i]")
                        video_height = TEST_CREATION_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                        if (video_height != "1080"):    
                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.resolution_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.resolution_error_message)
                            error_codes = NOS_API.test_cases_results_info.resolution_error_code
                            error_messages = NOS_API.test_cases_results_info.resolution_error_message
                            NOS_API.set_error_message("Resolução")
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

                        TEST_CREATION_API.send_ir_rc_command("[LEFT]")
                    
                    if(NOS_API.SET_576):
                        TEST_CREATION_API.send_ir_rc_command("[RIGHT]")
                        
                        TEST_CREATION_API.send_ir_rc_command("[SET_RESOLUTION_1080_from_576p]")
                        video_height = TEST_CREATION_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                        if (video_height != "1080"):    
                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.resolution_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.resolution_error_message)
                            error_codes = NOS_API.test_cases_results_info.resolution_error_code
                            error_messages = NOS_API.test_cases_results_info.resolution_error_message
                            NOS_API.set_error_message("Resolução")
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

                        TEST_CREATION_API.send_ir_rc_command("[LEFT]")

                    TEST_CREATION_API.send_ir_rc_command("[LEFT]")
                    
                    TEST_CREATION_API.send_ir_rc_command("SIGNAL_MENU]")
                    if not(NOS_API.grab_picture("Signal_Menu")):
                        TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
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

                    try:          
                        ## Get SSignal values from menu
                        Signal_Power_line = fix_Signal_values(TEST_CREATION_API.OCR_recognize_text("Signal_Menu", "[SIGNAL]", "[DTA_FILTER]","Signal_Power"))
                        Signal_Quality_line = fix_Signal_values(TEST_CREATION_API.OCR_recognize_text("Signal_Menu", "[SIGNAL_QUALITY]", "[DTA_FILTER]","Signal_Quality"))
                        Signal_Power = float(Get_Values(Signal_Power_line, True))
                        Signal_Quality = Get_Values(Signal_Quality_line, False)

                        TEST_CREATION_API.write_log_to_file("Signal Power: " + str(Signal_Power))
                        TEST_CREATION_API.write_log_to_file("Signal Quality: " + str(Signal_Quality))
                        
                    except Exception as error:
                        ## Set test result to INCONCLUSIVE
                        TEST_CREATION_API.write_log_to_file(str(error))
                        Signal_Quality = ""
                        Signal_Power = 0

                    if (Signal_Power < SNR_VALUE_THRESHOLD_LOW and Signal_Power > SNR_VALUE_THRESHOLD_HIGH):
                        TEST_CREATION_API.write_log_to_file("SNR value is out of the threshold")
                        NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.snr_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.snr_error_message)
                        NOS_API.set_error_message("SNR")
                        error_codes = NOS_API.test_cases_results_info.snr_error_code
                        error_messages = NOS_API.test_cases_results_info.snr_error_message
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

                    TEST_CREATION_API.send_ir_rc_command("[BACK]")
                    TEST_CREATION_API.send_ir_rc_command("[UP]")
                    TEST_CREATION_API.send_ir_rc_command("[UP]")

                    TEST_CREATION_API.send_ir_rc_command("[LEFT]")
                    
                    TEST_CREATION_API.send_ir_rc_command("[SW_MENU]")
                    if not(NOS_API.grab_picture("SW_Menu")):
                        TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
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

                    try:          
                        ## Get SW from menu
                        SW_Version = TEST_CREATION_API.OCR_recognize_text("SW_Menu", "[SW_VERSION]", "[DTA_FILTER]","SW_Version")
                        Bootloader = TEST_CREATION_API.OCR_recognize_text("SW_Menu", "[BOOTLOADER]", "[DTA_FILTER]","Bootloader")

                        TEST_CREATION_API.write_log_to_file("SW Version: " + SW_Version)
                        TEST_CREATION_API.write_log_to_file("Bootloader Version: " + Bootloader)
                        
                    except Exception as error:
                        ## Set test result to INCONCLUSIVE
                        TEST_CREATION_API.write_log_to_file(str(error))
                        SW_Version = ""
                        Bootloader = ""
                        
                    if not(SW_Version == FIRMWARE_VERSION_PROD):
                        TEST_CREATION_API.write_log_to_file("Doesn't upgrade")
            
                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.upgrade_nok_error_code \
                                                        + "; Error message: " + NOS_API.test_cases_results_info.upgrade_nok_error_message)                                        
                        NOS_API.set_error_message("Não Actualiza") 
                        error_codes =  NOS_API.test_cases_results_info.upgrade_nok_error_code
                        error_messages = NOS_API.test_cases_results_info.upgrade_nok_error_message                               
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
 
                    else:
                       test_result = "PASS"
                    
                    TEST_CREATION_API.send_ir_rc_command("[BACK]")
                    TEST_CREATION_API.send_ir_rc_command("[UP]")
                    TEST_CREATION_API.send_ir_rc_command("[UP]")
                    TEST_CREATION_API.send_ir_rc_command("[UP]")
                    TEST_CREATION_API.send_ir_rc_command("[RIGHT]")
                    
                    TEST_CREATION_API.send_ir_rc_command("[EXIT]")
                elif(video_result_Config >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD or video_result_Config_ENG >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                    if(NOS_API.SET_720):                    
                        TEST_CREATION_API.send_ir_rc_command("[SET_RESOLUTION_1080i]")
                        video_height = TEST_CREATION_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                        if (video_height != "1080"):    
                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.resolution_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.resolution_error_message)
                            error_codes = NOS_API.test_cases_results_info.resolution_error_code
                            error_messages = NOS_API.test_cases_results_info.resolution_error_message
                            NOS_API.set_error_message("Resolução")
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
                                         
                    if(NOS_API.SET_576):                    
                        TEST_CREATION_API.send_ir_rc_command("[SET_RESOLUTION_1080_from_576p]")
                        video_height = TEST_CREATION_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                        if (video_height != "1080"):    
                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.resolution_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.resolution_error_message)
                            error_codes = NOS_API.test_cases_results_info.resolution_error_code
                            error_messages = NOS_API.test_cases_results_info.resolution_error_message
                            NOS_API.set_error_message("Resolução")
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
                    
                    TEST_CREATION_API.send_ir_rc_command("[SW_MENU]")
                    if not(NOS_API.grab_picture("SW_Menu")):
                        TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
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

                    try:          
                        ## Get SW from menu
                        SW_Version = TEST_CREATION_API.OCR_recognize_text("SW_Menu", "[SW_VERSION]", "[DTA_FILTER]","SW_Version")
                        Bootloader = TEST_CREATION_API.OCR_recognize_text("SW_Menu", "[BOOTLOADER]", "[DTA_FILTER]","Bootloader")

                        TEST_CREATION_API.write_log_to_file("SW Version: " + SW_Version)
                        TEST_CREATION_API.write_log_to_file("Bootloader Version: " + Bootloader)
                        
                    except Exception as error:
                        ## Set test result to INCONCLUSIVE
                        TEST_CREATION_API.write_log_to_file(str(error))
                        SW_Version = ""
                        Bootloader = ""
                    
                    if not(SW_Version == FIRMWARE_VERSION_PROD):
                        TEST_CREATION_API.write_log_to_file("Doesn't upgrade")
            
                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.upgrade_nok_error_code \
                                                        + "; Error message: " + NOS_API.test_cases_results_info.upgrade_nok_error_message)                                        
                        NOS_API.set_error_message("Não Actualiza") 
                        error_codes =  NOS_API.test_cases_results_info.upgrade_nok_error_code
                        error_messages = NOS_API.test_cases_results_info.upgrade_nok_error_message                               
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

                    TEST_CREATION_API.send_ir_rc_command("[BACK]")
                    TEST_CREATION_API.send_ir_rc_command("[UP]")
                    TEST_CREATION_API.send_ir_rc_command("[UP]")
                    TEST_CREATION_API.send_ir_rc_command("[UP]")
                    TEST_CREATION_API.send_ir_rc_command("[RIGHT]")
                    TEST_CREATION_API.send_ir_rc_command("[SIGNAL_MENU]")
                    

                    if not(NOS_API.grab_picture("Signal_Menu")):
                        TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
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

                    try:          
                        ## Get SSignal values from menu
                        Signal_Power_line = fix_Signal_values(TEST_CREATION_API.OCR_recognize_text("Signal_Menu", "[SIGNAL]", "[DTA_FILTER]","Signal_Power"))
                        Signal_Quality_line = fix_Signal_values(TEST_CREATION_API.OCR_recognize_text("Signal_Menu", "[SIGNAL_QUALITY]", "[DTA_FILTER]","Signal_Quality"))
                        Signal_Power = float(Get_Values(Signal_Power_line, True))
                        Signal_Quality = Get_Values(Signal_Power_line, False)

                        TEST_CREATION_API.write_log_to_file("Signal Power: " + str(Signal_Power))
                        TEST_CREATION_API.write_log_to_file("Signal Quality: " + str(Signal_Quality))
                        
                    except Exception as error:
                        ## Set test result to INCONCLUSIVE
                        TEST_CREATION_API.write_log_to_file(str(error))
                        Signal_Quality = ""
                        Signal_Power = 0

                    if (Signal_Power < SNR_VALUE_THRESHOLD_LOW and Signal_Power > SNR_VALUE_THRESHOLD_HIGH):
                        TEST_CREATION_API.write_log_to_file("SNR value is out of the threshold")
                        NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.snr_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.snr_error_message)
                        NOS_API.set_error_message("SNR")
                        error_codes = NOS_API.test_cases_results_info.snr_error_code
                        error_messages = NOS_API.test_cases_results_info.snr_error_message
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
                        test_result = "PASS"

                    TEST_CREATION_API.send_ir_rc_command("[BACK]")
                    TEST_CREATION_API.send_ir_rc_command("[UP]")
                    TEST_CREATION_API.send_ir_rc_command("[UP]")    
                    TEST_CREATION_API.send_ir_rc_command("[EXIT]")
                    
                else:
                    
                    TEST_CREATION_API.send_ir_rc_command("[MENU]")
                    time.sleep(1)
                    if not(NOS_API.grab_picture("Menu_1")):
                        TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
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
                    
                    if(NOS_API.SET_576):
                        video_result_Install = NOS_API.compare_pictures("Install_Menu_576_ref", "Menu_1", "[MENU_ICON_576p]")
                        video_result_Install1 = NOS_API.compare_pictures("Install_Menu_576_ref1", "Menu_1", "[MENU_ICON_576p]")
                        video_result_Install_Eng = NOS_API.compare_pictures("Install_Menu_576_ENG_ref", "Menu_1", "[MENU_ICON_576p]")
                        video_result_Channel = NOS_API.compare_pictures("Channel_Menu_576_ref", "Menu_1", "[MENU_ICON_576p]")
                        video_result_Channel_ENG = NOS_API.compare_pictures("Channel_Menu_576_ENG_ref", "Menu_1", "[MENU_ICON_576p]")
                        video_result_Config = NOS_API.compare_pictures("Config_menu_576_ref", "Menu_1", "[MENU_ICON_576p]")
                        video_result_Config_ENG = NOS_API.compare_pictures("Config_menu_576_ENG_ref", "Menu_1", "[MENU_ICON_576p]")
                    elif(NOS_API.SET_720):
                        video_result_Install = NOS_API.compare_pictures("Install_Menu_720_ref", "Menu_1", "[MENU_ICON_720p]")
                        video_result_Install1 = NOS_API.compare_pictures("Install_Menu_720_ref1", "Menu_1", "[MENU_ICON_720p]")
                        video_result_Install_Eng = NOS_API.compare_pictures("Install_Menu_720_ENG_ref", "Menu_1", "[MENU_ICON_720p]")
                        video_result_Channel = NOS_API.compare_pictures("Channel_Menu_720_ref", "Menu_1", "[MENU_ICON_720p]")
                        video_result_Channel_ENG = NOS_API.compare_pictures("Channel_Menu_720_ENG_ref", "Menu_1", "[MENU_ICON_720p]")
                        video_result_Config = NOS_API.compare_pictures("Config_menu_720_ref", "Menu_1", "[MENU_ICON_720p]")
                        video_result_Config_ENG = NOS_API.compare_pictures("Config_menu_720_ENG_ref", "Menu_1", "[MENU_ICON_720p]")
                    else:
                        video_result_Install = NOS_API.compare_pictures("Install_Menu_1080_ref", "Menu_1", "[MENU_ICON_1080p]")
                        video_result_Install1 = NOS_API.compare_pictures("Install_Menu_1080_ref1", "Menu_1", "[MENU_ICON_1080p]")
                        video_result_Install_Eng = NOS_API.compare_pictures("Install_Menu_1080_ENG_ref", "Menu_1", "[MENU_ICON_1080p]")
                        video_result_Install_Eng1 = NOS_API.compare_pictures("Install_Menu_1080_ENG_ref1", "Menu_1", "[MENU_ICON_1080p]")
                        video_result_Channel = NOS_API.compare_pictures("Channel_Menu_1080_ref", "Menu_1", "[MENU_ICON_1080p]")
                        video_result_Channel_ENG = NOS_API.compare_pictures("Channel_Menu_1080_ENG_ref", "Menu_1", "[MENU_ICON_1080p]")
                        video_result_Config = NOS_API.compare_pictures("Config_menu_1080_ref", "Menu_1", "[MENU_ICON_1080p]")
                        video_result_Config_ENG = NOS_API.compare_pictures("Config_menu_1080_ENG_ref", "Menu_1", "[MENU_ICON_1080p]")
                    
                    
                    
                    if(video_result_Install >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD or video_result_Install1 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD or video_result_Install_Eng >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD or video_result_Install_Eng1 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                        if(NOS_API.SET_720):
                            TEST_CREATION_API.send_ir_rc_command("[LEFT]")
                            
                            TEST_CREATION_API.send_ir_rc_command("[SET_RESOLUTION_1080i]")
                            video_height = TEST_CREATION_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                            if (video_height != "1080"):    
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.resolution_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.resolution_error_message)
                                error_codes = NOS_API.test_cases_results_info.resolution_error_code
                                error_messages = NOS_API.test_cases_results_info.resolution_error_message
                                NOS_API.set_error_message("Resolução")
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
                                            
                            
                            TEST_CREATION_API.send_ir_rc_command("[RIGHT]")
                        if(NOS_API.SET_576):
                            TEST_CREATION_API.send_ir_rc_command("[LEFT]")
                            
                            TEST_CREATION_API.send_ir_rc_command("[SET_RESOLUTION_1080_from_576p]")
                            video_height = TEST_CREATION_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                            if (video_height != "1080"):    
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.resolution_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.resolution_error_message)
                                error_codes = NOS_API.test_cases_results_info.resolution_error_code
                                error_messages = NOS_API.test_cases_results_info.resolution_error_message
                                NOS_API.set_error_message("Resolução")
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
                                            
                            
                            TEST_CREATION_API.send_ir_rc_command("[RIGHT]")
                        
                        TEST_CREATION_API.send_ir_rc_command("[SIGNAL_MENU]")
                        if not(NOS_API.grab_picture("Signal_Menu")):
                            TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
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

                        try:          
                            ## Get SSignal values from menu
                            Signal_Power_line = fix_Signal_values(TEST_CREATION_API.OCR_recognize_text("Signal_Menu", "[SIGNAL]", "[DTA_FILTER]","Signal_Power"))
                            Signal_Quality_line = fix_Signal_values(TEST_CREATION_API.OCR_recognize_text("Signal_Menu", "[SIGNAL_QUALITY]", "[DTA_FILTER]","Signal_Quality"))
                            Signal_Power = float(Get_Values(Signal_Power_line, True))
                            Signal_Quality = Get_Values(Signal_Quality_line, False)
                            TEST_CREATION_API.write_log_to_file("Signal Power: " + str(Signal_Power))
                            TEST_CREATION_API.write_log_to_file("Signal Quality: " + str(Signal_Quality))
                            
                        except Exception as error:
                            ## Set test result to INCONCLUSIVE
                            TEST_CREATION_API.write_log_to_file(str(error))
                            Signal_Quality = ""
                            Signal_Power = 0
                            
                        if (Signal_Power < SNR_VALUE_THRESHOLD_LOW and Signal_Power > SNR_VALUE_THRESHOLD_HIGH):
                            TEST_CREATION_API.write_log_to_file("SNR value is out of the threshold")
                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.snr_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.snr_error_message)
                            NOS_API.set_error_message("SNR")
                            error_codes = NOS_API.test_cases_results_info.snr_error_code
                            error_messages = NOS_API.test_cases_results_info.snr_error_message
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

                        TEST_CREATION_API.send_ir_rc_command("[BACK]")
                        TEST_CREATION_API.send_ir_rc_command("[UP]")
                        TEST_CREATION_API.send_ir_rc_command("[UP]")
                        TEST_CREATION_API.send_ir_rc_command("[LEFT]")
                        
                        TEST_CREATION_API.send_ir_rc_command("[SW_MENU]")
                        if not(NOS_API.grab_picture("SW_Menu")):
                            TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
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

                        try:          
                            ## Get SW from menu
                            SW_Version = TEST_CREATION_API.OCR_recognize_text("SW_Menu", "[SW_VERSION]", "[DTA_FILTER]","SW_Version")
                            Bootloader = TEST_CREATION_API.OCR_recognize_text("SW_Menu", "[BOOTLOADER]", "[DTA_FILTER]","Bootloader")
        
                            TEST_CREATION_API.write_log_to_file("SW Version: " + SW_Version)
                            TEST_CREATION_API.write_log_to_file("Bootloader Version: " + Bootloader)
                            
                        except Exception as error:
                            ## Set test result to INCONCLUSIVE
                            TEST_CREATION_API.write_log_to_file(str(error))
                            SW_Version = ""
                            Bootloader = ""
                            
                            
                        if not(SW_Version == FIRMWARE_VERSION_PROD):
                            TEST_CREATION_API.write_log_to_file("Doesn't upgrade")
                
                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.upgrade_nok_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.upgrade_nok_error_message)                                        
                            NOS_API.set_error_message("Não Actualiza") 
                            error_codes =  NOS_API.test_cases_results_info.upgrade_nok_error_code
                            error_messages = NOS_API.test_cases_results_info.upgrade_nok_error_message                               
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

                        else:
                            test_result = "PASS"
                        
                        TEST_CREATION_API.send_ir_rc_command("[BACK]")
                        TEST_CREATION_API.send_ir_rc_command("[UP]")
                        TEST_CREATION_API.send_ir_rc_command("[UP]")
                        TEST_CREATION_API.send_ir_rc_command("[UP]")
                        TEST_CREATION_API.send_ir_rc_command("[RIGHT]")
                        
                        TEST_CREATION_API.send_ir_rc_command("[EXIT]")
                    elif(video_result_Channel >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD or video_result_Channel_ENG >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                        if(NOS_API.SET_720):
                            TEST_CREATION_API.send_ir_rc_command("[RIGHT]")
                            
                            TEST_CREATION_API.send_ir_rc_command("[SET_RESOLUTION_1080i]")
                            video_height = TEST_CREATION_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                            if (video_height != "1080"):    
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.resolution_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.resolution_error_message)
                                error_codes = NOS_API.test_cases_results_info.resolution_error_code
                                error_messages = NOS_API.test_cases_results_info.resolution_error_message
                                NOS_API.set_error_message("Resolução")
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

                            TEST_CREATION_API.send_ir_rc_command("[LEFT]")
                        
                        if(NOS_API.SET_576):
                            TEST_CREATION_API.send_ir_rc_command("[RIGHT]")
                            
                            TEST_CREATION_API.send_ir_rc_command("[SET_RESOLUTION_1080_from_576p]")
                            video_height = TEST_CREATION_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                            if (video_height != "1080"):    
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.resolution_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.resolution_error_message)
                                error_codes = NOS_API.test_cases_results_info.resolution_error_code
                                error_messages = NOS_API.test_cases_results_info.resolution_error_message
                                NOS_API.set_error_message("Resolução")
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

                            TEST_CREATION_API.send_ir_rc_command("[LEFT]")

                        TEST_CREATION_API.send_ir_rc_command("[LEFT]")
                        
                        TEST_CREATION_API.send_ir_rc_command("SIGNAL_MENU]")
                        if not(NOS_API.grab_picture("Signal_Menu")):
                            TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
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

                        try:          
                            ## Get SSignal values from menu
                            Signal_Power_line = fix_Signal_values(TEST_CREATION_API.OCR_recognize_text("Signal_Menu", "[SIGNAL]", "[DTA_FILTER]","Signal_Power"))
                            Signal_Quality_line = fix_Signal_values(TEST_CREATION_API.OCR_recognize_text("Signal_Menu", "[SIGNAL_QUALITY]", "[DTA_FILTER]","Signal_Quality"))
                            Signal_Power = float(Get_Values(Signal_Power_line, True))
                            Signal_Quality = Get_Values(Signal_Quality_line, False)
        
                            TEST_CREATION_API.write_log_to_file("Signal Power: " + str(Signal_Power))
                            TEST_CREATION_API.write_log_to_file("Signal Quality: " + str(Signal_Quality))
                            
                        except Exception as error:
                            ## Set test result to INCONCLUSIVE
                            TEST_CREATION_API.write_log_to_file(str(error))
                            Signal_Quality = ""
                            Signal_Power = 0

                        if (Signal_Power < SNR_VALUE_THRESHOLD_LOW and Signal_Power > SNR_VALUE_THRESHOLD_HIGH):
                            TEST_CREATION_API.write_log_to_file("SNR value is out of the threshold")
                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.snr_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.snr_error_message)
                            NOS_API.set_error_message("SNR")
                            error_codes = NOS_API.test_cases_results_info.snr_error_code
                            error_messages = NOS_API.test_cases_results_info.snr_error_message
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

                        TEST_CREATION_API.send_ir_rc_command("[BACK]")
                        TEST_CREATION_API.send_ir_rc_command("[UP]")
                        TEST_CREATION_API.send_ir_rc_command("[UP]")
        
                        TEST_CREATION_API.send_ir_rc_command("[LEFT]")
                        
                        TEST_CREATION_API.send_ir_rc_command("[SW_MENU]")
                        if not(NOS_API.grab_picture("SW_Menu")):
                            TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
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

                        try:          
                            ## Get SW from menu
                            SW_Version = TEST_CREATION_API.OCR_recognize_text("SW_Menu", "[SW_VERSION]", "[DTA_FILTER]","SW_Version")
                            Bootloader = TEST_CREATION_API.OCR_recognize_text("SW_Menu", "[BOOTLOADER]", "[DTA_FILTER]","Bootloader")
        
                            TEST_CREATION_API.write_log_to_file("SW Version: " + SW_Version)
                            TEST_CREATION_API.write_log_to_file("Bootloader Version: " + Bootloader)
                            
                        except Exception as error:
                            ## Set test result to INCONCLUSIVE
                            TEST_CREATION_API.write_log_to_file(str(error))
                            SW_Version = ""
                            Bootloader = ""
                            
                        if not(SW_Version == FIRMWARE_VERSION_PROD):
                            TEST_CREATION_API.write_log_to_file("Doesn't upgrade")
                
                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.upgrade_nok_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.upgrade_nok_error_message)                                        
                            NOS_API.set_error_message("Não Actualiza") 
                            error_codes =  NOS_API.test_cases_results_info.upgrade_nok_error_code
                            error_messages = NOS_API.test_cases_results_info.upgrade_nok_error_message                               
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

                        else:
                            test_result = "PASS"
                            
                        TEST_CREATION_API.send_ir_rc_command("[BACK]")
                        TEST_CREATION_API.send_ir_rc_command("[UP]")
                        TEST_CREATION_API.send_ir_rc_command("[UP]")
                        TEST_CREATION_API.send_ir_rc_command("[UP]")
                        TEST_CREATION_API.send_ir_rc_command("[RIGHT]")
                            
                        TEST_CREATION_API.send_ir_rc_command("[EXIT]")
                    elif(video_result_Config >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD or video_result_Config_ENG >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                        if(NOS_API.SET_720):                    
                            TEST_CREATION_API.send_ir_rc_command("[SET_RESOLUTION_1080i]")
                            video_height = TEST_CREATION_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                            if (video_height != "1080"):    
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.resolution_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.resolution_error_message)
                                error_codes = NOS_API.test_cases_results_info.resolution_error_code
                                error_messages = NOS_API.test_cases_results_info.resolution_error_message
                                NOS_API.set_error_message("Resolução")
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
                                            
                        if(NOS_API.SET_576):                    
                            TEST_CREATION_API.send_ir_rc_command("[SET_RESOLUTION_1080_from_576p]")
                            video_height = TEST_CREATION_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                            if (video_height != "1080"):    
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.resolution_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.resolution_error_message)
                                error_codes = NOS_API.test_cases_results_info.resolution_error_code
                                error_messages = NOS_API.test_cases_results_info.resolution_error_message
                                NOS_API.set_error_message("Resolução")
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
                        
                        TEST_CREATION_API.send_ir_rc_command("[SW_MENU]")
                        if not(NOS_API.grab_picture("SW_Menu")):
                            TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
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

                        try:          
                            ## Get SW from menu
                            SW_Version = TEST_CREATION_API.OCR_recognize_text("SW_Menu", "[SW_VERSION]", "[DTA_FILTER]","SW_Version")
                            Bootloader = TEST_CREATION_API.OCR_recognize_text("SW_Menu", "[BOOTLOADER]", "[DTA_FILTER]","Bootloader")
        
                            TEST_CREATION_API.write_log_to_file("SW Version: " + SW_Version)
                            TEST_CREATION_API.write_log_to_file("Bootloader Version: " + Bootloader)
                            
                        except Exception as error:
                            ## Set test result to INCONCLUSIVE
                            TEST_CREATION_API.write_log_to_file(str(error))
                            SW_Version = ""
                            Bootloader = ""
                        
                        if not(SW_Version == FIRMWARE_VERSION_PROD):
                            TEST_CREATION_API.write_log_to_file("Doesn't upgrade")
                
                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.upgrade_nok_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.upgrade_nok_error_message)                                        
                            NOS_API.set_error_message("Não Actualiza") 
                            error_codes =  NOS_API.test_cases_results_info.upgrade_nok_error_code
                            error_messages = NOS_API.test_cases_results_info.upgrade_nok_error_message                               
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

                        TEST_CREATION_API.send_ir_rc_command("[BACK]")
                        TEST_CREATION_API.send_ir_rc_command("[UP]")
                        TEST_CREATION_API.send_ir_rc_command("[UP]")
                        TEST_CREATION_API.send_ir_rc_command("[UP]")
                        TEST_CREATION_API.send_ir_rc_command("[RIGHT]")
                        TEST_CREATION_API.send_ir_rc_command("[SIGNAL_MENU]")

                        if not(NOS_API.grab_picture("Signal_Menu")):
                            TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
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

                        try:          
                            ## Get SSignal values from menu
                            Signal_Power_line = fix_Signal_values(TEST_CREATION_API.OCR_recognize_text("Signal_Menu", "[SIGNAL]", "[DTA_FILTER]","Signal_Power"))
                            Signal_Quality_line = fix_Signal_values(TEST_CREATION_API.OCR_recognize_text("Signal_Menu", "[SIGNAL_QUALITY]", "[DTA_FILTER]","Signal_Quality"))
                            Signal_Power = float(Get_Values(Signal_Power_line, True))
                            Signal_Quality = Get_Values(Signal_Power_line, False)
        
                            TEST_CREATION_API.write_log_to_file("Signal Power: " + str(Signal_Power))
                            TEST_CREATION_API.write_log_to_file("Signal Quality: " + str(Signal_Quality))
                            
                        except Exception as error:
                            ## Set test result to INCONCLUSIVE
                            TEST_CREATION_API.write_log_to_file(str(error))
                            Signal_Quality = ""
                            Signal_Power = 0

                        if (Signal_Power < SNR_VALUE_THRESHOLD_LOW and Signal_Power > SNR_VALUE_THRESHOLD_HIGH):
                            TEST_CREATION_API.write_log_to_file("SNR value is out of the threshold")
                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.snr_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.snr_error_message)
                            NOS_API.set_error_message("SNR")
                            error_codes = NOS_API.test_cases_results_info.snr_error_code
                            error_messages = NOS_API.test_cases_results_info.snr_error_message
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
                            test_result = "PASS"

                        TEST_CREATION_API.send_ir_rc_command("[BACK]")
                        TEST_CREATION_API.send_ir_rc_command("[UP]")
                        TEST_CREATION_API.send_ir_rc_command("[UP]")    
                        TEST_CREATION_API.send_ir_rc_command("[EXIT]")
                    else:
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
            else:
                TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                        + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                NOS_API.set_error_message("Reboot")
                error_codes = NOS_API.test_cases_results_info.reboot_error_code
                error_messages = NOS_API.test_cases_results_info.reboot_error_message
                
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
                    "- - " + str(Signal_Power) + " " + str(Signal_Quality) + " - - - - - - - - - - - - - " + str(SW_Version) + " " + str(Bootloader) + " - - - - -",
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
   
def fix_Signal_values(input_text):
    # Replace "S" with "5"
    if ("S" in input_text):
        input_text = input_text.replace('S','5')
    # Replace "O" with "0"
    if ("O" in input_text):
        input_text = input_text.replace('O','0')
        
    return input_text
    
    
def Get_Values(input_text, case):
    mySubString = ""
    if(case):
        mySubString=input_text[0:input_text.find("%")]
    else:
        mySubString=input_text[input_text.find("(")+1:input_text.find(")")]
    return mySubString
        