# bot/ml_model/train_model.py

import pandas as pd
import numpy as np
import pickle
import os
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Embedding, Conv1D, GlobalMaxPooling1D
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import json

class HealthcareChatbot:
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.label_encoder = None
        self.max_sequence_length = 100
        self.vocab_size = 3000
        
    def load_data(self, csv_path='bot/datasets/medical_qa.csv'):
        """Load the medical Q&A dataset"""
        print("📁 Loading dataset...")
        df = pd.read_csv(csv_path)
        
        questions = df['questions'].values
        answers = df['answers'].values
        categories = df['category'].values
        
        return questions, answers, categories
    
    def preprocess_data(self, questions, categories):
        """Preprocess text data"""
        print("🔄 Preprocessing data...")
        
        # Initialize tokenizer
        self.tokenizer = Tokenizer(num_words=self.vocab_size, oov_token='<OOV>')
        self.tokenizer.fit_on_texts(questions)
        
        # Convert text to sequences
        sequences = self.tokenizer.texts_to_sequences(questions)
        
        # Pad sequences
        X = pad_sequences(sequences, maxlen=self.max_sequence_length, padding='post')
        
        # Encode labels
        self.label_encoder = LabelEncoder()
        y = self.label_encoder.fit_transform(categories)
        
        return X, y
    
    def build_model(self, num_classes):
        """Build CNN model"""
        print("🏗️  Building CNN model...")
        
        model = Sequential([
            # Embedding layer
            Embedding(self.vocab_size, 128, input_length=self.max_sequence_length),
            
            # First Conv1D layer
            Conv1D(128, 5, activation='relu'),
            GlobalMaxPooling1D(),
            
            # Deeper dense layers
            Dense(256, activation='relu'),
            Dropout(0.5),
            
            Dense(128, activation='relu'),
            Dropout(0.4),
            
            Dense(64, activation='relu'),
            Dropout(0.3),
            
            # Output layer
            Dense(num_classes, activation='softmax')
        ])
        
        model.compile(
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        print("\n📊 Model Architecture:")
        model.summary()
        return model
    
    def train(self, X, y, epochs=100, batch_size=8):
        """Train the model"""
        print("\n🚀 Training model...")
        print(f"⚙️  Configuration: {epochs} epochs, batch size {batch_size}")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        print(f"\n📊 Dataset Split:")
        print(f"   Training samples: {len(X_train)}")
        print(f"   Testing samples: {len(X_test)}")
        
        # Build model
        num_classes = len(np.unique(y))
        self.model = self.build_model(num_classes)
        
        # Train
        print("\n⏳ Training in progress...\n")
        history = self.model.fit(
            X_train, y_train,
            epochs=epochs,
            batch_size=batch_size,
            validation_data=(X_test, y_test),
            verbose=1
        )
        
        # Evaluate
        print("\n📈 Evaluating model...")
        loss, accuracy = self.model.evaluate(X_test, y_test, verbose=0)
        print(f"\n✅ Training Complete!")
        print(f"   Test Accuracy: {accuracy*100:.2f}%")
        print(f"   Test Loss: {loss:.4f}")
        
        return history
    
    def save_model(self, model_dir='bot/ml_model/saved_models'):
        """Save model and preprocessing objects"""
        print(f"\n💾 Saving model to {model_dir}...")
        
        os.makedirs(model_dir, exist_ok=True)
        
        # Save Keras model
        model_path = os.path.join(model_dir, 'chatbot_model.h5')
        self.model.save(model_path)
        print(f"   ✅ Model saved: chatbot_model.h5")
        
        # Save tokenizer
        tokenizer_path = os.path.join(model_dir, 'tokenizer.pkl')
        with open(tokenizer_path, 'wb') as f:
            pickle.dump(self.tokenizer, f)
        print(f"   ✅ Tokenizer saved: tokenizer.pkl")
        
        # Save label encoder
        encoder_path = os.path.join(model_dir, 'label_encoder.pkl')
        with open(encoder_path, 'wb') as f:
            pickle.dump(self.label_encoder, f)
        print(f"   ✅ Label encoder saved: label_encoder.pkl")
        
        # Save configuration
        config = {
            'max_sequence_length': self.max_sequence_length,
            'vocab_size': self.vocab_size,
            'classes': self.label_encoder.classes_.tolist()
        }
        
        config_path = os.path.join(model_dir, 'config.json')
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=4)
        print(f"   ✅ Config saved: config.json")
        
        print(f"\n🎉 All files saved successfully!")
    
    def predict(self, question):
        """Predict category for a question"""
        # Preprocess question
        sequence = self.tokenizer.texts_to_sequences([question])
        padded = pad_sequences(sequence, maxlen=self.max_sequence_length, padding='post')
        
        # Predict
        prediction = self.model.predict(padded, verbose=0)
        predicted_class = np.argmax(prediction[0])
        confidence = prediction[0][predicted_class]
        
        # Decode label
        category = self.label_encoder.inverse_transform([predicted_class])[0]
        
        return category, confidence


# Main training function
def main():
    print("="*60)
    print("🏥 AI HEALTHCARE BOT - MODEL TRAINING")
    print("="*60)
    print()
    
    # Create model directories
    os.makedirs('bot/ml_model', exist_ok=True)
    os.makedirs('bot/ml_model/saved_models', exist_ok=True)
    
    # Initialize chatbot
    chatbot = HealthcareChatbot()
    
    # Load data
    questions, answers, categories = chatbot.load_data()
    
    print(f"✅ Dataset loaded successfully!")
    print(f"   Total samples: {len(questions)}")
    print(f"   Unique categories: {len(set(categories))}")
    print(f"   Categories: {set(categories)}")
    print()
    
    # Preprocess
    X, y = chatbot.preprocess_data(questions, categories)
    print(f"✅ Data preprocessed!")
    print(f"   Input shape: {X.shape}")
    print()
    
    # Train
    history = chatbot.train(X, y, epochs=50, batch_size=8)
    
    # Save model
    chatbot.save_model()
    
    # Test prediction
    print("\n" + "="*60)
    print("🧪 TESTING MODEL")
    print("="*60)
    test_questions = [
        "I have fever and body pain",
        "How to stay healthy",
        "I have chest pain"
    ]
    
    for test_q in test_questions:
        category, confidence = chatbot.predict(test_q)
        print(f"\n❓ Question: {test_q}")
        print(f"   Category: {category}")
        print(f"   Confidence: {confidence*100:.2f}%")
    
    print("\n" + "="*60)
    print("✅ MODEL TRAINING COMPLETED SUCCESSFULLY!")
    print("="*60)
    print("\n📁 Model files saved in: bot/ml_model/saved_models/")
    print("   - chatbot_model.h5")
    print("   - tokenizer.pkl")
    print("   - label_encoder.pkl")
    print("   - config.json")
    print("\n🎉 Your AI Healthcare Bot is now ready to chat!")


if __name__ == '__main__':
    main()