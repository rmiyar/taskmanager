from django.core.mail import send_mail

def enviar_recordatorio(usuario, tarea):
    asunto = f"Recordatorio: {tarea.title}"
    mensaje = f"""
Hola {usuario.username},

📝 Recordatorio de tarea próxima:

Título: {tarea.title}
Fecha: {tarea.date}
Hora: {tarea.time.strftime('%H:%M')}

TaskMaster
"""
    send_mail(
        asunto,
        mensaje,
        None,  # DEFAULT_FROM_EMAIL
        [usuario.email], 
        fail_silently=False
    )
