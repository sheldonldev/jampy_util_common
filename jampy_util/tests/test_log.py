import json

def json_to_bytes(json_: dict):
    return bytes(json.dumps(json_, indent=4, ensure_ascii=False), encoding="utf-8")


def str_to_bytes(text: str):
    return bytes(text, encoding="utf-8")


@staticmethod
def imdecode(image: Union[str, Path, bytes, np.ndarray], mode=cv2.IMREAD_UNCHANGED) -> np.ndarray:
    if isinstance(image, np.ndarray):
        return image
    elif isinstance(image, bytes):
        return cv2.imdecode(np.frombuffer(image, dtype=np.uint8), mode)
    elif isinstance(image, Path):
        return __class__.imdecode(image.read_bytes())
    elif isinstance(image, str):
        return __class__.imdecode(Path(image))
    else:
        raise NotImplementedError


@staticmethod
def imencode(image: np.ndarray, format="jpg"):
    _, data = cv2.imencode(f".{format}", image)
    return data.tobytes()
