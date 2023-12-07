from celery import shared_task

@shared_task
def p_task():
    text = f"Celery-Beats-Works"
    with open('text.txt','w') as file:
        file.write(text)
    file.close()


