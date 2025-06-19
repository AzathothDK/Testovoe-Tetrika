import inspect

def strict(func):
    def wrapper(*args, **kwargs):
        sig = inspect.signature(func)
        bound_args = sig.bind(*args, **kwargs)
        annotations = func.__annotations__

        for name, value in bound_args.arguments.items():
            if name in annotations:
                expected_type = annotations[name]
                if not isinstance(value, expected_type):
                    raise TypeError(f"Argument '{name}' must be {expected_type.__name__}, got {type(value).__name__}")
        return func(*args, **kwargs)

    return wrapper
