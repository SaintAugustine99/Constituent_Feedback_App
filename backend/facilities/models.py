from django.db import models
from django.conf import settings
from locations.models import Ward
from django.core.exceptions import ValidationError

class Facility(models.Model):
    TYPE_CHOICES = [
        ('HALL', 'Social Hall'),
        ('FIELD', 'Sports Field'),
        ('PARK', 'Public Park'),
        ('OTHER', 'Other'),
    ]

    name = models.CharField(max_length=255)
    facility_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE, related_name='facilities')
    capacity = models.IntegerField(help_text="Max number of people")
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='facilities/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.get_facility_type_display()}) - {self.ward.name}"

class Booking(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending Approval'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
        ('COMPLETED', 'Completed'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name='bookings')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    purpose = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # Validate that end_time is after start_time
        if self.end_time <= self.start_time:
            raise ValidationError("End time must be after start time.")

        # Check for overlapping bookings for the same facility
        # Overlap condition: Not (ExistingEnd <= NewStart OR ExistingStart >= NewEnd)
        # Which simplifies to: ExistingEnd > NewStart AND ExistingStart < NewEnd
        overlapping = Booking.objects.filter(
            facility=self.facility,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time,
            status__in=['PENDING', 'CONFIRMED']
        ).exclude(pk=self.pk)  # Exclude self if updating

        if overlapping.exists():
            raise ValidationError("This facility is already booked for the selected time slot.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.facility.name} ({self.start_time.strftime('%Y-%m-%d %H:%M')})"
