from time import sleep

from tasks import app


@app.task
def say_hello(name: str = "World"):
    sleep(5)
    return f"Hello {name}"


def ok_say_hello():
    print("ok_say_hello")
