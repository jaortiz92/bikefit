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
        '''
        return:
         List[points, connections, angles, special_moments]
        '''
        special_point_one = (cls.LEFT_HEEL, cls.LEFT_FOOT_INDEX)
        special_point_two = (cls.LEFT_SHOULDER, cls.LEFT_HIP)
        foot_index = (cls.LEFT_FOOT_INDEX, cls.LEFT_FOOT_INDEX)
        hip = (cls.LEFT_HIP, cls.LEFT_HIP)
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
                (special_point_one,foot_index),
                (special_point_two, hip)
            ],
            {
                'lower_part':[
                    cls.LEFT_ANKLE, cls.LEFT_HIP, cls.LEFT_KNEE, False
                ],
                'mid_part':[
                    cls.LEFT_KNEE, cls.LEFT_SHOULDER, cls.LEFT_HIP, False
                ],
                'back':[
                    special_point_two, cls.LEFT_SHOULDER, cls.LEFT_HIP, True
                ],
                'hight_part':[
                    cls.LEFT_HIP, cls.LEFT_WRIST, cls.LEFT_SHOULDER, False
                ],
                'arm':[
                    cls.LEFT_SHOULDER, cls.LEFT_WRIST, cls.LEFT_ELBOW, False
                ],
                'foot':[
                    cls.LEFT_KNEE,  cls.LEFT_FOOT_INDEX, cls.LEFT_ANKLE, False
                ]
            },
            keys_to_special_moments
        ]

    @classmethod
    def get_right_body(cls) -> list:
        '''
        return:
         List[
            points, 
            connections, 
            angles[point_one, point_two, center, is_secundary], 
            special_moments
        ]
        '''
        special_point_one = (cls.RIGHT_HEEL, cls.RIGHT_FOOT_INDEX)
        special_point_two = (cls.RIGHT_SHOULDER, cls.RIGHT_HIP)
        foot_index = (cls.RIGHT_FOOT_INDEX, cls.RIGHT_FOOT_INDEX)
        hip = (cls.RIGHT_HIP, cls.RIGHT_HIP)

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
                (special_point_one,foot_index),
                (special_point_two, hip)
            ],
            {
                'lower_part':[
                    cls.RIGHT_ANKLE, cls.RIGHT_HIP, cls.RIGHT_KNEE, False
                ],
                'mid_part':[
                    cls.RIGHT_KNEE, cls.RIGHT_SHOULDER, cls.RIGHT_HIP, False
                ],
                'back':[
                    special_point_two, cls.RIGHT_SHOULDER, cls.RIGHT_HIP, True
                ],
                'hight_part':[
                    cls.RIGHT_HIP, cls.RIGHT_WRIST, cls.RIGHT_SHOULDER, False
                ],
                'arm':[
                    cls.RIGHT_SHOULDER, cls.RIGHT_WRIST, cls.RIGHT_ELBOW, False
                ],
                'foot':[
                    cls.RIGHT_KNEE,  cls.RIGHT_FOOT_INDEX, cls.RIGHT_ANKLE, False
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
