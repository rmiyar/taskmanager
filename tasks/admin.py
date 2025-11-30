from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'priority', 'date', 'time', 'completed', 'created_at')
    list_filter = ('priority', 'completed', 'date', 'user')
    search_fields = ('title', 'description', 'user__username', 'user__email')
    list_editable = ('priority', 'completed')
    date_hierarchy = 'date'
    readonly_fields = ('created_at',)

    fieldsets = (
        ('Información de la Tarea', {
            'fields': ('title', 'description', 'user')
        }),
        ('Planificación', {
            'fields': ('date', 'time', 'priority')
        }),
        ('Estado', {
            'fields': ('completed', 'created_at')
        }),
    )

    actions = ['mark_as_completed']

    @admin.action(description='Marcar tareas seleccionadas como completadas')
    def mark_as_completed(self, request, queryset):
        queryset.update(completed=True)
