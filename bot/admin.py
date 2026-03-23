# bot/admin.py

from django.contrib import admin
from .models import (
    UserProfile, Disease, Symptom, QuestionAnswer, 
    ChatHistory, Doctor, Hospital
)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'city', 'state', 'created_at']
    search_fields = ['user__username', 'user__email', 'phone']
    list_filter = ['state', 'created_at']


@admin.register(Disease)
class DiseaseAdmin(admin.ModelAdmin):
    list_display = ['name', 'severity', 'created_at']
    search_fields = ['name', 'symptoms']
    list_filter = ['severity', 'created_at']


@admin.register(Symptom)
class SymptomAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(QuestionAnswer)
class QuestionAnswerAdmin(admin.ModelAdmin):
    list_display = ['question_preview', 'category', 'disease', 'is_active', 'created_at']
    search_fields = ['question', 'answer', 'category']
    list_filter = ['category', 'is_active', 'created_at']
    
    def question_preview(self, obj):
        return obj.question[:50] + '...' if len(obj.question) > 50 else obj.question
    question_preview.short_description = 'Question'


@admin.register(ChatHistory)
class ChatHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'question_preview', 'confidence_score', 'timestamp']
    search_fields = ['user__username', 'question', 'answer']
    list_filter = ['timestamp', 'confidence_score']
    date_hierarchy = 'timestamp'
    
    def question_preview(self, obj):
        return obj.question[:50] + '...' if len(obj.question) > 50 else obj.question
    question_preview.short_description = 'Question'


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['name', 'specialization', 'clinic_name', 'phone', 'is_active']
    search_fields = ['name', 'specialization', 'clinic_name', 'phone']
    list_filter = ['specialization', 'is_active', 'created_at']


@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ['name', 'hospital_type', 'emergency_available', 'phone', 'is_active']
    search_fields = ['name', 'address', 'phone']
    list_filter = ['hospital_type', 'emergency_available', 'is_active']
