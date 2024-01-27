#import dependencies
import cv2
import mediapipe as mp
import MouseControl as mc
import time
#initialize pose estimator
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

pose = mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)


# create capture object (uncomment to use a video file)
# cap = cv2.VideoCapture('video2.mp4')

#capture webcam (uncomment to use webcam)
cap = cv2.VideoCapture(0)

position_epaules_initiales = None
position = "normal"
previous_position = "normal"

position_hauteur = "normal"
previous_position_hauteur = "normal"

width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
print(width , height)

while cap.isOpened():
    # read frame from capture object
    ret , frame = cap.read()
    
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    key = cv2.waitKey(1)

    try:
        start_time = time.time()

    	# convert the frame to RGB format
        RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # process the RGB frame to get the result
        results = pose.process(RGB)
        # draw detected skeleton on the frame
        mp_drawing.draw_landmarks(
            frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # show the final output
        cv2.imshow('Output', frame)
        position_hauteur = "normal"
        position = "normal"
        if position_epaules_initiales!=None and results.pose_landmarks!=None : 
            actual_position_epaules = (results.pose_landmarks.landmark[0], results.pose_landmarks.landmark[0])
            lhand_pos = results.pose_landmarks.landmark[15]
            rhand_pos = results.pose_landmarks.landmark[14]
            if position_epaules_initiales[0].x < actual_position_epaules[0].x - 0.1:
                position = "gauche"
            if position_epaules_initiales[0].x > actual_position_epaules[0].x + 0.1:
                position = "droite"
            if position_epaules_initiales[0].y < actual_position_epaules[0].y - 0.05 and lhand_pos_initial.y < lhand_pos.y - 0.1 and rhand_pos_initial.y < rhand_pos.y - 0.1 :
                position_hauteur = "bas"
            if position_epaules_initiales[0].y > actual_position_epaules[0].y + 0.03 and lhand_pos_initial.y < lhand_pos.y + 0.1 and rhand_pos_initial.y < rhand_pos.y + 0.1 :
                position_hauteur = "haut"

            if position != previous_position:
                if position == "gauche":
                    print("gauche")
                    mc.go_left_arrow()
                if position == "droite":
                    print("droite")
                    mc.go_right_arrow()
                if position == "normal" and previous_position == "gauche":
                    print("normal")
                    mc.go_right_arrow()
                if position == "normal" and previous_position == "droite":
                    print("normal")
                    mc.go_left_arrow()
            if position_hauteur != previous_position_hauteur:
                if position_hauteur == "bas":
                    print("baisse")
                    mc.go_bot_arrow()
                if position_hauteur == "haut":
                    print("saute")
                    mc.go_top_arrow()
                

            previous_position = position
            previous_position_hauteur = position_hauteur
                
        end_time = time.time()
        elapsed_time = end_time - start_time
        # print(f"Elapsed time: {elapsed_time} seconds")
        if key == ord('q'):
            print("q pressed")
            break
        if key == ord('d'):
            print("d pressed")
            position_epaules_initiales = (results.pose_landmarks.landmark[0], results.pose_landmarks.landmark[0])
            lhand_pos_initial = results.pose_landmarks.landmark[15]
            rhand_pos_initial = results.pose_landmarks.landmark[14]
            print( position_epaules_initiales[0].x, 0, position_epaules_initiales[0].x, int(height))
            cv2.line(frame, (10, 0), (10, int(height)), (0, 255, 0), 2)
    except Exception as e:
        print(e)
        print("Error in processing frame")
        break
    
print("ok avant release")
cap.release()
cv2.destroyAllWindows()
print("ok apres release")



