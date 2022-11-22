# ==================================================================================================
# -- imports ---------------------------------------------------------------------------------------
# ==================================================================================================


# ==================================================================================================
# -- functions -------------------------------------------------------------------------------------
# ==================================================================================================

def add_video_writer(width, height, fps, save_path,
                     file_name=None):
    import cv2, os
    ## step1: init path
    if file_name is None:  # default use current time as video's file name
        import time
        file_name = time.strftime('%Y%m%d-%H-%M-%S.mp4', time.localtime())
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    if os.path.isdir(save_path):
        save_path = os.path.join(save_path, file_name)
    ## step2: init video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(save_path, fourcc, fps, (width, height))

    return writer, save_path


def save_video_frame(writer, frame):
    if writer is not None:
        writer.write(frame)

