import os 
import cv2
from utils import is_video_file, add_tags


def reverse_video(input_file, output_file):
    """_summary_

    Args:
        input_file (_type_): _description_
        output_file (_type_): _description_
    """
    # Open the video file
    cap = cv2.VideoCapture(input_file)
    
    # Get the frames per second (fps) of the video
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    # Get the total number of frames in the video
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(total_frames)
    # Create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_file, fourcc, fps, (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))
    
    # Read frames from the video and write them in reverse order
    for frame_num in range(total_frames - 1, -1, -1):
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
        ret, frame = cap.read()

        if ret:
            out.write(frame)
    
    # Release the video objects
    cap.release()
    out.release()


def is_video_file(file_path):
    video_extensions = ['avi', 'mp4', 'mkv', 'mov', 'flv', 'wmv', 'webm']
    ext = file_path.split('.')[-1].lower()
    return ext in video_extensions


if __name__ == "__main__":
    path_a = os.path.normpath("/home/apple/Desktop/Snehankit/Work/action_recog/code/Data_pipeline/DVC_testing/Data/Normal")
    out_p = os.path.normpath("/home/apple/Desktop/Snehankit/Work/action_recog/code/Data_pipeline/DVC_testing/Data/flipped")

    for pat in os.listdir(path_a):
        if is_video_file(pat) == True:
            input_file = os.path.join(path_a, pat)
            output_name = add_tags(input_file,"rev","avi")
            output_file = os.path.join(out_p, output_name)
            reverse_video(input_file, output_file)
            print(f"Video is reversed : {output_name}")
  