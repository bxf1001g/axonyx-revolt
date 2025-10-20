# Axonyx Revolt - Flutter GUI

<div align="center">

![Axonyx Revolt](https://img.shields.io/badge/Axonyx-Revolt-6C63FF?style=for-the-badge)
![Flutter](https://img.shields.io/badge/Flutter-3.0+-02569B?style=for-the-badge&logo=flutter)
![Windows](https://img.shields.io/badge/Windows-11-0078D6?style=for-the-badge&logo=windows)
![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python)

**Beautiful, Modern, Frameless Desktop GUI for Windows Agent**

[Features](#-features) • [Installation](#-quick-start) • [Screenshots](#-screenshots) • [Documentation](#-documentation)

</div>

---

## ✨ Features

### 🎨 **Modern Design**
- Frameless window with custom title bar
- Dark theme with gradient accents
- Glassmorphism effects
- Smooth animations

### 💬 **Chat Interface**
- Beautiful message bubbles
- User vs Agent distinction
- Tool execution indicators
- Timestamp display
- Auto-scroll to latest message

### 🎯 **Model Selection**
- Switch between Claude models on-the-fly
- Haiku 3.5 (Fast & Cheap ⚡)
- Sonnet 3.5 (Balanced 🎯)
- Sonnet 4 (Most Powerful 🚀)

### 📊 **Real-time Status**
- Connection indicator (green/red)
- Loading animations
- Tool call success/failure badges
- System messages

### 🔧 **Window Controls**
- Drag to move
- Minimize, Maximize, Close
- Hover effects
- Responsive design

---

## 🚀 Quick Start

### **Option 1: Automated Setup (Recommended)**

```powershell
# Run setup script
.\setup_gui.ps1

# Launch application
.\launch_gui.ps1 -Both
```

### **Option 2: Manual Setup**

#### 1. Install Flutter
```powershell
winget install --id=Flutter.Flutter -e
# Or download from: https://flutter.dev/
```

#### 2. Install Python Dependencies
```powershell
.\.venv\Scripts\Activate.ps1
pip install fastapi uvicorn[standard]
```

#### 3. Setup Flutter Project
```powershell
cd axonyx_gui
flutter pub get
flutter config --enable-windows-desktop
flutter create --platforms=windows .
```

#### 4. Run Application

**Terminal 1 - Backend:**
```powershell
python src/api_server.py
```

**Terminal 2 - GUI:**
```powershell
cd axonyx_gui
flutter run -d windows
```

---

## 📸 Screenshots

### Main Chat Interface
```
┌─────────────────────────────────────────────────────────────┐
│  ⚡ Axonyx Revolt                              [ - ] [ □ ] [ X ] │
├──────────────┬──────────────────────────────────────────────┤
│  🎯 Axonyx   │  💬 Chat Area                                │
│  Revolt Agent│                                              │
│──────────────│  Empty State:                                │
│              │  🤖 Welcome to Axonyx Revolt                 │
│ Model:       │     Ask me to automate Windows tasks         │
│ [Haiku 3.5 ▼]│                                              │
│              │  Suggestions:                                │
│──────────────│  [Open Chrome] [Screenshot] [List Apps]      │
│              │                                              │
│ 🟢 Connected │  After Messages:                             │
│ [Refresh]    │  👤 User: "Take a screenshot"                │
│              │  🤖 Agent: "Screenshot saved to Desktop"     │
│──────────────│       ✅ take_screenshot                      │
│              │       ✅ get_desktop_path                     │
│  [Clear Chat]│                                              │
└──────────────┴──────────────────────────────────────────────┘
│  [Type your message...]                         [Send 🚀]   │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎨 Design Specifications

### Color Palette
| Color | Hex | Usage |
|-------|-----|-------|
| Primary Purple | `#6C63FF` | Buttons, User messages |
| Secondary Cyan | `#00D9FF` | Accents, Gradients |
| Background | `#0F0F1E` | Main background |
| Surface | `#1A1A2E` | Sidebar, Cards |
| Text Primary | `#FFFFFF` | Main text |
| Text Secondary | `#B0B3B8` | Descriptions |
| Success | `#00D97E` | Success indicators |
| Error | `#FF6B6B` | Error messages |

### Typography
- **Font Family**: Inter (Google Fonts)
- **Heading**: 20-32px, Bold (700)
- **Body**: 14-16px, Regular (400)
- **Small**: 11-12px, Regular (400)

### Layout
- **Window Size**: 1200x800 (default)
- **Minimum Size**: 800x600
- **Sidebar Width**: 280px
- **Border Radius**: 8-16px
- **Spacing**: 8-24px increments

---

## 🏗️ Architecture

### Frontend (Flutter)
```
lib/
├── main.dart                 # Entry point, window config
├── theme/app_theme.dart      # Dark theme definition
├── models/                   # Data models
│   ├── message.dart          # Message & ToolCall
│   └── agent_response.dart   # API response
├── providers/                # State management (Provider)
│   └── agent_provider.dart   # Agent state & API calls
├── screens/                  # Main screens
│   └── chat_screen.dart      # Chat interface
└── widgets/                  # Reusable components
    ├── custom_title_bar.dart # Window controls
    ├── model_selector.dart   # Model dropdown
    ├── message_bubble.dart   # Chat message
    └── message_input.dart    # Input field
```

### Backend (FastAPI)
```python
src/api_server.py  # REST API exposing agent functionality

Endpoints:
- GET  /health           # Health check
- POST /execute          # Execute task
- POST /set-model        # Change Claude model
- GET  /models           # List available models
- GET  /tools            # List available tools
```

### Communication Flow
```
Flutter GUI → HTTP POST → FastAPI → WindowsAgent → Claude API
                                     ↓
                                  Tool Execution
                                     ↓
                                  Tool Results
                                     ↓
         Response ← JSON ← AgentResponse ← Final Response
```

---

## 🔌 API Reference

### Execute Task
```http
POST http://localhost:8000/execute
Content-Type: application/json

{
  "task": "Open Chrome and go to Python.org",
  "model": "claude-3-5-haiku-20241022"
}
```

**Response:**
```json
{
  "final_response": "Opened Chrome and navigated to Python.org",
  "success": true,
  "tool_calls": [
    {
      "name": "start_browser",
      "input": {},
      "result": {"success": true},
      "success": true
    },
    {
      "name": "navigate_to_url",
      "input": {"url": "https://python.org"},
      "result": {"success": true},
      "success": true
    }
  ],
  "iterations": 2
}
```

### Change Model
```http
POST http://localhost:8000/set-model
Content-Type: application/json

{
  "model": "claude-3-5-sonnet-20241022"
}
```

**Response:**
```json
{
  "success": true,
  "model": "claude-3-5-sonnet-20241022",
  "message": "Model changed to claude-3-5-sonnet-20241022"
}
```

---

## 🛠️ Development

### Hot Reload (Flutter)
```powershell
flutter run -d windows
# Press 'r' for hot reload
# Press 'R' for hot restart
# Press 'q' to quit
```

### Backend Auto-Reload
```powershell
uvicorn src.api_server:app --reload --port 8000
```

### Build Release
```powershell
cd axonyx_gui
flutter build windows --release

# Executable location:
# build\windows\runner\Release\axonyx_gui.exe
```

---

## 📦 Distribution

### Standalone Executable
The release build includes all dependencies:
```
build\windows\runner\Release\
├── axonyx_gui.exe          # Main executable
├── flutter_windows.dll      # Flutter runtime
└── data\                    # Assets & ICU data
```

### Create Installer (Inno Setup)
```iss
[Setup]
AppName=Axonyx Revolt
AppVersion=1.0.0
DefaultDirName={pf}\Axonyx Revolt
OutputDir=installer
OutputBaseFilename=AxonyxRevolt_Setup

[Files]
Source: "build\windows\runner\Release\*"; DestDir: "{app}"; Flags: recursesubdirs

[Icons]
Name: "{group}\Axonyx Revolt"; Filename: "{app}\axonyx_gui.exe"
```

---

## 🐛 Troubleshooting

### Backend Not Connecting
```powershell
# Check if backend is running:
curl http://localhost:8000/health

# Check port usage:
netstat -ano | findstr :8000

# Restart backend:
python src/api_server.py
```

### Flutter Issues
```powershell
# Clean and rebuild:
flutter clean
flutter pub get
flutter run -d windows

# Check Flutter doctor:
flutter doctor -v
```

### Window Manager Issues
```powershell
# If window doesn't appear:
# 1. Check lib/main.dart has proper window config
# 2. Verify window_manager package installed
# 3. Try debug mode: flutter run -d windows --debug
```

---

## 📚 Documentation

- **[Complete Setup Guide](docs/FLUTTER_GUI_SETUP.md)** - Detailed installation
- **[API Documentation](http://localhost:8000/docs)** - Interactive API docs (when backend running)
- **[Flutter Windows Docs](https://docs.flutter.dev/desktop)** - Official Flutter docs
- **[FastAPI Docs](https://fastapi.tiangolo.com/)** - FastAPI documentation

---

## 🎯 Roadmap

### v1.1 (Planned)
- [ ] Settings panel
- [ ] Conversation history persistence
- [ ] Export chat to file
- [ ] Custom themes
- [ ] Keyboard shortcuts

### v1.2 (Future)
- [ ] WebSocket support (real-time)
- [ ] Voice input
- [ ] Tool confirmation dialogs
- [ ] Screenshot preview
- [ ] System tray integration

---

## 🤝 Contributing

Contributions welcome! Areas to improve:
- UI/UX enhancements
- New widgets
- Performance optimizations
- Bug fixes
- Documentation

---

## 📄 License

MIT License - See LICENSE file for details

---

## 🙏 Acknowledgments

- **Flutter Team** - Amazing cross-platform framework
- **FastAPI** - Modern Python web framework
- **Claude AI** - Powerful language model
- **Community** - For feedback and support

---

<div align="center">

**Made with ❤️ by the Axonyx Team**

[![GitHub](https://img.shields.io/badge/GitHub-Repository-181717?style=for-the-badge&logo=github)](https://github.com/yourusername/axonyx_revolt)

</div>
