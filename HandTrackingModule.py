import cv2
import mediapipe as mp
import math

class handDetector:
    def __init__(self, maxHands=1, detectionCon=0.5, trackCon=0.5):
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=False,
            max_num_hands=maxHands,
            min_detection_confidence=detectionCon,
            min_tracking_confidence=trackCon
        )
        self.mpDraw = mp.solutions.drawing_utils
        self.results = None  # Store results

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)  # Store results for later use

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)

        return img

    def findPosition(self, img, handNo=0, draw=True):
        lmList = []
        if self.results and self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

        return lmList

    def get_distance(self, points):
        """Calculate the Euclidean distance between two landmarks."""
        if len(points) != 2:
            raise ValueError("get_distance() requires exactly two points.")

        x1, y1 = points[0][1], points[0][2]  # cx, cy from first point
        x2, y2 = points[1][1], points[1][2]  # cx, cy from second point

        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def main():
    cap = cv2.VideoCapture(0)  # Open webcam
    detector = handDetector()  # Create hand detector instance

    while cap.isOpened():
        success, img = cap.read()
        if not success:
            print("Failed to grab frame.")
            break

        img = detector.findHands(img)  # Detect hands
        lmList = detector.findPosition(img, draw=True)  # Get hand landmarks

        if lmList:
            # Example: Calculate distance between thumb (id=4) and index finger (id=8)
            if len(lmList) > 8:  # Ensure index exists
                thumb_index_dist = detector.get_distance([lmList[4], lmList[8]])
                print(f"Thumb-Index Distance: {thumb_index_dist:.2f}")

        cv2.imshow("Hand Tracking", img)  # Show output

        if cv2.waitKey(1) & 0xFF == 27:  # Press 'ESC' to exit
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
