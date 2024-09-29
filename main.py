import cv2
import mediapipe as mp

from poseValues import PoseValues

COLOR_POINT = (250, 100, 250)
COLOR_CONNECTION = (250, 250, 250)
RADIUS_SIZE = 6
LINE_SIZE = 3

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

with mp_pose.Pose(static_image_mode=True) as pose:
    image = cv2.imread('image2.jpeg')
    print(image.shape)
    height, width, _ = image.shape

    image_rgb = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    results = pose.process(image_rgb)

    if results.pose_landmarks:

        landmarks = results.pose_landmarks.landmark

        points, connections = PoseValues.get_left_body()

        for point in points:
            cv2.circle(
                image,
                (
                    int(landmarks[point].x * width),
                    int(landmarks[point].y * height)
                ),
                RADIUS_SIZE,
                COLOR_POINT,
                -1
            )

        for connection in connections:
            x1 = int(landmarks[connection[0]].x * width)
            x2 = int(landmarks[connection[1]].x * width)
            y1 = int(landmarks[connection[0]].y * height)
            y2 = int(landmarks[connection[1]].y * height)

            cv2.line(
                image,
                (x1, y1),
                (x2, y2),
                COLOR_CONNECTION,
                LINE_SIZE
            )

        cv2.imwrite('result_image2.jpeg', image)
