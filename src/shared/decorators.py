from time import time
import threading
from multiprocessing import Process


def count_elapsed_time(f):
    """
    Decorator.
    Execute the function and calculate the elapsed time.
    Print the result to the standard output.
    """

    def wrapper(*args, **kwargs):
        # Start counting.
        start_time = time()
        # Take the original function's return value.
        ret = f(*args, **kwargs)
        # Calculate the elapsed time.
        elapsed_time = time() - start_time
        print("Elapsed time: %0.10f seconds." % elapsed_time)
        return ret

    return wrapper


def execute_in_thread(name=None, daemon=None, ponerDelay=None):
    def _execute_in_thread(f):
        """
        Decorator.
        Execute the function in thread.
        """

        def wrapper(*args, **kwargs):
            thread_f = threading.Thread(target=f, args=args, kwargs=kwargs)

            if daemon is not None:
                thread_f.setDaemon(True)

            if name is not None:
                thread_f.setName(name)

            thread_f.start()

            if ponerDelay is not None:
                thread_f.join()

            return thread_f

        return wrapper

    return _execute_in_thread


def execute_in_thread_timer(seconds):
    def _execute_in_thread_timer(f):
        """
        Decorator.
        Execute the function in thread timer, with out parameters.
        """

        def wrapper(*args, **kwargs):
            thread_f = threading.Timer(seconds, f)

            thread_f.start()

            return thread_f

        return wrapper

    return _execute_in_thread_timer


def execute_in_process(f):
    """
    Decorator.
    Execute the function in thread.
    """

    def wrapper(*args, **kwargs):
        process_f = Process(target=f, args=args, kwargs=kwargs)
        process_f.start()

        return process_f

    return wrapper
