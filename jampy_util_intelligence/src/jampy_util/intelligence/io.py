from pathlib import Path
from typing import Union

import cv2
import numpy as np


def imdecode(image: Union[str, Path, bytes, np.ndarray], mode=cv2.IMREAD_UNCHANGED) -> np.ndarray:
    if isinstance(image, np.ndarray):
        return image
    elif isinstance(image, bytes):
        return cv2.imdecode(np.frombuffer(image, dtype=np.uint8), mode)
    elif isinstance(image, Path):
        return imdecode(image.read_bytes())
    elif isinstance(image, str):
        return imdecode(Path(image))
    else:
        raise NotImplementedError


def imencode(image: np.ndarray, format="jpg"):
    _, data = cv2.imencode(f".{format}", image)
    return data.tobytes()
