# ⚡ Axonyx Revolt GUI - Quick Reference Card

## 🚀 Launch Commands

```powershell
# Quick Start (Recommended)
.\launch_gui.ps1 -Both

# Backend Only
python src/api_server.py

# GUI Only
cd axonyx_gui; flutter run -d windows
```

---

## 📁 Key Files

| File | Purpose |
|------|---------|
| `lib/main.dart` | App entry, window config |
| `lib/theme/app_theme.dart` | Colors & styling |
| `lib/screens/chat_screen.dart` | Main chat UI |
| `lib/providers/agent_provider.dart` | State management |
| `src/api_server.py` | Backend REST API |

---

## 🎨 Color Codes

```dart
Primary:    #6C63FF  // Purple
Secondary:  #00D9FF  // Cyan
Background: #0F0F1E  // Dark Navy
Surface:    #1A1A2E  // Cards
Success:    #00D97E  // Green
Error:      #FF6B6B  // Red
```

---

## 🔌 API Endpoints

```http
GET  /health         # Check status
POST /execute        # Run task
POST /set-model      # Change model
GET  /models         # List models
GET  /tools          # List tools (74)
```

**Base URL:** `http://localhost:8000`

---

## 🛠️ Common Tasks

### Change Colors
Edit `lib/theme/app_theme.dart`:
```dart
static const primaryColor = Color(0xFFYOURCOLOR);
```

### Add New Widget
1. Create file in `lib/widgets/`
2. Import in screen
3. Use widget in build method

### Modify API
Edit `src/api_server.py`:
```python
@app.post("/your-endpoint")
async def your_function():
    # Your code
```

### Build Release
```powershell
cd axonyx_gui
flutter build windows --release
# Output: build\windows\runner\Release\axonyx_gui.exe
```

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| Backend not connecting | `python src/api_server.py` |
| Flutter errors | `flutter clean && flutter pub get` |
| Window doesn't show | Check `window_manager` in `main.dart` |
| Port 8000 in use | `netstat -ano \| findstr :8000` |

---

## 📦 Dependencies

**Flutter:** window_manager, provider, http, google_fonts  
**Python:** fastapi, uvicorn, anthropic, pywinauto

---

## 🎯 File Structure

```
axonyx_gui/
├── lib/
│   ├── main.dart
│   ├── theme/app_theme.dart
│   ├── models/*.dart
│   ├── providers/agent_provider.dart
│   ├── screens/chat_screen.dart
│   └── widgets/*.dart
├── pubspec.yaml
└── README.md

src/api_server.py  # Backend
```

---

## ⌨️ Keyboard Shortcuts (Future)

```
Ctrl+N     New conversation
Ctrl+L     Clear chat
Ctrl+,     Settings
Enter      Send message
Esc        Cancel/Close
```

---

## 📚 Documentation

- Setup: `docs/FLUTTER_GUI_SETUP.md`
- Visual: `docs/GUI_VISUAL_GUIDE.md`
- Summary: `docs/GUI_SUMMARY.md`
- API Docs: http://localhost:8000/docs

---

## 🎉 Quick Tips

1. Use `launch_gui.ps1 -Both` for fastest start
2. Keep backend running in separate terminal
3. Press 'r' in Flutter for hot reload
4. Check connection indicator (green/red)
5. View API docs while backend running

---

**Made with ❤️ using Flutter + FastAPI + Claude** ✨
