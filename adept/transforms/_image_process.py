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

def img_transfer(img, fro="bgr", to="rgb"):
    import numpy as np
    import cv2
    if fro == "bgr" and to == "rgb":
        return cv2.cvtColor(img, cv2.COLORBGR2RGB)
    if fro == "bgr" and to == "nrgb":
        return np.expand_dims(
            cv2.cvtColor(img, cv2.COLORBGR2RGB), axis=0
        )
