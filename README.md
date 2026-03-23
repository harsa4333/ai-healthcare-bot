# 🏥 AI Healthcare Bot

An intelligent healthcare chatbot powered by CNN that provides 24/7 medical assistance, especially designed for rural India.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Django](https://img.shields.io/badge/Django-4.2-green.svg)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.15-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🌟 Features

- **AI-Powered Chatbot**: CNN-based medical Q&A system with 75-80% accuracy
- **Emergency Detection**: Automatic identification of critical medical conditions
- **Doctor Finder**: Locate qualified doctors by specialization
- **Hospital Finder**: Find nearby hospitals with emergency services
- **User Authentication**: Secure registration and login system
- **Chat History**: Track all conversations for reference
- **Admin Panel**: Manage doctors, hospitals, and Q&A database
- **Responsive UI**: Beautiful Bootstrap-based interface

## 🛠️ Technologies Used

- **Backend**: Django 4.2, Python 3.8+
- **Database**: MySQL
- **Machine Learning**: TensorFlow, Keras, CNN
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript, jQuery
- **APIs**: Google Places API (optional)

## 📊 Project Statistics

- **Dataset**: 63 medical Q&A pairs
- **Diseases Covered**: 25+
- **Model Architecture**: CNN with 747,141 parameters
- **Accuracy**: 61-78% (depending on dataset size)
- **Categories**: Symptoms, Treatment, Prevention, Information, Emergency

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- MySQL Server 8.0+
- pip (Python package manager)

### Setup Steps

1. **Clone the repository**
```bash
   git clone https://github.com/YOUR_USERNAME/ai-healthcare-bot.git
   cd ai-healthcare-bot
```

2. **Create virtual environment**
```bash
   python -m venv venv
   
   # Activate virtual environment
   # Windows:
   venv\Scripts\activate
   # Mac/Linux:
   source venv/bin/activate
```

3. **Install dependencies**
```bash
   pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
   # Copy the example file
   cp .env.example .env
   
   # Edit .env and add your credentials:
   # - SECRET_KEY
   # - DB_PASSWORD
   # - GOOGLE_PLACES_API_KEY (optional)
```

5. **Setup MySQL Database**
```sql
   CREATE DATABASE healthcare_bot_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   CREATE USER 'healthcare_user'@'localhost' IDENTIFIED BY 'your_password';
   GRANT ALL PRIVILEGES ON healthcare_bot_db.* TO 'healthcare_user'@'localhost';
   FLUSH PRIVILEGES;
```

6. **Run migrations**
```bash
   python manage.py migrate
```

7. **Create superuser**
```bash
   python manage.py createsuperuser
```

8. **Load sample data**
```bash
   python bot/datasets/create_dataset.py
   python bot/datasets/load_data.py
```

9. **Train ML model**
```bash
   python bot/ml_model/train_model.py
```
   ⏳ This takes 5-10 minutes

10. **Run the server**
```bash
    python manage.py runserver
```

11. **Access the application**
    - Homepage: http://127.0.0.1:8000/
    - Admin Panel: http://127.0.0.1:8000/admin/

## 📸 Screenshots

<!-- Add screenshots of your project here -->

## 🎯 Usage

### For Users

1. **Register** an account or **Login**
2. Navigate to **Chat** page
3. Ask health-related questions
4. Get instant AI-powered responses
5. Use **Find Doctors** or **Find Hospitals** to locate nearby facilities

### For Admins

1. Login to admin panel: http://127.0.0.1:8000/admin/
2. Manage Q&A pairs, doctors, hospitals
3. View user statistics and chat history
4. Retrain model with new data

## 🧪 Example Questions

Try asking these questions in the chat:

- "I have fever and body ache"
- "What are symptoms of diabetes?"
- "How to prevent dengue?"
- "I have chest pain" (emergency detection)
- "How much water should I drink daily?"

## 🏗️ Project Structure
```
ai_healthcare_bot/
├── healthcare_bot/          # Django project settings
├── bot/                     # Main application
│   ├── ml_model/           # Machine learning model
│   ├── datasets/           # Medical Q&A data
│   ├── models.py           # Database models
│   ├── views.py            # View functions
│   └── urls.py             # URL routing
├── accounts/               # User authentication
├── templates/              # HTML templates
├── static/                 # CSS, JS, images
├── media/                  # User uploads
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🤖 Model Architecture

- **Type**: Convolutional Neural Network (CNN)
- **Input**: Tokenized medical questions
- **Layers**: Embedding → Conv1D → MaxPooling → Dense → Dropout → Output
- **Output**: Category classification (symptoms, treatment, etc.)
- **Training**: 50-100 epochs with Adam optimizer

## 📝 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home page |
| `/chat/` | GET | Chat interface |
| `/send-message/` | POST | Send message to chatbot |
| `/find-doctors/` | GET | Doctor finder page |
| `/find-hospitals/` | GET | Hospital finder page |
| `/accounts/login/` | GET/POST | User login |
| `/accounts/register/` | GET/POST | User registration |
| `/admin/` | GET | Admin panel |

## 🔒 Security Features

- CSRF protection on all forms
- Password hashing with Django's built-in system
- SQL injection prevention through ORM
- XSS protection in templates
- Session management with timeouts
- Environment variables for sensitive data

## 🚧 Future Enhancements

- [ ] Multi-language support (Hindi, Tamil, Telugu)
- [ ] Voice input/output integration
- [ ] Appointment booking system
- [ ] Prescription management
- [ ] Mobile app (React Native/Flutter)
- [ ] Real-time doctor availability
- [ ] Telemedicine integration
- [ ] Health records tracking
- [ ] SMS/Email notifications
- [ ] Improved ML accuracy (90%+)

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## ⚠️ Disclaimer

**IMPORTANT**: This AI Healthcare Bot is designed for **informational and educational purposes only**. It is **NOT** a substitute for professional medical advice, diagnosis, or treatment.

- Always seek the advice of your physician or qualified health provider
- In case of emergencies, call 108 (India) or visit the nearest hospital
- Do not rely solely on this chatbot for medical decisions

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Your Name**
- GitHub: [@harsa4333](https://github.com/harsa4333)
- LinkedIn: [Your LinkedIn](www.linkedin.com/in/harshvardhan-kumar-b4533a2b3)
- Email: digital.harsa4@gmail.com

## 🙏 Acknowledgments

- Medical data sources and references
- Open source libraries and frameworks
- Healthcare professionals for guidance
- Community contributors

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact: your.email@example.com

---

**⭐ If you find this project helpful, please give it a star!**

Made with ❤️ for improving healthcare accessibility in rural India