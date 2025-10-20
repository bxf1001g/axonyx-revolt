# Browser Automation with Selenium

## 📦 Installation

```powershell
# Activate your virtual environment
.\venv\Scripts\Activate.ps1

# Install Selenium
pip install selenium

# Install browser drivers (Chrome will auto-download with Selenium 4+)
# For Firefox or Edge, you may need to download drivers separately
```

## 🚀 Quick Start

### 1. Basic Browser Operations

```
"Start a Chrome browser"
"Navigate to https://google.com"
"Get the page text"
"Close the browser"
```

### 2. Web Automation Examples

```
"Start browser and go to https://google.com"
"Type 'Python automation' in the search box with selector 'textarea[name=q]'"
"Click the search button with selector 'input[name=btnK]'"
"Take a screenshot"
```

### 3. WhatsApp Web Automation

```
"Start Chrome browser"
"Navigate to https://web.whatsapp.com"
"Wait for the QR code to load"
"Take a screenshot of the QR code"
```

## 🎯 Available Browser Tools

### start_browser
Start a browser session for automation
```
"Start a Chrome browser"
"Start Firefox in headless mode"
"Start Edge browser"
```

### navigate_to_url
Navigate to any website
```
"Go to https://example.com"
"Navigate to https://web.whatsapp.com"
"Open https://github.com"
```

### click_element
Click buttons, links, or any element
```
"Click the button with id 'submit-btn'"
"Click the element with xpath '//button[@class=\"login\"]'"
"Click the link with CSS selector 'a.nav-link'"
```

### type_text_browser
Type text into input fields
```
"Type 'hello@example.com' in the email field with id 'email'"
"Enter 'my search query' in the search box with name 'q'"
"Fill 'John Doe' in the input with CSS selector 'input.username'"
```

### get_page_text
Extract all visible text from the page
```
"Get all text from the current page"
"What text is on this webpage?"
"Show me the page content"
```

### take_screenshot
Capture the current page
```
"Take a screenshot"
"Save screenshot to D:/screenshots/page.png"
"Capture the current page"
```

### execute_javascript
Run custom JavaScript in the browser
```
"Execute JavaScript: alert('Hello World')"
"Run this script: document.title = 'New Title'"
"Execute JS: window.scrollTo(0, document.body.scrollHeight)"
```

### wait_for_element
Wait for elements to load
```
"Wait for the element with id 'content' to appear"
"Wait 20 seconds for the button with class 'submit'"
"Wait for xpath '//div[@id=\"result\"]'"
```

### close_browser
End the browser session
```
"Close the browser"
"Quit the browser session"
"Close Chrome"
```

## 📖 Real-World Examples

### Login Automation
```
"Start browser and navigate to https://example.com/login"
"Type 'user@example.com' in field with id 'email'"
"Type 'password123' in field with id 'password'"
"Click the submit button with id 'login-btn'"
"Wait for element with id 'dashboard'"
"Take a screenshot to confirm login"
```

### Web Scraping
```
"Start browser and go to https://quotes.toscrape.com"
"Get all page text"
"Take a screenshot"
"Close browser"
```

### Form Filling
```
"Start Chrome browser"
"Navigate to https://example.com/form"
"Type 'John' in field with name 'firstname'"
"Type 'Doe' in field with name 'lastname'"
"Type 'john@example.com' in field with id 'email'"
"Click submit button with CSS selector 'button[type=submit]'"
"Wait for confirmation message with id 'success'"
```

### WhatsApp Web Automation
```
"Start browser"
"Navigate to https://web.whatsapp.com"
"Wait 5 seconds for page to load"
"Take screenshot to see QR code"
```
(Then scan QR code with phone)
```
"Wait for element with xpath '//div[@contenteditable=\"true\"]'"
"Type 'Hello from automation!' in element with xpath '//div[@contenteditable=\"true\"]'"
"Click send button with CSS selector 'span[data-icon=\"send\"]'"
```

### Social Media Automation
```
"Start browser and go to https://twitter.com"
"Type 'Python automation' in search box with selector 'input[aria-label=\"Search\"]'"
"Press Enter"
"Wait 3 seconds"
"Take screenshot of results"
```

### E-commerce Testing
```
"Start Chrome"
"Navigate to https://demo.opencart.com"
"Click search button with name 'search'"
"Type 'MacBook' in search field"
"Execute JavaScript to scroll down: window.scrollTo(0, 500)"
"Take screenshot"
"Close browser"
```

## 🎓 Selector Guide

### CSS Selectors (Recommended)
- By ID: `#submit-button`
- By Class: `.login-form`
- By Attribute: `input[name="email"]`
- By Type: `button[type="submit"]`

### XPath
- Basic: `//button[@id="submit"]`
- Text contains: `//button[contains(text(), "Login")]`
- Complex: `//div[@class="form"]//input[@type="email"]`

### By ID
```
"Click element with id 'submit-btn' using 'id' selector"
```

### By Name
```
"Type 'test' in element with name 'username' using 'name' selector"
```

## 🔧 Advanced Patterns

### Multi-Step Workflow
```python
# Through natural language:
"Start browser, navigate to https://google.com, type 'Python' in search box with name 'q', click search button with name 'btnK', wait 2 seconds, take screenshot, close browser"
```

### Handling Popups/Alerts
```
"Execute JavaScript: alert('Test')"
"Execute JavaScript: document.querySelector('.popup-close').click()"
```

### Scrolling
```
"Execute JavaScript: window.scrollTo(0, document.body.scrollHeight)"
"Execute JavaScript: document.querySelector('#footer').scrollIntoView()"
```

### Getting Data
```
"Execute JavaScript: return document.title"
"Execute JavaScript: return document.querySelector('h1').innerText"
"Get all page text"
```

## ⚠️ Important Notes

### Browser Drivers
- **Chrome**: Auto-managed by Selenium 4+ (no manual download needed)
- **Firefox**: May need geckodriver
- **Edge**: Uses built-in Edge WebDriver

### Headless Mode
For automation without UI:
```
"Start browser in headless mode"
```

### Timeouts
Default wait time is 10 seconds. Adjust if needed:
```
"Wait 30 seconds for element with id 'slow-loader'"
```

### Session Persistence
Browser session persists across commands until you close it:
```
"Start browser"
"Navigate to site1.com"
"Navigate to site2.com"  # Same browser window
"Close browser"
```

## 🚨 Common Issues

### Element Not Found
- Use `wait_for_element` before interacting
- Verify selector using browser DevTools (F12)
- Try different selector types (CSS vs XPath)

### Timing Issues
- Add explicit waits: `"Wait for element..."`
- Use `execute_javascript` to check page state
- Increase timeout for slow-loading elements

### Browser Not Starting
- Ensure Chrome/Firefox/Edge is installed
- Check browser driver compatibility
- Try different browser: `"Start Firefox browser"`

## 🎯 Next Steps

1. **Install Selenium**:
   ```powershell
   pip install selenium
   ```

2. **Restart Agent**:
   ```powershell
   python src/main.py
   ```

3. **Test Browser Automation**:
   ```
   "Start browser and navigate to https://google.com"
   ```

Happy automating! 🌐🤖
