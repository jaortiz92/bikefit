import cv2
import mediapipe as mp

from poseValues import PoseValues

COLOR_POINT = (250, 100, 250)
COLOR_CONNECTION = (250, 250, 250)
COLOR_FONT = (0, 0, 0)
COLOR_BACKGROUND = (250, 250, 250)
RADIUS_SIZE = 6
LINE_SIZE = 3


def add_values(result_pose, image, is_right, width, height):

    landmarks = result_pose.pose_landmarks.landmark

    if is_right:
        funct = PoseValues.get_right_body
    else:
        funct = PoseValues.get_left_body

    points, connections, angles = funct()

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

    for angle in angles:
        angle_result = PoseValues.get_angle(
            (landmarks[angle[0]].x, landmarks[angle[0]].y),
            (landmarks[angle[1]].x, landmarks[angle[1]].y),
            (landmarks[angle[2]].x, landmarks[angle[2]].y)
        )

        rectangle = [
            [
                int((landmarks[angle[2]].x + 0.01) * width),
                int((landmarks[angle[2]].y - 0.05) * height)
            ],
            [
                int((landmarks[angle[2]].x + 0.15) * width),
                int((landmarks[angle[2]].y + 0.01) * height)
            ]
        ]

        cv2.rectangle(
            image,
            rectangle[0],
            rectangle[1],
            COLOR_BACKGROUND,
            -1
        )

        cv2.putText(
            image,
            '{:.2f}'.format(angle_result),
            (
                int(landmarks[angle[2]].x * width * 1.05),
                int(landmarks[angle[2]].y * height)
            ),
            cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,
            1,
            COLOR_FONT
        )

    cv2.putText(image, str((landmarks[angles[2][0]].x,
                landmarks[angles[2][0]].y)), (0, 50), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1, COLOR_BACKGROUND)
    cv2.putText(image, str((landmarks[angles[2][1]].x,
                landmarks[angles[2][1]].y)), (0, 80), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1, COLOR_BACKGROUND)
    cv2.putText(image, str((landmarks[angles[2][2]].x,
                landmarks[angles[2][2]].y)), (0, 110), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1, COLOR_BACKGROUND)
    return image


def generate_report(path, name, format, is_image=True, is_right=True):
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    with mp_pose.Pose(static_image_mode=is_image) as pose:
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

                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image.flags.writeable = False

                result_pose = pose.process(image)

                if result_pose.pose_landmarks:
                    image.flags.writeable = True
                    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                    image = add_values(result_pose, image,
                                       is_right, width, height)
                out.write(image)


def run():
    # generate_report('./', 'image', 'jpeg', is_right=False)
    # generate_report('./', 'image2', 'jpeg', is_right=False)
    # generate_report('./', 'image3', 'jpeg', is_right=False)
    # generate_report('./', 'image4', 'jpeg', is_right=True)
    # generate_report('./', 'video', 'mp4', is_image=False, is_right=True)
    # generate_report('./', 'video2', 'mp4', is_image=False, is_right=False)
    # generate_report('./', 'video3', 'mp4', is_image=False, is_right=True)
    generate_report('./', 'video4', 'mp4', is_image=False, is_right=True)


if __name__ == '__main__':
    run()
