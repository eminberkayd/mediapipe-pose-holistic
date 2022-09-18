import cv2
import numpy as np
import mediapipe as mp
import pandas as pd
import matplotlib.pyplot as plt

column_list = ['NOSE_x',
 'NOSE_y',
 'NOSE_z',
 'LEFT_EYE_INNER_x',
 'LEFT_EYE_INNER_y',
 'LEFT_EYE_INNER_z',
 'LEFT_EYE_x',
 'LEFT_EYE_y',
 'LEFT_EYE_z',
 'LEFT_EYE_OUTER_x',
 'LEFT_EYE_OUTER_y',
 'LEFT_EYE_OUTER_z',
 'RIGHT_EYE_INNER_x',
 'RIGHT_EYE_INNER_y',
 'RIGHT_EYE_INNER_z',
 'RIGHT_EYE_x',
 'RIGHT_EYE_y',
 'RIGHT_EYE_z',
 'RIGHT_EYE_OUTER_x',
 'RIGHT_EYE_OUTER_y',
 'RIGHT_EYE_OUTER_z',
 'LEFT_EAR_x',
 'LEFT_EAR_y',
 'LEFT_EAR_z',
 'RIGHT_EAR_x',
 'RIGHT_EAR_y',
 'RIGHT_EAR_z',
 'MOUTH_LEFT_x',
 'MOUTH_LEFT_y',
 'MOUTH_LEFT_z',
 'MOUTH_RIGHT_x',
 'MOUTH_RIGHT_y',
 'MOUTH_RIGHT_z',
 'LEFT_SHOULDER_x',
 'LEFT_SHOULDER_y',
 'LEFT_SHOULDER_z',
 'RIGHT_SHOULDER_x',
 'RIGHT_SHOULDER_y',
 'RIGHT_SHOULDER_z',
 'LEFT_ELBOW_x',
 'LEFT_ELBOW_y',
 'LEFT_ELBOW_z',
 'RIGHT_ELBOW_x',
 'RIGHT_ELBOW_y',
 'RIGHT_ELBOW_z',
 'LEFT_WRIST_x',
 'LEFT_WRIST_y',
 'LEFT_WRIST_z',
 'RIGHT_WRIST_x',
 'RIGHT_WRIST_y',
 'RIGHT_WRIST_z',
 'LEFT_PINKY_x',
 'LEFT_PINKY_y',
 'LEFT_PINKY_z',
 'RIGHT_PINKY_x',
 'RIGHT_PINKY_y',
 'RIGHT_PINKY_z',
 'LEFT_INDEX_x',
 'LEFT_INDEX_y',
 'LEFT_INDEX_z',
 'RIGHT_INDEX_x',
 'RIGHT_INDEX_y',
 'RIGHT_INDEX_z',
 'LEFT_THUMB_x',
 'LEFT_THUMB_y',
 'LEFT_THUMB_z',
 'RIGHT_THUMB_x',
 'RIGHT_THUMB_y',
 'RIGHT_THUMB_z',
 'LEFT_HIP_x',
 'LEFT_HIP_y',
 'LEFT_HIP_z',
 'RIGHT_HIP_x',
 'RIGHT_HIP_y',
 'RIGHT_HIP_z',
 'LEFT_KNEE_x',
 'LEFT_KNEE_y',
 'LEFT_KNEE_z',
 'RIGHT_KNEE_x',
 'RIGHT_KNEE_y',
 'RIGHT_KNEE_z',
 'LEFT_ANKLE_x',
 'LEFT_ANKLE_y',
 'LEFT_ANKLE_z',
 'RIGHT_ANKLE_x',
 'RIGHT_ANKLE_y',
 'RIGHT_ANKLE_z',
 'LEFT_HEEL_x',
 'LEFT_HEEL_y',
 'LEFT_HEEL_z',
 'RIGHT_HEEL_x',
 'RIGHT_HEEL_y',
 'RIGHT_HEEL_z',
 'LEFT_FOOT_INDEX_x',
 'LEFT_FOOT_INDEX_y',
 'LEFT_FOOT_INDEX_z',
 'RIGHT_FOOT_INDEX_x',
 'RIGHT_FOOT_INDEX_y',
 'RIGHT_FOOT_INDEX_z']

def imagePose(img_path:str,
              model_complexity=1,
              smooth_landmarks=True,
              enable_segmentation=False,
              smooth_segmentation=True,
              min_detection_confidence=0.5,
              min_tracking_confidence=0.5,
              plot=True,
              display=True):
    """
    img_path = `str` : full path of the image, including name and extension\n
    """
    global column_list

    img = cv2.imread(filename=img_path)
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils

    with mp_pose.Pose(
        model_complexity,
        smooth_landmarks,
        enable_segmentation,
        smooth_segmentation,
        min_detection_confidence,
        min_tracking_confidence,
        static_image_mode=True,
    ) as pose:
    

        result = pose.process(img)

        landmarks = []
        for landmark in result.pose_landmarks.landmark:
            values = [landmark.x,landmark.y,landmark.z]
            landmarks.extend(values)
        
        new_landmarks = pd.DataFrame(landmarks,index=column_list)

        if(plot):
            
            mp_drawing.plot_landmarks(result.pose_landmarks,
                                    mp_pose.POSE_CONNECTIONS)
        if(display):
            mp_drawing.draw_landmarks(image=img,
                                    landmark_list=result.pose_landmarks,
                                    connections=mp_pose.POSE_CONNECTIONS)
        
        new_filename = img_path.split("\\")[-1].split(".")[0]
        extension = img_path.split("\\")[-1].split(".")[1]
        new_img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
        cv2.imwrite(new_filename+"_landmarked."+extension, new_img)
        new_landmarks.to_csv(new_filename+".csv")

    return new_landmarks, new_img

def videoPose(video_path: str,
              model_complexity=1,
              smooth_landmarks=True,
              enable_segmentation=False,
              smooth_segmentation=True,
              min_detection_confidence=0.5,
              min_tracking_confidence=0.5,
              display=True):
    """
    video_path = `str` : full path of the video, including name and extension\n
    
    """
    global column_list
    cap = cv2.VideoCapture(video_path)
    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils
    
    with mp_pose.Pose(
        model_complexity,
        smooth_landmarks,
        enable_segmentation,
        smooth_segmentation,
        min_detection_confidence,
        min_tracking_confidence
    ) as pose:
        landmarked_df = pd.DataFrame(columns=column_list)
        counter = 0
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break
            counter+=1
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_result = pose.process(frame)
            
            if(counter==10):
                counter=0
                landmarks = []
                for landmark in frame_result.pose_landmarks.landmark:
                    values = [landmark.x,landmark.y,landmark.z]
                    landmarks.extend(values)
                
                new_landmarks = pd.Series(landmarks,index=column_list)

                landmarked_df = landmarked_df.append(new_landmarks, ignore_index=True)
                print(landmarked_df)
            
            if (display):
                mp_drawing.draw_landmarks(
                frame,
                frame_result.pose_landmarks,
                mp_pose.POSE_CONNECTIONS)

                cv2.imshow("Landmarked",cv2.cvtColor(frame,cv2.COLOR_RGB2BGR))
                if(cv2.waitKey(5) & 0xFF == 27):
                    break
           
    cap.release()
    cv2.destroyAllWindows()
    landmarked_df.to_csv("landmarked_video.csv")


#serie, new_img = imagePose(img_path="full-path-of-the-image")
#cv2.imshow("Landmark Image", new_img)
#cv2.waitKey(0)

videoPose(video_path="full-path-of-the-video")
