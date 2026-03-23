# bot/datasets/create_dataset.py

import json
import pandas as pd
import os

# Get the directory where this script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Sample medical Q&A dataset
medical_data = {
    'questions': [],
    'answers': [],
    'category': [],
    'disease': []
}

# Medical Q&A pairs
qa_pairs = [
    # Fever related
    {
        'question': 'I have high fever and body ache',
        'answer': 'High fever with body ache could indicate flu or viral infection. Take rest, drink plenty of fluids, and take paracetamol for fever. If fever persists for more than 3 days or goes above 103°F, consult a doctor immediately.',
        'category': 'symptoms',
        'disease': 'Fever'
    },
    {
        'question': 'What should I do for fever',
        'answer': 'For fever: Rest well, drink plenty of water and fluids, take paracetamol as per dosage, use cold compress on forehead, wear light clothing. Monitor temperature every 4-6 hours. Consult doctor if fever exceeds 103°F or lasts more than 3 days.',
        'category': 'treatment',
        'disease': 'Fever'
    },
    {
        'question': 'How to reduce fever naturally',
        'answer': 'Natural remedies for fever: Stay hydrated, take lukewarm bath, use cold compress, drink herbal teas, get adequate rest, eat light foods. However, if fever is high or persistent, medical consultation is necessary.',
        'category': 'treatment',
        'disease': 'Fever'
    },
    
    # Cold and Cough
    {
        'question': 'I have cold and cough',
        'answer': 'Cold and cough are usually viral infections. Drink warm water, take steam inhalation 2-3 times daily, have honey with warm water, avoid cold foods and drinks. If symptoms persist for more than a week or breathing difficulty occurs, consult a doctor.',
        'category': 'symptoms',
        'disease': 'Cold'
    },
    {
        'question': 'Home remedies for cough',
        'answer': 'For cough relief: Drink warm water with honey, take steam inhalation, gargle with salt water, drink ginger tea, avoid cold and oily foods, stay hydrated. If cough is severe or has blood, seek immediate medical attention.',
        'category': 'treatment',
        'disease': 'Cough'
    },
    {
        'question': 'Best medicine for cold',
        'answer': 'For cold: Rest, stay hydrated, use saline nasal drops, take steam inhalation. Over-the-counter medicines like paracetamol can help with symptoms. Antibiotics are NOT needed for viral cold. Consult doctor if symptoms worsen or last more than 10 days.',
        'category': 'treatment',
        'disease': 'Cold'
    },
    
    # Headache
    {
        'question': 'I have severe headache',
        'answer': 'Severe headache can have various causes. Rest in a quiet, dark room, apply cold compress on forehead, stay hydrated, take prescribed pain relief medication. If headache is sudden and severe, accompanied by vision problems, confusion, or stiff neck, seek emergency care immediately.',
        'category': 'symptoms',
        'disease': 'Headache'
    },
    {
        'question': 'What causes headache',
        'answer': 'Common headache causes include: stress, dehydration, lack of sleep, eye strain, skipping meals, caffeine withdrawal, sinus problems. Serious causes include migraine, high blood pressure, infections. Regular severe headaches need medical evaluation.',
        'category': 'information',
        'disease': 'Headache'
    },
    
    # Stomach issues
    {
        'question': 'I have stomach pain and diarrhea',
        'answer': 'Stomach pain with diarrhea suggests gastroenteritis or food poisoning. Stay hydrated with ORS, eat bland foods like rice and banana, avoid spicy and oily foods. If you notice blood in stools, severe dehydration, or pain persists for more than 24 hours, consult a doctor.',
        'category': 'symptoms',
        'disease': 'Gastroenteritis'
    },
    {
        'question': 'Treatment for stomach pain',
        'answer': 'For stomach pain: Avoid solid foods for few hours, drink clear fluids, avoid spicy and oily foods, take antacids if needed. If pain is severe, accompanied by fever, vomiting blood, or lasts more than 24 hours, seek medical help immediately.',
        'category': 'treatment',
        'disease': 'Gastroenteritis'
    },
    
    # Diabetes related
    {
        'question': 'What are symptoms of diabetes',
        'answer': 'Common diabetes symptoms include: frequent urination, excessive thirst, unexplained weight loss, increased hunger, blurred vision, slow healing wounds, frequent infections, and fatigue. If you experience these symptoms, get your blood sugar tested and consult a doctor.',
        'category': 'information',
        'disease': 'Diabetes'
    },
    {
        'question': 'How to control diabetes',
        'answer': 'Diabetes management: Monitor blood sugar regularly, take prescribed medications, follow diabetic diet (low sugar, high fiber), exercise 30 minutes daily, maintain healthy weight, regular health checkups, manage stress, avoid smoking and alcohol.',
        'category': 'prevention',
        'disease': 'Diabetes'
    },
    
    # Hypertension
    {
        'question': 'What is high blood pressure',
        'answer': 'High blood pressure (hypertension) is when blood pressure consistently exceeds 140/90 mmHg. Often called silent killer as it has few symptoms. Can cause headaches, shortness of breath, nosebleeds in severe cases. Regular monitoring, low salt diet, exercise, and prescribed medication help manage it.',
        'category': 'information',
        'disease': 'Hypertension'
    },
    {
        'question': 'How to reduce blood pressure',
        'answer': 'To reduce blood pressure: Reduce salt intake, eat potassium-rich foods, exercise regularly, maintain healthy weight, limit alcohol, quit smoking, manage stress, take prescribed medications regularly, monitor BP at home.',
        'category': 'prevention',
        'disease': 'Hypertension'
    },
    
    # Asthma
    {
        'question': 'I have breathing difficulty',
        'answer': 'Breathing difficulty requires immediate attention. Sit upright, take slow deep breaths, use prescribed inhaler if you have asthma. If breathing difficulty is severe, accompanied by chest pain, bluish lips, or confusion, call emergency services (108) immediately.',
        'category': 'emergency',
        'disease': 'Asthma'
    },
    {
        'question': 'What is asthma',
        'answer': 'Asthma is a chronic condition affecting airways, causing breathing difficulty, wheezing, chest tightness, and coughing. Triggered by allergens, exercise, cold air, or stress. Managed with inhalers, avoiding triggers, and regular doctor visits.',
        'category': 'information',
        'disease': 'Asthma'
    },
    
    # Chest pain - Emergency
    {
        'question': 'I have chest pain',
        'answer': '⚠️ EMERGENCY! Chest pain can be serious. If pain is severe, radiating to arm/jaw, with sweating, nausea, or shortness of breath, call 108 immediately as it could be heart attack. For mild chest pain due to acidity or muscle strain, rest and take antacid, but consult doctor for proper diagnosis.',
        'category': 'emergency',
        'disease': 'Cardiac'
    },
    {
        'question': 'Heart attack symptoms',
        'answer': '⚠️ Heart attack symptoms: Severe chest pain/pressure, pain radiating to left arm/jaw/back, shortness of breath, sweating, nausea, dizziness, extreme fatigue. If you experience these, call 108 IMMEDIATELY. Time is critical in heart attacks.',
        'category': 'emergency',
        'disease': 'Cardiac'
    },
    
    # General health
    {
        'question': 'How to stay healthy',
        'answer': 'To stay healthy: Eat balanced diet with fruits and vegetables, exercise 30 minutes daily, drink 8 glasses of water, sleep 7-8 hours, avoid smoking and excessive alcohol, manage stress, maintain hygiene, get regular health checkups, and stay positive.',
        'category': 'prevention',
        'disease': 'General'
    },
    {
        'question': 'What is healthy diet',
        'answer': 'Healthy diet includes: Variety of fruits and vegetables, whole grains, lean proteins, nuts and seeds, low-fat dairy, limited sugar and salt, adequate water intake. Avoid processed foods, trans fats, and excessive red meat.',
        'category': 'prevention',
        'disease': 'General'
    },
    
    # COVID-19
    {
        'question': 'What are COVID symptoms',
        'answer': 'Common COVID-19 symptoms: fever, dry cough, fatigue, body ache, loss of taste or smell, sore throat. In severe cases: difficulty breathing, chest pain, confusion. If you have symptoms, isolate yourself, monitor oxygen levels, and consult doctor. Get tested and vaccinated.',
        'category': 'information',
        'disease': 'COVID-19'
    },
    {
        'question': 'COVID prevention tips',
        'answer': 'COVID-19 prevention: Wear mask in crowded places, maintain 6 feet distance, wash hands frequently, use sanitizer, avoid touching face, get vaccinated, boost immunity with healthy diet, avoid large gatherings if possible.',
        'category': 'prevention',
        'disease': 'COVID-19'
    },
    
    # Skin issues
    {
        'question': 'I have skin rash and itching',
        'answer': 'Skin rash and itching can be due to allergy, infection, or skin condition. Keep area clean and dry, avoid scratching, apply prescribed cream, identify and avoid allergens. If rash spreads rapidly, has blisters, or is accompanied by fever, consult dermatologist.',
        'category': 'symptoms',
        'disease': 'Dermatitis'
    },
    
    # Eye problems
    {
        'question': 'My eyes are red and watery',
        'answer': 'Red watery eyes suggest conjunctivitis or eye irritation. Avoid rubbing eyes, wash hands frequently, use clean towels, apply prescribed eye drops, avoid sharing personal items. If vision is affected or pain is severe, consult eye specialist immediately.',
        'category': 'symptoms',
        'disease': 'Conjunctivitis'
    },
    
    # Back pain
    {
        'question': 'I have lower back pain',
        'answer': 'Lower back pain is common. Rest but avoid prolonged bed rest, apply hot/cold compress, do gentle stretching, maintain good posture, use firm mattress. Avoid heavy lifting. If pain radiates to legs, causes numbness, or accompanied by fever, consult orthopedic doctor.',
        'category': 'symptoms',
        'disease': 'Back Pain'
    },
    
    # General queries
    {
        'question': 'When should I see a doctor',
        'answer': 'See a doctor if: Symptoms persist for more than few days, severe pain, high fever (>103°F), difficulty breathing, chest pain, sudden severe headache, unexplained weight loss, bleeding, persistent vomiting, signs of infection, or any symptom that concerns you.',
        'category': 'information',
        'disease': 'General'
    },
    {
        'question': 'What is normal body temperature',
        'answer': 'Normal body temperature is around 98.6°F (37°C), but can range from 97°F to 99°F. Temperature above 100.4°F (38°C) is considered fever. Temperature can vary based on time of day, activity, and individual factors.',
        'category': 'information',
        'disease': 'General'
    },
    {
        'question': 'What are dengue symptoms',
        'answer': 'Dengue symptoms include: high fever (104°F), severe headache, pain behind eyes, joint and muscle pain, nausea, vomiting, skin rash appearing 2-5 days after fever. Severe dengue can cause bleeding, organ damage. Drink plenty of fluids, take paracetamol (NOT aspirin), and consult doctor immediately if symptoms appear.',
        'category': 'symptoms',
        'disease': 'Dengue'
    },
    {
        'question': 'How to prevent dengue',
        'answer': 'Dengue prevention: Use mosquito repellent, wear long-sleeved clothes, use mosquito nets, eliminate standing water around home, keep water containers covered, use window screens. Mosquitoes that spread dengue bite during daytime. Community effort in keeping surroundings clean is important.',
        'category': 'prevention',
        'disease': 'Dengue'
    },
    {
        'question': 'What are dengue symptoms',
        'answer': 'Dengue symptoms include: high fever (104°F), severe headache, pain behind eyes, joint and muscle pain, nausea, vomiting, skin rash appearing 2-5 days after fever. Severe dengue can cause bleeding, organ damage. Drink plenty of fluids, take paracetamol (NOT aspirin), and consult doctor immediately if symptoms appear.',
        'category': 'symptoms',
        'disease': 'Dengue'
    },
    {
        'question': 'How to prevent dengue',
        'answer': 'Dengue prevention: Use mosquito repellent, wear long-sleeved clothes, use mosquito nets, eliminate standing water around home, keep water containers covered, use window screens. Mosquitoes that spread dengue bite during daytime. Community effort in keeping surroundings clean is important.',
        'category': 'prevention',
        'disease': 'Dengue'
    },

    # Malaria
    {
        'question': 'I have fever with chills',
        'answer': 'Fever with chills can indicate malaria, dengue, or severe infection. Other symptoms to watch: sweating, headache, body ache, nausea. Get blood test done immediately to confirm. Take prescribed antimalarial medication if positive. Prevent mosquito bites, use nets, and keep surroundings clean.',
        'category': 'symptoms',
        'disease': 'Malaria'
    },
    {
        'question': 'Malaria prevention tips',
        'answer': 'Malaria prevention: Sleep under mosquito nets, use insect repellent, wear protective clothing, take antimalarial tablets if traveling to endemic areas, eliminate mosquito breeding sites, use mosquito coils/vaporizers. Mosquitoes bite during night time. Get immediate treatment if fever develops.',
        'category': 'prevention',
        'disease': 'Malaria'
    },

    # Typhoid
    {
        'question': 'Symptoms of typhoid fever',
        'answer': 'Typhoid symptoms: Prolonged high fever (103-104°F), weakness, stomach pain, headache, loss of appetite, constipation or diarrhea, rash on chest. Fever gradually increases over several days. Get blood test (Widal test) done. Take complete antibiotic course as prescribed. Maintain hygiene and drink clean water.',
        'category': 'symptoms',
        'disease': 'Typhoid'
    },
    {
        'question': 'How to prevent typhoid',
        'answer': 'Typhoid prevention: Drink only boiled or filtered water, eat freshly cooked hot food, avoid street food and raw vegetables, wash hands before eating, get typhoid vaccination, maintain good hygiene, avoid ice and ice cream from unknown sources. Wash fruits and vegetables properly.',
        'category': 'prevention',
        'disease': 'Typhoid'
    },

    # Jaundice
    {
        'question': 'My eyes are yellow',
        'answer': 'Yellow eyes (jaundice) indicate liver problem or hepatitis. Other symptoms: yellow skin, dark urine, pale stools, tiredness, abdominal pain. Stop all medications, avoid alcohol completely, drink plenty of water, eat light diet. Get liver function test done immediately and consult doctor. Jaundice needs proper medical treatment.',
        'category': 'symptoms',
        'disease': 'Jaundice'
    },
    {
        'question': 'Diet for jaundice patient',
        'answer': 'Jaundice diet: Drink plenty of water and fresh fruit juices, eat easily digestible foods like rice, dal, vegetables, avoid oily and spicy foods, avoid alcohol completely, eat small frequent meals, include sugarcane juice, fruits like papaya and banana. Avoid red meat and processed foods. Rest is important.',
        'category': 'treatment',
        'disease': 'Jaundice'
    },

    # Tuberculosis (TB)
    {
        'question': 'What are TB symptoms',
        'answer': 'TB symptoms include: persistent cough for more than 3 weeks, coughing up blood or sputum, chest pain, fever (especially evening), night sweats, weight loss, loss of appetite, fatigue. TB is curable with 6-9 months of medication. Get sputum test done if symptoms present. TB treatment is FREE in government hospitals.',
        'category': 'information',
        'disease': 'Tuberculosis'
    },
    {
        'question': 'Is TB contagious',
        'answer': 'Yes, TB is contagious and spreads through air when infected person coughs or sneezes. However, it is curable with proper treatment. TB patients should: cover mouth while coughing, take complete medication course (6-9 months), avoid crowded places initially, ensure good ventilation at home. Family members should get tested. TB treatment is free in India.',
        'category': 'information',
        'disease': 'Tuberculosis'
    },

    # Thyroid Issues
    {
        'question': 'Symptoms of thyroid problem',
        'answer': 'Thyroid symptoms vary: Hyperthyroid - weight loss, rapid heartbeat, nervousness, sweating, tremors. Hypothyroid - weight gain, fatigue, cold sensitivity, constipation, dry skin, hair loss. Get TSH blood test done for diagnosis. Thyroid disorders need lifelong medication but are easily manageable with proper treatment.',
        'category': 'information',
        'disease': 'Thyroid'
    },
    {
        'question': 'Diet for thyroid patients',
        'answer': 'Thyroid diet tips: Include iodized salt, seafood, eggs, dairy products. For hypothyroid: eat selenium-rich foods (brazil nuts, fish), avoid excessive cabbage/cauliflower. For hyperthyroid: limit iodine intake. Maintain regular meal times, exercise regularly, take thyroid medication on empty stomach. Regular checkups important.',
        'category': 'treatment',
        'disease': 'Thyroid'
    },

    # Kidney Stones
    {
        'question': 'I have severe pain in lower back',
        'answer': 'Severe lower back or side pain may indicate kidney stones. Other symptoms: blood in urine, frequent urination, nausea, vomiting. Drink 10-12 glasses of water daily, apply hot compress, take pain relief as prescribed. Small stones pass naturally. If pain is unbearable or fever develops, visit hospital immediately.',
        'category': 'symptoms',
        'disease': 'Kidney Stones'
    },
    {
        'question': 'How to prevent kidney stones',
        'answer': 'Kidney stone prevention: Drink 8-10 glasses of water daily, reduce salt intake, limit animal protein, eat calcium-rich foods with meals, reduce oxalate-rich foods (spinach, nuts), avoid soft drinks, maintain healthy weight, exercise regularly. Lemon water helps prevent stone formation. Regular health checkups important.',
        'category': 'prevention',
        'disease': 'Kidney Stones'
    },

    # Anemia
    {
        'question': 'I feel tired all the time',
        'answer': 'Constant tiredness can indicate anemia (low hemoglobin), thyroid problem, vitamin deficiency, or other conditions. Other anemia symptoms: pale skin, dizziness, shortness of breath, cold hands and feet. Get CBC blood test done. Eat iron-rich foods (spinach, dates, jaggery), take iron supplements if prescribed. Vitamin C helps iron absorption.',
        'category': 'symptoms',
        'disease': 'Anemia'
    },
    {
        'question': 'Iron rich foods for anemia',
        'answer': 'Iron-rich foods: Green leafy vegetables (spinach, fenugreek), dates, jaggery, pomegranate, beetroot, raisins, meat, fish, eggs, beans, lentils. Include vitamin C foods (citrus fruits, tomatoes) to improve iron absorption. Avoid tea/coffee with meals. Take iron tablets if prescribed. Cook in iron utensils when possible.',
        'category': 'treatment',
        'disease': 'Anemia'
    },

    # Migraine
    {
        'question': 'I get frequent headaches with nausea',
        'answer': 'Frequent headaches with nausea, sensitivity to light and sound suggest migraine. Triggers include: stress, certain foods, lack of sleep, hormonal changes. During attack: rest in dark quiet room, cold compress on forehead, drink water, take prescribed medication early. Identify and avoid triggers. If frequency increases, consult neurologist.',
        'category': 'symptoms',
        'disease': 'Migraine'
    },
    {
        'question': 'How to prevent migraine attacks',
        'answer': 'Migraine prevention: Maintain regular sleep schedule, stay hydrated, eat regular meals, avoid trigger foods (chocolate, cheese, caffeine), manage stress, exercise regularly, maintain headache diary to identify triggers. Limit screen time, practice relaxation techniques. Take preventive medication if prescribed by doctor.',
        'category': 'prevention',
        'disease': 'Migraine'
    },

    # Allergies
    {
        'question': 'I have constant sneezing and runny nose',
        'answer': 'Constant sneezing, runny nose, itchy eyes indicate allergic rhinitis. Common triggers: dust, pollen, pet dander, mold. Treatment: antihistamine tablets, nasal sprays, avoid allergens, keep home clean and dust-free, use air purifiers. If symptoms persist, get allergy test done to identify specific allergens. Seasonal allergies are common.',
        'category': 'symptoms',
        'disease': 'Allergies'
    },
    {
        'question': 'How to manage allergies',
        'answer': 'Allergy management: Identify and avoid triggers, keep home clean, use dust-proof covers on pillows, wash bedding in hot water weekly, avoid pets if allergic, keep windows closed during high pollen season, take antihistamines as needed, use saline nasal rinse. Consider immunotherapy for severe allergies.',
        'category': 'treatment',
        'disease': 'Allergies'
    },

    # Acidity/GERD
    {
        'question': 'I have burning sensation in chest',
        'answer': 'Burning sensation in chest (heartburn) indicates acidity or GERD. Other symptoms: sour taste, difficulty swallowing, burping. Avoid spicy/oily foods, eat small frequent meals, don\'t lie down immediately after eating, elevate head while sleeping, avoid tight clothes, reduce stress. Take antacids if needed. If severe, consult gastroenterologist.',
        'category': 'symptoms',
        'disease': 'Acidity'
    },
    {
        'question': 'Foods to avoid in acidity',
        'answer': 'Avoid in acidity: Spicy foods, citrus fruits, tomatoes, chocolate, coffee, tea, carbonated drinks, alcohol, fried and fatty foods, mint, onions, garlic. Eat: bananas, melons, oatmeal, rice, bread, green vegetables, ginger, fennel. Eat slowly, chew properly, drink water 30 minutes before meals.',
        'category': 'treatment',
        'disease': 'Acidity'
    },

    # Urinary Tract Infection (UTI)
    {
        'question': 'Burning sensation while urinating',
        'answer': 'Burning during urination suggests UTI (urinary tract infection). Other symptoms: frequent urge to urinate, cloudy or bloody urine, lower abdominal pain, fever. Drink plenty of water (8-10 glasses), cranberry juice helps, maintain hygiene. Get urine test done. Complete antibiotic course as prescribed. Women are more prone to UTI.',
        'category': 'symptoms',
        'disease': 'UTI'
    },
    {
        'question': 'How to prevent UTI',
        'answer': 'UTI prevention: Drink plenty of water, urinate frequently, don\'t hold urine, wipe front to back after toilet, urinate after sexual intercourse, avoid tight underwear, maintain genital hygiene, avoid harsh soaps, wear cotton underwear, cranberry juice may help. Women should be especially careful during menstruation.',
        'category': 'prevention',
        'disease': 'UTI'
    },

    # Vitamin D Deficiency
    {
        'question': 'I have bone pain and weakness',
        'answer': 'Bone pain, muscle weakness, fatigue can indicate Vitamin D deficiency. Other symptoms: frequent infections, depression, slow wound healing. Get Vitamin D blood test done. Increase sun exposure (15-20 minutes daily), eat vitamin D rich foods (fish, eggs, fortified milk), take supplements if prescribed. Very common deficiency in India.',
        'category': 'symptoms',
        'disease': 'Vitamin D Deficiency'
    },
    {
        'question': 'Sources of vitamin D',
        'answer': 'Vitamin D sources: Sunlight exposure (15-20 minutes daily before 10 AM or after 4 PM), fatty fish (salmon, mackerel), egg yolks, fortified milk and cereals, mushrooms. Take Vitamin D3 supplements if deficient. Regular blood tests to monitor levels. Vitamin D is crucial for bone health and immunity.',
        'category': 'prevention',
        'disease': 'Vitamin D Deficiency'
    },

    # Anxiety and Stress
    {
        'question': 'I feel anxious and stressed all the time',
        'answer': 'Constant anxiety and stress affect physical and mental health. Symptoms: restlessness, rapid heartbeat, sweating, difficulty concentrating, sleep problems. Practice: deep breathing, meditation, yoga, regular exercise, adequate sleep, healthy diet. Talk to loved ones, consider counseling. If severe, consult psychiatrist. Mental health is as important as physical health.',
        'category': 'symptoms',
        'disease': 'Anxiety'
    },
    {
        'question': 'How to manage stress',
        'answer': 'Stress management: Exercise regularly, practice meditation and yoga, maintain sleep schedule, eat healthy, stay connected with friends and family, pursue hobbies, limit caffeine and alcohol, take breaks from work, practice time management, seek professional help if needed. Deep breathing and mindfulness help immediately.',
        'category': 'treatment',
        'disease': 'Anxiety'
    },

    # Insomnia
    {
        'question': 'I cannot sleep at night',
        'answer': 'Insomnia (sleep problems) can be due to stress, anxiety, poor sleep habits, or medical conditions. Tips: maintain regular sleep schedule, avoid caffeine after 4 PM, reduce screen time before bed, create dark quiet bedroom, avoid heavy meals at night, exercise regularly but not before bed. If persistent, consult doctor.',
        'category': 'symptoms',
        'disease': 'Insomnia'
    },
    {
        'question': 'Tips for better sleep',
        'answer': 'Better sleep tips: Go to bed and wake up at same time daily, avoid daytime naps, limit screen time 1 hour before sleep, keep bedroom cool and dark, avoid caffeine and alcohol, do relaxing activities before bed, don\'t eat heavy meals late, exercise during day, try warm milk or chamomile tea before bed.',
        'category': 'treatment',
        'disease': 'Insomnia'
    },

    # Joint Pain/Arthritis
    {
        'question': 'My joints are painful and stiff',
        'answer': 'Joint pain and stiffness can indicate arthritis, vitamin D deficiency, or injury. Common in: knees, hips, hands. Apply hot/cold compress, gentle exercises, maintain healthy weight, avoid prolonged sitting. Eat: turmeric, ginger, omega-3 rich foods. Take calcium and vitamin D supplements. If severe or progressive, consult orthopedic doctor.',
        'category': 'symptoms',
        'disease': 'Arthritis'
    },
    {
        'question': 'How to prevent joint pain',
        'answer': 'Joint pain prevention: Maintain healthy weight, exercise regularly (walking, swimming), strengthen muscles, avoid repetitive stress, maintain good posture, eat calcium and vitamin D rich foods, stay hydrated, avoid high heels, use proper techniques when lifting heavy objects. Early morning stiffness needs medical evaluation.',
        'category': 'prevention',
        'disease': 'Arthritis'
    },

    # Dehydration
    {
        'question': 'Signs of dehydration',
        'answer': 'Dehydration symptoms: dry mouth and lips, dark yellow urine, dizziness, fatigue, decreased urination, rapid heartbeat, sunken eyes. Severe dehydration is emergency. Treatment: drink water immediately, ORS solution, coconut water, avoid caffeinated drinks. In severe cases with vomiting/diarrhea, may need IV fluids. Prevent by drinking 8-10 glasses water daily.',
        'category': 'symptoms',
        'disease': 'Dehydration'
    },

    # General Wellness
    {
        'question': 'How much water should I drink daily',
        'answer': 'Drink 8-10 glasses (2-3 liters) of water daily. More if: exercising, hot weather, pregnant/breastfeeding, illness with fever/vomiting. Signs of good hydration: pale yellow urine, no excessive thirst, good energy levels. Increase intake gradually. Include water-rich fruits and vegetables. Don\'t wait until thirsty to drink water.',
        'category': 'prevention',
        'disease': 'General'
    },
    {
        'question': 'Benefits of regular exercise',
        'answer': 'Regular exercise benefits: maintains healthy weight, reduces disease risk (diabetes, heart disease, cancer), improves mental health, strengthens bones and muscles, increases energy, better sleep, improves mood. Aim for 30 minutes daily. Include: walking, jogging, yoga, swimming, cycling. Start slowly and increase gradually. Consult doctor before starting intense exercise.',
        'category': 'prevention',
        'disease': 'General'
    },
    {
        'question': 'Balanced diet components',
        'answer': 'Balanced diet includes: Whole grains (rice, wheat, oats), proteins (dal, legumes, eggs, fish, lean meat), plenty of fruits and vegetables, dairy products, nuts and seeds, healthy fats. Avoid: processed foods, excess sugar and salt, trans fats. Eat at regular times, drink plenty of water, portion control is important.',
        'category': 'prevention',
        'disease': 'General'
    },    
]


# Populate the dataset
for item in qa_pairs:
    medical_data['questions'].append(item['question'])
    medical_data['answers'].append(item['answer'])
    medical_data['category'].append(item['category'])
    medical_data['disease'].append(item['disease'])

# Create DataFrame
df = pd.DataFrame(medical_data)

# Save to CSV
csv_path = os.path.join(BASE_DIR, 'medical_qa.csv')
df.to_csv(csv_path, index=False)

# Save to JSON
json_path = os.path.join(BASE_DIR, 'medical_qa.json')
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(medical_data, f, indent=4, ensure_ascii=False)

print(f"✅ Dataset created successfully with {len(df)} Q&A pairs!")
print(f"📁 Files created:")
print(f"   - {csv_path}")
print(f"   - {json_path}")
print(f"\n📊 Dataset Statistics:")
print(f"   - Total questions: {len(df)}")
print(f"   - Categories: {df['category'].nunique()}")
print(f"   - Diseases covered: {df['disease'].nunique()}")
print(f"\n🏥 Categories breakdown:")
print(df['category'].value_counts())

# Disease information dataset
diseases_info = [
    {
        'name': 'Fever',
        'description': 'Elevated body temperature, usually due to infection or illness',
        'symptoms': 'High temperature, body ache, chills, sweating, weakness',
        'precautions': 'Rest, hydration, paracetamol, monitor temperature',
        'severity': 'medium'
    },
    {
        'name': 'Cold',
        'description': 'Viral infection of upper respiratory tract',
        'symptoms': 'Runny nose, sneezing, sore throat, cough, congestion',
        'precautions': 'Rest, warm fluids, steam inhalation, avoid cold exposure',
        'severity': 'low'
    },
    {
        'name': 'Cough',
        'description': 'Reflex action to clear airways',
        'symptoms': 'Persistent coughing, throat irritation, phlegm',
        'precautions': 'Warm water, honey, steam, avoid irritants',
        'severity': 'low'
    },
    {
        'name': 'Diabetes',
        'description': 'Chronic condition affecting blood sugar regulation',
        'symptoms': 'Frequent urination, excessive thirst, weight loss, blurred vision',
        'precautions': 'Regular monitoring, medication, diet control, exercise',
        'severity': 'high'
    },
    {
        'name': 'Hypertension',
        'description': 'Persistently elevated blood pressure',
        'symptoms': 'Headache, shortness of breath, nosebleeds (in severe cases)',
        'precautions': 'Low salt diet, regular exercise, medication, stress management',
        'severity': 'high'
    },
    {
        'name': 'Asthma',
        'description': 'Chronic respiratory condition causing breathing difficulty',
        'symptoms': 'Wheezing, shortness of breath, chest tightness, coughing',
        'precautions': 'Avoid triggers, use inhaler, clean environment, regular checkups',
        'severity': 'high'
    },
    {
        'name': 'Gastroenteritis',
        'description': 'Inflammation of digestive tract',
        'symptoms': 'Stomach pain, diarrhea, nausea, vomiting',
        'precautions': 'Hydration (ORS), bland diet, rest, hygiene',
        'severity': 'medium'
    },
    {
        'name': 'Headache',
        'description': 'Pain in head or upper neck',
        'symptoms': 'Head pain, sensitivity to light, nausea',
        'precautions': 'Rest, hydration, pain relief, identify triggers',
        'severity': 'low'
    },
]

diseases_df = pd.DataFrame(diseases_info)
diseases_csv_path = os.path.join(BASE_DIR, 'diseases.csv')
diseases_df.to_csv(diseases_csv_path, index=False)

print(f"\n✅ Disease information dataset created with {len(diseases_df)} diseases!")
print(f"📁 File created: {diseases_csv_path}")