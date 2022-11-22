# ==================================================================================================
# -- imports ---------------------------------------------------------------------------------------
# ==================================================================================================

from enum import Enum, unique


# ==================================================================================================
# -- classes ---------------------------------------------------------------------------------------
# ==================================================================================================

@unique
class ColorSpace(Enum):
    """
    This is the color space for image
    """

    RGB = "rgb"
    BGR = "bgr"
    BGRA = "bgra"
    GRAY = "gray"
    HSV = "hsv"
    YUV = "yuv"


# ==================================================================================================
# -- functions -------------------------------------------------------------------------------------
# ==================================================================================================

def show_image(image, window_name=None, width=None, height=None, delta_time=1):
    import cv2

    if window_name is None:  # default use current time as image's window name
        import time
        window_name = time.strftime('%Y%m%d-%H-%M-%S.mp4', time.localtime())

    cv2.imshow(window_name, cv2.resize(
        image,
        (
            image.shape[0] if width is None else width,
            image.shape[1] if height is None else height
        )
    ))

    cv2.waitKey(int(delta_time))


def add_image_queue(size=1):
    import queue
    return queue.Queue(1)


def get_image_from_queue(q):
    if not q.empty():
        return q.get()


def put_image_to_queue(q, img):
    q.clear()
    q.put_nowait(img)
