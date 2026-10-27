# 🚀 Quick Start Guide - Deaf-Mute Communication System

## ✅ Setup Complete!

Your VS Code workspace is now configured to run the application without any chatbot interruptions.

---

## 🎯 How to Run (Choose One Method)

### **Method 1: VS Code Tasks (Easiest)**
1. Press `Ctrl+Shift+B` or go to Terminal → Run Task
2. Select **"🚀 Start Deaf-Mute App"**
3. The application will start in the integrated terminal

### **Method 2: VS Code Debugger**
1. Press `Ctrl+Shift+D` (Run & Debug)
2. Select **"🐍 Python: Run App"** from dropdown
3. Press F5 or click the Play button

### **Method 3: Direct Terminal Command**
```powershell
py -3.11 run_app.py
```

---

## 📍 Application Endpoints

Once running, you can access:

- **Desktop GUI**: Automatically opens in a window
- **Web Interface**: http://localhost:5000
- **Server Port**: localhost:5555

---

## 🧪 Other Available Tasks

### Test Gesture Classifier
```
Ctrl+Shift+P → Run Task → "🧪 Test Gesture Classifier"
```

### Test Multi-Language Support
```
Ctrl+Shift+P → Run Task → "🧪 Test Multi-Language"
```

### Reinstall Dependencies
```
Ctrl+Shift+P → Run Task → "📦 Install Dependencies"
```

---

## 🛑 Stopping the Application

Press `Ctrl+C` in the terminal to gracefully shut down all services.

---

## 📁 Files Created

- **`run_app.py`** - Python launcher script (no batch file issues)
- **`.vscode/tasks.json`** - VS Code task definitions
- **`.vscode/launch.json`** - Debug configurations
- **`.vscode/settings.json`** - Workspace Python settings
- **`.vscode/extensions.json`** - Recommended extensions

---

## ⚙️ Configuration Details

- **Python Version**: 3.11
- **TensorFlow Logging**: Minimized (quieter startup)
- **Terminal**: Integrated VS Code terminal
- **All Services Start Automatically**

---

## 🐛 Troubleshooting

**Issue**: Port already in use
- Change port in `src/server.py` and `src/web_bridge.py`

**Issue**: Module not found
- Run: `Ctrl+Shift+P → Run Task → "📦 Install Dependencies"`

**Issue**: Webcam not detected
- Ensure camera permissions are granted in Windows Settings

---

Enjoy using the Deaf-Mute Communication System! 🎉
