from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Clinic)
class ClinicAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "created_at")
    search_fields = ("name", "address")

@admin.register(models.Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("username", "first_name", "last_name", "father_name", "mother_name", "address", "age", "gender", "clinic")
    search_fields = ("username", "father_name", "mother_name")
    list_filter = ("clinic",)