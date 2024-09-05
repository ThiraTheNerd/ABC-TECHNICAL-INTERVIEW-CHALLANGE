from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count, Sum
from django.db import connection
from django.shortcuts import render, redirect
from .models import Service, Vehicle, Owner, StoredFile
from .serializers import  OwnerSerializer, VehicleSerializer, FileSerializer
from .utils import compress_image
from django.http import JsonResponse
from rest_framework import generics
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.conf import settings
from django.core.cache import cache


CACHE_TTL = getattr(settings, 'CACHE_TTL', 60 * 15)  # Default is 15 minutes

# Create your views here.
def get_services(request):
    # list of all service activities
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                v.model AS vehicle_model, 
                v.registration_number AS vehicle_registration, 
                o.name AS owner_name, 
                s.cost, 
                s.date 
            FROM 
                maintainance_service s
                JOIN maintainance_vehicle v ON s.vehicle_id = v.id
                JOIN maintainance_owner o ON v.owner_id = o.id
            ORDER BY 
                s.date
        """)
        rows = cursor.fetchall()

    # Convert to JSON
    services = [
        {
            'vehicle_model': row[0],
            'vehicle_registration': row[1],
            'owner_name': row[2],
            'cost': row[3],
            'date': row[4],
        }
        for row in rows
    ]
    return JsonResponse(services, safe=False)

class OwnerStatsView(APIView):
    def get(self, request):
        # Query to get the list of owners and their total service count and amount spent
        owners = Owner.objects.annotate(
            total_services=Count('vehicle__service'),
            total_spent=Sum('vehicle__service__cost')
        ).order_by('-total_spent')
        serializer = OwnerSerializer(owners, many=True)
        return Response(serializer.data)
class VehicleStatsView(generics.ListAPIView):
    serializer_class = VehicleSerializer

    def get_queryset(self):
        # stats for each vehicle
        return (
            Vehicle.objects
            .annotate(
                service_count=Count('service'),
                total_income=Sum('service__cost')
            )
            .order_by('-service_count')  # Order by service frequency
        )
    
@method_decorator(cache_page(CACHE_TTL), name='get')
class FileListView(generics.ListAPIView):
    queryset = StoredFile.objects.all()
    serializer_class = FileSerializer

class FileUploadView(generics.CreateAPIView):
    serializer_class = FileSerializer

    def post(self, request, *args, **kwargs):
        file = request.FILES['file']

        # Check if the uploaded file is an image and compress it
        if file.content_type.startswith('image/'):
            compressed_file = compress_image(file)
            file_instance = StoredFile.objects.create(file=compressed_file)
        else:
            # Non-image file upload
            file_instance = StoredFile.objects.create(file=file)

        # Create the file instance and save the URL
        file_instance.url = request.build_absolute_uri(file_instance.file.url)
        file_instance.save()

        # Invalidate the file list cache after uploading a file
        cache.delete('views.decorators.cache.cache_page')

        return Response({'message': 'File uploaded successfully', 'data': FileSerializer(file_instance).data})
    
class FileSummaryView(generics.GenericAPIView):
    def get(self, request):
        total_files = StoredFile.objects.count()
        total_size = StoredFile.objects.aggregate(total_size=Sum('file_size'))['total_size']
        return Response({
            'total_files': total_files,
            'total_size': total_size
        })
