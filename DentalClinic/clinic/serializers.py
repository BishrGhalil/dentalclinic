from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField
from .models import Clinic, Patient, Appointment, DentalRecord, File, Blocklist, Note, Ad
from django.contrib.auth.models import User


class PatientFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ["id", "first_name", "last_name", "full_name"]

class ClinicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinic
        fields = ["id", "name", "address", "image"]

class PhoneNumberSerializer(serializers.Serializer):
    phonenumber = PhoneNumberField()

class PatientSerializer(serializers.ModelSerializer):
    phonenumber = PhoneNumberField()
    class Meta:
        model = Patient
        fields = [
            "id",
            "user",
            "first_name",
            "last_name",
            "full_name",
            "father_name",
            "mother_name",
            "gender",
            "birth",
            "age",
            "phonenumber",
            "address",
            "social_status",
            "general_history",
            "clinic",
        ]

class AppointmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Appointment
        fields = ["id", "user", "patient", "clinic", "date", "status"]


class DentalRecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = DentalRecord
        fields = ["id", "clinic", "patient", "date", "complaint", "diagnoses", "treatment"]


class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        fields = ["id", "appointment", "name", "type", "file"]


class BlocklistSerializer(serializers.ModelSerializer):

    class Meta:
        model = Blocklist
        fields = ["id", "user", "ip_addr", "created_at"]


class NoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Note
        fields = ["id", "user", "title", "body", "created_at"]

class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ["id", "user", "image", "expires_at", "created_at"]
