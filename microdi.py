""" Super tiny and minimal dependency injection package for Python.

Repository: https://github.com/atomicptr/microdi

License:

Copyright (C) 2021 Christopher Kaster


Everyone is permitted to copy and distribute verbatim or modified
copies of this license document, and changing it is allowed as long
as the name is changed.

           DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
  TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

 0. You just DO WHAT THE FUCK YOU WANT TO.
"""
from typing import Any, Callable, List

_implementations = {}


def get_instance(name: str, *args: Any, **kwargs: Any) -> Any:
    """ Return an implementation registered under the given name """
    if name not in _implementations:
        raise Exception(f"Unknown implementation: {name}")
    constructor, is_singleton = _implementations[name]["constructor"], _implementations[name]["is_singleton"]
    if not is_singleton:
        return constructor(*args, **kwargs)
    if "instance" not in _implementations[name]:
        _implementations[name]["instance"] = constructor(*args, **kwargs)
    return _implementations[name]["instance"]


def register(name: str, is_singleton=False) -> Callable:
    """ Register an implementation under the given name.

    Keyword arguments:
    name -- the name of implementation
    is_singleton -- is this a singleton? If True the object will only be created once and then reused (default False)
    """

    def register_wrapper(constructor: Callable) -> Callable:
        _implementations[name] = {
            "constructor": constructor,
            "is_singleton": is_singleton,
        }

        def constructor_wrapper(*args: Any, **kwargs: Any) -> None:
            return constructor(*args, **kwargs)

        return constructor_wrapper

    return register_wrapper


def inject(**inject_kwargs: Any) -> Callable:
    """ Inject an implementation.

    Examples:
    @inject(client="my.Client") -- will inject the implementation registered as "my.Client" into the client attribute
    @inject(client=["my.Client", "apikey"]) -- the first parameter does the same as above, all other parameters are
                                               given to the constructor of the "my.Client" implementation. This will
                                               not work with singletons.
    """

    def inject_wrapper(inject_target_func: Callable) -> Callable:
        def target_func_wrapper(*args: Any, **kwargs: Any) -> None:
            for key, name in inject_kwargs.items():
                constructor_args = []
                if isinstance(name, List):
                    constructor_args = name[1:]
                    name = name[0]
                # local arguments overwrite the thing we want to inject, ignore
                if key in kwargs:
                    continue
                kwargs[key] = get_instance(name, *constructor_args)
            return inject_target_func(*args, **kwargs)

        return target_func_wrapper

    return inject_wrapper
