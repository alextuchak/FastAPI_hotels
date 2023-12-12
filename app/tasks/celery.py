from celery import Celery
from app.settings import settings
from kombu import Queue, Exchange

celery = Celery(
    'tasks',
    broker=f"amqp://{settings.RABBITMQ_DEFAULT_USER}:{settings.RABBITMQ_DEFAULT_PASS}@rabbitmq:5672",
    include=['app.tasks.tasks'],
)
celery.conf.task_default_queue = 'default'
celery.conf.task_queues = (
    Queue('default', routing_key='default'),
    Queue('image_tasks', exchange=Exchange('mediatasks', type='direct'),
          routing_key='image.compress')
)
celery.conf.task_routes = {
    'app.tasks.tasks.fit_image': {
        'queue': 'image_tasks',
        'routing_key': 'image.compress'
    }
}