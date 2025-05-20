from bikefit import DrawPoseValues


def run():
    DrawPoseValues('image2', 'jpeg', is_right=False)
    DrawPoseValues('image3', 'jpeg', is_right=False)
    DrawPoseValues('image4', 'jpeg', is_right=True)
    DrawPoseValues('image6', 'jpeg', is_right=True)
    DrawPoseValues('image', 'jpeg', is_right=False)
    # DrawPoseValues('video', 'mp4', is_image=False, is_right=True)
    # DrawPoseValues('video2', 'mp4', is_image=False, is_right=False)
    # DrawPoseValues('video3', 'mp4', is_image=False, is_right=True)
    # DrawPoseValues('video4', 'mp4', is_image=False, is_right=True)
    # DrawPoseValues('mtb_left', 'mp4', is_image=False, is_right=False)
    # DrawPoseValues('mtb_left_slow', 'mp4', is_image=False, is_right=False)
    #DrawPoseValues('VideoMTBLeft', 'mp4', is_image=False, is_right=False)
    DrawPoseValues('road_green_left_e', 'mp4', is_image=False, is_right=False)
    #DrawPoseValues('road_green_right_e', 'mp4', is_image=False, is_right=True)


if __name__ == '__main__':
    run()
