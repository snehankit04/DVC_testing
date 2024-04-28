from collections import defaultdict
import cv2
import numpy as np
from ultralytics import YOLO
import os
from tqdm import tqdm
import argparse
from utils import create_directory_if_not_exists


# mods 
# 1 make a fuction to increase and reduce Bounding box size 

# model = YOLO('models/yolov8m.pt')
# pickup_path = "/home/apple/Desktop/Snehankit/Work/action_recog/code/Data_pipeline/DVC_testing/Data/Stage_1"
# drop_path = os.path.join(pickup_path,'result')

def person_crop_videos(model, pickup_path, drop_path):

    sub_dir = os.listdir(pickup_path)

    for i in sub_dir:
        video_list = os.listdir(os.path.join(pickup_path,i))
        for video in tqdm(video_list):
            video_path = os.path.join(pickup_path,i,video)
            print(video_path)
            os.makedirs("result"+"/"+i+"_crop_person",exist_ok=True)
            
            cap = cv2.VideoCapture(video_path)

            track_history = defaultdict(lambda: [])
            video_writers = {}

            while cap.isOpened():
                success, frame = cap.read()
                if success:
                    try:
                        results = model.track(frame, persist=True,classes=0,verbose=False)
                    except Exception as e:
                        print(f"error : {e}")
                    try:
                        boxes = results[0].boxes.xywh.cpu()
                        track_ids = results[0].boxes.id.int().cpu().tolist()
                        for box, track_id in zip(boxes, track_ids):
                            x, y, w, h = box
                            track = track_history[track_id]
                            track.append((float(x), float(y)))  
                            if len(track) > 30:
                                track.pop(0)
                            obj_crop = frame[int(y - h / 2):int(y + h / 2), int(x - w / 2):int(x + w / 2)]
                            vertical_pad = max(0, (256 - obj_crop.shape[0]) // 2)
                            horizontal_pad = max(0, (256 - obj_crop.shape[1]) // 2)

                            obj_crop = cv2.copyMakeBorder(obj_crop, vertical_pad, vertical_pad, horizontal_pad, horizontal_pad, cv2.BORDER_CONSTANT, value=(0, 255, 0))
                            if obj_crop.shape[1] > 256:
                                obj_crop = cv2.resize(obj_crop, (256, obj_crop.shape[0]))
                            # Resize only height if it's greater than 256
                            if obj_crop.shape[0] > 256:
                                obj_crop = cv2.resize(obj_crop, (obj_crop.shape[1], 256))
                            if track_id not in video_writers:
                                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                                out_vid_name = video.split(".")[0]+f"track_{track_id}.avi"
                                out_dir_name = os.path.join(drop_path,i+"_crop_person")

                                create_directory_if_not_exists(out_dir_name)

                                out_vid_path = os.path.join(out_dir_name,out_vid_name)

                                video_writer = cv2.VideoWriter(out_vid_path, fourcc, 30.0, (256, 256))
                                video_writers[track_id] = video_writer
                            video_writers[track_id].write(obj_crop)
                    except:
                        pass
                    #cv2.imshow("YOLOv8 Tracking", frame)

                    #if cv2.waitKey(1) & 0xFF == ord("q"):
                    #     break
                else:
                    cap.release()
                    cv2.destroyAllWindows()
                    for writer in video_writers.values():
                        writer.release()
                    break


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Process data.')
    parser.add_argument('--input', type=str, help='Input file path')
    parser.add_argument('--model', type=str, help='Model file path')
    args = parser.parse_args()

    if args.input is None or args.model is None:
        parser.error("--input and --model are required")

    model_in = YOLO(args.model)
    pickup_path = args.input
    drop_path = drop_path = os.path.join(pickup_path,'result')
    # create_directory_if_not_exists(drop_path)

    person_crop_videos(model_in, pickup_path, drop_path)
