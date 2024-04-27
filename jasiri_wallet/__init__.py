from environ import Env
from .celery import app as celery_app


Env.read_env()
env = Env()

__all__ = ("celery_app", "env")