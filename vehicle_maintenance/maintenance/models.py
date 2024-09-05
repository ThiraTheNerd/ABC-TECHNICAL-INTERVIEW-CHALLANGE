from django.db import models
from django.utils import timezone
from .utils import compress_image

# Create your models here.

class Owner(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Vehicle(models.Model):
    model = models.CharField(max_length=255)
    registration_number = models.CharField(max_length=255, unique=True)
    owner = models.ForeignKey(Owner, related_name='vehicles', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.model} ({self.registration_number})"

class Service(models.Model):
    SERVICE_TYPES = (
        ('Maintenance', 'Maintenance'),
        ('Repair', 'Repair'),
        ('Inspection', 'Inspection'),
    )

    service_type = models.CharField(max_length=255, choices=SERVICE_TYPES)
    date = models.DateField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    vehicle = models.ForeignKey(Vehicle, related_name='services', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.vehicle} - {self.service_type} - {self.date}"

class StoredFile(models.Model):
    file = models.FileField(upload_to='files/')
    name = models.CharField(max_length=255)
    file_size = models.IntegerField()
    url = models.URLField(blank=True)
    upload_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.file.name
    def save(self, *args, **kwargs):
        if 'image' in self.file.content_type:
            self.file = compress_image(self.file)
        self.name = self.file.name
        self.file_size = self.file.size
        super().save(*args, **kwargs)