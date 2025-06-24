from django.contrib import admin
from .models import OperationsAndSurgeries, Department, Worker, Slider


@admin.register(OperationsAndSurgeries)
class OperationsAndSurgeriesTypesModelAdmin(admin.ModelAdmin):
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