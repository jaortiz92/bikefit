from typing import Tuple

class Constants:
    IN: str = './in/'
    OUT: str = './out/'

    COLOR_POINT: Tuple[int] = (0, 255, 0)
    COLOR_CONNECTION: Tuple[int] = (250, 250, 250)
    COLOR_CONNECTION_SECONDARY: Tuple[int] = (200, 200, 200)
    COLOR_FONT: Tuple[int] = (0, 0, 0)
    COLOR_BACKGROUND: Tuple[int] = (250, 250, 250)
    COLOR_BACKGROUND_ESPECIAL: Tuple[int] = (229, 255, 204)
    RADIUS_SIZE: int = 6
    LINE_SIZE: int = 3
    LINE_SIZE_SECONDARY: int = 1
    ALPHA_BACKGROUND: int = 0.6


    FRAMES_TO_KEY_MOMENTS: int = 1
    MINIMUN_TIME: int = 30 * 6

    #ANGLE_LOCATION
    ANGLE_X_FACTOR: float = 0.03
    ANGLE_Y_FACTOR: float = 0
    SECONDARY_ANGLE_Y_FACTOR: float = 0.04


    #Pose types
    FRONT: str = 'front'
    BACK: str = 'back'
    LEFT: str = 'left'
    RIGHT: str = 'right'