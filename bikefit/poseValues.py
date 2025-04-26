import numpy as np


class PoseValues():
    NOSE = 0
    LEFT_EYE_INNER = 1
    LEFT_EYE = 2
    LEFT_EYE_OUTER = 3
    RIGHT_EYE_INNER = 4
    RIGHT_EYE = 5
    RIGHT_EYE_OUTER = 6
    LEFT_EAR = 7
    RIGHT_EAR = 8
    MOUTH_LEFT = 9
    MOUTH_RIGHT = 10
    LEFT_SHOULDER = 11
    RIGHT_SHOULDER = 12
    LEFT_ELBOW = 13
    RIGHT_ELBOW = 14
    LEFT_WRIST = 15
    RIGHT_WRIST = 16
    LEFT_PINKY = 17
    RIGHT_PINKY = 18
    LEFT_INDEX = 19
    RIGHT_INDEX = 20
    LEFT_THUMB = 21
    RIGHT_THUMB = 22
    LEFT_HIP = 23
    RIGHT_HIP = 24
    LEFT_KNEE = 25
    RIGHT_KNEE = 26
    LEFT_ANKLE = 27
    RIGHT_ANKLE = 28
    LEFT_HEEL = 29
    RIGHT_HEEL = 30
    LEFT_FOOT_INDEX = 31
    RIGHT_FOOT_INDEX = 32

    @classmethod
    def get_left_body(cls) -> list:
        special_point_one = (cls.LEFT_HEEL, cls.LEFT_FOOT_INDEX)
        foot_index = (cls.LEFT_FOOT_INDEX, cls.LEFT_FOOT_INDEX)
        heel = (cls.LEFT_HEEL, cls.LEFT_HEEL)
        keys_to_special_moments = {
            'lowest_point': special_point_one,
            'highest_point': special_point_one,
            'middle_point': special_point_one
        }

        return [
            [
                cls.LEFT_ANKLE,
                cls.LEFT_KNEE,
                cls.LEFT_HIP,
                cls.LEFT_SHOULDER,
                cls.LEFT_ELBOW,
                cls.LEFT_WRIST,
                cls.LEFT_HEEL,
                cls.LEFT_FOOT_INDEX,
                special_point_one
            ],
            [
                (cls.LEFT_ANKLE, cls.LEFT_KNEE),
                (cls.LEFT_KNEE, cls.LEFT_HIP),
                (cls.LEFT_HIP, cls.LEFT_SHOULDER),
                (cls.LEFT_SHOULDER,
                 cls.LEFT_ELBOW),
                (cls.LEFT_ELBOW, cls.LEFT_WRIST),
                (cls.LEFT_ANKLE, cls.LEFT_HEEL),
                (cls.LEFT_HEEL, cls.LEFT_FOOT_INDEX),
                (
                    special_point_one,
                    foot_index
                )
            ],
            {
                'lower_part':[
                    cls.LEFT_ANKLE, cls.LEFT_HIP, cls.LEFT_KNEE
                ],
                'mid_part':[
                    cls.LEFT_KNEE, cls.LEFT_SHOULDER, cls.LEFT_HIP
                ],
                'hight_part':[
                    cls.LEFT_HIP, cls.LEFT_WRIST, cls.LEFT_SHOULDER
                ],
                'foot':[
                    special_point_one, heel, foot_index
                ]
            },
            keys_to_special_moments
        ]

    @classmethod
    def get_right_body(cls) -> list:
        special_point_one = (cls.RIGHT_HEEL, cls.RIGHT_FOOT_INDEX)
        foot_index = (cls.RIGHT_FOOT_INDEX, cls.RIGHT_FOOT_INDEX)
        heel = (cls.RIGHT_HEEL, cls.RIGHT_HEEL)

        keys_to_special_moments = {
            'lowest_point': special_point_one,
            'highest_point': special_point_one,
            'middle_point': special_point_one
        }

        return [
            [
                cls.RIGHT_ANKLE,
                cls.RIGHT_KNEE,
                cls.RIGHT_HIP,
                cls.RIGHT_SHOULDER,
                cls.RIGHT_ELBOW,
                cls.RIGHT_WRIST,
                cls.RIGHT_HEEL,
                cls.RIGHT_FOOT_INDEX,
                special_point_one
            ],
            [
                (cls.RIGHT_ANKLE, cls.RIGHT_KNEE),
                (cls.RIGHT_KNEE, cls.RIGHT_HIP),
                (cls.RIGHT_HIP, cls.RIGHT_SHOULDER),
                (cls.RIGHT_SHOULDER,
                 cls.RIGHT_ELBOW),
                (cls.RIGHT_ELBOW, cls.RIGHT_WRIST),
                (cls.RIGHT_ANKLE, cls.RIGHT_HEEL),
                (cls.RIGHT_HEEL, cls.RIGHT_FOOT_INDEX),
                (
                    special_point_one,
                    foot_index
                )
            ],
            {
                'lower_part':[
                    cls.LEFT_ANKLE, cls.LEFT_HIP, cls.LEFT_KNEE
                ],
                'mid_part':[
                    cls.LEFT_KNEE, cls.LEFT_SHOULDER, cls.LEFT_HIP
                ],
                'hight_part':[
                    cls.LEFT_HIP, cls.LEFT_WRIST, cls.LEFT_SHOULDER
                ],
                'foot':[
                    special_point_one, heel, foot_index
                ]
            },
            keys_to_special_moments
        ]

    @classmethod
    def get_angle(cls, a, b, center):
        a = np.array(a)
        b = np.array(b)
        center = np.array(center)
        a_center = a - center
        b_center = b - center

        cos_angle = np.dot(a_center, b_center) / \
            (np.linalg.norm(a_center) * np.linalg.norm(b_center))
        cos_angle = np.clip(cos_angle, -1, 1)

        return np.degrees(np.arccos(cos_angle))
