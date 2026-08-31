import cv2
import mediapipe as mp
import pyautogui
import math
import time

# -----------------------------
# CAMERA
# -----------------------------
cap = cv2.VideoCapture(0)

# -----------------------------
# MEDIAPIPE
# -----------------------------
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# -----------------------------
# VARIABLES
# -----------------------------
neutral_angle = None
current_key = None

# Steering settings
DEAD_ZONE = 8
MAX_ANGLE = 45

# Smoothing
smooth_angle = 0

print("Virtual Steering Started")
print("Put both hands in front of the camera.")
print("Press C to calibrate the center position.")
print("Press Q to quit.")

# -----------------------------
# KEYBOARD CONTROL
# -----------------------------
def change_key(new_key):

    global current_key

    if new_key == current_key:
        return

    # Release previous key
    if current_key == "left":
        pyautogui.keyUp("left")

    elif current_key == "right":
        pyautogui.keyUp("right")

    # Press new key
    if new_key == "left":
        pyautogui.keyDown("left")

    elif new_key == "right":
        pyautogui.keyDown("right")

    current_key = new_key


# -----------------------------
# MAIN LOOP
# -----------------------------
while True:

    success, frame = cap.read()

    if not success:
        break

    # Mirror camera
    frame = cv2.flip(frame, 1)

    h, w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb)

    # -----------------------------
    # FIND BOTH HANDS
    # -----------------------------
    hand_points = []

    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

            # Wrist landmark
            wrist = hand_landmarks.landmark[0]

            x = int(wrist.x * w)
            y = int(wrist.y * h)

            hand_points.append((x, y))

            # Draw hand
            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            # Draw wrist
            cv2.circle(
                frame,
                (x, y),
                12,
                (0, 255, 0),
                -1
            )

    # -----------------------------
    # TWO HAND STEERING
    # -----------------------------
    if len(hand_points) == 2:

        # Sort hands from left to right
        hand_points = sorted(hand_points)

        left_hand = hand_points[0]
        right_hand = hand_points[1]

        x1, y1 = left_hand
        x2, y2 = right_hand

        # Draw imaginary steering wheel line
        cv2.line(
            frame,
            left_hand,
            right_hand,
            (255, 255, 255),
            5
        )

        # Midpoint of both hands
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2

        # Draw steering wheel center
        cv2.circle(
            frame,
            (center_x, center_y),
            25,
            (255, 255, 255),
            3
        )

        # Calculate angle of line connecting both hands
        angle = math.degrees(
            math.atan2(
                y2 - y1,
                x2 - x1
            )
        )

        # Convert angle to steering angle
        # Horizontal = 0 degrees
        steering_angle = angle

        # -----------------------------
        # CALIBRATION
        # -----------------------------
        if neutral_angle is None:
            neutral_angle = steering_angle

        relative_angle = steering_angle - neutral_angle

        # Keep angle between -180 and 180
        if relative_angle > 180:
            relative_angle -= 360

        if relative_angle < -180:
            relative_angle += 360

        # Smoothing
        smooth_angle = (
            smooth_angle * 0.8
            + relative_angle * 0.2
        )

        # -----------------------------
        # STEERING DECISION
        # -----------------------------
        if smooth_angle < -DEAD_ZONE:
            direction = "LEFT"
            change_key("left")

        elif smooth_angle > DEAD_ZONE:
            direction = "RIGHT"
            change_key("right")

        else:
            direction = "CENTER"
            change_key(None)

        # -----------------------------
        # DISPLAY
        # -----------------------------
        cv2.putText(
            frame,
            f"Angle: {smooth_angle:.1f}",
            (30, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"STEERING: {direction}",
            (30, 90),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        # -----------------------------
        # VIRTUAL STEERING WHEEL
        # -----------------------------
        wheel_radius = 100

        cv2.circle(
            frame,
            (center_x, center_y),
            wheel_radius,
            (255, 255, 255),
            4
        )

        # Calculate wheel pointer
        wheel_angle = math.radians(
            -smooth_angle
        )

        pointer_x = int(
            center_x
            + wheel_radius * math.cos(wheel_angle)
        )

        pointer_y = int(
            center_y
            + wheel_radius * math.sin(wheel_angle)
        )

        cv2.line(
            frame,
            (center_x, center_y),
            (pointer_x, pointer_y),
            (0, 255, 0),
            6
        )

    else:

        # No two hands
        change_key(None)

        cv2.putText(
            frame,
            "SHOW BOTH HANDS",
            (30, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2
        )

    # -----------------------------
    # INSTRUCTIONS
    # -----------------------------
    cv2.putText(
        frame,
        "C = Calibrate | Q = Quit",
        (30, h - 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )

    cv2.imshow(
        "Two-Hand Virtual Steering",
        frame
    )

    key = cv2.waitKey(1) & 0xFF

    # Calibration
    if key == ord("c"):

        if len(hand_points) == 2:

            x1, y1 = hand_points[0]
            x2, y2 = hand_points[1]

            neutral_angle = math.degrees(
                math.atan2(
                    y2 - y1,
                    x2 - x1
                )
            )

            smooth_angle = 0

            print("Steering center calibrated!")

    # Quit
    if key == ord("q"):
        break


# -----------------------------
# CLEANUP
# -----------------------------
change_key(None)

cap.release()
cv2.destroyAllWindows()