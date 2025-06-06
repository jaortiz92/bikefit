import cv2
import mediapipe as mp
import numpy as np
import matplotlib.pyplot as plt
from typing import Literal
import os


from .constants import Constants
from .poseValues import PoseValues
from .utils import save_data
#from ultralytics import YOLO


class DrawPoseValues():
    #model = YOLO("yolo11m-seg")

    def __init__(
        self, name: str,
        format: str, is_image: bool = True,
        pose_type: Literal['front', 'back', 'left', 'right'] = Constants.RIGHT,
        folder: str = None,
        show: bool = False
    ):
        self.is_image: bool = is_image
        self.pose_type: bool = pose_type
        self.show: bool = show
        self.counter: int = 0
        if folder is None:
            self.name_input: str = '{}{}.{}'.format(Constants.IN, name, format)
            self.name_output: str = '{}result_{}.{}'.format(
            Constants.OUT, name, format)
        else:
            path_in: str = '{}{}/'.format(Constants.IN, folder)
            path_out: str = '{}{}/'.format(Constants.OUT, folder)
            self.name_input: str = '{}{}.{}'.format(path_in, name, format)
            self.name_output: str = '{}result_{}.{}'.format(
                path_out, name, format
            )
            if not os.path.exists(path_out):
                os.makedirs(path_out)

        print(self.name_input)

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

    def _preprocess_frame(self, frame):
        """Proprocess the image or frame to a better result"""
        # Upscale 2x
        high_res = cv2.resize(
            frame, (0, 0), fx=2, fy=2,
            interpolation=cv2.INTER_CUBIC
        )

        # CLAHE para contraste
        lab = cv2.cvtColor(high_res, cv2.COLOR_RGB2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        l = clahe.apply(l)
        enhanced = cv2.merge((l, a, b))
        return cv2.cvtColor(enhanced, cv2.COLOR_LAB2RGB)

    def generate(self):
        mp_drawing = mp.solutions.drawing_utils
        mp_pose = mp.solutions.pose

        with mp_pose.Pose(
            static_image_mode=self.is_image,
            model_complexity=2,       # Máxima complejidad del modelo
            smooth_landmarks=not self.is_image,    # Suavizado entre frames
            # Más estricto para evitar falsos positivos
            min_detection_confidence=0.8 if self.is_image else 0.7,
            min_tracking_confidence=0.7,    # Exigir seguimiento consistente
            enable_segmentation=True,        # Usar máscara para aislar al ciclista
            smooth_segmentation=True,        # Suavizar máscara entre frames
        ) as pose:
            if self.is_image:
                image = cv2.imread(self.name_input)
                height, width, _ = image.shape

                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                image_rgb = self._preprocess_frame(image_rgb)

                result_pose = pose.process(image_rgb)
                if result_pose.pose_landmarks:
                    image = self.add_values(
                        result_pose, image,
                        self.pose_type, width, height
                    )
                    cv2.imwrite(self.name_output, image)

            else:
                cap = cv2.VideoCapture(self.name_input)
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                fps = int(cap.get(cv2.CAP_PROP_FPS))
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

                # Create background subtractor
                bg_subtractor = cv2.createBackgroundSubtractorMOG2(
                    history=500,  # Frames used to create the background
                    varThreshold=10,  # Sensibility to the movements
                    detectShadows=True,  # Detect shadow
                )
                kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
                heatmap_refined = None

                out = cv2.VideoWriter(
                    self.name_output,
                    fourcc, fps, (width, height))

                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret:
                        break

                    #yolo_masks = self.get_yolo_person_mask(frame)
                    #roi_frame = cv2.bitwise_and(frame, frame, mask=yolo_masks)
                    roi_frame = frame
                    
                    image_rgb = cv2.cvtColor(roi_frame, cv2.COLOR_BGR2RGB)
                    image_rgb = self._preprocess_frame(image_rgb)
                    result_pose = pose.process(image_rgb)

                    if result_pose.pose_landmarks:
                        image = self.add_values(
                            result_pose, frame,
                            self.pose_type, width,
                            height
                        )
                    else:
                        image = frame

                    if self.key_moments['status']:
                        for _ in range(self.key_moments['frames_to_key_moments']):
                            out.write(image)
                    else:
                        out.write(image)

                    if self.show:
                        cv2.imshow('Cyclist Tracking', frame)
                        #cv2.imshow('Cyclist Trackingmask', roi_frame)
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break

                    self.counter += 1

                cap.release()
                out.release()
                cv2.destroyAllWindows()

    def get_yolo_person_mask(self, frame):
        results = self.model(frame, verbose=False)[0]
        combined_mask = np.zeros(frame.shape[:2], dtype=np.uint8)

        if results.masks is not None:
            for mask, cls in zip(results.masks.data, results.boxes.cls):
                if int(cls) == 0 or int(cls) == 1:  # Person class and cycling
                    mask_np = mask.cpu().numpy().astype(np.uint8) * 255
                    resized_mask = cv2.resize(
                        mask_np, (frame.shape[1], frame.shape[0]))
                    combined_mask = cv2.bitwise_or(combined_mask, resized_mask)

        return combined_mask

    def add_values(
            self, result_pose, image, pose_type: str,
            width: int, height: int
    ):
        landmarks = result_pose.pose_landmarks.landmark

        if pose_type == Constants.RIGHT:
            funct = PoseValues.get_right_body
        elif pose_type == Constants.LEFT:
            funct = PoseValues.get_left_body
        elif pose_type == Constants.FRONT:
            funct = PoseValues.get_front_body
        else:
            funct = PoseValues.get_back_body

        points, connections, angles, special_moments = funct()

        # Draw lines to connect points
        for index, connection in enumerate(connections):
            if not isinstance(connection[0], tuple):
                x1 = landmarks[connection[0]].x
                x2 = landmarks[connection[1]].x
                y1 = landmarks[connection[0]].y
                y2 = landmarks[connection[1]].y
            else:
                x1 = landmarks[connection[0][0]].x
                x2 = landmarks[connection[1][0]].x
                y1 = landmarks[connection[0][1]].y
                y2 = landmarks[connection[1][1]].y

            start_point = mp.solutions.drawing_utils._normalized_to_pixel_coordinates(
                x1, y1, width, height
            )
            end_point = mp.solutions.drawing_utils._normalized_to_pixel_coordinates(
                x2, y2, width, height
            )

            if start_point and end_point:
                if connection[2]:
                    cv2.line(
                        image,
                        start_point,
                        end_point,
                        Constants.COLOR_CONNECTION,
                        Constants.LINE_SIZE
                    )
                else:
                    cv2.line(
                        image,
                        start_point,
                        end_point,
                        Constants.COLOR_CONNECTION_SECONDARY,
                        Constants.LINE_SIZE_SECONDARY
                    )

        # Draw points
        for point in points:
            if isinstance(point, tuple):
                center = (
                    int(landmarks[point[0]].x * width),
                    int(landmarks[point[1]].y * height)
                )
            else:
                center = (
                    int(landmarks[point].x * width),
                    int(landmarks[point].y * height)
                )
            cv2.circle(
                image,
                center,
                Constants.RADIUS_SIZE,
                Constants.COLOR_POINT,
                -1
            )

        try:
            lowest_y = landmarks[special_moments['lowest_point'][1]].y * height
            highest_y = landmarks[special_moments['highest_point']
                                  [1]].y * height
            middle_x = landmarks[special_moments['middle_point'][0]].x * width
        except (IndexError, KeyError) as e:
            print(f"Landmark index error: {e}")
            return image

        self.validate_special_moment(lowest_y, highest_y, middle_x)

        #Draw Angles
        data_temp = []
        for name_angle, angle_def in angles.items():
            try:
                points = [
                    (
                        landmarks[angle_def[i][0]].x * width, 
                        landmarks[angle_def[i][1]].y * height
                    )
                    if isinstance(angle_def[i], tuple) else
                    (
                        landmarks[angle_def[i]].x * width,
                        landmarks[angle_def[i]].y * height
                    )
                    for i in range(3)
                ]

                angle = PoseValues.get_angle(*points)
                self.draw_angle_display(
                    image, points[2], angle, Constants.ALPHA_BACKGROUND, 
                    width, height, angle_def[3]
                )

                if self.key_moments['status']:
                    data_temp.append(self._create_angle_data(
                        name_angle, points, angle))

            except (IndexError, KeyError) as e:
                print(f"Angle calculation error: {e}")

        if data_temp:
            self._store_angle_data(data_temp)

        return image

    def draw_angle_display(self, frame, center_point, angle, alpha, width, height, secundaryAngle: False):
        overlay = frame.copy()

        x_center, y_center = center_point

        if not secundaryAngle: 
            text_pos = (
                int(x_center + width * Constants.ANGLE_X_FACTOR),
                int(y_center - height * Constants.ANGLE_Y_FACTOR),
            )
        else:
            text_pos = (
                int(x_center + width * Constants.ANGLE_X_FACTOR),
                int(y_center - height * Constants.SECONDARY_ANGLE_Y_FACTOR),
            )
        
        color_background = (
            Constants.COLOR_BACKGROUND_ESPECIAL
            if self.key_moments['status'] else
            Constants.COLOR_BACKGROUND
        )

        # Draw background
        cv2.rectangle(
            overlay,
            (text_pos[0] - 10, text_pos[1] - 25),
            (text_pos[0] + 100, text_pos[1] + 10),
            color_background,
            -1
        )

        # Draw text
        cv2.putText(
            overlay, f"{angle:.2f}", text_pos,
            cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 0.8,
            Constants.COLOR_FONT, 2
        )

        cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

    def _create_angle_data(self, name, points, angle):
        return [
            name,
            *points[0],
            *points[2],
            *points[1],  # Center point
            angle
        ]

    def _store_angle_data(self, data_temp):
        data_temp.append(self.counter)
        active_moment = self.key_moments['key_moment_active']
        self.data[active_moment].append(data_temp)

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
