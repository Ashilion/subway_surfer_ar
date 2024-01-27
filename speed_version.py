#import dependencies
import cv2
import mediapipe as mp
import MouseControl as mc
import time

from collections import deque
from statistics import mean

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

last_speed = deque([0 for i in range(6)])
last_speed_hauteur = deque([0 for i in range(6)])

list_speed  = []
list_speed_hauteur = []

already_swiped = False
already_swiped_top = False
already_swiped_bot = False

test_finished = False
#param speed
speed_cap = 0.07
speed_cap_hauteur = 0.07

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

        #instant speed calculation
        # Assuming last_speed is your deque
        if results.pose_landmarks!=None and results.pose_landmarks.landmark[0] is not None :
            last_speed.popleft()  # remove element from left
            last_speed.append(results.pose_landmarks.landmark[0].x) # add var to right
            # Calculate the average speed of the left half and the right half
            half = len(last_speed) // 2
            left_half = mean(list(last_speed)[:half])
            right_half = mean(list(last_speed)[half:])
            
            # vertical speed
            last_speed_hauteur.popleft()
            last_speed_hauteur.append(results.pose_landmarks.landmark[0].y)
            half_hauteur = len(last_speed_hauteur) // 2
            left_half_hauteur = mean(list(last_speed_hauteur)[:half_hauteur])
            right_half_hauteur = mean(list(last_speed_hauteur)[half_hauteur:])
            
            
            # Calculate the speed
            speed = right_half - left_half
            list_speed.append(speed)
            if speed > speed_cap and already_swiped == False:
                print("swipe left ")
                mc.go_left_arrow()
                already_swiped = True
            if speed < -speed_cap and already_swiped == False:
                print("swipe right")
                mc.go_right_arrow()
                already_swiped = True
            if speed < speed_cap and speed > -speed_cap:
                already_swiped = False
            
            # calculate the vertical speed
            speed_hauteur = right_half_hauteur - left_half_hauteur
            list_speed_hauteur.append(speed_hauteur)
            
            
            # the test is different , for a swipe up we need to go up and then down , so we need to put already_swiped_hauteur to False when we are back to normal
            if speed_hauteur > speed_cap_hauteur and already_swiped_bot == False and already_swiped_top== False:
                print("swipe down", already_swiped_top, already_swiped_bot)
                mc.go_bot_arrow()
                already_swiped_bot = True
            if speed_hauteur < -speed_cap_hauteur and already_swiped_bot == False and already_swiped_top== False:
                print("swipe up", already_swiped_top, already_swiped_bot)
                mc.go_top_arrow()
                already_swiped_top = True
            if speed_hauteur < -speed_cap_hauteur and already_swiped_bot == True:
                test_finished = True
                print(already_swiped_top, already_swiped_bot)
            if speed_hauteur > speed_cap_hauteur  and already_swiped_top == True:
                test_finished = True
                print(already_swiped_top, already_swiped_bot)
            if speed_hauteur < 0.03 and speed_hauteur > -0.03  and test_finished == True :
                print(test_finished, already_swiped_top, already_swiped_bot)
                already_swiped_bot = False
                already_swiped_top = False
                test_finished = False
            
            
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
            if position_epaules_initiales[0].y < actual_position_epaules[0].y - 0.03  :
                position_hauteur = "bas"
            if position_epaules_initiales[0].y > actual_position_epaules[0].y + 0.02 :
                position_hauteur = "haut"

            # if position != previous_position:
            #     if position == "gauche":
            #         print("gauche")
            #         mc.go_left_arrow()
            #     if position == "droite":
            #         print("droite")
            #         mc.go_right_arrow()
            #     if position == "normal" and previous_position == "gauche":
            #         print("normal")
            #         mc.go_right_arrow()
            #     if position == "normal" and previous_position == "droite":
            #         print("normal")
            #         mc.go_left_arrow()
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

import matplotlib.pyplot as plt

plt.plot([i for i in range(len(list_speed_hauteur))], list_speed_hauteur)
plt.show()


