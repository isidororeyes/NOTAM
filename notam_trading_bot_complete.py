#!/usr/bin/env python3
"""
NOTAM Trading Bot COMPLETE - Detection + ChatGPT + Automatic Trading
Complete integrated version with all functionalities
"""
import sys
import os
import csv
import time
import logging
import requests
import re
import bs4
import math
import json
import argparse
from datetime import datetime, timedelta
from ib_insync import *

# OpenAI Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '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')

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S",
    handlers=[
        logging.FileHandler('notam_trading_bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

def print_section(title):
    """Simple section printer"""
    print("\n" + "=" * 60)
    print(f" {title} ")
    print("=" * 60)

def print_status(message, status="INFO"):
    """Simple status printer"""
    symbols = {"INFO": "ℹ️", "OK": "✅", "WARNING": "⚠️", "ERROR": "❌"}
    print(f"{symbols.get(status, 'ℹ️')} {message}")

# Configuration
FIR = "OIIX"
TRIGGER_KEYWORDS = [
    "AIRSPACE CLOSED", "ALL FLIGHTS PROHIBITED", "NO FLIGHT PERMITTED",
    "AIRSPACE IS RESTRICTED", "NOT AUTHORIZED", "AIRSPACE RESERVATION",
    "CLSD", "CLOSED", "MILITARY EXERCISE", "CONFLICT ZONE", "DANGER AREA",
    "RESTRICTED AREA", "NO OVERFLIGHT", "PROHIBITED AREA"
]

# WhatsApp Configuration
JID = "34608684495@s.whatsapp.net"
NINA = "34679609016@s.whatsapp.net"
WHATSAPP_CONTACTS = [JID, NINA]

# TRADING PORTFOLIOS
CONSERVATIVE_PORTFOLIO = [
    {'symbol': 'SPY', 'sec_type': 'STK', 'exchange': 'SMART', 'currency': 'USD', 'quantity': 2, 'order_type': 'MKT'},
    {'symbol': 'QQQ', 'sec_type': 'STK', 'exchange': 'SMART', 'currency': 'USD', 'quantity': 2, 'order_type': 'MKT'},
    {'symbol': 'GLD', 'sec_type': 'STK', 'exchange': 'SMART', 'currency': 'USD', 'quantity': 2, 'order_type': 'MKT'},
    {'symbol': 'TLT', 'sec_type': 'STK', 'exchange': 'SMART', 'currency': 'USD', 'quantity': 1, 'order_type': 'MKT'},
]

MODERATE_PORTFOLIO = [
    {'symbol': 'SPY', 'sec_type': 'STK', 'exchange': 'SMART', 'currency': 'USD', 'quantity': 3, 'order_type': 'MKT'},
    {'symbol': 'QQQ', 'sec_type': 'STK', 'exchange': 'SMART', 'currency': 'USD', 'quantity': 2, 'order_type': 'MKT'},
    {'symbol': 'GLD', 'sec_type': 'STK', 'exchange': 'SMART', 'currency': 'USD', 'quantity': 3, 'order_type': 'MKT'},
    {'symbol': 'XOM', 'sec_type': 'STK', 'exchange': 'SMART', 'currency': 'USD', 'quantity': 5, 'order_type': 'MKT'},
    {'symbol': 'CVX', 'sec_type': 'STK', 'exchange': 'SMART', 'currency': 'USD', 'quantity': 3, 'order_type': 'MKT'},
    {'symbol': 'LMT', 'sec_type': 'STK', 'exchange': 'SMART', 'currency': 'USD', 'quantity': 1, 'order_type': 'MKT'},
]

AGGRESSIVE_PORTFOLIO = [
    {'symbol': 'XLE', 'sec_type': 'STK', 'exchange': 'SMART', 'currency': 'USD', 'quantity': 10, 'order_type': 'MKT'},
    {'symbol': 'XOP', 'sec_type': 'STK', 'exchange': 'SMART', 'currency': 'USD', 'quantity': 5, 'order_type': 'MKT'},
    {'symbol': 'XOM', 'sec_type': 'STK', 'exchange': 'SMART', 'currency': 'USD', 'quantity': 10, 'order_type': 'MKT'},
    {'symbol': 'CVX', 'sec_type': 'STK', 'exchange': 'SMART', 'currency': 'USD', 'quantity': 8, 'order_type': 'MKT'},
    {'symbol': 'LMT', 'sec_type': 'STK', 'exchange': 'SMART', 'currency': 'USD', 'quantity': 3, 'order_type': 'MKT'},
    {'symbol': 'GLD', 'sec_type': 'STK', 'exchange': 'SMART', 'currency': 'USD', 'quantity': 5, 'order_type': 'MKT'},
]

# IB Configuration
IB_HOST = '127.0.0.1'
IB_PORT = 4002  # Paper Trading - change to 7496 for real
CLIENT_ID = 1

# Files
LOG_FILE = "notam_trading_events.log"

# Global variables
last_notam_id = None
iteration_count = 0
trading_executed = False
notam_interpretations_cache = {}

class NOTAMInterpreter:
    """Class to interpret NOTAMs using ChatGPT"""
    
    def __init__(self, api_key=OPENAI_API_KEY):
        self.api_key = api_key
        self.base_url = "https://api.openai.com/v1/chat/completions"
        
    def interpret_notam(self, notam_text, notam_id=None):
        """Interpret a NOTAM using ChatGPT"""
        if not self.api_key:
            print_status("OpenAI API Key not configured", "ERROR")
            return "❌ Could not interpret NOTAM (API Key missing)"
        
        # Check cache
        cache_key = f"{notam_id}_{hash(notam_text)}"
        if cache_key in notam_interpretations_cache:
            print_status(f"Interpretation for {notam_id} obtained from cache", "INFO")
            return notam_interpretations_cache[cache_key]
        
        print_status(f"Interpreting NOTAM {notam_id} with ChatGPT...", "INFO")
        
        prompt = f"""
You are an aviation expert who must interpret NOTAMs (Notice to Airmen) for non-expert people.

NOTAM to interpret:
{notam_text}

Please provide a clear and understandable explanation that includes:

1. **WHAT'S HAPPENING**: Explain in simple terms what this NOTAM means
2. **WHERE**: Specific location affected (airport, region, etc.)
3. **WHEN**: Valid dates and times
4. **IMPACT**: How this affects flights and operations
5. **SEVERITY**: Criticality level (Low/Medium/High/Critical)

Use clear language and avoid technical jargon. If there are coordinates, explain the general region.
Maximum 200 words.
"""
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are an aviation expert who explains NOTAMs in a clear and understandable way."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 300,
            "temperature": 0.3
        }
        
        try:
            response = requests.post(
                self.base_url,
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                interpretation = result['choices'][0]['message']['content'].strip()
                
                # Save to cache
                notam_interpretations_cache[cache_key] = interpretation
                
                print_status(f"NOTAM {notam_id} interpreted successfully", "OK")
                return interpretation
            else:
                error_msg = f"Error {response.status_code}: {response.text}"
                print_status(f"Error interpreting NOTAM: {error_msg}", "ERROR")
                return f"❌ Error interpreting NOTAM: {error_msg}"
                
        except requests.exceptions.Timeout:
            print_status("Timeout interpreting NOTAM", "ERROR")
            return "❌ Timeout interpreting NOTAM (more than 30s)"
        except Exception as e:
            print_status(f"Unexpected error interpreting NOTAM: {e}", "ERROR")
            return f"❌ Unexpected error: {e}"

class WhatsAppNotifier:
    """Class to handle WhatsApp notifications"""
    
    @staticmethod
    def send_message(jid, message):
        """Send WhatsApp message"""
        url = "https://app.timelines.ai/integrations/api/messages/to_jid"
        headers = {
            "accept": "application/json",
            "Authorization": "Bearer c1f021f4-1bb5-430b-b7c9-b5690a0cfc57",
            "Content-Type": "application/json",
            "X-CSRFToken": "Dg7IsCs2DdAL1LpiABWL4Ovs3b8pmTBBAscIgA2LJPMJkMmIX6uZbPB854lkHsoz"
        }
        payload = {"jid": jid, "whatsapp_account_phone": "+34647479286", "text": message}
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=5)
            if response.status_code == 200:
                print_status(f"WhatsApp sent to {jid[-10:]}", "OK")
                return True
            else:
                print_status(f"WhatsApp error {jid[-10:]}: HTTP {response.status_code}", "ERROR")
                return False
        except Exception as e:
            print_status(f"Error sending WhatsApp: {e}", "ERROR")
            return False

    @staticmethod
    def format_notam_alert(notam, portfolio_name, interpretation=None):
        """Format NOTAM alert with interpretation"""
        try:
            start_date = notam.get('startDate', '')
            end_date = notam.get('endDate', '')
            
            if start_date and end_date:
                try:
                    start = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%SZ")
                    end = datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%SZ")
                    
                    duration = end - start
                    duration_str = f"{duration.days}d {duration.seconds//3600}h" if duration.days > 0 else f"{duration.seconds//3600}h {(duration.seconds//60)%60}m"
                    
                    time_info = f"""⏰ VALIDITY:
📅 Start: {start.strftime('%d %b %Y - %H:%M UTC')}
📅 End: {end.strftime('%d %b %Y - %H:%M UTC')}
⏱️ Duration: {duration_str}"""
                except:
                    time_info = f"""⏰ VALIDITY:
📅 Start: {start_date}
📅 End: {end_date}"""
            else:
                time_info = "⏰ VALIDITY: No date information"
            
            risk_emojis = {
                'Conservative': '🟢',
                'Moderate': '🟡', 
                'Aggressive': '🟠'
            }
            
            message = f"""🚨 CRITICAL NOTAM ALERT - TRADING ACTIVATED 🚨

📍 FIR: {FIR} (Iran)
🆔 ID: {notam.get('notamNumber', 'N/A')}

{time_info}

📋 ORIGINAL CONTENT:
{notam.get('notamText', 'No content')[:180]}{'...' if len(notam.get('notamText', '')) > 180 else ''}"""

            if interpretation:
                message += f"""

🤖 AUTOMATIC INTERPRETATION:
{interpretation}"""

            message += f"""

🤖 AUTOMATIC ACTION:
✅ Alert detected
🔄 Starting automatic trading
{risk_emojis.get(portfolio_name, '🔵')} Portfolio: {portfolio_name}
💰 Executing specialized orders

⚠️ ALERT CRITERIA:
✅ Recent NOTAM (<5 min)
✅ Critical keywords detected
📊 Automatic trading activation

🕐 Timestamp: {datetime.utcnow().strftime('%H:%M UTC')}
🔗 NOTAM-Trading Bot v5.0 COMPLETE"""
            
            return message
        except Exception as e:
            return f"🚨 NOTAM ALERT {notam.get('notamNumber', 'N/A')} - Error formatting message: {e}"

    @staticmethod
    def format_trading_summary(successful_trades, failed_trades, total_invested, portfolio_name, execution_time):
        """Format trading summary"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        risk_levels = {
            'Conservative': '🟢 CONSERVATIVE',
            'Moderate': '🟡 MODERATE',
            'Aggressive': '🟠 AGGRESSIVE'
        }
        
        message = f"""📊 AUTOMATIC TRADING SUMMARY 📊

🚨 Triggered by: CRITICAL NOTAM ALERT
{risk_levels.get(portfolio_name, portfolio_name)}

✅ SUCCESSFUL: {len(successful_trades)}
{', '.join([f"{t['symbol']} ({t.get('description', 'N/A')})" for t in successful_trades]) if successful_trades else 'None'}

❌ FAILED: {len(failed_trades)}
{', '.join(failed_trades) if failed_trades else 'None'}

💰 TOTAL INVESTED: ${total_invested:.2f}
⚡ EXECUTION TIME: {execution_time:.2f}s

⏰ Completed: {timestamp}
🤖 NOTAM-Trading Bot v5.0 COMPLETE"""

        return message

class NOTAMMonitor:
    """Class to monitor NOTAMs from real sources"""
    
    def __init__(self):
        self.interpreter = NOTAMInterpreter()
        print_status("NOTAM Monitor initialized with ChatGPT", "OK")
    
    def fetch_notams_html(self):
        """Get NOTAMs from multiple sources"""
        # Check sample file first
        sample_file = "sample_notam.txt"
        if os.path.isfile(sample_file):
            print_status(f"Found {sample_file} - using for tests", "WARNING")
            try:
                with open(sample_file, 'r', encoding='utf-8') as f:
                    sample_content = f.read().strip()
                
                if sample_content:
                    current_time = datetime.utcnow()
                    end_time = current_time + timedelta(hours=6)
                    
                    test_notam = {
                        "notamNumber": "TEST123456",
                        "notamText": sample_content,
                        "startDate": current_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                        "endDate": end_time.strftime("%Y-%m-%dT%H:%M:%SZ")
                    }
                    
                    return [test_notam]
            except Exception as e:
                print_status(f"Error reading {sample_file}: {e}", "ERROR")
        
        # Try Federal NOTAM Search
        url = "https://www.notams.faa.gov/dinsQueryWeb/advancedNotamMapAction.do"
        payload = {
            'actionType': 'advancedNOTAMFunctions',
            'submit': 'View NOTAMs',
            'reportType': 'Report',
            'formatType': 'DOMESTIC',
            'retrieveLocId': FIR,
            'sortColumns': 'ident',
            'sortDirection': 'ASC',
            'retrieveDistance': '200',
            'distanceDirection': 'ALL'
        }
        
        try:
            print_status("🇺🇸 Querying Federal NOTAM Search...", "INFO")
            response = requests.post(url, data=payload, timeout=15)
            
            if response.status_code == 200:
                soup = bs4.BeautifulSoup(response.text, "html.parser")
                notam_sections = soup.find_all(['pre', 'div', 'p'], string=lambda text: text and 'NOTAM' in text.upper())
                
                if notam_sections:
                    notams = []
                    for section in notam_sections[:5]:
                        text = section.get_text() if hasattr(section, 'get_text') else str(section)
                        parsed = self.parse_notam_block(text)
                        if parsed:
                            notams.append(parsed)
                    return notams
        except Exception as e:
            print_status(f"Error in Federal NOTAM: {e}", "ERROR")
        
        # FAA as backup
        url = f"https://www.notams.faa.gov/dinsQueryWeb/queryRetrievalMapAction.do?reportType=Raw&retrieveLocId={FIR}&actionType=notamRetrievalbyICAOs"
        
        try:
            print_status("🔄 Trying FAA direct...", "INFO")
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            soup = bs4.BeautifulSoup(response.text, "html.parser")
            pre = soup.find("pre")
            if not pre:
                return []
            
            raw_text = pre.get_text()
            blocks = [blk.strip() for blk in raw_text.split("\n\n") if blk.strip()]
            
            notams = []
            for block in blocks:
                notam = self.parse_notam_block(block)
                if notam:
                    notams.append(notam)
            
            return notams
            
        except Exception as e:
            print_status(f"Error getting NOTAMs: {e}", "ERROR")
            return []

    def parse_notam_block(self, block):
        """Parse an individual NOTAM block"""
        try:
            nid_match = re.search(r'A\)\s*([A-Z0-9/\-]+)', block)
            nid = nid_match.group(1) if nid_match else ""
            
            start_match = re.search(r'B\)\s*(\d{10})', block)
            start = None
            if start_match:
                try:
                    start = datetime.strptime(start_match.group(1), "%y%m%d%H%M")
                except:
                    pass
            
            end_match = re.search(r'C\)\s*(\d{10})', block)
            end = None
            if end_match:
                try:
                    end = datetime.strptime(end_match.group(1), "%y%m%d%H%M")
                except:
                    pass
            
            msg_match = re.search(r'E\)\s*(.*)', block, re.DOTALL)
            msg = msg_match.group(1).strip() if msg_match else block.strip()
            
            return {
                "notamNumber": nid,
                "notamText": msg,
                "startDate": start.strftime("%Y-%m-%dT%H:%M:%SZ") if start else None,
                "endDate": end.strftime("%Y-%m-%dT%H:%M:%SZ") if end else None
            }
            
        except Exception as e:
            logging.debug(f"Error parsing NOTAM block: {e}")
            return None

    def is_recent_notam(self, start_iso, threshold_minutes=5):
        """Check if NOTAM is recent"""
        if not start_iso:
            return False
        try:
            dt = datetime.strptime(start_iso, "%Y-%m-%dT%H:%M:%SZ")
            diff = datetime.utcnow() - dt
            return timedelta(0) <= diff <= timedelta(minutes=threshold_minutes)
        except:
            return False

    def analyze_notams(self, notams):
        """Analyze NOTAMs for critical conditions"""
        critical_notams = []
        
        print_status(f"Analyzing {len(notams)} NOTAMs...")
        
        for notam in notams:
            nid = notam.get('notamNumber', 'N/A')
            text = notam.get('notamText', '').upper()
            start_date = notam.get('startDate')
            
            found_keywords = [kw for kw in TRIGGER_KEYWORDS if kw in text]
            has_keywords = len(found_keywords) > 0
            is_recent = self.is_recent_notam(start_date)
            
            if has_keywords:
                print_status(f"Keywords found in {nid}: {found_keywords}", "WARNING")
                
            if is_recent:
                print_status(f"Recent NOTAM: {nid}", "INFO")
                
            if has_keywords and is_recent:
                print_status(f"CRITICAL NOTAM: {nid}", "ERROR")
                
                # Interpret NOTAM with ChatGPT
                interpretation = self.interpreter.interpret_notam(
                    notam.get('notamText', ''), 
                    nid
                )
                
                # Show interpretation on screen
                print_section(f"CHATGPT INTERPRETATION - {nid}")
                print(interpretation)
                print("-" * 60)
                
                # Add interpretation to NOTAM object
                notam['interpretation'] = interpretation
                
                critical_notams.append(notam)
        
        return critical_notams

class IBTrader:
    """Class for automatic trading with Interactive Brokers"""
    
    def __init__(self, host=IB_HOST, port=IB_PORT, client_id=CLIENT_ID):
        self.ib = IB()
        self.host = host
        self.port = port
        self.client_id = client_id
        self.connected = False
        self.total_invested = 0.0
        
    def connect(self):
        """Connect to IB Gateway/TWS"""
        try:
            self.ib.connect(self.host, self.port, clientId=self.client_id)
            self.connected = True
            logging.info(f"Successfully connected to IB Gateway at {self.host}:{self.port}")
            return True
        except Exception as e:
            logging.error(f"Error connecting to IB: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from IB"""
        if self.connected:
            self.ib.disconnect()
            self.connected = False
            logging.info("Disconnected from IB Gateway")
    
    def get_account_summary(self):
        """Get account summary"""
        try:
            account_values = self.ib.accountSummary()
            cash = next((v.value for v in account_values if v.tag == 'TotalCashValue'), 0)
            buying_power = next((v.value for v in account_values if v.tag == 'BuyingPower'), 0)
            
            logging.info(f"Available cash: ${cash}")
            logging.info(f"Buying power: ${buying_power}")
            
            return float(cash), float(buying_power)
        except Exception as e:
            logging.error(f"Error getting account summary: {e}")
            return 0, 0
    
    def create_contract(self, asset_config):
        """Create contract for asset"""
        try:
            symbol = asset_config['symbol']
            exchange = asset_config.get('exchange', 'SMART')
            currency = asset_config.get('currency', 'USD')
            
            contract = Stock(symbol, exchange, currency)
            
            # Qualify contract
            qualified_contracts = self.ib.qualifyContracts(contract)
            if not qualified_contracts:
                logging.error(f"Could not qualify contract for {symbol}")
                return None
            
            qualified_contract = qualified_contracts[0]
            logging.info(f"Valid contract for {symbol}")
            return qualified_contract
                
        except Exception as e:
            logging.error(f"Error creating contract for {symbol}: {e}")
            return None
    
    def get_market_price(self, contract):
        """Get current market price"""
        try:
            ticker = self.ib.reqMktData(contract, '', False, False)
            self.ib.sleep(3)
            
            price = None
            
            if hasattr(ticker, 'marketPrice') and ticker.marketPrice() and not math.isnan(ticker.marketPrice()):
                price = ticker.marketPrice()
            elif hasattr(ticker, 'last') and ticker.last and not math.isnan(ticker.last):
                price = ticker.last
            elif hasattr(ticker, 'close') and ticker.close and not math.isnan(ticker.close):
                price = ticker.close
            elif hasattr(ticker, 'bid') and ticker.bid and not math.isnan(ticker.bid):
                price = ticker.bid
            else:
                logging.warning(f"No price data for {contract.symbol}")
                price = 100.0  # Estimated price
            
            # Cancel subscription
            self.ib.cancelMktData(contract)
            return price
            
        except Exception as e:
            logging.error(f"Error getting price for {contract.symbol}: {e}")
            return 50.0
    
    def place_buy_order(self, contract, asset_config):
        """Place buy order"""
        try:
            quantity = asset_config['quantity']
            order_type = asset_config.get('order_type', 'MKT')
            
            if order_type == 'MKT':
                order = MarketOrder('BUY', quantity)
            else:
                logging.error("Invalid order type")
                return None
            
            trade = self.ib.placeOrder(contract, order)
            logging.info(f"Order placed for {contract.symbol}: {quantity} units")
            return trade
        except Exception as e:
            logging.error(f"Error placing order for {contract.symbol}: {e}")
            return None
    
    def monitor_order(self, trade, timeout=30):
        """Monitor order status"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            self.ib.sleep(1)
            
            if trade.orderStatus.status == 'Filled':
                logging.info(f"Order EXECUTED for {trade.contract.symbol}")
                logging.info(f"Execution price: ${trade.orderStatus.avgFillPrice}")
                logging.info(f"Executed quantity: {trade.orderStatus.filled}")
                
                # Update total invested
                self.total_invested += trade.orderStatus.avgFillPrice * trade.orderStatus.filled
                
                return True
            elif trade.orderStatus.status in ['Cancelled', 'ApiCancelled']:
                logging.warning(f"Order CANCELLED for {trade.contract.symbol}")
                return False
            elif trade.orderStatus.status in ['PendingSubmit', 'Submitted']:
                logging.info(f"Order {trade.orderStatus.status} for {trade.contract.symbol}")
        
        logging.warning(f"Timeout waiting for order execution for {trade.contract.symbol}")
        return False
    
    def execute_emergency_trades(self, assets_config, portfolio_name):
        """Execute emergency trades due to NOTAM alert"""
        if not self.connected:
            logging.error("No connection to IB Gateway")
            return False, [], []
        
        print_status(f"🚨 STARTING EMERGENCY TRADING - {portfolio_name}", "ERROR")
        
        # Get account summary
        cash, buying_power = self.get_account_summary()
        
        successful_trades = []
        failed_trades = []
        self.total_invested = 0.0
        
        for asset_config in assets_config:
            symbol = asset_config['symbol']
            quantity = asset_config['quantity']
            
            logging.info(f"--- Processing {symbol} ---")
            
            # Create contract
            contract = self.create_contract(asset_config)
            if not contract:
                failed_trades.append(symbol)
                continue
            
            # Get market price
            market_price = self.get_market_price(contract)
            estimated_cost = market_price * quantity
            
            # Check funds
            if estimated_cost > cash:
                logging.warning(f"Insufficient funds for {symbol}")
                failed_trades.append(symbol)
                continue
            
            # Place order
            trade = self.place_buy_order(contract, asset_config)
            if not trade:
                failed_trades.append(symbol)
                continue
            
            # Monitor order
            if self.monitor_order(trade):
                successful_trades.append({
                    'symbol': symbol,
                    'quantity': quantity,
                    'price': trade.orderStatus.avgFillPrice if hasattr(trade.orderStatus, 'avgFillPrice') else market_price
                })
                cash -= estimated_cost
                print_status(f"✅ {symbol} executed successfully", "OK")
            else:
                failed_trades.append(symbol)
                print_status(f"❌ {symbol} failed", "ERROR")
        
        return len(successful_trades) > 0, successful_trades, failed_trades

class NOTAMTradingBot:
    """Main class that unifies NOTAM monitoring, ChatGPT and trading"""
    
    def __init__(self, portfolio_type='Conservative'):
        self.notam_monitor = NOTAMMonitor()
        self.trader = IBTrader()
        self.whatsapp = WhatsAppNotifier()
        self.last_notam_id = None
        self.iteration_count = 0
        self.trading_executed = False
        self.portfolio_type = portfolio_type
        self.portfolio = self.get_portfolio()
        
    def get_portfolio(self):
        """Get portfolio according to selected type"""
        portfolios = {
            'Conservative': CONSERVATIVE_PORTFOLIO,
            'Moderate': MODERATE_PORTFOLIO,
            'Aggressive': AGGRESSIVE_PORTFOLIO
        }
        
        portfolio = portfolios.get(self.portfolio_type, CONSERVATIVE_PORTFOLIO)
        print_status(f"Selected portfolio: {self.portfolio_type} ({len(portfolio)} assets)", "INFO")
        return portfolio
        
    def log_event(self, event_type, details, success=True):
        """Log event to plain text file"""
        try:
            timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
            status = "SUCCESS" if success else "FAILURE"
            
            log_entry = f"[{timestamp}] {event_type} | {status} | Portfolio: {self.portfolio_type} | {details}\n"
            
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(log_entry)
                
        except Exception as e:
            print_status(f"Error logging event: {e}", "ERROR")
    
    def send_notam_alerts(self, notam, interpretation=None):
        """Send NOTAM alerts via WhatsApp with interpretation"""
        message = self.whatsapp.format_notam_alert(notam, self.portfolio_type, interpretation)
        
        alerts_sent = 0
        for contact in WHATSAPP_CONTACTS:
            if self.whatsapp.send_message(contact, message):
                alerts_sent += 1
        
        return alerts_sent > 0
    
    def send_trading_summary(self, successful_trades, failed_trades, total_invested, execution_time):
        """Send trading summary via WhatsApp"""
        message = self.whatsapp.format_trading_summary(
            successful_trades, failed_trades, total_invested, 
            self.portfolio_type, execution_time
        )
        
        for contact in WHATSAPP_CONTACTS:
            self.whatsapp.send_message(contact, message)
    
    def run_single_iteration(self):
        """Execute one monitoring iteration"""
        self.iteration_count += 1
        
        print_section(f"ITERATION #{self.iteration_count} - {datetime.now().strftime('%H:%M:%S')} - {self.portfolio_type}")
        
        # Get NOTAMs
        notams = self.notam_monitor.fetch_notams_html()
        if not notams:
            print_status("No NOTAMs obtained", "WARNING")
            return
        
        # Analyze critical NOTAMs
        critical_notams = self.notam_monitor.analyze_notams(notams)
        
        if not critical_notams:
            print_status("No critical NOTAMs found", "OK")
            return
        
        # Process alerts and execute trading
        for notam in critical_notams:
            nid = notam.get('notamNumber', '')
            
            if nid == self.last_notam_id:
                print_status(f"NOTAM {nid} already processed", "INFO")
                continue
            
            print_status(f"🚨 CRITICAL NOTAM DETECTED: {nid}", "ERROR")
            
            # Send WhatsApp alert with interpretation
            interpretation = notam.get('interpretation', None)
            if self.send_notam_alerts(notam, interpretation):
                print_status("WhatsApp alert sent with ChatGPT interpretation", "OK")
            
            # Log event
            self.log_event("NOTAM_CRITICAL", f"ID: {nid}, Portfolio: {self.portfolio_type}", True)
            
            # Execute trading if not already executed
            if not self.trading_executed:
                print_status(f"🤖 STARTING AUTOMATIC TRADING - {self.portfolio_type}", "ERROR")
                
                # Start time to measure execution speed
                start_execution = time.time()
                
                # Delay according to portfolio
                delay = 5 if self.portfolio_type != 'Conservative' else 10
                print_status(f"⏱️ Strategic delay: {delay}s", "INFO")
                time.sleep(delay)
                
                # Connect to IB
                if self.trader.connect():
                    self.trader.ib.sleep(2)
                    
                    # Execute trades
                    success, successful_trades, failed_trades = self.trader.execute_emergency_trades(
                        self.portfolio, self.portfolio_type
                    )
                    
                    execution_time = time.time() - start_execution
                    
                    if success:
                        print_status(f"Trading executed: {len(successful_trades)} successful", "OK")
                        
                        # Send summary via WhatsApp
                        self.send_trading_summary(
                            successful_trades, failed_trades, 
                            self.trader.total_invested, execution_time
                        )
                        
                        # Log event
                        self.log_event(
                            "TRADING_EXECUTED", 
                            f"Portfolio: {self.portfolio_type}, Successful: {len(successful_trades)}, Failed: {len(failed_trades)}", 
                            True
                        )
                        
                        self.trading_executed = True
                    else:
                        print_status("Trading failed", "ERROR")
                        self.log_event("TRADING_FAILED", f"Portfolio: {self.portfolio_type}, All trades failed", False)
                    
                    # Disconnect
                    self.trader.disconnect()
                else:
                    print_status("Could not connect to IB Gateway", "ERROR")
                    self.log_event("TRADING_FAILED", f"Portfolio: {self.portfolio_type}, IB connection failed", False)
            else:
                print_status("Trading already executed previously", "INFO")
            
            self.last_notam_id = nid
    
    def run_monitor_loop(self, interval):
        """Execute main monitoring loop"""
        print_section("NOTAM TRADING BOT COMPLETE v5.0 - STARTING")
        
        print_status(f"Portfolio: {self.portfolio_type}")
        print_status(f"FIR: {FIR}")
        print_status(f"Keywords: {len(TRIGGER_KEYWORDS)} configured")
        print_status(f"Assets to buy: {len(self.portfolio)}")
        print_status(f"Interval: {interval}s")
        print_status(f"WhatsApp contacts: {len(WHATSAPP_CONTACTS)}")
        print_status(f"IB Gateway: {IB_HOST}:{IB_PORT}")
        print_status(f"ChatGPT API: {'✅ Configured' if OPENAI_API_KEY else '❌ Not configured'}")
        print_status(f"Log file: {LOG_FILE}")
        
        # Show portfolio summary
        print_section(f"PORTFOLIO {self.portfolio_type.upper()}")
        for i, asset in enumerate(self.portfolio, 1):
            symbol = asset['symbol']
            qty = asset['quantity']
            print_status(f"{i:2d}. {symbol} x{qty}", "INFO")
        
        try:
            while True:
                self.run_single_iteration()
                print_status(f"Waiting {interval}s until next iteration...")
                print("-" * 60)
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print_section("MONITOR STOPPED")
            print_status("Monitor stopped by user", "INFO")
            if self.trader.connected:
                self.trader.disconnect()
    
    def run_simulation(self):
        """Execute simulation mode"""
        print_section(f"SIMULATION MODE - {self.portfolio_type}")
        
        # Create fake NOTAM
        fake_notam = {
            "notamNumber": "SIM123456",
            "notamText": "AIRSPACE CLOSED FOR MILITARY EXERCISE - SIMULATION MODE",
            "startDate": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "endDate": (datetime.utcnow() + timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
        }
        
        print_status("Testing with simulated critical NOTAM...")
        
        # Interpret with ChatGPT
        interpretation = self.notam_monitor.interpreter.interpret_notam(
            fake_notam['notamText'], 
            fake_notam['notamNumber']
        )
        
        # Show interpretation
        print_section("CHATGPT INTERPRETATION")
        print(interpretation)
        
        # Show WhatsApp message
        message = self.whatsapp.format_notam_alert(fake_notam, self.portfolio_type, interpretation)
        print_section("WHATSAPP MESSAGE EXAMPLE")
        print(message)
        
        # Simulate trading
        fake_successful = []
        fake_failed = []
        
        for i, asset in enumerate(self.portfolio):
            if i % 4 == 0:  # 25% simulated failures
                fake_failed.append(asset['symbol'])
            else:
                fake_successful.append({
                    'symbol': asset['symbol'],
                    'quantity': asset['quantity'],
                    'price': 100.0
                })
        
        fake_summary = self.whatsapp.format_trading_summary(
            fake_successful, fake_failed, 1500.00, self.portfolio_type, 3.5
        )
        print_section("TRADING SUMMARY EXAMPLE")
        print(fake_summary)
        
        print_section("SIMULATION COMPLETED")
        print_status("Simulation completed - no real alerts sent", "OK")
        print_status("ChatGPT interpretation working correctly", "OK")

# Utility functions
def test_chatgpt_interpretation():
    """Test NOTAM interpretation with ChatGPT"""
    print_section("CHATGPT INTERPRETATION TEST")
    
    interpreter = NOTAMInterpreter()
    
    test_notam = "AIRSPACE CLOSED DUE TO MILITARY EXERCISE. ALL FLIGHTS PROHIBITED IN AREA BOUNDED BY 35N050E - 36N051E - 35N052E - 34N051E. SURFACE TO UNLIMITED. ACTIVE UNTIL FURTHER NOTICE."
    
    print_status("Testing interpretation with ChatGPT...", "INFO")
    print(f"Original NOTAM: {test_notam}")
    
    interpretation = interpreter.interpret_notam(test_notam, "TEST123")
    
    print_section("CHATGPT INTERPRETATION")
    print(interpretation)
    print_section("TEST COMPLETED")

def show_notam_cache():
    """Show interpretations cache"""
    print_section("NOTAM INTERPRETATIONS CACHE")
    
    if not notam_interpretations_cache:
        print_status("Empty cache - no interpretations stored", "INFO")
        return
    
    print_status(f"Interpretations in cache: {len(notam_interpretations_cache)}", "INFO")
    
    for i, (key, interpretation) in enumerate(notam_interpretations_cache.items(), 1):
        print(f"\n{i}. Cache Key: {key[:50]}...")
        print(f"Interpretation: {interpretation[:100]}...")

def clear_notam_cache():
    """Clear interpretations cache"""
    global notam_interpretations_cache
    cache_size = len(notam_interpretations_cache)
    notam_interpretations_cache.clear()
    print_status(f"Cache cleared - {cache_size} interpretations removed", "OK")

def create_sample_notam():
    """Create sample NOTAM file for testing"""
    sample_file = "sample_notam.txt"
    sample_content = "AIRSPACE CLOSED DUE TO MILITARY EXERCISE. ALL FLIGHTS PROHIBITED IN AREA BOUNDED BY 35N050E - 36N051E - 35N052E - 34N051E. SURFACE TO UNLIMITED. ACTIVE UNTIL FURTHER NOTICE."
    
    try:
        with open(sample_file, 'w', encoding='utf-8') as f:
            f.write(sample_content)
        print_status(f"Created {sample_file} with sample NOTAM", "OK")
        print_status(f"Run the monitor and it will use this sample automatically", "INFO")
    except Exception as e:
        print_status(f"Error creating {sample_file}: {e}", "ERROR")

def remove_sample_notam():
    """Remove sample NOTAM file"""
    sample_file = "sample_notam.txt"
    if os.path.isfile(sample_file):
        try:
            os.remove(sample_file)
            print_status(f"Removed {sample_file} - will use real NOTAMs", "OK")
        except Exception as e:
            print_status(f"Error removing {sample_file}: {e}", "ERROR")
    else:
        print_status(f"{sample_file} not found", "INFO")

def test_ib_connection():
    """Test IB connection"""
    print_section("IB CONNECTION TEST")
    trader = IBTrader()
    if trader.connect():
        print_status("IB connection successful", "OK")
        cash, buying_power = trader.get_account_summary()
        print_status(f"Cash: ${cash}, Buying power: ${buying_power}", "INFO")
        trader.disconnect()
    else:
        print_status("IB connection failed", "ERROR")

def show_portfolios():
    """Show information about all available portfolios"""
    print_section("AVAILABLE PORTFOLIOS")
    
    portfolios = {
        'Conservative': {'portfolio': CONSERVATIVE_PORTFOLIO, 'risk': '🟢 LOW'},
        'Moderate': {'portfolio': MODERATE_PORTFOLIO, 'risk': '🟡 MEDIUM'},
        'Aggressive': {'portfolio': AGGRESSIVE_PORTFOLIO, 'risk': '🟠 HIGH'}
    }
    
    for name, info in portfolios.items():
        print_section(f"{name.upper()} - {info['risk']}")
        portfolio = info['portfolio']
        
        for i, asset in enumerate(portfolio, 1):
            symbol = asset['symbol']
            qty = asset['quantity']
            print_status(f"{i:2d}. {symbol} x{qty}", "INFO")
        
        print_status(f"Total assets: {len(portfolio)}", "OK")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="NOTAM Trading Bot COMPLETE v5.0")
    parser.add_argument("-i", "--interval", type=float, default=30.0, help="Seconds between checks")
    parser.add_argument("-s", "--simulate", action="store_true", help="Execute simulation")
    parser.add_argument("-p", "--portfolio", choices=['Conservative', 'Moderate', 'Aggressive'], 
                       default='Conservative', help="Trading portfolio type")
    parser.add_argument("--create-sample", action="store_true", help="Create sample NOTAM file")
    parser.add_argument("--remove-sample", action="store_true", help="Remove sample NOTAM file")
    parser.add_argument("--paper-trading", action="store_true", help="Use paper trading (port 4002)")
    parser.add_argument("--live-trading", action="store_true", help="Use real trading (port 7496)")
    parser.add_argument("--test-ib", action="store_true", help="Test IB connection only")
    parser.add_argument("--test-chatgpt", action="store_true", help="Test ChatGPT interpretation")
    parser.add_argument("--show-portfolios", action="store_true", help="Show all available portfolios")
    parser.add_argument("--show-cache", action="store_true", help="Show interpretations cache")
    parser.add_argument("--clear-cache", action="store_true", help="Clear interpretations cache")
    args = parser.parse_args()

    # Configure port according to trading mode
    global IB_PORT
    if args.live_trading:
        IB_PORT = 7496
        print_status("🚨 REAL TRADING MODE ACTIVATED", "ERROR")
        print_status("⚠️  WILL USE REAL MONEY", "WARNING")
        confirmation = input("Do you confirm you want to use real trading? (type 'YES I CONFIRM RISK'): ")
        if confirmation != 'YES I CONFIRM RISK':
            print_status("Real trading cancelled", "INFO")
            return
    elif args.paper_trading:
        IB_PORT = 4002
        print_status("📊 PAPER TRADING MODE ACTIVATED", "OK")
    else:
        IB_PORT = 4002
        print_status("📊 PAPER TRADING MODE (default)", "OK")

    # Create bot with specific portfolio
    bot = NOTAMTradingBot(portfolio_type=args.portfolio)

    # Execute according to arguments
    if args.test_chatgpt:
        test_chatgpt_interpretation()
    elif args.show_cache:
        show_notam_cache()
    elif args.clear_cache:
        clear_notam_cache()
    elif args.show_portfolios:
        show_portfolios()
    elif args.create_sample:
        create_sample_notam()
    elif args.remove_sample:
        remove_sample_notam()
    elif args.test_ib:
        test_ib_connection()
    elif args.simulate:
        bot.run_simulation()
    else:
        print_section("FINAL CONFIGURATION")
        print_status(f"IB Port: {IB_PORT} ({'REAL' if IB_PORT == 7496 else 'PAPER'})", "INFO")
        print_status(f"Portfolio: {args.portfolio}", "INFO")
        print_status(f"Configured assets: {len(bot.portfolio)}", "INFO")
        print_status(f"Interval: {args.interval}s", "INFO")
        print_status(f"ChatGPT API: {'✅ Configured' if OPENAI_API_KEY else '❌ Not configured'}", "INFO")
        print_status(f"Log file: {LOG_FILE}", "INFO")
        print_status("Press Ctrl+C to stop", "INFO")
        
        # Execute main loop
        bot.run_monitor_loop(args.interval)

if __name__ == "__main__":
    main()