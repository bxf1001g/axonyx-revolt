# Axonyx Revolt GUI - Visual Design Guide

## 🎨 Window Layout

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  ⚡ Axonyx Revolt                                  [ - ] [ □ ] [ × ] ┃ ← Custom Title Bar
┣━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃              ┃                                                        ┃
┃   ┌────┐     ┃                   💬 Chat Area                        ┃
┃   │ 🌟 │     ┃                                                        ┃
┃   └────┘     ┃  ┌─────────────────────────────────────────────┐     ┃
┃   Axonyx     ┃  │                                               │     ┃
┃   Revolt     ┃  │         🤖 Welcome to Axonyx Revolt          │     ┃
┃              ┃  │      Ask me to automate Windows tasks        │     ┃
┃──────────────┃  │                                               │     ┃
┃              ┃  │        ┌──────────────────────────┐          │     ┃
┃ Model:       ┃  │        │  Open Chrome to Python   │          │     ┃
┃              ┃  │        └──────────────────────────┘          │     ┃
┃ ┌──────────┐ ┃  │        ┌──────────────────────────┐          │     ┃
┃ │ Haiku 3.5▼┃  │        │  Take a screenshot       │          │     ┃
┃ │          │ ┃  │        └──────────────────────────┘          │     ┃
┃ │ Fast ⚡  │ ┃  │                                               │     ┃
┃ └──────────┘ ┃  └─────────────────────────────────────────────┘     ┃
┃              ┃                                                        ┃
┃──────────────┃  After sending messages:                              ┃
┃              ┃                                                        ┃
┃ ┌──────────┐ ┃  ┌───────────────────────────────────────┐           ┃
┃ │🟢Connected│ ┃  │ 👤  Take a screenshot of my desktop   │ 18:25     ┃
┃ │ Refresh  │ ┃  └───────────────────────────────────────┘           ┃
┃ └──────────┘ ┃                                                        ┃
┃              ┃  ┌───────────────────────────────────────────────┐    ┃
┃              ┃  │ 🤖 Screenshot saved to Desktop                │    ┃
┃              ┃  │    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │    ┃
┃              ┃  │    ✅ take_screenshot                        │    ┃
┃              ┃  │       Input: {}                              │    ┃
┃              ┃  │    ✅ get_desktop_path                       │    ┃
┃              ┃  │       Input: {}                              │ 18:25
┃  ┌────────┐  ┃  └───────────────────────────────────────────────┘    ┃
┃  │ 🗑 Clear│  ┃                                                        ┃
┃  │  Chat  │  ┃  🔄 Agent is thinking...                              ┃
┃  └────────┘  ┃                                                        ┃
┃              ┃                                                        ┃
┗━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
┃  ┌──────────────────────────────────────────────┐ ┌────────────┐    ┃
┃  │ Ask me to automate anything...               │ │ 🚀 Send    │    ┃
┃  └──────────────────────────────────────────────┘ └────────────┘    ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

---

## 🎨 Color Swatches

### Primary Colors
```
┌──────────────────┬──────────────────┐
│  Primary Purple  │  Secondary Cyan  │
│    #6C63FF       │    #00D9FF       │
│  ████████████    │  ████████████    │
└──────────────────┴──────────────────┘
```

### Background Colors
```
┌──────────────────┬──────────────────┬──────────────────┐
│   Background     │     Surface      │      Card        │
│    #0F0F1E       │    #1A1A2E       │    #16213E       │
│  ████████████    │  ████████████    │  ████████████    │
└──────────────────┴──────────────────┴──────────────────┘
```

### Text Colors
```
┌──────────────────┬──────────────────┬──────────────────┐
│  Primary Text    │  Secondary Text  │  Tertiary Text   │
│    #FFFFFF       │    #B0B3B8       │    #8E8E93       │
│  ████████████    │  ████████████    │  ████████████    │
└──────────────────┴──────────────────┴──────────────────┘
```

### Status Colors
```
┌──────────────────┬──────────────────┬──────────────────┐
│     Success      │      Error       │     Warning      │
│    #00D97E       │    #FF6B6B       │    #FFA502       │
│  ████████████    │  ████████████    │  ████████████    │
└──────────────────┴──────────────────┴──────────────────┘
```

---

## 📐 Component Dimensions

### Window
```
Default Size:  1200 x 800 px
Minimum Size:   800 x 600 px
Title Bar:       50 px height
Sidebar Width:  280 px
```

### Spacing
```
Extra Large:  24px  ████████████████████████
Large:        16px  ████████████████
Medium:       12px  ████████████
Small:         8px  ████████
Extra Small:   4px  ████
```

### Border Radius
```
Large:  16px  ╭────────────────╮
             │                │
             ╰────────────────╯

Medium: 12px  ╭──────────────╮
             │              │
             ╰──────────────╯

Small:   8px  ╭────────────╮
             │            │
             ╰────────────╯
```

---

## 💬 Message Bubble Examples

### User Message (Right-aligned)
```
                    ┌─────────────────────────────────────┐
                    │ 👤  Install Python from Downloads   │
                    │                                     │
                    │     with Add to PATH checked        │
                    └─────────────────────────────────────┘
                                                        18:30
```
- Background: Purple gradient (#6C63FF)
- Rounded corners: 16px (top-right: 4px)
- Avatar: User icon with gradient
- Text: White (#FFFFFF)

### Agent Message (Left-aligned)
```
┌───────────────────────────────────────────────────────┐
│ 🤖  Python installer launched successfully            │
│                                                       │
│     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│     ✅ automate_python_installer_v2                   │
│        Input: {"installer_path": "C:\\Downloads\\..."}│
│                                                       │
│     ✅ click_checkbox_in_window_v2                    │
│        Input: {"checkbox_text": "Add Python to PATH"}│
│                                                       │
│     ✅ click_button_in_window_v2                      │
│        Input: {"button_text": "Install Now"}         │
└───────────────────────────────────────────────────────┘
18:30
```
- Background: Dark gray (#1E1E2E)
- Rounded corners: 16px (top-left: 4px)
- Avatar: Robot icon with gradient
- Text: White (#FFFFFF)
- Tool badges: Success (green) / Error (red)

### System Message (Centered)
```
                ┌─────────────────────────────────┐
                │ ℹ️  Model changed to Sonnet 3.5 │
                └─────────────────────────────────┘
```
- Background: Surface color (#1A1A2E)
- Border: White 10% opacity
- Icon: Info (cyan)
- Text: Secondary color (#B0B3B8)

### Error Message
```
┌───────────────────────────────────────────────────────┐
│ ⚠️  Connection error: Backend not responding          │
└───────────────────────────────────────────────────────┘
```
- Background: Error color 10% (#FF6B6B10)
- Border: Error color 30% (#FF6B6B30)
- Icon: Error outline (red)
- Text: Error color (#FF6B6B)

---

## 🎯 Model Selector States

### Collapsed
```
┌─────────────────────────────────────┐
│  Model Selection                    │
│  ┌───────────────────────────────┐  │
│  │ Haiku 3.5                  ▼ │  │
│  │ Fast & Cheap ⚡              │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
```

### Expanded
```
┌─────────────────────────────────────┐
│  Model Selection                    │
│  ┌───────────────────────────────┐  │
│  │ Haiku 3.5                  ▲ │  │ ← Selected
│  │ Fast & Cheap ⚡              │  │
│  ├───────────────────────────────┤  │
│  │ Sonnet 3.5                   │  │
│  │ Balanced 🎯                   │  │
│  ├───────────────────────────────┤  │
│  │ Sonnet 4                     │  │
│  │ Most Powerful 🚀              │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
```

---

## 🔘 Button States

### Send Button
```
Normal:
┌──────────────┐
│ 🚀 Send      │  ← Gradient: Purple → Cyan
└──────────────┘

Hover:
┌──────────────┐
│ 🚀 Send      │  ← Slightly brighter
└──────────────┘

Loading:
┌──────────────┐
│ ⏳ ...       │  ← Spinner animation
└──────────────┘

Disabled:
┌──────────────┐
│ 🚀 Send      │  ← Grayed out, 50% opacity
└──────────────┘
```

### Clear Chat Button
```
Normal:
┌──────────────┐
│ 🗑️ Clear Chat│  ← Outlined, secondary color
└──────────────┘

Hover:
┌──────────────┐
│ 🗑️ Clear Chat│  ← Filled, slight red tint
└──────────────┘
```

---

## 🪟 Window Control Buttons

```
┌────┬────┬────┐
│ -  │ □  │ ×  │
└────┴────┴────┘

Normal:
- Background: Transparent
- Icon: Gray (#B0B3B8)

Hover (Minimize/Maximize):
- Background: White 10%
- Icon: White

Hover (Close):
- Background: Red (#FF0000)
- Icon: White
```

---

## ⚡ Animation Examples

### Loading Spinner
```
⠋ ⠙ ⠹ ⠸ ⠼ ⠴ ⠦ ⠧ ⠇ ⠏
```
Duration: 1s infinite
Colors: Primary purple

### Message Slide-in
```
Opacity:    0% → 100%
Position:  +20px → 0px
Duration:  300ms
Easing:    ease-out
```

### Button Press
```
Scale:     1.0 → 0.95 → 1.0
Duration:  150ms
Easing:    cubic-bezier
```

---

## 📱 Responsive Breakpoints

```
Minimum Width: 800px
│
├─ Sidebar: 280px (fixed)
│  └─ Collapses to 60px (icon only) < 1000px
│
└─ Chat Area: Remaining space (520px+)
   ├─ Message max-width: 600px
   └─ Input full-width minus padding
```

---

## 🎨 Typography Scale

```
Display Large:   32px / Bold   ► Heading 1
Display Medium:  28px / Bold   ► Heading 2
Display Small:   24px / Bold   ► Heading 3
Headline:        20px / SemiBold ► Section titles
Title Large:     18px / SemiBold ► Card titles
Title Medium:    16px / Medium  ► Subtitles
Body Large:      16px / Regular ► Main text
Body Medium:     14px / Regular ► Secondary text
Body Small:      12px / Regular ► Captions
Caption:         11px / Regular ► Timestamps
```

---

## 🌟 Special Effects

### Glassmorphism (Future)
```
Background:     blur(10px)
Opacity:        0.7
Border:         1px solid white 20%
Shadow:         0 8px 32px rgba(0,0,0,0.3)
```

### Gradient Overlays
```
Primary Button:
linear-gradient(135deg, #6C63FF 0%, #00D9FF 100%)

User Avatar:
linear-gradient(135deg, #FF6B6B 0%, #FF8E53 100%)

Agent Avatar:
linear-gradient(135deg, #6C63FF 0%, #00D9FF 100%)
```

### Shadows
```
Elevation 1:  0 1px 3px rgba(0,0,0,0.2)
Elevation 2:  0 2px 8px rgba(0,0,0,0.3)
Elevation 3:  0 4px 16px rgba(0,0,0,0.4)
```

---

## 🎯 Iconography

```
App Icon:       auto_awesome ⚡ (gradient)
User Avatar:    person 👤 (orange gradient)
Agent Avatar:   auto_awesome 🤖 (purple gradient)
Success:        check_circle ✅ (green)
Error:          error ❌ (red)
Info:           info_outline ℹ️ (cyan)
Warning:        warning ⚠️ (yellow)
Settings:       settings ⚙️
Clear:          delete_outline 🗑️
Send:           send_rounded 🚀
Minimize:       remove ─
Maximize:       crop_square □
Close:          close ×
Refresh:        refresh 🔄
```

---

## 🎬 User Flow

```
1. Launch Application
   ↓
2. See Welcome Screen (empty state)
   ↓
3. Type message in input field
   ↓
4. Click Send (or press Enter)
   ↓
5. Loading indicator appears
   ↓
6. Agent message appears with response
   ↓
7. Tool execution badges shown
   ↓
8. Auto-scroll to bottom
   ↓
9. Input field auto-focused for next message
```

---

This visual guide provides all the design specifications needed to recreate or customize the Axonyx Revolt GUI! 🎨✨
