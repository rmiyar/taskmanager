from django.core.mail import send_mail

def enviar_recordatorio(nombre_usuario, task):
    asunto = "Recordatorio de tarea"
    mensaje = (
        f"Hola {nombre_usuario},\n\n"
        f"Tu tarea '{task.title}' está por vencer a las {task.time.strftime('%I:%M %p')}.\n\n"
        "TaskMaster"
    )

    send_mail(
        asunto,
        mensaje,
        'taskmaster@noreply.com',  # remitente
        [task.user.email],        # destinatario real
        fail_silently=False,
    )
