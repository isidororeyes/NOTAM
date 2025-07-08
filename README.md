# NOTAM Trading Bot v5.0 - Complete Documentation

> **⚠️ IMPORTANT DISCLAIMER**: This bot is for educational and research purposes. Automated trading involves substantial financial risk. Always test thoroughly with paper trading before considering any live implementation.

## 📋 Overview

The NOTAM Trading Bot is an automated system that monitors aviation NOTAMs (Notice to Airmen) for critical airspace closures and automatically executes trading strategies when specific conditions are met. The bot integrates NOTAM monitoring, AI interpretation via ChatGPT, WhatsApp notifications, and automated trading through Interactive Brokers.

### Key Features

- **Real-time NOTAM monitoring** from FAA sources
- **AI-powered interpretation** using ChatGPT API for clear explanations
- **Automatic trading execution** with configurable portfolios
- **WhatsApp notifications** with detailed alerts and summaries
- **Multiple trading modes** (Paper/Live trading)
- **Risk-based portfolios** (Conservative/Moderate/Aggressive)
- **Comprehensive logging** and event tracking

## 🏗️ System Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   NOTAM Sources │───▶│  NOTAM Monitor   │───▶│   ChatGPT API   │
│   (FAA/ICAO)    │    │  & Analysis      │    │  (Interpretation)│
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                 │
                                 ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  WhatsApp API   │◀───│  Trading Bot     │───▶│ Interactive     │
│  (Notifications)│    │  Core System     │    │ Brokers API     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 🛠️ Installation & Setup

### Prerequisites

1. **Python 3.8+** with required packages:
   ```bash
   pip install ib_insync requests beautifulsoup4 lxml
   ```

2. **Interactive Brokers Account** and TWS/Gateway installed

3. **OpenAI API Key** for ChatGPT integration

4. **WhatsApp Integration** (TimelinesAI service)

### Environment Configuration

1. **Set OpenAI API Key:**
   ```bash
   export OPENAI_API_KEY="your-openai-api-key"
   ```
   Or modify the `OPENAI_API_KEY` variable in the code.

2. **Configure Interactive Brokers:**
   - Install TWS or IB Gateway
   - Enable API connections in settings
   - Configure ports:
     - Paper trading: 4002
     - Live trading: 7496

3. **WhatsApp Setup:**
   - Update `JID` and `NINA` variables with target WhatsApp numbers
   - Configure TimelinesAI API credentials

## 📊 Trading Portfolios

### Conservative Portfolio (🟢 Low Risk)
- **SPY** (S&P 500 ETF) - 2 shares
- **QQQ** (NASDAQ ETF) - 2 shares  
- **GLD** (Gold ETF) - 2 shares
- **TLT** (Treasury Bonds) - 1 share

### Moderate Portfolio (🟡 Medium Risk)
- **SPY** - 3 shares
- **QQQ** - 2 shares
- **GLD** - 3 shares
- **XOM** (Exxon Mobil) - 5 shares
- **CVX** (Chevron) - 3 shares
- **LMT** (Lockheed Martin) - 1 share

### Aggressive Portfolio (🟠 High Risk)
- **XLE** (Energy ETF) - 10 shares
- **XOP** (Oil & Gas ETF) - 5 shares
- **XOM** - 10 shares
- **CVX** - 8 shares
- **LMT** - 3 shares
- **GLD** - 5 shares

## 🚀 Usage Guide

### Basic Commands

#### Start Monitoring (Paper Trading)
```bash
python notam_trading_bot_complete.py
```

#### Start with Specific Portfolio
```bash
python notam_trading_bot_complete.py --portfolio Aggressive
```

#### Custom Check Interval
```bash
python notam_trading_bot_complete.py --interval 15
```

### Advanced Commands

#### Live Trading Mode ⚠️
```bash
python notam_trading_bot_complete.py --live-trading --portfolio Moderate
```
**Warning:** This uses real money! Requires explicit confirmation.

#### Paper Trading Mode (Default)
```bash
python notam_trading_bot_complete.py --paper-trading
```

#### Simulation Mode
```bash
python notam_trading_bot_complete.py --simulate --portfolio Conservative
```

### Testing & Utilities

#### Test ChatGPT Integration
```bash
python notam_trading_bot_complete.py --test-chatgpt
```

#### Test IB Connection
```bash
python notam_trading_bot_complete.py --test-ib
```

#### Show Available Portfolios
```bash
python notam_trading_bot_complete.py --show-portfolios
```

#### Create Sample NOTAM for Testing
```bash
python notam_trading_bot_complete.py --create-sample
```

#### Remove Sample NOTAM
```bash
python notam_trading_bot_complete.py --remove-sample
```

### Cache Management

#### View Interpretation Cache
```bash
python notam_trading_bot_complete.py --show-cache
```

#### Clear Cache
```bash
python notam_trading_bot_complete.py --clear-cache
```

## ⚙️ Configuration Options

### Core Settings

| Parameter | Default | Description |
|-----------|---------|-------------|
| `FIR` | "OIIX" | Flight Information Region (Iran) |
| `IB_HOST` | "127.0.0.1" | Interactive Brokers host |
| `IB_PORT` | 4002 | IB port (4002=paper, 7496=live) |
| `CLIENT_ID` | 1 | IB client identifier |

### Trigger Keywords

The system monitors for these critical keywords in NOTAMs:
- AIRSPACE CLOSED
- ALL FLIGHTS PROHIBITED  
- NO FLIGHT PERMITTED
- AIRSPACE IS RESTRICTED
- MILITARY EXERCISE
- CONFLICT ZONE
- DANGER AREA
- RESTRICTED AREA
- NO OVERFLIGHT
- PROHIBITED AREA

### Alert Criteria

A NOTAM triggers trading when:
1. **Contains trigger keywords** (airspace closure indicators)
2. **Is recent** (issued within last 5 minutes)
3. **Affects monitored FIR** (OIIX - Iran region)

## 📱 WhatsApp Notifications

### Alert Message Format
```
🚨 CRITICAL NOTAM ALERT - TRADING ACTIVATED 🚨

📍 FIR: OIIX (Iran)
🆔 ID: A1234/24

⏰ VALIDITY:
📅 Start: 15 Jan 2025 - 14:30 UTC
📅 End: 15 Jan 2025 - 18:30 UTC
⏱️ Duration: 4h 0m

📋 ORIGINAL CONTENT:
AIRSPACE CLOSED DUE TO MILITARY EXERCISE...

🤖 AUTOMATIC INTERPRETATION:
[ChatGPT explanation in clear language]

🤖 AUTOMATIC ACTION:
✅ Alert detected
🔄 Starting automatic trading
🟢 Portfolio: Conservative
💰 Executing specialized orders
```

### Trading Summary Format
```
📊 AUTOMATIC TRADING SUMMARY 📊

🚨 Triggered by: CRITICAL NOTAM ALERT
🟡 MODERATE

✅ SUCCESSFUL: 4
SPY, QQQ, GLD, XOM

❌ FAILED: 1
CVX

💰 TOTAL INVESTED: $1,247.50
⚡ EXECUTION TIME: 3.45s

⏰ Completed: 14:32:15
🤖 NOTAM-Trading Bot v5.0 COMPLETE
```

## 🤖 AI Integration (ChatGPT)

### Features
- **Automatic interpretation** of complex NOTAMs
- **Plain language explanations** for non-aviation experts
- **Caching system** to avoid duplicate API calls
- **Structured analysis** including severity assessment

### Interpretation Format
- **WHAT'S HAPPENING**: Clear explanation
- **WHERE**: Specific location affected  
- **WHEN**: Valid dates and times
- **IMPACT**: Effect on flights and operations
- **SEVERITY**: Risk level (Low/Medium/High/Critical)

## 📈 Trading Logic

### Execution Flow
1. **NOTAM Detection** → Critical alert identified
2. **AI Interpretation** → ChatGPT analyzes content
3. **WhatsApp Alert** → Immediate notification sent
4. **Trading Delay** → Strategic delay (5-10s based on portfolio)
5. **IB Connection** → Connect to broker
6. **Order Execution** → Buy orders for portfolio assets
7. **Monitoring** → Track order status (30s timeout)
8. **Summary Report** → Results sent via WhatsApp

### Risk Management
- **Paper trading default** for safety
- **Explicit confirmation** required for live trading
- **Position limits** defined per portfolio
- **Timeout protection** on order execution
- **Comprehensive logging** of all activities

## 📁 File Structure

```
notam_trading_bot/
├── notam_trading_bot_complete.py    # Main bot script
├── notam_trading_events.log         # Trading events log
├── notam_trading_bot.log           # General application log
├── sample_notam.txt                # Optional test NOTAM file
└── README.md                       # This documentation
```

## 📝 Logging & Monitoring

### Log Files

#### `notam_trading_events.log`
Records all trading events:
```
[2025-01-15 14:30:25 UTC] NOTAM_CRITICAL | SUCCESS | Portfolio: Moderate | ID: A1234/24
[2025-01-15 14:30:45 UTC] TRADING_EXECUTED | SUCCESS | Portfolio: Moderate | Successful: 4, Failed: 1
```

#### `notam_trading_bot.log`  
Detailed application logs with timestamps and debug information.

### Console Output
Real-time status updates with emojis:
- ℹ️ **INFO**: General information
- ✅ **OK**: Successful operations
- ⚠️ **WARNING**: Important notices
- ❌ **ERROR**: Error conditions

## 🔒 Security Considerations

### API Keys
- Store OpenAI API key in environment variables
- Never commit API keys to version control
- Use separate keys for development/production

### Trading Safety
- **Always test with paper trading first**
- Set appropriate position limits
- Monitor account balance and buying power
- Keep separate accounts for automated trading

### Network Security
- Use secure connections for all API calls
- Implement proper timeout handling
- Monitor for unusual activity patterns

## 🚨 Error Handling

### Common Issues & Solutions

#### "Could not connect to IB Gateway"
- Ensure TWS or IB Gateway is running
- Check port configuration (4002/7496)
- Verify API settings are enabled
- Confirm client ID is unique

#### "ChatGPT interpretation failed"
- Verify OpenAI API key is valid
- Check internet connection
- Monitor API usage limits
- Review error messages in logs

#### "WhatsApp notification failed"
- Verify TimelinesAI credentials
- Check WhatsApp number format
- Test with simplified message
- Review API endpoint status

#### "No NOTAMs obtained"
- Check internet connectivity
- Verify FAA website accessibility
- Review FIR configuration
- Test with sample NOTAM file

## 📊 Performance Metrics

### Typical Response Times
- **NOTAM Detection**: 1-3 seconds
- **ChatGPT Interpretation**: 2-5 seconds  
- **WhatsApp Notification**: 1-2 seconds
- **Trading Execution**: 3-8 seconds
- **Total Alert-to-Trade**: 10-20 seconds

### Resource Usage
- **Memory**: ~50-100 MB
- **CPU**: Low (periodic checks)
- **Network**: Moderate (API calls)
- **Storage**: Minimal (logs only)

## 🔄 Maintenance

### Regular Tasks
- Monitor log file sizes
- Clear interpretation cache periodically
- Update trigger keywords as needed
- Review and adjust portfolios
- Test API connections weekly

### Updates
- Check for new NOTAM data sources
- Update trading strategies based on performance
- Enhance error handling based on logs
- Optimize ChatGPT prompts for better interpretations

## ⚠️ Disclaimers

1. **Financial Risk**: Automated trading involves substantial risk of loss
2. **Testing Required**: Always test thoroughly before live trading
3. **Market Volatility**: Rapid market movements may affect execution
4. **API Limitations**: External services may have rate limits or downtime
5. **Aviation Data**: NOTAM interpretation may not be 100% accurate

## 📞 Support

For technical issues:
1. Check logs for error details
2. Test individual components (IB, ChatGPT, WhatsApp)
3. Review configuration settings
4. Use simulation mode for debugging
5. Monitor system resources and connectivity

## 📈 Future Enhancements

- Multiple FIR monitoring
- Advanced risk management rules
- Machine learning for NOTAM classification
- Real-time portfolio optimization
- Enhanced reporting and analytics
- Mobile app integration

---

## 📋 Quick Start Checklist

### For Your Friends - Getting Started:

**Step 1: Prerequisites**
- [ ] Python 3.8+ installed
- [ ] Interactive Brokers account (paper trading recommended)
- [ ] OpenAI API key for ChatGPT
- [ ] Basic understanding of trading risks

**Step 2: Installation**
```bash
pip install ib_insync requests beautifulsoup4 lxml
export OPENAI_API_KEY="your-key-here"
```

**Step 3: First Test**
```bash
# Test everything works
python notam_trading_bot_complete.py --simulate --portfolio Conservative

# Test real monitoring (paper trading only)
python notam_trading_bot_complete.py --paper-trading --portfolio Conservative
```

**Step 4: Understand the System**
- Review the portfolios section
- Test with sample NOTAMs first
- Monitor logs carefully
- Never use live trading without extensive testing

---

## 🤝 Sharing Instructions

**To share this bot safely:**

1. **Always emphasize the risks** - this involves real money
2. **Recommend starting with simulation mode** only
3. **Suggest paper trading** for at least several weeks
4. **Provide this documentation** in full
5. **Recommend independent testing** and verification
6. **Stress the importance** of understanding the code before use

**For Questions:**
- Review the documentation thoroughly
- Test each component individually  
- Start with conservative settings
- Monitor all operations closely
- Never invest more than you can afford to lose

---

*Generated: January 2025 - Version 5.0*
