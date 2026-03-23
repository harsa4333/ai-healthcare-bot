# bot/models.py

from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """Extended user profile with additional health information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Disease(models.Model):
    """Disease information database"""
    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('emergency', 'Emergency')
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    symptoms = models.TextField(help_text="Comma-separated symptoms")
    precautions = models.TextField()
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Symptom(models.Model):
    """Symptom database"""
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class QuestionAnswer(models.Model):
    """Q&A pairs for chatbot training"""
    question = models.TextField()
    answer = models.TextField()
    disease = models.ForeignKey(Disease, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.CharField(max_length=100, default='general')
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Q: {self.question[:50]}..."

    class Meta:
        ordering = ['-created_at']


class ChatHistory(models.Model):
    """Store all chat conversations"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()
    confidence_score = models.FloatField(default=0.0)
    timestamp = models.DateTimeField(auto_now_add=True)
    session_id = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username} - {self.timestamp}"

    class Meta:
        ordering = ['-timestamp']


class Doctor(models.Model):
    """Doctor listings"""
    SPECIALIZATION_CHOICES = [
        ('general', 'General Physician'),
        ('cardiologist', 'Cardiologist'),
        ('dermatologist', 'Dermatologist'),
        ('orthopedic', 'Orthopedic'),
        ('pediatrician', 'Pediatrician'),
        ('gynecologist', 'Gynecologist'),
        ('ent', 'ENT Specialist'),
        ('neurologist', 'Neurologist'),
        ('psychiatrist', 'Psychiatrist'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=200)
    specialization = models.CharField(max_length=50, choices=SPECIALIZATION_CHOICES)
    qualification = models.CharField(max_length=200)
    clinic_name = models.CharField(max_length=200)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    timings = models.CharField(max_length=200, help_text="e.g., Mon-Sat 9AM-5PM")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Dr. {self.name} - {self.get_specialization_display()}"

    class Meta:
        ordering = ['name']


class Hospital(models.Model):
    """Hospital listings"""
    HOSPITAL_TYPE_CHOICES = [
        ('government', 'Government'),
        ('private', 'Private'),
        ('charitable', 'Charitable Trust')
    ]
    
    name = models.CharField(max_length=200)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    emergency_available = models.BooleanField(default=True)
    hospital_type = models.CharField(max_length=50, choices=HOSPITAL_TYPE_CHOICES)
    facilities = models.TextField(help_text="Available facilities")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']