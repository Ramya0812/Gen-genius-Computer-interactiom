import cv2
import mediapipe as mp
import pyautogui
import random
from pynput.mouse import Button, Controller

# Initialize mouse control
mouse = Controller()
screen_width, screen_height = pyautogui.size()

# Initialize MediaPipe Hands
mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
    max_num_hands=1
)

def calculate_distance(point1, point2):
    """Calculate Euclidean distance between two points."""
    if point1 is None or point2 is None:
        return float('inf')  # Avoid crashes when points are missing
    x1, y1 = point1
    x2, y2 = point2
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

def move_mouse(index_finger_tip):
    """Move the mouse cursor to the position of the index finger."""
    if index_finger_tip:
        x = int(index_finger_tip[0])
        y = int(index_finger_tip[1])
        pyautogui.moveTo(x, y)

def is_left_click(landmark_list):
    """Detect left-click gesture."""
    return calculate_distance(landmark_list.get(4), landmark_list.get(8)) < 40

def is_right_click(landmark_list):
    """Detect right-click gesture."""
    return calculate_distance(landmark_list.get(4), landmark_list.get(12)) < 40

def is_double_click(landmark_list):
    """Detect double-click gesture."""
    return is_left_click(landmark_list) and is_right_click(landmark_list)

def is_screenshot(landmark_list):
    """Detect screenshot gesture."""
    return calculate_distance(landmark_list.get(4), landmark_list.get(16)) < 40

def detect_gesture(frame, landmark_list):
    """Detect gestures and perform actions."""
    if not landmark_list:  # Ensure there are landmarks
        return

    index_finger_tip = landmark_list.get(8)
    move_mouse(index_finger_tip)

    if is_left_click(landmark_list):
        mouse.press(Button.left)
        mouse.release(Button.left)
        cv2.putText(frame, "Left Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    elif is_right_click(landmark_list):
        mouse.press(Button.right)
        mouse.release(Button.right)
        cv2.putText(frame, "Right Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    
    elif is_double_click(landmark_list):
        pyautogui.doubleClick()
        cv2.putText(frame, "Double Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
    
    elif is_screenshot(landmark_list):
        screenshot = pyautogui.screenshot()
        label = random.randint(1, 1000)
        screenshot.save(f'my_screenshot_{label}.png')
        cv2.putText(frame, "Screenshot Taken", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

def main():
    """Main function to run the hand gesture control system."""
    draw = mp.solutions.drawing_utils
    cap = cv2.VideoCapture(0)

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            processed = hands.process(frameRGB)

            landmark_list = {}
            if processed.multi_hand_landmarks:
                for hand_landmarks in processed.multi_hand_landmarks:
                    draw.draw_landmarks(frame, hand_landmarks, mpHands.HAND_CONNECTIONS)

                    # Extract landmark positions
                    for id, lm in enumerate(hand_landmarks.landmark):
                        x, y = int(lm.x * screen_width), int(lm.y * screen_height)
                        landmark_list[id] = (x, y)  # Store landmarks in dictionary

            # Detect gestures
            detect_gesture(frame, landmark_list)

            cv2.imshow('Hand Gesture Control', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
