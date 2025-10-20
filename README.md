# 🤖 Axonyx Revolt - Windows 11 Agentic AI Automation

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Flutter 3.35+](https://img.shields.io/badge/flutter-3.35+-blue.svg)](https://flutter.dev/)
[![Claude API](https://img.shields.io/badge/Claude-Anthropic-orange.svg)](https://www.anthropic.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Intelligent Windows automation agent powered by Claude AI with beautiful Flutter GUI**

Transform natural language commands into Windows actions: install apps, automate tasks, browse the web, download images, and control your desktop—all through an elegant chat interface.

![Axonyx Revolt](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)

---

## 🎯 **What Can It Do?**

### 🚀 Application Management
- **Install applications** from downloads folder with intelligent automation
- **Check installed software** and versions
- **Uninstall applications** by name
- **Launch and control apps** with UI automation

### 🌐 Web Automation
- **Browser control** with native Chrome profile support
- **Google Images search & download** - bulk image downloads
- **Form filling** and web navigation
- **Download monitoring** with OneDrive compatibility

### 🖥️ System Control
- **File operations** - create, move, copy, search files
- **Process management** - kill, list, monitor processes
- **System info** - hardware details, disk space, network
- **Desktop automation** - keyboard/mouse control, screenshots

### 🔧 Advanced Features
- **OCR text extraction** with Tesseract
- **Installer automation** - Python, Chrome, etc with V2 robust detection
- **Cross-PC compatibility** - OneDrive path handling
- **77 automation tools** available through Claude API

---

## 📸 **Screenshots**

### Flutter GUI
- 🎨 **Frameless modern design** with purple/cyan gradient theme
- 💬 **Chat interface** with message history
- 🔧 **Tool execution tracking** with success/error badges
- 🎛️ **Model selection** - Switch between Haiku, Sonnet, Opus
- 🟢 **Live connection status** indicator

---

## ⚡ **Quick Start**

### **Prerequisites**

#### 1️⃣ **Python 3.12+**
```powershell
# Check Python version
python --version  # Should be 3.12 or higher

# If not installed, download from:
# https://www.python.org/downloads/
```

#### 2️⃣ **Flutter 3.35+** (for GUI)
```powershell
# Check Flutter version
flutter --version  # Should be 3.35.3 or higher

# If not installed:
# 1. Download Flutter SDK: https://docs.flutter.dev/get-started/install/windows
# 2. Extract to C:\flutter
# 3. Add to PATH: C:\flutter\bin
# 4. Run: flutter doctor
```

#### 3️⃣ **Anthropic API Key**
Get your API key from [Anthropic Console](https://console.anthropic.com/)

---

### **Installation**

#### **Option 1: Automated Setup (Recommended)**
```powershell
# Clone the repository
git clone https://github.com/YOUR_USERNAME/axonyx-revolt.git
cd axonyx-revolt

# Run automated setup
.\start.ps1
```

This automatically:
- ✅ Creates Python virtual environment
- ✅ Installs Python dependencies
- ✅ Creates `.env` file from template
- ✅ Launches the CLI agent

#### **Option 2: Manual Setup**
```powershell
# 1. Clone repository
git clone https://github.com/YOUR_USERNAME/axonyx-revolt.git
cd axonyx-revolt

# 2. Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Setup environment
Copy-Item .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

# 5. Run CLI agent
python src/main.py
```

---

### **🎨 Launch Flutter GUI**

#### **First Time Setup**
```powershell
# Run automated GUI setup
.\setup_gui.ps1
```

This will:
- ✅ Verify Flutter installation
- ✅ Check Python virtual environment
- ✅ Install FastAPI and Uvicorn
- ✅ Download Flutter dependencies
- ✅ Enable Windows desktop support
- ✅ Create Windows runner files

#### **Launch GUI & Backend**
```powershell
# Option 1: Launch both (Recommended)
.\launch_gui.ps1 -Both

# Option 2: Launch backend only
.\launch_gui.ps1 -Backend

# Option 3: Launch GUI only (backend must be running)
.\launch_gui.ps1 -GUI
```

The GUI will open at **1200x800** frameless window with:
- Dark theme with purple/cyan gradients
- Chat interface with message bubbles
- Model selector dropdown
- Tool execution badges
- Live backend connection indicator

---

## 📋 **Configuration**

### **Environment Variables (.env)**

```ini
# Required
ANTHROPIC_API_KEY=sk-ant-api03-your-key-here

# Model Selection (choose one)
CLAUDE_MODEL=claude-3-5-haiku-20241022  # Fast & Cheap (Recommended)
# CLAUDE_MODEL=claude-3-7-sonnet-20250219  # Balanced
# CLAUDE_MODEL=claude-opus-4-20250514     # Most Powerful

# Optional Settings
REQUIRE_CONFIRMATION=false  # GUI mode doesn't need confirmation
MAX_ITERATIONS=10
DRY_RUN_MODE=false
```

### **Model Comparison**

| Model | Cost (Input/Output) | Speed | Best For |
|-------|---------------------|-------|----------|
| **Haiku 3.5** | $0.80 / $4 per MTok | ⚡⚡⚡ Fastest | Automation, quick tasks |
| **Sonnet 3.7** | $3 / $15 per MTok | ⚡⚡ Fast | Complex reasoning |
| **Opus 4** | $15 / $75 per MTok | ⚡ Moderate | Most difficult tasks |

**💡 Recommendation**: Start with **Haiku 3.5** for automation tasks.

---

## 🛠️ **Project Structure**

```
axonyx-revolt/
├── src/
│   ├── agent.py              # Core agent with 77 tools
│   ├── api_server.py         # FastAPI backend for GUI
│   ├── main.py               # CLI interface
│   └── tools/                # Automation tool modules
│       ├── file_ops.py       # File operations (8 tools)
│       ├── process_ops.py    # Process management (6 tools)
│       ├── ui_automation.py  # Desktop automation (10 tools)
│       ├── browser_automation.py  # Web control (12 tools)
│       ├── chrome_launcher.py     # Native Chrome (2 tools)
│       ├── image_downloader.py    # Image downloads (3 tools)
│       ├── screen_reader.py       # OCR tools (6 tools)
│       ├── installer_automation.py     # Basic installers (5 tools)
│       ├── installer_automation_v2.py  # Robust installers (5 tools)
│       ├── download_manager.py    # Download tracking (4 tools)
│       ├── app_installation.py    # App management (5 tools)
│       ├── app_control.py         # App control (4 tools)
│       ├── system_info.py         # System info (4 tools)
│       └── system_settings.py     # Settings control (3 tools)
├── axonyx_gui/               # Flutter Windows GUI
│   ├── lib/
│   │   ├── main.dart         # App entry point
│   │   ├── theme/            # Dark theme with gradients
│   │   ├── models/           # Data models
│   │   ├── providers/        # State management
│   │   ├── screens/          # Chat screen
│   │   └── widgets/          # Reusable UI components
│   └── windows/              # Windows desktop runner
├── docs/                     # Comprehensive documentation
├── examples/                 # Usage examples
├── requirements.txt          # Python dependencies
├── .env.example              # Environment template
├── setup_gui.ps1            # GUI setup script
├── launch_gui.ps1           # GUI launcher
└── start.ps1                # CLI launcher

**77 Tools Total** across 13 modules
```

---

## 📚 **Usage Examples**

### **CLI Mode**
```powershell
python src/main.py
```

Example commands:
```
> Install Python from my Downloads folder
> Take a screenshot of my desktop
> Open Chrome and search for "AI automation"
> List all running processes using more than 100MB RAM
> Download 10 images of sports cars
> Create a new folder called "Projects" on my Desktop
```

### **GUI Mode**
1. Launch with `.\launch_gui.ps1 -Both`
2. Select model from dropdown (Haiku 3.5 recommended)
3. Type natural language commands in the input field
4. Watch tool execution with badges:
   - ✅ Success
   - ❌ Error
   - 🔄 In progress

---

## 🔧 **Advanced Features**

### **Image Download Tool**
```
Command: "Download 10 images of cars"

Process:
1. Opens Chrome to Google Images
2. Searches for query
3. Clicks thumbnails systematically
4. Downloads full-size images
5. Saves to: Downloads/google_images/cars/

Result: 10 JPG files downloaded
```

### **Installer Automation V2**
Robust multi-strategy installer automation:
- Exact window title matching
- Fallback strategies (4 levels)
- Checkbox detection with multiple methods
- Detailed step-by-step results
- Works with: Python, Chrome, Node.js, Git, etc.

### **OneDrive Desktop Support**
Automatically handles OneDrive-redirected paths:
```
Desktop → C:\Users\USERNAME\OneDrive\Desktop
```

---

## 📖 **Documentation**

### **Setup Guides**
- [GETTING_STARTED.md](./GETTING_STARTED.md) - First-time setup
- [SETUP_GUIDE.md](./SETUP_GUIDE.md) - Detailed installation
- [docs/FLUTTER_GUI_SETUP.md](./docs/FLUTTER_GUI_SETUP.md) - GUI setup guide

### **Feature Guides**
- [MODEL_SELECTION_GUIDE.md](./MODEL_SELECTION_GUIDE.md) - Choose the right model
- [CONFIRMATION_GUIDE.md](./CONFIRMATION_GUIDE.md) - Confirmation mode
- [CROSS_PC_COMPATIBILITY.md](./CROSS_PC_COMPATIBILITY.md) - Multi-PC setup
- [TESSERACT_SETUP.md](./TESSERACT_SETUP.md) - OCR setup

### **Advanced Topics**
- [HYBRID_INSTALLER_AUTOMATION.md](./HYBRID_INSTALLER_AUTOMATION.md) - Installer automation
- [docs/IMAGE_DOWNLOAD_FEATURE.md](./docs/IMAGE_DOWNLOAD_FEATURE.md) - Image downloads
- [docs/INSTALLER_AUTOMATION_V2.md](./docs/INSTALLER_AUTOMATION_V2.md) - V2 installers
- [examples/](./examples/) - Code examples

### **Reference**
- [QUICK_REFERENCE.md](./QUICK_REFERENCE.md) - One-page cheat sheet
- [PROJECT_OVERVIEW.md](./PROJECT_OVERVIEW.md) - Architecture overview
- [docs/CORRECT_MODEL_IDS.md](./docs/CORRECT_MODEL_IDS.md) - Model IDs

---

## 🔒 **Security & Privacy**

- ✅ **API keys stored locally** in `.env` file (not committed to git)
- ✅ **No data sent to third parties** except Anthropic API
- ✅ **Confirmation mode** available for safety
- ✅ **OneDrive-aware** path handling
- ⚠️ **Use with caution** - agent has system-level access

---

## 🤝 **Contributing**

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🐛 **Troubleshooting**

### **Common Issues**

#### **"Module not found" error**
```powershell
# Ensure virtual environment is activated
.\.venv\Scripts\Activate.ps1
# Reinstall dependencies
pip install -r requirements.txt
```

#### **"Flutter command not found"**
```powershell
# Add Flutter to PATH
$env:PATH += ";C:\flutter\bin"
# Verify
flutter doctor
```

#### **"Port 8000 already in use"**
```powershell
# Kill existing process
netstat -ano | findstr :8000
Stop-Process -Id <PID> -Force
```

#### **"Model not found" error**
Check that you're using correct model IDs:
- ✅ `claude-3-5-haiku-20241022`
- ✅ `claude-3-7-sonnet-20250219`
- ✅ `claude-opus-4-20250514`

See [docs/CORRECT_MODEL_IDS.md](./docs/CORRECT_MODEL_IDS.md) for details.

---

## 🌟 **Acknowledgments**

- **Anthropic** - Claude AI API
- **Flutter** - Beautiful GUI framework
- **Python** - Automation backbone
- **pywinauto** - Windows UI automation
- **Selenium** - Browser automation

---

## 📧 **Contact**

- **Issues**: [GitHub Issues](https://github.com/YOUR_USERNAME/axonyx-revolt/issues)
- **Discussions**: [GitHub Discussions](https://github.com/YOUR_USERNAME/axonyx-revolt/discussions)

---

<div align="center">

**Made with ❤️ for Windows automation enthusiasts**

⭐ **Star this repo if you find it useful!** ⭐

</div>
