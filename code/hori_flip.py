import os 
import cv2
from utils import is_video_file, add_tags


def flip_video(input_file, output_file):
    # Open the video file
    cap = cv2.VideoCapture(input_file)
    
    # Get the frames per second (fps) of the video
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    # Get the total number of frames in the video
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Get the width and height of the frames
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # Create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))
    
    # Read frames from the video, flip them horizontally, and write them to the output file
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        flipped_frame = cv2.flip(frame, 1)  # Flip horizontally (1)
        out.write(flipped_frame)
        print(f"Done  putting in place : {output_file}")
    # Release the video objects
    cap.release()
    out.release()

if __name__ == "__main__":
    path_a = os.path.normpath("/home/apple/Desktop/Snehankit/Work/action_recog/code/Data_pipeline/DVC_testing/Data/Normal")
    out_p = os.path.normpath("/home/apple/Desktop/Snehankit/Work/action_recog/code/Data_pipeline/DVC_testing/Data/flipped")
    
    for pat in os.listdir(path_a):
        if is_video_file(pat) == True:
            input_file = os.path.join(path_a, pat)
            output_name = add_tags(input_file,"hp","avi")
            output_file = os.path.join(out_p, output_name)
            flip_video(input_file, output_file)
            print(f"Video is flipped  : {output_name}")
    
