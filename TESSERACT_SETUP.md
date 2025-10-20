# Tesseract OCR Setup Guide

OCR (Optical Character Recognition) features require Tesseract to be installed on your system.

## Quick Installation

### Option 1: Direct Download (Recommended)
1. Download installer from: https://github.com/UB-Mannheim/tesseract/wiki
2. Run the installer (tesseract-ocr-w64-setup-*.exe)
3. Default installation path: `C:\Program Files\Tesseract-OCR\`
4. Restart your agent - it will auto-detect Tesseract

### Option 2: Chocolatey (Requires Admin)
```powershell
# Run PowerShell as Administrator
choco install tesseract -y
```

### Option 3: Manual Path Configuration
If installed in a custom location, the agent will try these paths:
- `C:\Program Files\Tesseract-OCR\tesseract.exe`
- `C:\Program Files (x86)\Tesseract-OCR\tesseract.exe`
- `~\AppData\Local\Programs\Tesseract-OCR\tesseract.exe`

## What Works Without Tesseract?

✅ **Screenshots** - `take_screenshot()` works perfectly
✅ **Screen size** - `get_screen_size()` works
✅ **Image location** - `locate_image_on_screen()` works
✅ **Keyboard/Mouse** - All pyautogui automation works

❌ **Text extraction** - `extract_text_from_screen()` needs Tesseract
❌ **Text search** - `find_text_on_screen()` needs Tesseract
❌ **Currency extraction** - `extract_currency_from_screen()` needs Tesseract

## Testing Installation

After installing Tesseract, restart the agent and try:
```
take a screenshot and extract all text from it
```

If Tesseract is installed correctly, the agent will read all text on your screen!

## Troubleshooting

**"Tesseract OCR not installed" error:**
- Download and install from the link above
- Make sure to restart the agent after installation
- Check that tesseract.exe exists in Program Files

**"Failed to extract text" error:**
- Ensure your screen is visible (not locked/blanked)
- Try a smaller region if full screen fails
- Check that the text is clear and readable

## Language Support

By default, English is used. To add more languages:
1. During Tesseract installation, select additional language data
2. Or download language files from: https://github.com/tesseract-ocr/tessdata
3. Place in `C:\Program Files\Tesseract-OCR\tessdata\`

Use with agent: `extract text in French` (will use `fra` language code)
