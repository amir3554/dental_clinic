from django.contrib import admin
from .models import Operation, Department, Worker, Slider, Role


@admin.register(Operation)
class OperationTypesModelAdmin(admin.ModelAdmin):
    list_per_page = 20



@admin.register(Department)
class DepartmentTypesModelAdmin(admin.ModelAdmin):
    list_per_page = 20



@admin.register(Worker)
class WorkerTypesModelAdmin(admin.ModelAdmin):
    list_per_page = 20


@admin.register(Slider)
class SliderTypesModelAdmin(admin.ModelAdmin):
    list_per_page = 20

@admin.register(Role)
class RoleTypesModelAdmin(admin.ModelAdmin):
    list_per_page = 20

    list_select_related = ( 'operation', 'worker' )

    ordering = ['operation__dental_type']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('worker__department')