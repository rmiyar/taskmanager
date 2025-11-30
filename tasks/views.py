from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
import calendar
from datetime import date, datetime, timedelta
from .models import Task, ReminderSettings
from .forms import TaskForm
from .email_utils import enviar_recordatorio   # 👈 INTEGRADO AQUÍ


@login_required
def dashboard(request):
    today = date.today()

    # tareas del día
    tasks_today = Task.objects.filter(
        user=request.user,
        date=today
    ).order_by('time')

    # tareas futuras
    tasks_upcoming = Task.objects.filter(
        user=request.user,
        date__gt=today
    ).order_by('date', 'time')

    return render(request, 'tasks/dashboard.html', {
        'tasks_today': tasks_today,
        'tasks_upcoming': tasks_upcoming,
        'today': today
    })


@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('dashboard')
    else:
        form = TaskForm()
    return render(request, 'tasks/create_task.html', {'form': form})


@login_required
def toggle_task_complete(request, task_id):
    task = Task.objects.get(id=task_id, user=request.user)
    task.completed = not task.completed
    task.save()
    return redirect('dashboard')


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()

        messages.success(request, "Perfil actualizado correctamente.")
        return redirect('edit_profile')

    return render(request, 'tasks/edit_profile.html')


@login_required
def calendar_view(request):
    today = date.today()

    year = int(request.GET.get("year", today.year))
    month = int(request.GET.get("month", today.month))
    day_param = request.GET.get("day")

    cal = calendar.monthcalendar(year, month)
    month_name = calendar.month_name[month]

    # Día seleccionado
    selected_date = date(year, month, int(day_param)) if day_param else today

    # Tareas del día seleccionado
    tasks_selected_day = Task.objects.filter(
        user=request.user,
        date=selected_date
    ).order_by("time")

    # PRIORIDAD POR DÍA
    tasks_by_priority = {}

    month_tasks = Task.objects.filter(
        user=request.user,
        date__year=year,
        date__month=month
    )

    for task in month_tasks:
        day = task.date.day
        pr = task.priority

        if day not in tasks_by_priority:
            tasks_by_priority[day] = pr
        else:
            # lógica prioridad
            if pr == "Alta":
                tasks_by_priority[day] = "Alta"
            elif pr == "Media" and tasks_by_priority[day] == "Baja":
                tasks_by_priority[day] = "Media"

    return render(request, "tasks/calendar.html", {
        "today": today,
        "calendar": cal,
        "month_name": month_name,
        "month": month,
        "year": year,
        "selected_date": selected_date,
        "tasks_selected_day": tasks_selected_day,
        "tasks_by_priority": tasks_by_priority,
    })


@login_required
def reminders(request):
    settings, created = ReminderSettings.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        # Booleanos
        settings.push_notifications = request.POST.get('push_notifications') == 'Activadas'
        settings.email_notifications = request.POST.get('email_notifications') == 'Activadas'

        # Tiempo recordatorio
        settings.reminder_time = int(request.POST.get('reminder_time'))

        # Horario silencioso
        settings.quiet_start = request.POST.get('quiet_start')
        settings.quiet_end = request.POST.get('quiet_end')

        settings.save()
        messages.success(request, "Configuración de recordatorios guardada.")
        return redirect('dashboard')

    return render(request, 'tasks/reminders.html', {'settings': settings})


@login_required
def check_due_tasks(request):
    try:
        settings = request.user.reminder_settings
    except ReminderSettings.DoesNotExist:
        return JsonResponse({'tasks': []})

    # Si notificaciones push están apagadas → no notificar nada
    if not settings.push_notifications:
        return JsonResponse({'tasks': []})

    # Horas silenciosas
    now = datetime.now().time()
    if settings.quiet_start and settings.quiet_end:
        start = settings.quiet_start
        end = settings.quiet_end

        # Rango cruzando medianoche
        if start > end:
            if start <= now or now <= end:
                return JsonResponse({'tasks': []})
        else:
            if start <= now <= end:
                return JsonResponse({'tasks': []})

    # Calcular tiempo objetivo
    now_dt = datetime.now()
    target_time = now_dt + timedelta(minutes=settings.reminder_time)

    # Ventana ±30s
    start_window = target_time - timedelta(seconds=30)
    end_window = target_time + timedelta(seconds=30)

    target_date = target_time.date()

    tasks = Task.objects.filter(
        user=request.user,
        date=target_date,
        time__range=(start_window.time(), end_window.time()),
        completed=False
    )

    task_list = []

    #  ENVÍO DE CORREO INTEGRADO
    for t in tasks:
        task_list.append({'title': t.title, 'time': t.time.strftime('%H:%M')})

        # Si email notifications está activado → Enviar correo
        if settings.email_notifications:
            enviar_recordatorio(request.user, t)

    return JsonResponse({'tasks': task_list})



@login_required
def test_email(request):
    try:
        settings = request.user.reminder_settings
    except ReminderSettings.DoesNotExist:
        messages.error(request, "Primero configura tus recordatorios.")
        return redirect('reminders')

    # Simular UNA tarea ficticia
    class DummyTask:
        title = "Correo de prueba"
        date = date.today()
        time = datetime.now().time()

    dummy = DummyTask()

    # Enviar el correo usando tu función real
    enviar_recordatorio(request.user, dummy)

    messages.success(request, "Correo de prueba enviado. Revisa la consola del servidor.")
    return redirect('reminders')
