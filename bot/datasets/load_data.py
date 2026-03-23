# bot/datasets/load_data.py

import os
import sys
import django
import pandas as pd

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthcare_bot.settings')
django.setup()

from bot.models import Disease, QuestionAnswer
from django.contrib.auth.models import User

# Get admin user
admin_user = User.objects.filter(is_superuser=True).first()

# Load diseases
print("Loading diseases into database...")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
diseases_df = pd.read_csv(os.path.join(BASE_DIR, 'diseases.csv'))

for _, row in diseases_df.iterrows():
    disease, created = Disease.objects.get_or_create(
        name=row['name'],
        defaults={
            'description': row['description'],
            'symptoms': row['symptoms'],
            'precautions': row['precautions'],
            'severity': row['severity']
        }
    )
    if created:
        print(f"✅ Added: {disease.name}")
    else:
        print(f"⏭️  Already exists: {disease.name}")

# Load Q&A pairs
print("\nLoading Q&A pairs into database...")
qa_df = pd.read_csv(os.path.join(BASE_DIR, 'medical_qa.csv'))

for _, row in qa_df.iterrows():
    # Try to find the related disease
    disease = Disease.objects.filter(name=row['disease']).first()
    
    qa, created = QuestionAnswer.objects.get_or_create(
        question=row['questions'],
        defaults={
            'answer': row['answers'],
            'category': row['category'],
            'disease': disease,
            'created_by': admin_user
        }
    )
    if created:
        print(f"✅ Added Q&A: {row['questions'][:50]}...")

print(f"\n🎉 Data loading complete!")
print(f"📊 Total Diseases: {Disease.objects.count()}")
print(f"📊 Total Q&A Pairs: {QuestionAnswer.objects.count()}")