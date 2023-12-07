from celery import shared_task

@shared_task
def text_task():
    text = 'Celery work!!!!'
    with open('text.txt','w') as file:
        file.write(text)

