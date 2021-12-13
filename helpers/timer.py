from time import perf_counter


def print_message_and_timer(message: str):
    """
    Print a message, and then after running the inner function
    print out the runtime
    """

    def decorator(function):
        def wrapper(*args, **kwargs):
            print("\t ->", message)
            start_time = perf_counter()

            result = function(*args, **kwargs)

            end_time = perf_counter()

            runtime = end_time - start_time
            print(f"\t ....... finished in {round(runtime, 2)}")
            return result

        return wrapper

    return decorator
