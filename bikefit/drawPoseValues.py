import cv2
import mediapipe as mp
import numpy as np


from .constants import Constants
from .poseValues import PoseValues
from .utils import save_data

class DrawPoseValues():

    def __init__(
        self, name: str,
        format: str, is_image: bool = True,
        is_right: bool = True
    ):
        self.is_image: bool = is_image
        self.is_right: bool = is_right
        self.counter: int = 0
        self.name_input: str = '{}/{}.{}'.format(Constants.IN, name, format)
        self.name_output: str = '{}/result_{}.{}'.format(Constants.OUT, name, format)
        self.key_moments: dict = {
            'lowest_point': None,
            'highest_point': None,
            'middle_point_one': None,
            'middle_point_two': None,
            'frames_to_key_moments': Constants.FRAMES_TO_KEY_MOMENTS,
            'status': False,
            'key_moment_active': None,
            'minimum_time': Constants.MINIMUN_TIME
        }
        self.data: dict[str, list] = {
            'lowest_point': [],
            'highest_point': [],
            'middle_point_one': [],
            'middle_point_two': [],
        }
        self.generate()
        if not is_image:
            save_data(self.data)

    def generate(self):
        mp_drawing = mp.solutions.drawing_utils
        mp_pose = mp.solutions.pose

        with mp_pose.Pose(
            static_image_mode=self.is_image, # True, 
            model_complexity=2,
            min_detection_confidence=0.9,
            min_tracking_confidence=0.9,
            enable_segmentation=True
        ) as pose:
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
                        image = self.add_values(
                            result_pose, frame,
                            self.is_right, width,
                            height
                        )
                    else:
                        image = frame

                    if self.key_moments['status']:
                        for _ in range(self.key_moments['frames_to_key_moments']):
                            out.write(image)
                    else:
                        out.write(image)
                    self.counter += 1

                cap.release()
                out.release()

    def add_values(
            self, result_pose, image, is_right: bool,
            width: int, height: int
    ):
        landmarks = result_pose.pose_landmarks.landmark

        if is_right:
            funct = PoseValues.get_right_body
        else:
            funct = PoseValues.get_left_body

        points, connections, angles, special_moments = funct()

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

        lowest_point = landmarks[special_moments['lowest_point'][1]].y * height
        highest_point = landmarks[
            special_moments['highest_point'][1]
        ].y * height
        middle_point = landmarks[special_moments['middle_point'][0]].x * width

        self.validate_special_moment(
            lowest_point, highest_point, middle_point
        )

        data_temp = []
        for name_angle, angle in angles.items():
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

            color_background = (
                Constants.COLOR_BACKGROUND_ESPECIAL
                if self.key_moments['status'] else
                Constants.COLOR_BACKGROUND
            )

            cv2.rectangle(
                image_transparent,
                rectangle[0],
                rectangle[1],
                color_background,
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

            if self.key_moments['status']:
                data_temp.append(
                    [
                        name_angle, x1, y1, x2, y2,
                        x_center, y_center, angle_result
                    ]
                )
        if len(data_temp)>0:
            data_temp.append(self.counter)
            self.data[self.key_moments['key_moment_active']].append(
                data_temp
            )
        return image


    def validate_special_moment(self, lowest_point, highest_point, middle_point):
        status: bool = False
        if self.counter > self.key_moments['minimum_time']:
            if self.key_moments['lowest_point'] is None:
                self.key_moments['lowest_point'] = lowest_point
                self.key_moments['highest_point'] = highest_point
                self.key_moments['middle_point_one'] = middle_point
                self.key_moments['middle_point_two'] = middle_point
            else:
                if self.key_moments['lowest_point'] < lowest_point:
                    self.key_moments['lowest_point'] = lowest_point
                if self.key_moments['highest_point'] > highest_point:
                    self.key_moments['highest_point'] = highest_point
                if self.key_moments['middle_point_one'] > middle_point:
                    self.key_moments['middle_point_one'] = middle_point
                if self.key_moments['middle_point_two'] < middle_point:
                    self.key_moments['middle_point_two'] = middle_point

            if self.counter > self.key_moments['minimum_time'] + 60:
                alpha = 0.01
                if self.key_moments['lowest_point'] < lowest_point * (1 + alpha):
                    status = True
                    self.key_moments['key_moment_active'] = 'lowest_point'
                elif self.key_moments['highest_point'] > highest_point * (1 - alpha):
                    status = True
                    self.key_moments['key_moment_active'] = 'highest_point'
                elif self.key_moments['middle_point_one'] > middle_point * (1 - alpha):
                    status = True
                    self.key_moments['key_moment_active'] = 'middle_point_one'
                elif self.key_moments['middle_point_two'] < middle_point * (1 + alpha):
                    status = True
                    self.key_moments['key_moment_active'] = 'middle_point_two'
        self.key_moments['status'] = status