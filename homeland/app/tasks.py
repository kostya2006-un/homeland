from celery import shared_task
from .models import Order,Status
from django.utils import timezone
@shared_task
def order_status_update_task():
    status_finished = Status.objects.get(status='завершенный')
    status_in_procces = Status.objects.get(status='начатый')
    today = timezone.now().date()

    for order in Order.objects.all():
        if order.leave_date < today:
            order.status = status_finished
        elif order.arrive_date <= today < order.leave_date:
            order.status = status_in_procces
        order.save()





