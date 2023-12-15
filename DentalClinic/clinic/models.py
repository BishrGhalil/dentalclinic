from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget


class Clinic(models.Model):
    name = models.CharField("Name", max_length=255, unique=True, db_index=True)
    address = models.CharField("Address", max_length=255)
    # TODO: Change upload path or save in db
    image = models.ImageField("Image", blank=True, null=True)
    created_at = models.DateTimeField("Create Date", auto_now_add=True)

    def __str__(self):
        return self.name


class Patient(models.Model):
    class Gender(models.IntegerChoices):
        OTHER = 1
        MALE = 2
        FEMALE = 3

    class SocialStatus(models.IntegerChoices):
        SINGLE = 1
        MARRIED = 2
        DIVORCED = 3
        WIDOWED = 4
        ENGAGED = 5

    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        related_name="patient",
        null=False,
        blank=False,
        db_index=True,
    )
    first_name = models.CharField("First Name", max_length=50)
    last_name = models.CharField("Last Name", max_length=50)
    father_name = models.CharField(
        "Father's Name", max_length=50, null=True, blank=True
    )
    mother_name = models.CharField(
        "Mother's Name", max_length=50, null=True, blank=True
    )
    phonenumber = PhoneNumberField("Phone Number", null=False, blank=False, unique=True)
    address = models.CharField("Address", max_length=300, null=True, blank=True)
    gender = models.SmallIntegerField(
        "Gender", choices=Gender.choices, null=True, blank=True
    )
    social_status = models.SmallIntegerField(
        "Social Status",
        choices=SocialStatus.choices,
        null=True,
        blank=True,
    )
    birth = models.DateField("Birth Date", blank=False, null=False)
    general_history = models.TextField(
        "General History", max_length=5000, blank=True, null=True
    )
    clinic = models.ForeignKey(
        "Clinic", on_delete=models.DO_NOTHING, db_index=True, related_name="patients"
    )
    created_at = models.DateTimeField("Create Date", auto_now_add=True)

    @property
    def username(self):
        return self.user.username

    @property
    def age(self):
        return int((timezone.localdate() - self.birth).days // 365.2425)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self) -> str:
        return self.full_name


class Appointment(models.Model):
    class Status(models.IntegerChoices):
        PENDING = (1, "pending")
        SCHEDULED = (2, "scheduling")
        REJECTED = (3, "rejected")
        CANCELED = (4, "canceled")
        RESCHEDULED = (5, "rescheduled")
        COMPLETED = (6, "completed")
        MISSED = (7, "missed")

    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        db_index=True,
        related_name="appointments",
    )
    patient = models.ForeignKey(
        to=Patient,
        on_delete=models.CASCADE,
        db_index=True,
        null=True,
        blank=True,
        related_name="appointments",
    )
    clinic = models.ForeignKey(
        to="Clinic",
        on_delete=models.CASCADE,
        db_index=True,
        related_name="appointments",
    )
    date = models.DateTimeField("Date")
    status = models.SmallIntegerField("Status", choices=Status.choices, db_index=True)
    created_at = models.DateTimeField("Create Date", auto_now=True)

    def __str__(self):
        return f"{self.date} - {self.user} - {self.clinic}"


class DentalRecord(models.Model):
    clinic = models.ForeignKey("Clinic", on_delete=models.DO_NOTHING)
    patient = models.ForeignKey(
        "Patient", on_delete=models.CASCADE, db_index=True, related_name="dental_record"
    )
    date = models.DateTimeField("Date", auto_now_add=True)
    complaint = models.TextField("Complaint", max_length=1000)
    diagnoses = models.TextField("Diagnoses", max_length=1000)
    treatment = models.TextField("Treatment", max_length=5000)
    created_at = models.DateTimeField("Create Date", auto_now_add=True)

    def __str__(self):
        return f"Dental Record [{self.date}]: {self.patient}"


class File(models.Model):
    class FileType(models.TextChoices):
        PDF = ("pdf", "PDF")
        IMAGE = "image"

    appointment = models.ForeignKey(
        Appointment, on_delete=models.CASCADE, db_index=True, related_name="files"
    )
    name = models.CharField("File name", max_length=255, blank=False, null=False)
    type = models.CharField("File type", max_length=10, choices=FileType.choices)
    file = models.FileField("File", blank=False, null=False)
    created_at = models.DateTimeField("Create Date", auto_now_add=True)

    def __str__(self):
        return self.name


class Blocklist(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="blocklist",
        blank=True,
        null=True,
        db_index=True,
    )
    ip_addr = models.GenericIPAddressField("Ip Address", blank=True, null=True, db_index=True)
    created_at = models.DateTimeField("Create Date", auto_now_add=True)

    def __str__(self):
        if self.user:
            return f"{self.user} blocked"
        elif self.ip_addr:
            return f"{self.ip_addr} blocked"
        else:
            return f"Unkown entry"



class Note(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="notes",
        db_index=True,
    )
    title = models.CharField("Note Title", max_length=255, blank=False, null=False)
    body = models.TextField("Note Body", blank=False, null=False)
    created_at = models.DateTimeField("Create Date", auto_now_add=True)

    def __str__(self):
        return self.title


class Ad(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="ads",
        db_index=True,
    )
    image = models.ImageField("Ad Image", blank=False, null=False)
    expires_at = models.DateField("Expiration Date", blank=True, null=True)
    created_at = models.DateTimeField("Create Date", auto_now_add=True)

    def __str__(self):
        return f"{self.image} - {self.created_at}"