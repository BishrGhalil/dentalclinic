from .models import Patient, Clinic, Appointment, File, DentalRecord, Blocklist, Note, Ad
from .serializers import (
    PatientSerializer,
    ClinicSerializer,
    AppointmentSerializer,
    FileSerializer,
    DentalRecordSerializer,
    BlocklistSerializer,
    NoteSerializer,
    AdSerializer
)
from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response


class ClinicViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing clinic instances.
    """

    serializer_class = ClinicSerializer
    queryset = Clinic.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "address"]
    ordering_fields = ["name", "address", "created_at"]

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ["list", "retrieve"]:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class PatientViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing patient instances.
    """

    serializer_class = PatientSerializer
    queryset = Patient.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = ["clinic", "gender", "social_status"]
    search_fields = [
        "first_name",
        "last_name",
        "user__username",
        "father_name",
        "mother_name",
    ]
    ordering_fields = ["first_name", "last_name", "birth", "created_at", "clinic__name"]

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ["list"]:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=["get"])
    def me(self, request):
        self.kwargs["pk"] = request.user.pk
        return self.retrieve(request)

    @action(detail=True, methods=["git"], permission_classes=[IsAdminUser])
    def block(self, request):
        try:
            Blocklist.objects.create(user=request.user)
        except:
            return Response({'detail': "couldn't block user"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'status': 'user blocked'})


class AppointmentViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing appointment instances.
    """

    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.all()
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = ["clinic", "user", "status"]
    ordering_fields = ["date", "status", "clinic", "user", "created_at"]

    @action(detail=False, methods=["get"])
    def mine(self, request):
        appointment = get_object_or_404(Appointment.objects.filter(user=request.user))
        serializer = self.get_serializer(appointment)
        return Response(serializer.data)


class DentalRecordViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing dental record instances.
    """

    serializer_class = DentalRecordSerializer
    queryset = DentalRecord.objects.all()
    permission_classes = [IsAdminUser]
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = ["clinic", "patient"]
    search_fields = [
        "complaint",
        "diagnoses",
        "treatment",
        "patient__first_name",
        "patient__last_name",
    ]
    ordering_fields = ["date", "clinic", "patient", "created_at"]

    @action(detail=False, methods=["get"])
    def mine(self, request):
        drc = get_object_or_404(DentalRecord.objects.filter(patient__user=request.user))
        serializer = self.get_serializer(drc)
        return Response(serializer.data)


class FileViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing file instances.
    """

    serializer_class = FileSerializer
    queryset = File.objects.all()
    permission_classes = [IsAdminUser]
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = ["appointment", "type"]
    search_fields = ["name"]
    ordering_fields = ["name", "type", "appointment"]

    @action(detail=False, methods=["get"])
    def mine(self, request):
        file = get_object_or_404(
            File.objects.filter(appointment__user=request.user)
        )
        serializer = self.get_serializer(file)
        return Response(serializer.data)


class BlocklistViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing blocklist instances.
    """

    serializer_class = BlocklistSerializer
    queryset = Blocklist.objects.all()
    permission_classes = [IsAdminUser]
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    search_fields = ["user__username", "ip_addr"]
    ordering_fields = ["user", "ip_addr", "created_at"]

class NoteViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing note instances.
    """

    serializer_class = NoteSerializer
    queryset = Note.objects.all()
    permission_classes = [IsAdminUser]
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    search_fields = ["title", "body"]
    ordering_fields = ["title", "user", "created_at"]

    @action(detail=False, methods=["get"])
    def mine(self, request):
        file = get_object_or_404(
            Note.objects.filter(user=request.user)
        )
        serializer = self.get_serializer(file)
        return Response(serializer.data)




class AdViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing ad instances.
    """

    serializer_class = AdSerializer
    queryset = Ad.objects.all()
    permission_classes = [IsAdminUser]
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    ordering_fields = ["user", "created_at", "expires_at"]

    @action(detail=False, methods=["get"])
    def mine(self, request):
        file = get_object_or_404(
            Ad.objects.filter(user=request.user)
        )
        serializer = self.get_serializer(file)
        return Response(serializer.data)

