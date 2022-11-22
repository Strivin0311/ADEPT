"""
the view package contains all functions about visualization
including integrated-gui, simple-image-show, simple-video-show, etc
"""

# ==================================================================================================
# -- imports ---------------------------------------------------------------------------------------
# ==================================================================================================
from ._video import add_video_writer, save_video_frame
from ._image import ColorSpace, show_image, add_image_queue, get_image_from_queue, put_image_to_queue

# ==================================================================================================
# -- all -------------------------------------------------------------------------------------------
# ==================================================================================================

__all__ = [  # user interface and other dependent packages
    "add_video_writer", "save_video_frame",
    "ColorSpace",
    "show_image", "add_image_queue", "get_image_from_queue", "put_image_to_queue",
]