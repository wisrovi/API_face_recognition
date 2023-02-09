from tasks import tasks_demo
from tasks import tasks_facecode

tasks_facecode.ok_facecode()
tasks_demo.ok_say_hello()

# crear tarea para convertir un buffer en vector

# crear tarea para comparar un vector con una lista de vectores


# python -m celery multi start 10 -A tasks worker -l info -Q:1-3 --pool=solo
