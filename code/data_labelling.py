import pandas as pd
import cv2
import os
import uuid

def main():
    # Paths
    csv_file = r'C:\Users\assad\Desktop\data_labelling\Infra_Motion_annotation-Dev_Copy3_2_2024.csv'
    videos_folder = r'C:\Users\assad\Desktop\data_labelling\31-01-2024_malmo'
    output_folder = r'C:\Users\assad\Desktop\data_labelling\output_data'

    # Load data
    df = load_data(csv_file)

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
    for index, row in df.iterrows():
        video_name = row['Video_name']
        action = row['Action']
        start_time = row['Start_time']
        end_time = row['End_time']

        video_path = os.path.join(videos_folder, video_name)

        start_time_seconds = time_to_seconds(start_time)
        end_time_seconds = time_to_seconds(end_time)

        clip_video(video_path, start_time_seconds, end_time_seconds, action, output_folder)

def time_to_seconds(time_str):
    minutes, seconds = map(int, time_str.split(':'))
    return minutes * 60 + seconds

def clip_video(video_path, start_time_seconds, end_time_seconds, action, output_folder):
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
    main()
