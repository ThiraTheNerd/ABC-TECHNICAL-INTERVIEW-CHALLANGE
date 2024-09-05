from rest_framework import serializers
from .models import Service, Owner, Vehicle, StoredFile

class ServiceSerializer(serializers.ModelSerializer):
    vehicle_model = serializers.CharField(source='vehicle.model')
    vehicle_registration = serializers.CharField(source='vehicle.registration_number')
    owner_name = serializers.CharField(source='vehicle.owner.name')

    class Meta:
        model = Service
        fields = ['vehicle_model', 'vehicle_registration', 'owner_name', 'cost', 'date']

class OwnerSerializer(serializers.ModelSerializer):
    total_services = serializers.IntegerField()
    total_spent = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Owner
        fields = ['name', 'total_services', 'total_spent']

class VehicleSerializer(serializers.ModelSerializer):
    service_count = serializers.IntegerField()
    total_income = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Vehicle
        fields = ['model', 'service_count', 'total_income']

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoredFile
        fields = ['id', 'name', 'file_size', 'upload_date', 'url']