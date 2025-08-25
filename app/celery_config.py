# from celery import Celery
# import multiprocessing

# celery = Celery(
#     'myapp',
#     broker='redis://localhost:6379/0',  # Use your own broker URL
#     backend='redis://localhost:6379/0'  # Use your own backend URL
# )
import multiprocessing
# Chuyển phương thức start của multiprocessing sang spawn
multiprocessing.set_start_method('spawn', force=True)

from celery import Celery

celery = Celery(
    'myapp',
    broker='redis://redis:6379/0',  # Use your own broker URL
    backend='redis://redis:6379/0'  # Use your own backend URL
)


from tasks import *

