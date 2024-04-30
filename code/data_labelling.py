import os
import cv2
import sys
import yaml
import uuid
import argparse
import pandas as pd
from tqdm import tqdm
from utils import create_directory_if_not_exists


def main(csv_path,in_folder,out_folder):
    # Paths
    # csv_file = r'C:\Users\assad\Desktop\data_labelling\Infra_Motion_annotation-Dev_Copy3_2_2024.csv'
    # videos_folder = r'C:\Users\assad\Desktop\data_labelling\31-01-2024_malmo'
    # output_folder = r'C:\Users\assad\Desktop\data_labelling\output_data'


    csv_file = csv_path
    videos_folder = in_folder
    output_folder = out_folder


    print(f"csv_file: {csv_file}\nvideos_folder: {videos_folder} \noutput_folder: {output_folder}")
    print(f"csv_file: {type(csv_file)}\nvideos_folder: {type(videos_folder)} \noutput_folder: {type(output_folder)}")

    # Load data
    df = load_data(csv_file)
    # print(df.head(5))
    # Clean data
    df = clean_data(df)

    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Process videos
    process_videos(df, videos_folder, output_folder)

    print("Video clipping completed.")

def load_data(csv_file):
    return pd.read_csv(csv_file)

def clean_data(df):
    # Remove brackets and spaces from the DataFrame
    df = df.replace({'\[|\]|\s': ''}, regex=True)
    # Forward fill the 'Video_name' column
    df['Video_name'].ffill(inplace=True)
    # Remove all columns after the 'End_time' column
    df = df.iloc[:, :4]
    # Apply the function to 'Start_time' and 'End_time' columns
    df['Start_time'] = df['Start_time'].apply(remove_milliseconds)
    df['End_time'] = df['End_time'].apply(remove_milliseconds)
    return df

def remove_milliseconds(time_str):
    if ':' in time_str and time_str.count(':') == 2:  # Check if the string contains milliseconds
        return ':'.join(time_str.split(':')[:-1])  # Remove milliseconds
    return time_str  # If no milliseconds, return the original string

def process_videos(df, videos_folder, output_folder):
    # Iterate over rows in DataFrame
    for _, row in tqdm(df.iterrows()):
        video_name = row['Video_name']
        action = row['Action']
        start_time = row['Start_time']
        end_time = row['End_time']

        video_path = os.path.join(videos_folder, video_name)

        start_time_seconds = time_to_seconds(start_time)
        end_time_seconds = time_to_seconds(end_time)

        clip_video(video_path, video_name,start_time_seconds, end_time_seconds, action, output_folder)

def time_to_seconds(time_str):
    minutes, seconds = map(int, time_str.split(':'))
    return minutes * 60 + seconds

def clip_video(video_path, video_name, start_time_seconds, end_time_seconds, action, output_folder):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    unique_identifier = str(uuid.uuid4())[:8]
    output_filename = f"{video_name.split('.')[0]}_{unique_identifier}.avi"
    output_file_path = os.path.join(output_folder, action, output_filename)
    
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    out = cv2.VideoWriter(output_file_path, fourcc, fps, (width, height))

    cap.set(cv2.CAP_PROP_POS_FRAMES, int(start_time_seconds * fps))

    for _ in range(int((end_time_seconds - start_time_seconds) * fps)):
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)

    cap.release()
    out.release()

if __name__ == "__main__":
    
    
    # parser = argparse.ArgumentParser(description='Process data.')
    # parser.add_argument('--csv', type=str, help='Input csv path')
    # parser.add_argument('--input', type=str, help='Input folder path')
    # parser.add_argument('--output', type=str, help='Output folder path')
    # args = parser.parse_args()

    # if args.input is None or args.output is None or args.csv is None:
    #     parser.error("--input and --output and --csv are required")

    # csv_path = args.csv
    # input_folder = args.input
    # output_folder = args.output

    with open('params.yaml','r') as f:
        data = yaml.safe_load(f)

    print("Entered in Data labelling")
    # print(f'param file contains : {data}')

    csv_path = data['data_labelling']['csv_path']
    input_folder = data['data_labelling']['input_folder']
    output_folder = data['data_labelling']['output_folder']

    create_directory_if_not_exists(output_folder)

    # print(f"csv_path:{csv_path},\npickup_path:{input_folder},\ndrop_path:{output_folder}")

    print("\nDone with Data labelling")


    main(csv_path, input_folder, output_folder)
