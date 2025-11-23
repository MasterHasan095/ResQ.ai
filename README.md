# 🚨 ResQ.ai

Real-time fall detection system using YOLO-Pose, FastAPI, and Flutter. If a fall is detected and the user doesn’t respond within 30 seconds, the system alerts emergency contacts through SMS and automated phone calls.

## ⭐ Features
- 🔍 Real-time fall detection  
- ⏱️ 30-second cancellation timer  
- 📩 Automatic SMS alerts  
- 📞 Automated phone calls  
- 📱 Flutter mobile app  
- ⚙️ FastAPI backend  
- 🗄️ MongoDB database  

## 🧰 Built With
Ultralytics, OpenCV-Python, NumPy, FastAPI, Uvicorn, Pydantic, python-multipart, WebSockets, Twilio, Python, Dart, Flutter, MongoDB


## 🚀 Getting Started

Clone the repo:
git clone https://github.com/MasterHasan095/ResQ.ai.git


Backend setup:

cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload


Flutter app:

cd flutter_app
flutter pub get
flutter run


## 🔗 System Flow
Camera → YOLO Pose → Fall Logic → FastAPI → Flutter App → Emergency Contacts
