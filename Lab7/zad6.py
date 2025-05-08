import logging
import sys
import time

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
handler.setFormatter(formatter)
logger.addHandler(handler)

def log(level):
    def decorator(obj):
        if isinstance(obj, type):
            return log_class(obj, level)
        else:
            return log_function(obj, level)
    return decorator

def log_function(func, level):
    def wrapper(*args, **kwargs):
        logger.log(level, f"Calling function: {func.__name__}")
        start_time = time.time()
        logger.log(level, f"Args: {args}; Kwargs: {kwargs}")

        try:
            result = func(*args, **kwargs)
            end_time = time.time()
            time_taken = end_time - start_time
            logger.log(level, f"Execution time: {time_taken:.2f} seconds")
            logger.log(level, f"Function {func.__name__} returned: {result}")

            return result
        except Exception as e:
            logger.error(f"Function {func.__name__} raised an exception: {e}")
            raise

    return wrapper


def log_class(cls, level):
    def wrapper(*args, **kwargs):
        logger.log(level, f"Instantiating class {cls.__name__}")
        logger.log(level, f"Args: {args}; Kwargs: {kwargs}")

    return wrapper

@log(logging.INFO)
def test_func(a, b):
    return a + b

@log(logging.INFO)
class TestClass:
    def __init__(self, a, b):
        self.a = a
        self.b = b


if __name__ == "__main__":
    test_func(1, 2)
    print()
    test_instance = TestClass(1, 2)