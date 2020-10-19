#-----------------------------------------------------------------------------
# Copyright (c) 2017 - 2020, Constantino Álvarez, and CV_CONSA_Tools Contributors.
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
#-----------------------------------------------------------------------------

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import cv2
import time
import argparse
import glob
from datetime import datetime



#############################################################################################################################################
#  USAGE:  python3 ./tavideo2frames.py -if ./path/to/my/video/folder -of ./data/images/output -fr "CSV" -sr 0.25
#############################################################################################################################################



########################
#    MAIN FUNCTIONS
########################
def doVideo2Frames(video_path,  output_folder, sample_rate, save_results, show_output, format_results):

    # Starting point
    print("Starting to sample video: " + video_path)

    # For saving results in HDF5 or CSV
    dateTime = datetime.now()
    timestampStr = dateTime.strftime("%d-%b-%Y_(%H:%M:%S.%f)")

    if format_results == "HDF5":
        store_hdf5 = pd.HDFStore(output_folder + '/ta_video2frames_' + timestampStr + '.h5')

    # Record data video. Containers for saving the information.
    df = pd.DataFrame()
    frames_names = []
    time_stamps = []

    ######################
    # Reading input data #
    ######################
    video = video_path.split('/')
    video_name = video[-1].split('.')

    # Video Reader
    cap = cv2.VideoCapture(video_path)
    hasFrame, frame = cap.read()
    if not hasFrame:
        exit(-1)

    # General info from videos
    main_height, main_width, channels_main = frame.shape
    recording_fps = cap.get(cv2.CAP_PROP_FPS)  # Same than video input, but it can be changed.
    total_number_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)  # Same than video input, but it can be changed.

    # General Variables
    frame_count = 1  # We start from 1 because the frame 0 was used for getting the resolution and other meta-info.
    sampling_distance = int(recording_fps / sample_rate)

    # Visual settings
    if show_output:
        cv2.namedWindow("Video Output " + str(video_name[0]), cv2.WINDOW_NORMAL)

    #########################
    #       MAIN LOOP       #
    #########################
    print(" >> INFO:")
    print("     - Processing video: " + str(video_name[0]))
    print("     - Number of frames in the video: " + str(total_number_frames))
    print("     - Sampling 1 frame each " + str(sampling_distance) + " frames.")
    number_sample_frame = 0

    while (1):
        hasFrame, frame = cap.read()

        if not hasFrame:
            break

        output_frame = frame.copy()  # Frame for drawing results

        if frame_count % sampling_distance == 0:

            if number_sample_frame < 10:
                name_frame = video_name[0] + "_00" + str(number_sample_frame)
            elif number_sample_frame > 0 and number_sample_frame < 100:
                name_frame = video_name[0] + "_0" + str(number_sample_frame)
            else:
                name_frame = video_name[0] + "_" + str(number_sample_frame)

            cv2.imwrite(output_folder + "/" + name_frame + ".jpg", output_frame)
            frames_names.append(name_frame + ".jpg")
            time_stamps.append(frame_count / recording_fps)

            number_sample_frame += 1

            if show_output:
                cv2.imshow("Video Output " + str(video_name[0]), output_frame)
            print("           -> Sampled frame number " + str(frame_count) + " of video " + str(video_name[0]))

        frame_count += 1
        k = cv2.waitKey(1)
        if k == 27:
            break


    cv2.destroyAllWindows()

    # Save Dataframe results.
    if save_results:
        print("  >> Saving " + str(len(frames_names)) + " frames of the videos in the input folder...")
        df["Frame name"] = frames_names
        df["Timestamp (seconds)"] = time_stamps

        if format_results == "HDF5":
            store_hdf5.append(df)
        elif format_results == "CSV":
            df.to_csv(output_folder + '/ta_video2frames_' + timestampStr + '.csv', index=False, header=True)


def doVideoFolder2Frames(videos, output_folder, sample_rate, save_results, show_output, format_results):

    # For saving results in HDF5 or CSV
    dateTime = datetime.now()
    timestampStr = dateTime.strftime("%d-%b-%Y_(%H:%M:%S.%f)")

    if format_results == "HDF5":
        store_hdf5 = pd.HDFStore(output_folder + '/ta_videos2frames_' + timestampStr + '.h5')

    video_number = 1
    videos_n = len(videos)

    # Record data video. Containers for saving the information.
    df = pd.DataFrame()
    frames_names = []
    time_stamps = []

    for video_path in videos:

        # Starting point
        print("Starting to sample video: " + video_path)

        ######################
        # Reading input data #
        ######################
        video = video_path.split('/')
        video_name = video[-1].split('.')


        # Video Reader
        cap = cv2.VideoCapture(video_path)
        hasFrame, frame = cap.read()
        if not hasFrame:
            exit(-1)

        # General info from videos
        main_height, main_width, channels_main = frame.shape
        recording_fps = cap.get(cv2.CAP_PROP_FPS)  # Same than video input, but it can be changed.
        total_number_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)  # Same than video input, but it can be changed.




        # General Variables
        frame_count = 1  # We start from 1 because the frame 0 was used for getting the resolution and other meta-info.
        sampling_distance = int(recording_fps/sample_rate)

        # Visual settings
        if show_output:
            cv2.namedWindow("Video Output " + str(video_name[0]), cv2.WINDOW_NORMAL)



        #########################
        #       MAIN LOOP       #
        #########################
        print(" >> INFO:")
        print("     - Processing video: " + str(video_name[0]) + " (" + str(video_number) + "/" + str(videos_n) + ")")
        print("     - Number of frames in the video: " + str(total_number_frames))
        print("     - Sampling 1 frame each " + str(sampling_distance) + " frames.")
        number_sample_frame = 0


        while (1):
            hasFrame, frame = cap.read()

            if not hasFrame:
                break

            output_frame = frame.copy()  # Frame for drawing results

            if frame_count % sampling_distance == 0:

                if number_sample_frame < 10:
                    name_frame = video_name[0] + "_00" + str(number_sample_frame)
                elif number_sample_frame > 0 and number_sample_frame < 100:
                    name_frame = video_name[0] + "_0" + str(number_sample_frame)
                else:
                    name_frame = video_name[0] + "_" + str(number_sample_frame)

                cv2.imwrite(output_folder + "/" + name_frame + ".jpg", output_frame)
                frames_names.append(name_frame + ".jpg")
                time_stamps.append(frame_count/recording_fps)

                number_sample_frame += 1

                if show_output:
                    cv2.imshow("Video Output " + str(video_name[0]), output_frame)
                print("           -> Sampled frame number " + str(frame_count) + " of video " + str(video_name[0]))


            frame_count += 1
            k = cv2.waitKey(1)
            if k == 27:
                break

        video_number += 1
        cv2.destroyAllWindows()

    # Save Dataframe results.
    if save_results:
        print("  >> Saving " + str(len(frames_names)) + " frames of the videos in the input folder...")
        df["Frame name"] = frames_names
        df["Timestamp (seconds)"] = time_stamps

        if format_results == "HDF5":
            store_hdf5.append(df)
        elif format_results == "CSV":
            df.to_csv(output_folder + '/ta_videos2frames_' + timestampStr + '.csv', index=False, header=True)


def main():

    ##########################
    # Input arguments parser #
    ##########################
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video", required=False, help="Path to input video")
    ap.add_argument("-if", "--input_folder", required=False, help="Path to folder with input videos")
    ap.add_argument("-of", "--output_folder", required=False, help="Path to folder to save extracted frames")
    ap.add_argument("-sr", "--sample_rate",  type=float, default=1.0, required=False, help="Number of frames sampled per second")
    ap.add_argument("-sre", "--save_results", type=bool, default=False, required=False, help="Flag for saving the results in HDF5 by default. Default path: /data/images/output/.")
    ap.add_argument("-so", "--show", type=bool, default= False, required=False, help="Flag for showing the results while videos are processed")
    ap.add_argument("-fr", "--format_results", default="HDF5",  required=False,help="Which format will be used to save the results. Options HDF5 or CSV. Default HDF5")


    args = vars(ap.parse_args())


    ######################
    # Reading input data #
    ######################
    # Input data. For our data.
    if args["video"] != None:
        if args["output_folder"] != None:
            output_folder = args["output_folder"]
        else:
            output_folder = "./data/images/output"

        doVideo2Frames(args["video"], output_folder, args["sample_rate"], args["save_results"], args["show"], args["format_results"])

    elif args["input_folder"] != None:
        videos_mp4 = glob.glob(args["input_folder"] + '/*.mp4')
        videos_avi = glob.glob(args["input_folder"] + '/*.avi')
        videos_avi2 = glob.glob(args["input_folder"] + '/*.AVI')
        videos = videos_avi + videos_mp4 + videos_avi2

        if videos:
            print("Number of videos detected in " + args["input_folder"]+ " folder: " + str(len(videos)))
            if args["output_folder"] != None:
                output_folder = args["output_folder"]
            else:
                output_folder = "./data/images/output"
            doVideoFolder2Frames(videos, output_folder, args["sample_rate"], args["save_results"], args["show"], args["format_results"])
        else:
            print("The input folder passed through arguments is empty...")
    else:
        videos_mp4 = glob.glob('./data/videos/*.mp4')
        videos_avi = glob.glob('./data/videos/*.avi')
        videos_avi2 = glob.glob('./data/videos/*.AVI')
        videos = videos_avi + videos_mp4 + videos_avi2
        if videos:
            print("Number of videos detected in ./data/videos/ folder: " + str(len(videos)))
            if args["output_folder"] != None:
                output_folder = args["output_folder"]
            else:
                output_folder = "./data/images/output"
            doVideoFolder2Frames(videos, output_folder, args["sample_rate"], args["save_results"], args["show"], args["format_results"])
        else:
            print("The input default folder passed through arguments is empty...")

    print("Work done!")


if __name__ == "__main__":
    main()