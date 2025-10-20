# Claude Model Selection Guide

## 💰 Cost-Effective Automation

### Recommended: Claude 3.5 Haiku (Default)
**Best for most automation tasks** - Fast, cheap, and very capable!

```env
CLAUDE_MODEL=claude-3-5-haiku-20241022
```

**Pricing**: ~$0.25 per million input tokens, ~$1.25 per million output tokens
**Speed**: Fastest
**Best for**: 
- File operations
- Process management
- System queries
- Application installation
- Browser automation
- Most automation workflows

---

## 🎯 Model Comparison

### 1. Claude 3.5 Haiku 🏃‍♂️💰
**Recommended for automation!**
```env
CLAUDE_MODEL=claude-3-5-haiku-20241022
```
- ⚡ Fastest response time
- 💰 Most cost-effective
- ✅ Excellent for tool use and automation
- ✅ Perfect for repetitive tasks
- ✅ Great for straightforward automation

**Use when**: Doing standard automation tasks, batch operations, system management

---

### 2. Claude 3.5 Sonnet 🎯⚖️
**Balanced option**
```env
CLAUDE_MODEL=claude-3-5-sonnet-20240620
```
- ⚖️ Balanced speed and capability
- 💰💰 Moderate pricing
- ✅ Better reasoning than Haiku
- ✅ Good for complex automation
- ✅ Handles edge cases well

**Use when**: You need better reasoning, complex multi-step workflows, or Haiku struggles

---

### 3. Claude Opus 4 🚀💎
**Most capable, but expensive**
```env
CLAUDE_MODEL=claude-opus-4-20250514
```
- 🧠 Highest intelligence
- 💰💰💰 Most expensive
- ✅ Best for complex reasoning
- ✅ Handles ambiguous requests better
- ✅ Superior context understanding

**Use when**: Complex multi-step workflows, ambiguous instructions, critical tasks

---

### 3. Claude 3.5 Sonnet ⚖️
**Balanced option**
```env
CLAUDE_MODEL=claude-3-5-sonnet-20241022
```
- ⚖️ Good balance of capability and cost
- 💰💰 Moderate pricing
- ✅ Reliable for most tasks
- ✅ Better reasoning than Haiku

**Use when**: You need more reasoning power than Haiku but want to save vs Sonnet 4

---

### 4. Claude 3 Opus 🎓
**Previous generation flagship**
```env
CLAUDE_MODEL=claude-3-opus-20240229
```
- 🎓 Very capable (previous generation)
- 💰💰💰 Expensive
- ✅ Strong reasoning
- ⚠️ Slower than newer models

**Use when**: Sonnet 4 unavailable, need strong reasoning

---

## 💡 Recommendation for Your Use Case

### For Windows Automation:
**Use Haiku 3.5** - Here's why:

1. **Tool use is straightforward**: Installing apps, clicking buttons, copying files don't need complex reasoning
2. **Speed matters**: Faster responses = quicker automation
3. **Cost-effective**: Run thousands of tasks without breaking the bank
4. **Still very capable**: Haiku 3.5 is excellent at understanding and using tools

### Cost Example:
Running 1000 automation tasks:
- **Haiku**: ~$0.50 - $2
- **Sonnet 3.5**: ~$3 - $15
- **Sonnet 4**: ~$15 - $75

---

## 🔧 How to Switch Models

### Option 1: Edit .env file
```env
# Uncomment the model you want:
# CLAUDE_MODEL=claude-sonnet-4-20250514              # Most capable
CLAUDE_MODEL=claude-3-5-haiku-20241022              # Recommended!
# CLAUDE_MODEL=claude-3-5-sonnet-20241022           # Balanced
# CLAUDE_MODEL=claude-3-opus-20240229               # Previous gen
```

### Option 2: Quick Switch
Just change the active line in `.env` and restart the agent.

---

## 📊 When to Upgrade from Haiku

Consider using Sonnet or Opus when:

❌ **Haiku struggles with**:
- Very ambiguous requests ("fix my system")
- Complex multi-step reasoning requiring decision trees
- Tasks needing deep context understanding
- Creative problem-solving

✅ **Haiku excels at**:
- Clear tool-based automation
- File and process operations
- Browser automation
- Application installation
- System configuration
- Following explicit instructions

---

## 🎯 Real-World Scenarios

### Scenario: Install 10 Applications
- **Haiku**: ✅ Perfect! Clear task, straightforward automation
- **Cost**: ~$0.10

### Scenario: "Organize my desktop intelligently"
- **Haiku**: ⚠️ May need guidance
- **Sonnet 4**: ✅ Better at inferring organization logic
- **Cost**: ~$1-2

### Scenario: Copy 100 files with patterns
- **Haiku**: ✅ Excellent! Fast and cheap
- **Cost**: ~$0.20

### Scenario: "Debug why my app won't install"
- **Haiku**: ⚠️ Basic troubleshooting
- **Sonnet 4**: ✅ Better at diagnostic reasoning
- **Cost**: ~$0.50-1

---

## 💰 Cost Savings Tips

1. **Use Haiku by default** - Upgrade only when needed
2. **Be specific** - Clear instructions work better (cheaper model needed)
3. **Break complex tasks** - Multiple simple Haiku calls < One complex Sonnet call
4. **Test with Haiku first** - Only use expensive models when necessary

---

## 🔄 Switching Models Mid-Project

You can switch models anytime:

```powershell
# Edit .env file
code .env

# Change the CLAUDE_MODEL line
# Save and restart agent
python src/main.py
```

The agent will show which model is active on startup!

---

## 📝 My Recommendation for You

Based on your use case (app installation, desktop control, system settings):

### Start with Haiku 3.5 ✅
```env
CLAUDE_MODEL=claude-3-5-haiku-20241022
```

**Why?**
- Your tasks are well-defined (install, open, copy, configure)
- Tool usage is straightforward
- Fast execution is valuable
- Massive cost savings (10-30x cheaper than Sonnet 4!)

### Upgrade to Sonnet 4 only if:
- Haiku gives unclear results
- You need complex problem-solving
- Budget isn't a concern

---

## 🎉 Bottom Line

For **95% of Windows automation tasks**, **Haiku 3.5 is perfect**!

- ⚡ Fast
- 💰 Cheap  
- ✅ Capable
- 🎯 Purpose-built for tool use

**Save Sonnet 4 for the truly complex 5%!**

---

**Current Model**: Check the agent startup screen to see which model is active! 🤖
