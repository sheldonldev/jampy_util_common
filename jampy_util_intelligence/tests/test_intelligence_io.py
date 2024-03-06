from pathlib import Path

import numpy as np
from pytest import fixture

from jampy_util.intelligence.io import imdecode
from jampy_util.path import normalize_path


@fixture
def image_path_str():
    yield str(
        normalize_path(Path(__file__).parent.joinpath('data/test_image.png'))[1]
    )


@fixture
def image_bytes():
    yield Path(__file__).parent.joinpath('data/test_image.png').read_bytes()


def test_intelligence_io(image_path_str, image_bytes):
    image = imdecode(image_path_str)
    assert isinstance(image, np.ndarray)

    image = imdecode(image_bytes)
    assert isinstance(image, np.ndarray)
