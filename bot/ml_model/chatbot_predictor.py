# bot/ml_model/chatbot_predictor.py

import pickle
import json
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pandas as pd
from difflib import get_close_matches
import re
import os

class ChatbotPredictor:
    def __init__(self, model_dir='bot/ml_model/saved_models'):
        self.model_dir = model_dir
        self.model = None
        self.tokenizer = None
        self.label_encoder = None
        self.config = None
        self.qa_data = None
        self.load_resources()
        
    def load_resources(self):
        """Load all required resources"""
        try:
            print("🔄 Loading chatbot resources...")
            
            # Load model
            model_path = os.path.join(self.model_dir, 'chatbot_model.h5')
            self.model = load_model(model_path)
            print("   ✅ Model loaded")
            
            # Load tokenizer
            tokenizer_path = os.path.join(self.model_dir, 'tokenizer.pkl')
            with open(tokenizer_path, 'rb') as f:
                self.tokenizer = pickle.load(f)
            print("   ✅ Tokenizer loaded")
            
            # Load label encoder
            encoder_path = os.path.join(self.model_dir, 'label_encoder.pkl')
            with open(encoder_path, 'rb') as f:
                self.label_encoder = pickle.load(f)
            print("   ✅ Label encoder loaded")
            
            # Load config
            config_path = os.path.join(self.model_dir, 'config.json')
            with open(config_path, 'r') as f:
                self.config = json.load(f)
            print("   ✅ Config loaded")
            
            # Load Q&A dataset
            qa_path = 'bot/datasets/medical_qa.csv'
            self.qa_data = pd.read_csv(qa_path)
            print("   ✅ Q&A dataset loaded")
            
            print("✅ All resources loaded successfully!\n")
            
        except Exception as e:
            print(f"❌ Error loading resources: {e}")
            raise
    
    def preprocess_question(self, question):
        """Clean and preprocess user question"""
        # Convert to lowercase
        question = question.lower()
        
        # Remove extra spaces
        question = re.sub(r'\s+', ' ', question).strip()
        
        return question
    
    def get_answer(self, question, confidence_threshold=0.6):
        """Get answer for user question"""
        # Preprocess
        processed_question = self.preprocess_question(question)
        
        # Check for emergency keywords
        emergency_keywords = ['chest pain', 'heart attack', 'can\'t breathe', 
                            'breathing difficulty', 'unconscious', 'severe bleeding',
                            'stroke', 'suicide', 'can not breathe']
        
        if any(keyword in processed_question for keyword in emergency_keywords):
            return {
                'answer': "⚠️ EMERGENCY DETECTED!\n\nThis seems like an emergency situation. Please:\n\n"
                         "1. Call Emergency Services: 108 (India)\n"
                         "2. Go to nearest hospital immediately\n"
                         "3. Don't delay medical attention\n\n"
                         "This bot is NOT a substitute for emergency medical care!",
                'confidence': 1.0,
                'category': 'emergency',
                'is_emergency': True
            }
        
        # Try exact match first
        exact_match = self.qa_data[
            self.qa_data['questions'].str.lower() == processed_question
        ]
        
        if not exact_match.empty:
            answer_row = exact_match.iloc[0]
            return {
                'answer': answer_row['answers'],
                'confidence': 1.0,
                'category': answer_row['category'],
                'disease': answer_row['disease'],
                'is_emergency': False
            }
        
        # Use ML model prediction
        try:
            # Tokenize and pad
            sequence = self.tokenizer.texts_to_sequences([processed_question])
            padded = pad_sequences(
                sequence, 
                maxlen=self.config['max_sequence_length'], 
                padding='post'
            )
            
            # Predict
            prediction = self.model.predict(padded, verbose=0)
            predicted_class = np.argmax(prediction[0])
            confidence = float(prediction[0][predicted_class])
            
            # Decode category
            category = self.label_encoder.inverse_transform([predicted_class])[0]
            
            # If confidence is low, try fuzzy matching
            if confidence < confidence_threshold:
                similar_questions = get_close_matches(
                    processed_question, 
                    self.qa_data['questions'].str.lower().tolist(),
                    n=1,
                    cutoff=0.6
                )
                
                if similar_questions:
                    matched_row = self.qa_data[
                        self.qa_data['questions'].str.lower() == similar_questions[0]
                    ].iloc[0]
                    
                    return {
                        'answer': matched_row['answers'],
                        'confidence': 0.7,
                        'category': matched_row['category'],
                        'disease': matched_row['disease'],
                        'is_emergency': False,
                        'matched_question': similar_questions[0]
                    }
            
            # Get answer based on predicted category
            category_answers = self.qa_data[self.qa_data['category'] == category]
            
            if not category_answers.empty:
                # Get most relevant answer from category
                answer_row = category_answers.iloc[0]
                
                return {
                    'answer': answer_row['answers'],
                    'confidence': confidence,
                    'category': category,
                    'disease': answer_row['disease'],
                    'is_emergency': False
                }
            
        except Exception as e:
            print(f"Prediction error: {e}")
        
        # Default response if nothing matches
        return {
            'answer': "I'm sorry, I couldn't find specific information about your query. "
                     "Please try rephrasing your question or consult with a healthcare professional. "
                     "For emergencies, please call 108 or visit the nearest hospital.\n\n"
                     "You can also try:\n"
                     "- Being more specific about your symptoms\n"
                     "- Using common medical terms\n"
                     "- Finding doctors/hospitals near you using our location feature",
            'confidence': 0.0,
            'category': 'unknown',
            'is_emergency': False
        }
    
    def get_disclaimer(self):
        """Return medical disclaimer"""
        return ("\n\n⚠️ DISCLAIMER: This information is for educational purposes only "
                "and is NOT a substitute for professional medical advice, diagnosis, or treatment. "
                "Always seek the advice of your physician or qualified health provider.")


# Test function
def test_predictor():
    """Test the chatbot predictor"""
    print("="*60)
    print("🧪 TESTING CHATBOT PREDICTOR")
    print("="*60)
    
    predictor = ChatbotPredictor()
    
    test_questions = [
        "I have fever and body ache",
        "How to control diabetes",
        "I have chest pain",
        "What is healthy diet",
        "I have breathing difficulty"
    ]
    
    for question in test_questions:
        print(f"\n❓ Question: {question}")
        result = predictor.get_answer(question)
        print(f"📋 Category: {result['category']}")
        print(f"📊 Confidence: {result['confidence']*100:.2f}%")
        print(f"💬 Answer: {result['answer'][:100]}...")
        print("-"*60)
    
    print("\n✅ Testing complete!")


if __name__ == '__main__':
    test_predictor()