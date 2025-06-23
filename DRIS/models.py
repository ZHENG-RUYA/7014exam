# DRIS/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    class UserType(models.TextChoices):
        CITIZEN = 'CT', _('Citizen')
        VOLUNTEER = 'VL', _('Volunteer')
        AUTHORITY = 'AT', _('Authority')

    user_type = models.CharField(
        max_length=2,
        choices=UserType.choices,
        default=UserType.CITIZEN,
    )
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)


class DisasterReport(models.Model):
    class DisasterType(models.TextChoices):
        FLOOD = 'FL', _('Flood')
        LANDSLIDE = 'LS', _('Landslide')
        HAZE = 'HZ', _('Haze')
        OTHER = 'OT', _('Other')

    class SeverityLevel(models.TextChoices):
        LOW = 'LW', _('Low')
        MEDIUM = 'MD', _('Medium')
        HIGH = 'HG', _('High')
        CRITICAL = 'CR', _('Critical')

    reporter = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    disaster_type = models.CharField(max_length=2, choices=DisasterType.choices)
    location = models.CharField(max_length=100)
    gps_coordinates = models.CharField(max_length=50)
    severity = models.CharField(max_length=2, choices=SeverityLevel.choices)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)


class AidRequest(models.Model):
    class AidType(models.TextChoices):
        FOOD = 'FD', _('Food')
        SHELTER = 'SH', _('Shelter')
        RESCUE = 'RS', _('Rescue')
        MEDICAL = 'MD', _('Medical')
        OTHER = 'OT', _('Other')

    requester = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    disaster = models.ForeignKey(DisasterReport, on_delete=models.CASCADE)
    aid_type = models.CharField(max_length=2, choices=AidType.choices)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_fulfilled = models.BooleanField(default=False)


class Shelter(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    gps_coordinates = models.CharField(max_length=50)
    capacity = models.PositiveIntegerField()
    current_occupancy = models.PositiveIntegerField(default=0)
    contact_person = models.CharField(max_length=100)
    contact_phone = models.CharField(max_length=15)
    facilities = models.TextField()


class Volunteer(models.Model):
    class SkillType(models.TextChoices):
        MEDICAL = 'MD', _('Medical')
        RESCUE = 'RS', _('Rescue')
        CONSTRUCTION = 'CN', _('Construction')
        COOKING = 'CK', _('Cooking')
        DRIVING = 'DV', _('Driving')
        OTHER = 'OT', _('Other')

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    skills = models.CharField(max_length=2, choices=SkillType.choices)
    availability = models.BooleanField(default=True)
    certification = models.TextField(blank=True)
    experience = models.TextField(blank=True)


class VolunteerAssignment(models.Model):
    volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE)
    aid_request = models.ForeignKey(AidRequest, on_delete=models.CASCADE)
    assigned_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    assignment_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')
    notes = models.TextField(blank=True)