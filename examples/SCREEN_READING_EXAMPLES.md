# Screen Reading & OCR Examples

Complete guide to using screen reading and OCR capabilities to extract text, find content, and read balances from any application.

## 🎯 What You Can Do

### 1. Take Screenshots
Capture your screen or specific regions.

**Examples:**
```
"Take a screenshot"
"Take a screenshot and save it to Desktop/myshot.png"
"Capture the top-left 800x600 area of my screen"
```

**Technical Details:**
- Default location: `Desktop/screenshots/screenshot_TIMESTAMP.png`
- Supports custom paths with automatic directory creation
- Can capture specific regions: `[x, y, width, height]`
- Returns saved file path and dimensions

### 2. Extract All Text from Screen
Read everything visible using OCR.

**Examples:**
```
"What text is on my screen?"
"Extract all text from the current screen"
"Read the text in the top-right corner" (specify region)
```

**Use Cases:**
- Read PDF documents
- Extract text from images
- Read locked form fields
- Copy text from videos/streams
- Extract data from legacy applications

### 3. Search for Specific Text
Check if text exists on screen and get surrounding context.

**Examples:**
```
"Is 'Invoice' visible on screen?"
"Find 'Total Amount' on my screen"
"Do you see 'Error' anywhere?"
"Search for 'Balance' case-sensitive"
```

**Returns:**
- Whether text was found
- Surrounding context (50 chars before/after)
- Useful for validation and verification

### 4. Extract Currency Values
Automatically find and extract money amounts.

**Examples:**
```
"Get the balance from my screen"
"Extract all prices visible"
"What's the total amount shown?"
"Find dollar values on this page"
```

**Supported Formats:**
- `$1,234.56` (US Dollar)
- `€1.234,56` (Euro)
- `£1,234.56` (British Pound)
- `1234.56 USD` (with currency code)

**Perfect For:**
- Reading bank balances
- Extracting bill amounts
- Getting subscription prices
- Checking API credit balances (like Anthropic!)

### 5. Find Images on Screen
Locate buttons, icons, or UI elements by image.

**Examples:**
```
"Find the save button icon on screen" (provide reference image)
"Locate Desktop/chrome_logo.png on my screen"
```

**Use Cases:**
- Find buttons without accessible text
- Locate application icons
- Detect UI states (loading spinners, etc.)

### 6. Get Screen Dimensions
Useful for calculating regions and positions.

**Examples:**
```
"What's my screen resolution?"
"Get screen size"
```

## 🔥 Real-World Workflows

### Check Anthropic Billing Balance
```
User: "Open my Chrome and check my Anthropic balance"

Agent will:
1. open_chrome_with_profile("https://console.anthropic.com/settings/billing")
2. Wait a moment for page load
3. extract_currency_from_screen() - finds "$4.61"
4. Report: "Your Anthropic balance is $4.61"
```

### Extract Invoice Details
```
User: "Open Invoice.pdf and extract the total"

Agent will:
1. Launch PDF viewer with the file
2. extract_text_from_screen()
3. Use regex to find invoice number, date, total
4. Report structured data
```

### Read Email Content
```
User: "What's in the email on screen?"

Agent will:
1. extract_text_from_screen()
2. Parse sender, subject, body
3. Summarize content
```

### Monitor Application Status
```
User: "Is the download complete?"

Agent will:
1. find_text_on_screen("Complete")
2. Or find_text_on_screen("100%")
3. Report status
```

### Extract Table Data
```
User: "Read the data table from Excel"

Agent will:
1. take_screenshot() of visible area
2. extract_text_from_screen()
3. Parse into structured format
4. Return as JSON or summary
```

## ⚙️ Setup Requirements

### For Screenshots Only
✅ **Works out of the box** - pyautogui already installed

### For OCR (Text Extraction)
❌ **Requires Tesseract OCR**

**Quick Install:**
1. Download: https://github.com/UB-Mannheim/tesseract/wiki
2. Run installer (tesseract-ocr-w64-setup-*.exe)
3. Restart agent - auto-detects Tesseract

**Or with Chocolatey (as admin):**
```powershell
choco install tesseract -y
```

See `TESSERACT_SETUP.md` for detailed instructions.

## 🎨 Advanced Usage

### Capture Specific Regions
If you know the exact area:
```python
# Top-left quadrant: x=0, y=0, width=960, height=540 (for 1920x1080 screen)
"Take screenshot of region 0 0 960 540"
```

### Multi-Language OCR
```
"Extract text in French from screen"
"Read German text from this PDF"
```
*(Requires language data installed with Tesseract)*

### Combine with Automation
```
"Click on 'Settings', wait 2 seconds, then extract all text from the settings window"

"Open Calculator, type 123+456=, then read the result from screen"

"Launch Notepad, type 'Test', save to Desktop/test.txt, take screenshot, extract text to verify"
```

## 🐛 Troubleshooting

### "Tesseract OCR not installed" Error
- Screenshot still works, but text extraction needs Tesseract
- Install from: https://github.com/UB-Mannheim/tesseract/wiki
- Restart agent after installation

### Poor OCR Accuracy
- Ensure text is clearly visible (not tiny/blurry)
- Try capturing specific region instead of full screen
- Check that screen is not dim/low contrast
- Some fonts work better than others

### Can't Find Text That's Visible
- OCR isn't 100% accurate
- Try searching for partial text: "Balance" instead of "Remaining Balance"
- Use case-insensitive search (default)
- Check `full_text_context` in result to see what OCR actually read

### Region Coordinates
Use `get_screen_size()` first to understand dimensions:
- 1920x1080 screen: top-left is (0,0), bottom-right is (1919, 1079)
- Region format: `[x, y, width, height]`
- Example: Center 400x300: `[760, 390, 400, 300]`

## 💡 Pro Tips

1. **For balances**: Use `extract_currency_from_screen()` - it's smarter than generic text extraction
2. **For validation**: Use `find_text_on_screen()` - faster than extracting all text
3. **For specific areas**: Calculate region coordinates to avoid reading irrelevant screen content
4. **For automation**: Combine OCR with `press_key()` and `click_at()` for full workflows
5. **For screenshots**: Images are saved to Desktop/screenshots by default - easy to review

## 🔗 Related Tools

**Works with:**
- `open_chrome_with_profile()` - Open sites then read content
- `press_key()` / `type_text()` - Automate then verify with OCR
- `click_at()` - Click buttons found by OCR
- `launch_application()` - Open apps then read their UI

**Keystroke capabilities:**
Yes! The agent can already:
- `press_key("enter")`, `press_key("ctrl+c")`
- `type_text("Hello World")`
- `click_at(x, y)` for mouse clicks
- `move_mouse(x, y)` for hovering

Combine these with OCR for powerful automation:
```
"Find 'Username' on screen, click below it, type 'john@example.com'"
```
