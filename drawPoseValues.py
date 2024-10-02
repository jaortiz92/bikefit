import cv2
import mediapipe as mp


from constants import Constants
from poseValues import PoseValues


class DrawPoseValues():

    def __init__(
        self, path: str, name: str,
        format: str, is_image: bool = True,
        is_right: bool = True
    ):
        self.is_image: bool = is_image
        self.is_right: bool = is_right
        self.name_input: str = '{}/{}.{}'.format(path, name, format)
        self.name_output: str = '{}/result_{}.{}'.format(path, name, format)
        self.key_moments: dict = {
            'lowest_point': None,
            'highest_point': None,
            'middle_point': None
        }
        self.generate()

    def generate(self):
        mp_drawing = mp.solutions.drawing_utils
        mp_pose = mp.solutions.pose

        with mp_pose.Pose(static_image_mode=True) as pose:
            if self.is_image:
                image = cv2.imread(self.name_input)
                height, width, _ = image.shape

                image_rgb = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                result_pose = pose.process(image_rgb)
                if result_pose.pose_landmarks:
                    image = self.add_values(
                        result_pose, image,
                        self.is_right, width, height
                    )
                    cv2.imwrite(self.name_output, image)

            else:
                cap = cv2.VideoCapture(self.name_input)
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                fps = 30
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

                out = cv2.VideoWriter(
                    self.name_output,
                    fourcc, fps, (width, height))

                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret:
                        break

                    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    result_pose = pose.process(image_rgb)

                    if result_pose.pose_landmarks:
                        image = frame
                        image = self.add_values(
                            result_pose, image,
                            self.is_right, width, height,
                        )
                    out.write(image)

    def add_values(
            self, result_pose, image, is_right: bool,
            width: int, height: int
    ):
        landmarks = result_pose.pose_landmarks.landmark

        if is_right:
            funct = PoseValues.get_right_body
        else:
            funct = PoseValues.get_left_body

        points, connections, angles = funct()

        for connection in connections:
            if not isinstance(connection[0], tuple):
                x1 = int(landmarks[connection[0]].x * width)
                x2 = int(landmarks[connection[1]].x * width)
                y1 = int(landmarks[connection[0]].y * height)
                y2 = int(landmarks[connection[1]].y * height)
            else:
                x1 = int(landmarks[connection[0][0]].x * width)
                x2 = int(landmarks[connection[1][0]].x * width)
                y1 = int(landmarks[connection[0][1]].y * height)
                y2 = int(landmarks[connection[1][1]].y * height)

            cv2.line(
                image,
                (x1, y1),
                (x2, y2),
                Constants.COLOR_CONNECTION,
                Constants.LINE_SIZE
            )

        for point in points:
            if not isinstance(point, tuple):
                x = int(landmarks[point].x * width)
                y = int(landmarks[point].y * height)
            else:
                x = int(landmarks[point[0]].x * width)
                y = int(landmarks[point[1]].y * height)

            cv2.circle(
                image,
                (x, y),
                Constants.RADIUS_SIZE,
                Constants.COLOR_POINT,
                -1
            )

        for angle in angles:
            if not isinstance(angle[0], tuple):
                x1 = landmarks[angle[0]].x * width
                x2 = landmarks[angle[1]].x * width
                x_center = landmarks[angle[2]].x * width
                y1 = landmarks[angle[0]].y * height
                y2 = landmarks[angle[1]].y * height
                y_center = landmarks[angle[2]].y * height
            else:
                x1 = landmarks[angle[0][0]].x * width
                x2 = landmarks[angle[1][0]].x * width
                x_center = landmarks[angle[2][0]].x * width
                y1 = landmarks[angle[0][1]].y * height
                y2 = landmarks[angle[1][1]].y * height
                y_center = landmarks[angle[2][1]].y * height

            angle_result = PoseValues.get_angle(
                (x1, y1),
                (x2, y2),
                (x_center, y_center),
            )

            rectangle = [
                [
                    int(x_center + 0.01 * width),
                    int(y_center - 0.05 * height)
                ],
                [
                    int(x_center + 0.15 * width),
                    int(y_center + 0.01 * height)
                ]
            ]

            image_transparent = image.copy()

            cv2.rectangle(
                image_transparent,
                rectangle[0],
                rectangle[1],
                Constants.COLOR_BACKGROUND,
                -1
            )

            cv2.addWeighted(
                image, Constants.ALPHA_BACKGROUND,
                image_transparent, 1 - Constants.ALPHA_BACKGROUND, 0, image
            )

            cv2.putText(
                image,
                '{:.2f}'.format(angle_result),
                (
                    int(x_center * 1.05),
                    int(y_center)
                ),
                cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,
                1,
                Constants.COLOR_FONT
            )

        return image
