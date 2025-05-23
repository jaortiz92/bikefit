from typing import List
from bikefit import DrawPoseValues, Constants
import os


def run():
    read_folder('spinning')
    read_folder('general_left', is_right=False)
    read_folder('general_right', is_right=False)
    #DrawPoseValues('spinning_right_slow', 'mp4', is_image=False, is_right=True)
    #DrawPoseValues('spinning_right_gopro', 'mp4', is_image=False, is_right=True)
    #DrawPoseValues('VideoMTBLeft', 'mp4', is_image=False, is_right=False)
    #DrawPoseValues('VideoMTBLeft', 'mp4', is_image=False, is_right=False)
    #DrawPoseValues('road_green_right_e', 'mp4', is_image=False, is_right=True)

def read_folder(name_folder: str, is_right: bool=True) -> List[str]:
    files: List[str] = os.listdir(Constants.IN + name_folder)
    formats: List[str] = ['jpeg', 'jpg', 'png']
    for file in files:
        if file.split('.')[-1] in formats:
            DrawPoseValues(
                file.split('.')[0], 
                file.split('.')[-1],
                is_image=True,
                is_right=is_right,
                folder=name_folder
            )



if __name__ == '__main__':
    run()
