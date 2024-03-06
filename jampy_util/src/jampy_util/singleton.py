import threading
from typing import Any, Optional


# See https://gist.github.com/werediver/4396488
class SingletonMixin:
    """Mixin class to make your class a Singleton class."""

    _instance: Optional[Any] = None
    _rlock = threading.RLock()
    _inside_instance = False

    @classmethod
    def instance(cls, *args: Any, **kwargs: Any):
        """Get *the* instance of the class, constructed when needed using (kw)args.

        Return the instance of the class. If it did not yet exist, create it
        by calling the "constructor" with whatever arguments and keyword arguments
        provided.

        This routine is thread-safe. It uses the *double-checked locking* design
        pattern ``https://en.wikipedia.org/wiki/Double-checked_locking``_ for this.

        :param args: Used for constructing the instance, when not performed yet.
        :param kwargs: Used for constructing the instance, when not perfored yet.
        :return: An instance of the class
        """
        if cls._instance is not None:
            return cls._instance
        with cls._rlock:
            # re-check, perhaps it was created in the mean time...
            if cls._instance is None:
                cls._inside_instance = True
                try:
                    cls._instance = cls(*args, **kwargs)
                finally:
                    cls._inside_instance = False
        return cls._instance

    def __new__(cls, *args, **kwargs):
        """Raise Exception when not called from the :func:``instance``_ class method.

        This method raises RuntimeError when not called from the instance class method.

        :param args: Arguments eventually passed to :func:``__init__``_.
        :param kwargs: Keyword arguments eventually passed to :func:``__init__``_
        :return: the created instance.
        """
        if cls is SingletonMixin:
            raise TypeError(
                f"Attempt to instantiate mixin class {cls.__qualname__}"
            )

        if cls._instance is None:
            with cls._rlock:
                if cls._instance is None and cls._inside_instance:
                    return super().__new__(cls, *args, **kwargs)

        raise RuntimeError(
            f"Attempt to create a {cls.__qualname__} instance outside of instance()"
        )
