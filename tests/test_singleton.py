from jampy_utils.singleton import SingletonMixin


def test_singleton():
    class A(SingletonMixin):
        pass

    class B(SingletonMixin):
        pass

    a = A.instance()
    a2 = A.instance()
    assert a is a2

    b = B.instance()
    b2 = B.instance()
    assert b is b2

    assert a is not b2
