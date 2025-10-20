# Correct Claude Model IDs (October 2025)

## ✅ Valid Models (October 2025)

### Claude 3.5 Haiku (Recommended)
```
claude-3-5-haiku-20241022
```
- **Released**: October 22, 2024
- **Best for**: Fast, cost-effective automation
- **Pricing**: $0.80/$4 per MTok (input/output)
- **Status**: ✅ Active

### Claude 3.7 Sonnet (NEW - Replaces 3.5 Sonnet)
```
claude-3-7-sonnet-20250219
```
- **Released**: February 19, 2025
- **Best for**: Balanced performance
- **Pricing**: $3/$15 per MTok (input/output)
- **Status**: ✅ Active
- **Note**: Replaces deprecated Claude 3.5 Sonnet

### Claude Opus 4
```
claude-opus-4-20250514
```
- **Released**: May 14, 2025
- **Best for**: Most capable reasoning
- **Pricing**: $15/$75 per MTok (input/output)
- **Status**: ✅ Active

## ❌ Invalid Model IDs (Do Not Use)

These model IDs do NOT exist or are DEPRECATED:

```
❌ claude-3-5-sonnet-20241022  (Never existed)
❌ claude-3-5-sonnet-20240620  (DEPRECATED - use claude-3-7-sonnet-20250219)
❌ claude-sonnet-4-20250514     (Wrong naming - should be "opus-4")
❌ claude-3-5-opus-*            (No Opus 3.5 exists)
❌ claude-4-*                   (Should be "opus-4" or "sonnet-4")
```

### Why Claude 3.5 Sonnet is Deprecated

Anthropic replaced Claude 3.5 Sonnet with **Claude 3.7 Sonnet** in February 2025.
The new model offers improved intelligence and performance.

## GUI Model Selector

The Flutter GUI now uses these correct IDs:

```dart
availableModels = [
  {
    'id': 'claude-3-5-haiku-20241022',      // ✅ CORRECT
    'name': 'Haiku 3.5',
    'description': 'Fast & Cheap ⚡',
  },
  {
    'id': 'claude-3-7-sonnet-20250219',     // ✅ CORRECT (NEW!)
    'name': 'Sonnet 3.7',
    'description': 'Balanced 🎯',
  },
  {
    'id': 'claude-opus-4-20250514',         // ✅ CORRECT
    'name': 'Opus 4',
    'description': 'Most Powerful 🚀',
  },
];
```

## How to Verify

To check if a model exists, try this API call:

```bash
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: YOUR_KEY" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-3-5-haiku-20241022",
    "max_tokens": 10,
    "messages": [{"role": "user", "content": "Hi"}]
  }'
```

**Success**: Returns message  
**Failure**: Returns `{"error": {"type": "not_found_error", "message": "model: ..."}}`

## Updated Files

1. ✅ `axonyx_gui/lib/providers/agent_provider.dart` - Fixed model IDs
2. ✅ `MODEL_SELECTION_GUIDE.md` - Updated with correct IDs
3. ✅ This file - Created for reference

## What Went Wrong

**User's Action**: Selected "Sonnet 3.5" from GUI dropdown  
**GUI Sent**: `claude-3-5-sonnet-20241022`  
**API Response**: `404 not_found_error`  
**Reason**: That model version doesn't exist (should be `20240620`)

## Fix Applied

Changed in `agent_provider.dart`:
```diff
- 'id': 'claude-3-5-sonnet-20241022',    // ❌ WRONG
+ 'id': 'claude-3-5-sonnet-20240620',    // ✅ CORRECT

- 'id': 'claude-sonnet-4-20250514',      // ❌ WRONG
+ 'id': 'claude-opus-4-20250514',        // ✅ CORRECT
```

## Restart GUI

To use the fixed models:

```powershell
# Stop and restart Flutter app
cd axonyx_gui
flutter run -d windows --release
```

Or use hot reload in VS Code: Press `R` in the Flutter terminal.

## Backend Still Works

The backend doesn't need restart - it just passes the model ID to Anthropic API. The GUI needs to be restarted to load the corrected model IDs.
