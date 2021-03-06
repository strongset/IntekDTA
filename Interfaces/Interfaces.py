# -*- coding: utf-8 -*-
# Test name = Interfaces Test
# Test description = Check image and audio for all interfaces

from datetime import datetime
from time import gmtime, strftime
import time

import TEST_CREATION_API
#import shutil
#shutil.copyfile('\\\\bbtfs\\RT-Executor\\API\\NOS_API.py', 'NOS_API.py')
import NOS_API

## Max record audio time in miliseconds
MAX_RECORD_AUDIO_TIME = 2000

MAX_RECORD_VIDEO_TIME = 2000

def runTest():
    
    System_Failure = 0
    
    while(System_Failure < 2):
    
        try:
            ## Set test result default to FAIL
            test_result = "FAIL"
            pqm_analyse_check = True
            ch4_video_result = False
            ch1_1080_result = False
            ch1_720_result = False
            sound_720_result = False
            test_result_SCART_video = False
            scnd_change = False
            
            error_codes = ""
            error_messages = ""

            video_result = 0

            ## Initialize grabber device
            NOS_API.initialize_grabber()

            ## Start grabber device with video on default video source
            NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.HDMI1)
            TEST_CREATION_API.grabber_start_audio_source(TEST_CREATION_API.AudioInterface.HDMI1)
            time.sleep(3)        

            if (NOS_API.is_signal_present_on_video_source()):  
                if(System_Failure == 1):
                    TEST_CREATION_API.send_ir_rc_command("[BACK]")
                    TEST_CREATION_API.send_ir_rc_command("[BACK]")
                    TEST_CREATION_API.send_ir_rc_command("[BACK]")
                    time.sleep(1)
                    TEST_CREATION_API.send_ir_rc_command("[MENU]")
                    video_height = TEST_CREATION_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                    if (video_height != "1080"):   
                        scnd_change = True
                        TEST_CREATION_API.send_ir_rc_command("[SET_RESOLUTION_1080i]")
                        time.sleep(1)
                        TEST_CREATION_API.send_ir_rc_command("[BACK]")
                        TEST_CREATION_API.send_ir_rc_command("[BACK]")
                        TEST_CREATION_API.send_ir_rc_command("[BACK]")
                        video_height = TEST_CREATION_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                        if (video_height != "1080"):    
                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.resolution_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.resolution_error_message)
                            error_codes = NOS_API.test_cases_results_info.resolution_error_code
                            error_messages = NOS_API.test_cases_results_info.resolution_error_message
                            NOS_API.set_error_message("Resolu????o")
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
                
                ## Set volume to max
                TEST_CREATION_API.send_ir_rc_command("[VOL_MIN]")
                
                ## Set volume to half, because if vol is max, signal goes in saturation
                TEST_CREATION_API.send_ir_rc_command("[VOL_PLUS_HALF]")
            
                ## Zap to service
                TEST_CREATION_API.send_ir_rc_command("[CH_4]")
                TEST_CREATION_API.send_ir_rc_command("[EXIT]")
                TEST_CREATION_API.send_ir_rc_command("[EXIT]")  
                time.sleep(3)
                #while (chUp_counter < 3):                
        
                ## Close info banner
                #TEST_CREATION_API.send_ir_rc_command("[EXIT]")
                if not(NOS_API.grab_picture("CH4")):
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

                #video_result_ch4 = NOS_API.compare_pictures("HDMI_video_1080_ref", "CH4", "[HALF_SCREEN_1080p]")
                #video_result_ch4_1 = NOS_API.compare_pictures("HDMI_video_1080_ref1", "CH4", "[HALF_SCREEN_1080p]")
                
                video_result = NOS_API.compare_pictures("CH4_ref", "CH4", "[HALF_SCREEN_1080p]")
                video_result1 = NOS_API.compare_pictures("CH4_ref1", "CH4", "[HALF_SCREEN_1080p]")
                video_result2 = NOS_API.compare_pictures("CH4_ref2", "CH4", "[HALF_SCREEN_1080p]")
                video_result3 = NOS_API.compare_pictures("CH4_ref3", "CH4", "[HALF_SCREEN_1080p]")
                video_result4 = NOS_API.compare_pictures("CH4_ref4", "CH4", "[HALF_SCREEN_1080p]")
                #if(video_result_ch4 > TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD or video_result_ch4_1 > TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD or (video_result < 20 and video_result1 < 20)):
                if(video_result < TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD and video_result1 < TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD and video_result2 < TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD  and video_result3 < TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD and video_result4 < TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD): 
                    TEST_CREATION_API.send_ir_rc_command("[CH_4]")
                    time.sleep(1)
                    TEST_CREATION_API.send_ir_rc_command("[EXIT]")
                    TEST_CREATION_API.send_ir_rc_command("[EXIT]")  
                    time.sleep(3)
                
                    if not(NOS_API.grab_picture("CH4")):
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
              

                    video_result = NOS_API.compare_pictures("CH4_ref", "CH4", "[HALF_SCREEN_1080p]")
                    video_result1 = NOS_API.compare_pictures("CH4_ref1", "CH4", "[HALF_SCREEN_1080p]")
                    video_result2 = NOS_API.compare_pictures("CH4_ref2", "CH4", "[HALF_SCREEN_1080p]")
                    video_result3 = NOS_API.compare_pictures("CH4_ref3", "CH4", "[HALF_SCREEN_1080p]")
                    video_result4 = NOS_API.compare_pictures("CH4_ref4", "CH4", "[HALF_SCREEN_1080p]")
                if(video_result >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD or video_result1 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD or video_result2 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD or video_result3 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD or video_result4 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                    ch4_video_result = True
                else:
                    TEST_CREATION_API.write_log_to_file("Channel with RT-RK color bar pattern was not playing on HDMI 1080p.")
                    NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_1080p_image_freezing_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.hdmi_1080p_image_freezing_error_message)
                    error_codes = NOS_API.test_cases_results_info.hdmi_1080p_image_freezing_error_code
                    error_messages = NOS_API.test_cases_results_info.hdmi_1080p_image_freezing_error_message
                    NOS_API.set_error_message("Video HDMI")
                    
        
                if(ch4_video_result):
                
                
                    TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                    TEST_CREATION_API.send_ir_rc_command("[EXIT]")
                    TEST_CREATION_API.send_ir_rc_command("[EXIT]")  
                    time.sleep(3)
                    ## Record video with duration of recording (10 seconds)
                    NOS_API.record_video("video", MAX_RECORD_VIDEO_TIME)
                
                    ## Instance of PQMAnalyse type
                    pqm_analyse = TEST_CREATION_API.PQMAnalyse()
                
                    ## Set what algorithms should be checked while analyzing given video file with PQM.
                    # Attributes are set to false by default.
                    pqm_analyse.black_screen_activ = True
                    pqm_analyse.blocking_activ = True
                    pqm_analyse.freezing_activ = True
                
                    # Name of the video file that will be analysed by PQM.
                    pqm_analyse.file_name = "video"
                
                    ## Analyse recorded video
                    analysed_video = TEST_CREATION_API.pqm_analysis(pqm_analyse)
                
                    if (pqm_analyse.black_screen_detected == TEST_CREATION_API.AlgorythmResult.DETECTED):
                        pqm_analyse_check = False
                        NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_1080p_image_absence_error_code \
                                + "; Error message: " + NOS_API.test_cases_results_info.hdmi_1080p_image_absence_error_message)
                                
                        error_codes = NOS_API.test_cases_results_info.hdmi_1080p_image_absence_error_code
                        error_messages = NOS_API.test_cases_results_info.hdmi_1080p_image_absence_error_message
                
                    if (pqm_analyse.blocking_detected == TEST_CREATION_API.AlgorythmResult.DETECTED):
                        pqm_analyse_check = False
                        NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_1080p_blocking_error_code \
                                + "; Error message: " + NOS_API.test_cases_results_info.hdmi_1080p_blocking_error_message)
                        if (error_codes == ""):
                            error_codes = NOS_API.test_cases_results_info.hdmi_1080p_blocking_error_code
                        else:
                            error_codes = error_codes + " " + NOS_API.test_cases_results_info.hdmi_1080p_blocking_error_code
                        
                        if (error_messages == ""):
                            error_messages = NOS_API.test_cases_results_info.hdmi_1080p_blocking_error_message
                        else:
                            error_messages = error_messages + " " + NOS_API.test_cases_results_info.hdmi_1080p_blocking_error_message
                    
                    if (pqm_analyse.freezing_detected == TEST_CREATION_API.AlgorythmResult.DETECTED):
                        pqm_analyse_check = False
                        NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_1080p_image_freezing_error_code \
                                + "; Error message: " + NOS_API.test_cases_results_info.hdmi_1080p_image_freezing_error_message)
                        if (error_codes == ""):
                            error_codes = NOS_API.test_cases_results_info.hdmi_1080p_image_freezing_error_code
                        else:
                            error_codes = error_codes + " " + NOS_API.test_cases_results_info.hdmi_1080p_image_freezing_error_code
                            
                        if (error_messages == ""):
                            error_messages = NOS_API.test_cases_results_info.hdmi_1080p_image_freezing_error_message
                        else:
                            error_messages = error_messages + " " + NOS_API.test_cases_results_info.hdmi_1080p_image_freezing_error_message
                    
                    if not(pqm_analyse_check): 
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
                    
                    if not(analysed_video):
                        test_result = "FAIL"
                        TEST_CREATION_API.write_log_to_file("Could'n't Record Video")
                        NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.grabber_error_code \
                                                                            + "; Error message: " + NOS_API.test_cases_results_info.grabber_error_message)
                        error_codes = NOS_API.test_cases_results_info.grabber_error_code
                        error_messages = NOS_API.test_cases_results_info.grabber_error_message
                        NOS_API.set_error_message("Inspection")
                        
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
                        
                        return              
                    
            
                    video_result = 0
                    i = 0
                    
                    while(i < 3):
            
                        try:
                            ## Perform grab picture
                            if not(NOS_API.grab_picture("HDMI_video_1080p")):
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

                            ## Compare grabbed and expected image and get result of comparison
                            video_result = NOS_API.compare_pictures("HDMI_video_1080_ref", "HDMI_video_1080p", "[HALF_SCREEN_1080p]")
                            video_result1 = NOS_API.compare_pictures("HDMI_video_1080_ref1", "HDMI_video_1080p", "[HALF_SCREEN_1080p]")
                            video_result2 = NOS_API.compare_pictures("HDMI_video_1080_ref2", "HDMI_video_1080p", "[HALF_SCREEN_1080p]")
                            video_result3 = NOS_API.compare_pictures("HDMI_video_1080_ref3", "HDMI_video_1080p", "[HALF_SCREEN_1080p]")
                            video_result4 = NOS_API.compare_pictures("HDMI_video_1080_ref4", "HDMI_video_1080p", "[HALF_SCREEN_1080p]")
                    
                        except:
                            i = i + 1
                            continue
                    
                        ## Check video analysis results and update comments
                        if (video_result >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD or video_result1 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD or video_result2 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD or video_result3 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD  or video_result4 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                            i = 0
                            if (analysed_video): 
                                ch1_1080_result = True
                                #test_result = "PASS"
                            else:
                                NOS_API.set_error_message("Video HDMI")     
                            break
                        i = i + 1
                    if (i >= 3):
                        TEST_CREATION_API.write_log_to_file("Video with RT-RK pattern is not reproduced correctly on HDMI 1080p.")
                        NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_1080p_noise_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.hdmi_1080p_noise_error_message \
                                                            + "; V: " + str(video_result))
                        error_codes = NOS_API.test_cases_results_info.hdmi_1080p_noise_error_code
                        error_messages = NOS_API.test_cases_results_info.hdmi_1080p_noise_error_message
                        NOS_API.set_error_message("Video HDMI")

                    if(ch1_1080_result):
                        if (scnd_change):
                            TEST_CREATION_API.send_ir_rc_command("[SET_RESOLUTION_SCND_CHANGE]")
                        else:
                            if(NOS_API.SET_720 or NOS_API.SET_576):
                                TEST_CREATION_API.send_ir_rc_command("[SET_RESOLUTION_720p_AfterChange]")
                            else:
                                TEST_CREATION_API.send_ir_rc_command("[SET_RESOLUTION_720p]")

                                ## Perform grab picture
                                if not(NOS_API.grab_picture("Resolution_1080p")):
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
                                
                                video_result = NOS_API.compare_pictures("Resolution_1080p_ref", "Resolution_1080p", "[Resolution_1080p]")
                                
                                if (video_result >= NOS_API.thres):
                                    TEST_CREATION_API.send_ir_rc_command("[SET_RESOLUTION_720p_1]")
                                else:
                                    TEST_CREATION_API.send_ir_rc_command("[SET_RESOLUTION_720p_2]")
                                    
                            time.sleep(2)
                            
                            video_height = NOS_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                            if (video_height != "720"):
                                if not(NOS_API.grab_picture("CH4")):
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
                                TEST_CREATION_API.send_ir_rc_command("[SET_RESOLUTION_720p_Redo]")
                                time.sleep(2)
                                counter = 0
                                while(counter <6):
                                    video_height = NOS_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                                    if (video_height != "720"):
                                        TEST_CREATION_API.send_ir_rc_command("[LEFT]")
                                        counter +=1
                                    elif(video_height == "720"):
                                        counter = 7
                                        TEST_CREATION_API.send_ir_rc_command("[LEFT]")
                                        TEST_CREATION_API.send_ir_rc_command("[EXIT]")
                                        TEST_CREATION_API.send_ir_rc_command("[EXIT]")
                                        
                                if (video_height != "720"):
                                    NOS_API.set_error_message("Resolu????o")
                                    TEST_CREATION_API.write_log_to_file("Resolution Error! \nResolution: " + video_height + ". \nExpected Resolution: 720p"  )
                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.resolution_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.resolution_error_message) 
                                    error_codes = NOS_API.test_cases_results_info.resolution_error_code
                                    error_messages = NOS_API.test_cases_results_info.resolution_error_message
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

                        ## Record video with duration of recording (10 seconds)
                        NOS_API.record_video("video", MAX_RECORD_VIDEO_TIME)
                    
                        ## Instance of PQMAnalyse type
                        pqm_analyse = TEST_CREATION_API.PQMAnalyse()
                    
                        ## Set what algorithms should be checked while analyzing given video file with PQM.
                        # Attributes are set to false by default.
                        pqm_analyse.black_screen_activ = True
                        pqm_analyse.blocking_activ = True
                        pqm_analyse.freezing_activ = True
                    
                        # Name of the video file that will be analysed by PQM.
                        pqm_analyse.file_name = "video"
                    
                        ## Analyse recorded video
                        analysed_video = TEST_CREATION_API.pqm_analysis(pqm_analyse)
                    
                        if (pqm_analyse.black_screen_detected == TEST_CREATION_API.AlgorythmResult.DETECTED):
                            pqm_analyse_check = False
                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_720p_image_absence_error_code \
                                    + "; Error message: " + NOS_API.test_cases_results_info.hdmi_720p_image_absence_error_message)
                                    
                            error_codes = NOS_API.test_cases_results_info.hdmi_720p_image_absence_error_code
                            error_messages = NOS_API.test_cases_results_info.hdmi_720p_image_absence_error_message
                    
                        if (pqm_analyse.blocking_detected == TEST_CREATION_API.AlgorythmResult.DETECTED):
                            pqm_analyse_check = False
                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_720p_blocking_error_code \
                                    + "; Error message: " + NOS_API.test_cases_results_info.hdmi_720p_blocking_error_message)
                            if (error_codes == ""):
                                error_codes = NOS_API.test_cases_results_info.hdmi_720p_blocking_error_code
                            else:
                                error_codes = error_codes + " " + NOS_API.test_cases_results_info.hdmi_720p_blocking_error_code
                            
                            if (error_messages == ""):
                                error_messages = NOS_API.test_cases_results_info.hdmi_720p_blocking_error_message
                            else:
                                error_messages = error_messages + " " + NOS_API.test_cases_results_info.hdmi_720p_blocking_error_message
                        
                        if (pqm_analyse.freezing_detected == TEST_CREATION_API.AlgorythmResult.DETECTED):
                            pqm_analyse_check = False
                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_720p_image_freezing_error_code \
                                    + "; Error message: " + NOS_API.test_cases_results_info.hdmi_720p_image_freezing_error_message)
                            if (error_codes == ""):
                                error_codes = NOS_API.test_cases_results_info.hdmi_720p_image_freezing_error_code
                            else:
                                error_codes = error_codes + " " + NOS_API.test_cases_results_info.hdmi_720p_image_freezing_error_code
                                
                            if (error_messages == ""):
                                error_messages = NOS_API.test_cases_results_info.hdmi_720p_image_freezing_error_message
                            else:
                                error_messages = error_messages + " " + NOS_API.test_cases_results_info.hdmi_720p_image_freezing_error_message
                        
                        if not(pqm_analyse_check): 
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
                        
                        if not(analysed_video):
                            test_result = "FAIL"
                            TEST_CREATION_API.write_log_to_file("Could'n't Record Video")
                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.grabber_error_code \
                                                                                + "; Error message: " + NOS_API.test_cases_results_info.grabber_error_message)
                            error_codes = NOS_API.test_cases_results_info.grabber_error_code
                            error_messages = NOS_API.test_cases_results_info.grabber_error_message
                            NOS_API.set_error_message("Inspection")
                            
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
                            
                            return              
                        
                        ## Check if video is playing (check if video is not freezed)
                        if (NOS_API.is_video_playing(TEST_CREATION_API.VideoInterface.HDMI1, NOS_API.ResolutionType.resolution_720p)):
                    
                            video_result = 0
                            i = 0
                            
                            while(i < 3):
                    
                                try:
                                    ## Perform grab picture
                                    if not(NOS_API.grab_picture("HDMI_video")):
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
                            
                                    ## Compare grabbed and expected image and get result of comparison
                                    video_result = NOS_API.compare_pictures("HDMI_video_ref", "HDMI_video", "[HALF_SCREEN]")
                                    video_result1 = NOS_API.compare_pictures("HDMI_video_ref1", "HDMI_video", "[HALF_SCREEN]")
                                    video_result2 = NOS_API.compare_pictures("HDMI_video_ref2", "HDMI_video", "[HALF_SCREEN]")
                                    video_result3 = NOS_API.compare_pictures("HDMI_video_ref3", "HDMI_video", "[HALF_SCREEN]")
                                    video_result4 = NOS_API.compare_pictures("HDMI_video_ref4", "HDMI_video", "[HALF_SCREEN]")
                                    video_result5 = NOS_API.compare_pictures("HDMI_video_ref5", "HDMI_video", "[HALF_SCREEN]")
                            
                                except:
                                    i = i + 1
                                    continue
                            
                                ## Check video analysis results and update comments
                                if (video_result >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD or video_result1 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD or video_result2 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD or video_result3 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD or video_result4 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD or video_result5 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                                    i = 0
                                    if (analysed_video): 
                                        ch1_720_result = True
                                        #test_result = "PASS"
                                    else:
                                        NOS_API.set_error_message("Video HDMI")     
                                    break
                                i = i + 1
                            if (i >= 3):
                                TEST_CREATION_API.write_log_to_file("Video with RT-RK pattern is not reproduced correctly on HDMI 720p.")
                                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_720p_noise_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.hdmi_720p_noise_error_message \
                                                                    + "; V: " + str(video_result))
                                error_codes = NOS_API.test_cases_results_info.hdmi_1080p_noise_error_code
                                error_messages = NOS_API.test_cases_results_info.hdmi_1080p_noise_error_message
                                NOS_API.set_error_message("Video HDMI")
                        else:
                            TEST_CREATION_API.write_log_to_file("Channel with RT-RK color bar pattern was not playing on HDMI 720p.")
                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_720p_image_freezing_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.hdmi_720p_image_freezing_error_message)
                            error_codes = NOS_API.test_cases_results_info.hdmi_720p_image_freezing_error_code
                            error_messages = NOS_API.test_cases_results_info.hdmi_720p_image_freezing_error_message
                            NOS_API.set_error_message("Video HDMI")

                        if(ch1_720_result):                   
                            ## Record audio from HDMI
                            TEST_CREATION_API.record_audio("CH1_Audio", MAX_RECORD_AUDIO_TIME)
                            
                            audio_result_1 = NOS_API.compare_audio("No_Both_ref", "CH1_Audio")
                            
                            if (audio_result_1 < TEST_CREATION_API.AUDIO_THRESHOLD):                            
                                sound_720_result = True                        
                            else:
                        
                                TEST_CREATION_API.write_log_to_file("Audio with RT-RK pattern is not reproduced correctly on hdmi 720p interface.")
                                NOS_API.set_error_message("Audio HDMI")
                                NOS_API.update_test_slot_comment("Error codes: " + NOS_API.test_cases_results_info.hdmi_720p_signal_discontinuities_error_code  \
                                                                + ";\n" + NOS_API.test_cases_results_info.hdmi_720p_signal_interference_error_code  \
                                                                + "; Error messages: " + NOS_API.test_cases_results_info.hdmi_720p_signal_discontinuities_error_message \
                                                                + ";\n" + NOS_API.test_cases_results_info.hdmi_720p_signal_discontinuities_error_message)
                                error_codes = NOS_API.test_cases_results_info.hdmi_720p_signal_discontinuities_error_code + " " + NOS_API.test_cases_results_info.hdmi_720p_signal_interference_error_code
                                error_messages = NOS_API.test_cases_results_info.hdmi_720p_signal_discontinuities_error_message + " " + NOS_API.test_cases_results_info.hdmi_720p_signal_interference_error_message
                                    
                            if(sound_720_result):
                                
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
                                
                                if not(NOS_API.is_signal_present_on_video_source()):
                                    NOS_API.display_dialog("Confirme o cabo SCART e restantes cabos", NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "Continuar"
                                
                                
                                if (NOS_API.is_signal_present_on_video_source()):
        
                                    ## Check if video is playing (check if video is not freezed)
                                    if (NOS_API.is_video_playing(TEST_CREATION_API.VideoInterface.CVBS2)):
                                        video_result = 0
                                        i = 0
                                        
                                        while(i < 3):
                                
                                            try:
                                                ## Perform grab picture
                                                
                                                if not(NOS_API.grab_picture("SCART_video")):
                                                    TEST_CREATION_API.write_log_to_file("Image is not displayed on SCART")
                                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_scart_error_code \
                                                                                        + "; Error message: " + NOS_API.test_cases_results_info.image_absence_scart_error_message)
                                                    NOS_API.set_error_message("Video HDMI")
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
                            
                                                ## Compare grabbed and expected image and get result of comparison
                                                video_result = NOS_API.compare_pictures("SCART_video_ref", "SCART_video", "[HALF_SCREEN_576p]")
                                        
                                            except:
                                                i = i + 1
                                                continue
                                        
                                            ## Check video analysis results and update comments
                                            if (video_result >= NOS_API.DEFAULT_CVBS_VIDEO_THRESHOLD):
                                                ## Set test result to PASS
                                                test_result_SCART_video = True
                                                break
                                            i = i + 1
                                        if (i >= 3):
                                            TEST_CREATION_API.write_log_to_file("Video with RT-RK pattern is not reproduced correctly on SCART interface.")
                                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.scart_noise_error_code \
                                                                                + "; Error message: " + NOS_API.test_cases_results_info.scart_noise_error_message \
                                                                                + "; V: " + str(video_result))
                                            error_codes = NOS_API.test_cases_results_info.scart_noise_error_code
                                            error_messages = NOS_API.test_cases_results_info.scart_noise_error_message
                                            NOS_API.set_error_message("Video Scart")
                                    else:
                                        TEST_CREATION_API.write_log_to_file("Channel with RT-RK color bar pattern was not playing on SCART interface.")
                                        NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.scart_image_freezing_error_code \
                                                                                + "; Error message: " + NOS_API.test_cases_results_info.scart_image_freezing_error_message)
                                        error_codes = NOS_API.test_cases_results_info.scart_image_freezing_error_code
                                        error_messages = NOS_API.test_cases_results_info.scart_image_freezing_error_message
                                        NOS_API.set_error_message("Video Scart")
                                else:
                                    TEST_CREATION_API.write_log_to_file("No video SCART.")
                                    NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.scart_image_absence_error_code \
                                                                            + "; Error message: " + NOS_API.test_cases_results_info.scart_image_absence_error_message)
                                    error_codes = NOS_API.test_cases_results_info.scart_image_absence_error_code
                                    error_messages = NOS_API.test_cases_results_info.scart_image_absence_error_message
                                    NOS_API.set_error_message("Video Scart")
                                    
                                    
                                    
                                if(test_result_SCART_video):
                                
                                    NOS_API.grabber_stop_video_source()
                                    time.sleep(0.5)
                                
                                    ## Start grabber device with audio on SCART audio source
                                    TEST_CREATION_API.grabber_start_audio_source(TEST_CREATION_API.AudioInterface.LINEIN2)
                                    time.sleep(2)
                            
                                    ## Record audio from digital output (SCART)
                                    TEST_CREATION_API.record_audio("SCART_audio", MAX_RECORD_AUDIO_TIME)
                                    
                                    
                                    ## Compare recorded and expected audio and get result of comparison
                                    audio_result_1 = NOS_API.compare_audio("No_Left_ref", "SCART_audio", "[AUDIO_ANALOG]")
                                    audio_result_2 = NOS_API.compare_audio("No_right_ref", "SCART_audio", "[AUDIO_ANALOG]")
                                    audio_result_3 = NOS_API.compare_audio("No_Both_ref", "SCART_audio", "[AUDIO_ANALOG]")
                            
                                    if not(audio_result_1 >= TEST_CREATION_API.AUDIO_THRESHOLD or audio_result_2 >= TEST_CREATION_API.AUDIO_THRESHOLD or audio_result_3 >= TEST_CREATION_API.AUDIO_THRESHOLD):
                            
                                        ## Check is audio present on channel
                                        if (TEST_CREATION_API.is_audio_present("SCART_audio")):
                                            test_result = "PASS"
                                        else:
                                            TEST_CREATION_API.write_log_to_file("Audio is not present on SCART interface.")
                                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.scart_signal_absence_error_code \
                                                                                + "; Error message: " + NOS_API.test_cases_results_info.scart_signal_absence_error_message)
                                            error_codes = NOS_API.test_cases_results_info.scart_signal_absence_error_code
                                            error_messages = NOS_API.test_cases_results_info.scart_signal_absence_error_message
                                            NOS_API.set_error_message("Audio Scart") 
                                    else:
                                        time.sleep(3)
                                        
                                        NOS_API.display_dialog("Confirme o cabo SCART e restantes cabos", NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "Continuar"
                                        
                                        ## Record audio from digital output (SCART)
                                        TEST_CREATION_API.record_audio("SCART_audio1", MAX_RECORD_AUDIO_TIME)
                                    
                                        ## Compare recorded and expected audio and get result of comparison
                                        audio_result_1 = NOS_API.compare_audio("No_Left_ref", "SCART_audio1", "[AUDIO_ANALOG]")
                                        audio_result_2 = NOS_API.compare_audio("No_right_ref", "SCART_audio1", "[AUDIO_ANALOG]")
                                        audio_result_3 = NOS_API.compare_audio("No_Both_ref", "SCART_audio1", "[AUDIO_ANALOG]")
                                    
                                        if not(audio_result_1 >= TEST_CREATION_API.AUDIO_THRESHOLD or audio_result_2 >= TEST_CREATION_API.AUDIO_THRESHOLD or audio_result_3 >= TEST_CREATION_API.AUDIO_THRESHOLD):
                                    
                                            ## Check is audio present on channel
                                            if (TEST_CREATION_API.is_audio_present("SCART_audio1")):
                                                test_result = "PASS"
                                            else:
                                                TEST_CREATION_API.write_log_to_file("Audio is not present on SCART interface.")
                                                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.scart_signal_absence_error_code \
                                                                                        + "; Error message: " + NOS_API.test_cases_results_info.scart_signal_absence_error_message)
                                                error_codes = NOS_API.test_cases_results_info.scart_signal_absence_error_code
                                                error_messages = NOS_API.test_cases_results_info.scart_signal_absence_error_message
                                                NOS_API.set_error_message("Audio Scart") 
                                        else:           
                                            TEST_CREATION_API.write_log_to_file("Audio with RT-RK pattern is not reproduced correctly on SCART interface.")
                                            NOS_API.update_test_slot_comment("Error codes: " + NOS_API.test_cases_results_info.scart_signal_discontinuities_error_code  \
                                                                                        + ";\n" + NOS_API.test_cases_results_info.scart_signal_interference_error_code  \
                                                                                        + "; Error messages: " + NOS_API.test_cases_results_info.scart_signal_discontinuities_error_message \
                                                                                        + ";\n" + NOS_API.test_cases_results_info.scart_signal_interference_error_message)
                                            error_codes = NOS_API.test_cases_results_info.scart_signal_discontinuities_error_code + " " + NOS_API.test_cases_results_info.scart_signal_interference_error_code
                                            error_messages = NOS_API.test_cases_results_info.scart_signal_discontinuities_error_message + " " + NOS_API.test_cases_results_info.scart_signal_interference_error_message
                                            NOS_API.set_error_message("Audio Scart") 
                                            
            else:
                TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                        + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                NOS_API.set_error_message("Reboot")
                error_codes = NOS_API.test_cases_results_info.reboot_error_code
                error_messages = NOS_API.test_cases_results_info.reboot_error_message
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
            