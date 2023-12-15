from .views import ClinicViewSet, FileViewSet, PatientViewSet, AppointmentViewSet, DentalRecordViewSet, BlocklistViewSet, NoteViewSet, AdViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'clinics', ClinicViewSet, basename='clinic')
router.register(r'patients', PatientViewSet, basename='patient')
router.register(r'files', FileViewSet, basename='file')
router.register(r'appointments', AppointmentViewSet, basename='appointment')
router.register(r'dental-records', DentalRecordViewSet, basename='dental-record')
router.register(r'blocks', BlocklistViewSet, basename='block')
router.register(r'notes', NoteViewSet, basename='note')
router.register(r'ads', AdViewSet, basename='ad')

urlpatterns = router.urls