import cv2
import mediapipe as mp

from poseValues import PoseValues

COLOR_POINT = (250, 100, 250)
COLOR_CONNECTION = (250, 250, 250)
COLOR_FONT = (0, 0, 0)
COLOR_BACKGROUND = (250, 250, 250)
RADIUS_SIZE = 6
LINE_SIZE = 3
ALPHA_BACKGROUND = 0.5


def add_values(result_pose, image, is_right, width, height):

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
            COLOR_CONNECTION,
            LINE_SIZE
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
                RADIUS_SIZE,
                COLOR_POINT,
                1
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
            COLOR_BACKGROUND,
            -1
        )

        cv2.addWeighted(
            image, ALPHA_BACKGROUND,
            image_transparent, 1 - ALPHA_BACKGROUND, 0, image
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
            COLOR_FONT
        )

    return image


def generate_report(path, name, format, is_image=True, is_right=True):
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    with mp_pose.Pose(static_image_mode=True) as pose:
        format = '.' + format
        if is_image:
            image = cv2.imread(path + name + format)
            height, width, _ = image.shape

            image_rgb = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            result_pose = pose.process(image_rgb)
            if result_pose.pose_landmarks:
                image = add_values(result_pose, image, is_right, width, height)
                cv2.imwrite('result_' + name + format, image)

        else:
            cap = cv2.VideoCapture(path + name + format)
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            fps = 30
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

            out = cv2.VideoWriter(
                'result_' + name + format,
                fourcc, fps, (width, height))

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                result_pose = pose.process(image_rgb)

                if result_pose.pose_landmarks:
                    image = frame
                    image = add_values(result_pose, image,
                                       is_right, width, height)
                out.write(image)


def run():
    generate_report('./', 'image', 'jpeg', is_right=False)
    generate_report('./', 'image2', 'jpeg', is_right=False)
    generate_report('./', 'image3', 'jpeg', is_right=False)
    generate_report('./', 'image4', 'jpeg', is_right=True)
    generate_report('./', 'image6', 'jpeg', is_right=True)
    generate_report('./', 'video', 'mp4', is_image=False, is_right=True)
    generate_report('./', 'video2', 'mp4', is_image=False, is_right=False)
    generate_report('./', 'video3', 'mp4', is_image=False, is_right=True)
    generate_report('./', 'video4', 'mp4', is_image=False, is_right=True)


if __name__ == '__main__':
    run()
