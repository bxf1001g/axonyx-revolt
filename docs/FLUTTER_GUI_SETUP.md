# Axonyx Revolt - Beautiful Flutter GUI Setup

## 🎨 Overview

A modern, frameless Flutter Windows desktop GUI for the Axonyx Revolt agent featuring:
- ✨ Frameless window with custom title bar
- 💬 Beautiful chat interface with message bubbles
- 🎯 Model selection dropdown (Haiku/Sonnet 3.5/Sonnet 4)
- 🔄 Real-time agent communication
- 📊 Tool execution status indicators
- 🎭 Glassmorphism design

## 📁 Project Structure

```
axonyx_gui/
├── lib/
│   ├── main.dart              # App entry point
│   ├── theme/
│   │   └── app_theme.dart     # Dark theme with modern colors
│   ├── models/
│   │   ├── message.dart       # Message & ToolCall models
│   │   └── agent_response.dart # API response model
│   ├── providers/
│   │   └── agent_provider.dart # State management
│   ├── screens/
│   │   └── chat_screen.dart   # Main chat interface
│   └── widgets/
│       ├── custom_title_bar.dart  # Frameless window controls
│       ├── model_selector.dart    # Model dropdown
│       ├── message_bubble.dart    # Chat message UI
│       └── message_input.dart     # Input field & send button
├── assets/
│   ├── images/
│   └── icons/
├── pubspec.yaml               # Flutter dependencies
└── windows/                   # Windows-specific config
```

## 🚀 Installation Steps

### 1. Prerequisites

#### Flutter SDK (Windows)
```powershell
# Download Flutter from: https://flutter.dev/docs/get-started/install/windows
# Or use winget:
winget install --id=Flutter.Flutter -e

# Add to PATH:
# C:\flutter\bin

# Verify installation:
flutter doctor
```

#### Visual Studio 2022 (for Windows desktop)
- Download: https://visualstudio.microsoft.com/downloads/
- Install "Desktop development with C++" workload

### 2. Install Python Dependencies (Backend API)

```powershell
cd D:\Git\Axonyx_Revolt
.\.venv\Scripts\Activate.ps1

# Install FastAPI & Uvicorn
pip install fastapi uvicorn[standard]

# Or update from requirements.txt
pip install -r requirements.txt
```

### 3. Setup Flutter Project

```powershell
cd D:\Git\Axonyx_Revolt\axonyx_gui

# Get Flutter dependencies
flutter pub get

# Enable Windows desktop
flutter config --enable-windows-desktop

# Create Windows build files
flutter create --platforms=windows .
```

### 4. Configure Windows Runner

The GUI uses `window_manager` for frameless window. Update `windows/runner/main.cpp`:

```cpp
// Add before CreateAndShowWindow():
window_manager::WindowManager::SetInitialWindowSize(1200, 800);
```

## 🎯 Running the Application

### Step 1: Start the Backend API Server

```powershell
# Terminal 1 - Backend
cd D:\Git\Axonyx_Revolt
.\.venv\Scripts\Activate.ps1
python src/api_server.py
```

You should see:
```
🚀 Starting Axonyx Revolt API Server...
📡 Backend URL: http://localhost:8000
🤖 Model: claude-3-5-haiku-20241022
📚 API Docs: http://localhost:8000/docs
```

### Step 2: Launch Flutter GUI

```powershell
# Terminal 2 - Flutter GUI
cd D:\Git\Axonyx_Revolt\axonyx_gui
flutter run -d windows
```

Or build release:
```powershell
flutter build windows --release
```

Executable location:
```
axonyx_gui\build\windows\runner\Release\axonyx_gui.exe
```

## 🎨 Design Features

### Color Palette
- **Primary**: `#6C63FF` (Purple)
- **Secondary**: `#00D9FF` (Cyan)
- **Background**: `#0F0F1E` (Dark Navy)
- **Surface**: `#1A1A2E` (Cards)
- **User Message**: `#6C63FF` (Purple bubble)
- **Agent Message**: `#1E1E2E` (Dark bubble)

### Key Components

#### 1. Custom Title Bar
- Drag to move window
- Minimize, Maximize, Close buttons
- Hover effects
- Frameless (no Windows title bar)

#### 2. Sidebar
- App logo & branding
- Model selector dropdown
- Connection status indicator
- Clear chat button

#### 3. Chat Area
- Empty state with suggestions
- Message bubbles (user vs agent)
- Tool execution indicators
- Timestamps
- Scrollable history

#### 4. Message Input
- Multi-line text field
- Gradient send button
- Loading indicator
- Auto-focus after send

## 🔌 API Endpoints

The Flutter app communicates with these endpoints:

### Health Check
```http
GET http://localhost:8000/health
Response: {"status": "ok", "model": "...", "api_key_set": true}
```

### Execute Task
```http
POST http://localhost:8000/execute
Body: {"task": "Open Chrome", "model": "claude-3-5-haiku-20241022"}
Response: {
  "final_response": "Opened Chrome successfully",
  "success": true,
  "tool_calls": [...],
  "iterations": 3
}
```

### Change Model
```http
POST http://localhost:8000/set-model
Body: {"model": "claude-3-5-sonnet-20241022"}
Response: {"success": true, "model": "...", "message": "..."}
```

### Get Available Models
```http
GET http://localhost:8000/models
Response: {"models": [...], "current": "..."}
```

### Get Available Tools
```http
GET http://localhost:8000/tools
Response: {"tools": [...], "count": 74}
```

## 🐛 Troubleshooting

### Flutter Issues

**"flutter command not found"**
```powershell
# Add to PATH:
$env:Path += ";C:\flutter\bin"
# Or permanently add to System Environment Variables
```

**"Visual Studio required"**
```powershell
# Install Visual Studio 2022 with C++ desktop development
# Or use Visual Studio Build Tools
```

**"Windows desktop not enabled"**
```powershell
flutter config --enable-windows-desktop
flutter doctor  # Verify Windows is available
```

### Backend Issues

**"Connection refused" / Red status indicator**
```powershell
# Make sure backend is running:
python src/api_server.py

# Check if port 8000 is in use:
netstat -ano | findstr :8000
```

**"ANTHROPIC_API_KEY not set"**
```powershell
# Verify .env file:
cat .env | Select-String "ANTHROPIC_API_KEY"
```

### GUI Issues

**Blank screen**
- Check browser console (F12 in Flutter DevTools)
- Verify backend is running
- Check network tab for failed API calls

**Window doesn't move**
- `window_manager` needs to be initialized
- Check `main.dart` has proper window setup

**Models not loading**
- Check `/models` endpoint manually: http://localhost:8000/models
- Verify provider is initialized

## 🎯 Development Workflow

### Hot Reload (Flutter)
```powershell
# While flutter run is active:
# Press 'r' for hot reload
# Press 'R' for hot restart
# Press 'q' to quit
```

### Watch Mode (Backend)
```powershell
# Install uvicorn with reload:
pip install uvicorn[standard]

# Run with auto-reload:
uvicorn src.api_server:app --reload --port 8000
```

## 📦 Building for Distribution

### Create Standalone Executable

```powershell
cd D:\Git\Axonyx_Revolt\axonyx_gui

# Build release version
flutter build windows --release

# Executable location:
# build\windows\runner\Release\axonyx_gui.exe

# Package with dependencies:
# build\windows\runner\Release\
# ├── axonyx_gui.exe
# ├── flutter_windows.dll
# └── data\
```

### Create Installer (Optional)

Use **Inno Setup** or **NSIS**:

```iss
; Inno Setup script
[Setup]
AppName=Axonyx Revolt
AppVersion=1.0.0
DefaultDirName={pf}\Axonyx Revolt
DefaultGroupName=Axonyx Revolt
OutputDir=installer
OutputBaseFilename=AxonyxRevolt_Setup

[Files]
Source: "build\windows\runner\Release\*"; DestDir: "{app}"; Flags: recursesubdirs
```

## 🔥 Advanced Features

### Add Custom Themes
Edit `lib/theme/app_theme.dart`:
```dart
static const primaryColor = Color(0xFFYOURCOLOR);
```

### Add More Screens
1. Create file in `lib/screens/`
2. Add route in `main.dart`
3. Navigate using `Navigator.push()`

### WebSocket Support (Real-time)
Instead of HTTP polling, use WebSocket:
```dart
import 'package:web_socket_channel/web_socket_channel.dart';

final channel = WebSocketChannel.connect(
  Uri.parse('ws://localhost:8000/ws'),
);
```

Backend (FastAPI):
```python
from fastapi import WebSocket

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    # Handle messages
```

## 📚 Resources

- **Flutter Windows**: https://docs.flutter.dev/desktop
- **FastAPI**: https://fastapi.tiangolo.com/
- **window_manager**: https://pub.dev/packages/window_manager
- **Provider**: https://pub.dev/packages/provider
- **Google Fonts**: https://pub.dev/packages/google_fonts

## 🎉 Success!

You now have a beautiful, modern Flutter GUI for your Windows agent!

Test it:
1. Start backend: `python src/api_server.py`
2. Start GUI: `flutter run -d windows`
3. Type: "Take a screenshot of my desktop"
4. Watch the magic happen! ✨
