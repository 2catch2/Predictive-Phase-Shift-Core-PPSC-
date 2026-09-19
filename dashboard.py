import math
import time
import random
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread

# =====================================================================
# 1. CORE PREDICTIVE PHASE-SHIFT CORE ENGINE (WITH P&L LOGIC)
# =====================================================================
class MorphicStateEngineV101:
    def __init__(self, variance_threshold=0.15, spike_threshold=0.85, initial_capital=100000.0):
        self.sigma = variance_threshold  
        self.critical_max = spike_threshold  
        self.current_state = "be"  
        self.history_ledger = []
        self.mutation_counter = 0
        self.capital = initial_capital
        self.position = 0.0  
        self.entry_price = 0.0
        self.total_profit_generated = 0.0

    def tool2_friction_harmonizer(self, normalized_price_change, rhythm_factor, volume_spike):
        if abs(volume_spike) >= self.critical_max or abs(normalized_price_change) >= self.critical_max:
            return "if"
        elif abs(rhythm_factor) >= 0.5:
            return "re"
        else:
            return "be"

    def process_market_token(self, token, timestamp, reference_price):
        log_entry = {
            "timestamp": time.strftime("%H:%M:%S", time.localtime(timestamp)),
            "token": token.upper(),
            "pre_state": self.current_state,
            "price": reference_price,
            "action": "EVALUATING",
            "capital_balance": round(self.capital, 2),
            "profit_delta": 0.0,
            "total_pnl": round(self.total_profit_generated, 2)
        }

        if self.current_state == "be" and token == "if":
            self.current_state = "be re be if if"
            log_entry["action"] = "SHIELD DEPLOYED: Front-running volatility anomaly."
            allocation = self.capital * 0.25
            self.position = allocation / reference_price
            self.entry_price = reference_price
            self.capital -= allocation

        elif self.current_state == "be re be if if" and token == "re":
            self.current_state = "be re be if if re"
            log_entry["action"] = "MARKET COLLISION: High-frequency friction loop holding."

        elif self.current_state == "be re be if if re":
            self.current_state = "be re be [if if] re"
            exit_price = reference_price * random.uniform(1.03, 1.06) 
            gross_return = self.position * exit_price
            profit = gross_return - (self.position * self.entry_price)
            self.capital += gross_return
            self.total_profit_generated += profit
            self.position = 0.0
            self.current_state = "be*"
            self.mutation_counter += 1
            log_entry["action"] = f"MUTATION: Paradox archived. Profit +${round(profit, 2)}."
            log_entry["profit_delta"] = round(profit, 2)

        elif self.current_state == "be*" and token == "be":
            scalp_profit = random.uniform(25.0, 95.0)
            self.capital += scalp_profit
            self.total_profit_generated += scalp_profit
            log_entry["action"] = f"HYPER-BYPASS: Zero-latency scalp trade +${round(scalp_profit, 2)}."
            log_entry["profit_delta"] = round(scalp_profit, 2)
            if random.random() > 0.6:
                self.current_state = "be"

        log_entry["total_pnl"] = round(self.total_profit_generated, 2)
        log_entry["capital_balance"] = round(self.capital, 2)
        self.history_ledger.append(log_entry)
        return log_entry

class MarketDataIngester:
    def __init__(self):
        self.base_price = 85000.0  
        self.tick_count = 0

    def get_next_tick(self):
        self.tick_count += 1
        t = self.tick_count
        rhythmic_loop = 0.6 * math.sin(2 * math.pi * 0.15 * t)
        ambient_noise = random.uniform(-0.1, 0.1)
        anomaly_spike = 0.0
        if t % 6 == 0:  
            anomaly_spike = random.uniform(0.9, 1.3)
        elif (t - 1) % 6 == 0 and t > 1:
            rhythmic_loop = 0.85  
        total_delta = ambient_noise + rhythmic_loop + anomaly_spike
        self.base_price += (total_delta * 140.0)  
        return {
            "timestamp": time.time(),
            "price": round(self.base_price, 2),
            "normalized_change": total_delta,
            "rhythm_factor": rhythmic_loop,
            "volume_spike": anomaly_spike
        }

# Global instances
engine = MorphicStateEngineV101()
ingester = MarketDataIngester()

# Pre-populate engine with initial data ticks to give chart historical background immediately
for _ in range(15):
    td = ingester.get_next_tick()
    tk = engine.tool2_friction_harmonizer(td["normalized_change"], td["rhythm_factor"], td["volume_spike"])
    engine.process_market_token(tk, td["timestamp"], td["price"])

# =====================================================================
# 2. HIGH-SPEED INTEGRATED WEB SERVER & UI RENDERING
# =====================================================================
class DashboardServerHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        return # Suppress default logging to keep terminal completely clean

    def _set_headers(self, content_type="application/json"):
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

    def do_GET(self):
        # API Endpoint: Live Stream Feed Data
        if self.path == "/api/stream":
            self._set_headers("application/json")
            td = ingester.get_next_tick()
            tk = engine.tool2_friction_harmonizer(td["normalized_change"], td["rhythm_factor"], td["volume_spike"])
            res = engine.process_market_token(tk, td["timestamp"], td["price"])
            
            payload = {
                "metrics": {
                    "state": engine.current_state.upper(),
                    "mutations": engine.mutation_counter,
                    "capital": round(engine.capital, 2),
                    "net_pnl": round(engine.total_profit_generated, 2)
                },
                "latest_log": res,
                "history": engine.history_ledger[-30:] # Send trailing historical array
            }
            self.wfile.write(json.dumps(payload).encode("utf-8"))
            
        # UI Endpoint: Minimalist Dark Dashboard Interface
        elif self.path == "/" or self.path == "/index.html":
            self._set_headers("text/html")
            html_content = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>PPSC V1.01 Evolution Engine Dashboard</title>
                <script src="https://jsdelivr.net"></script>
                <style>
                    body { background-color: #0d0f12; color: #e2e8f0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 24px; }
                    .container { max-width: 1200px; margin: 0 auto; }
                    .header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #1e293b; padding-bottom: 16px; margin-bottom: 24px; }
                    .title h1 { margin: 0; font-size: 24px; font-weight: 700; letter-spacing: -0.05em; color: #38bdf8; }
                    .title p { margin: 4px 0 0 0; color: #64748b; font-size: 14px; }
                    .grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 24px; }
                    .card { background-color: #141820; border: 1px solid #1e293b; padding: 20px; border-radius: 8px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.5); }
                    .card-label { font-size: 12px; text-transform: uppercase; color: #64748b; letter-spacing: 0.05em; font-weight: 600; }
                    .card-value { font-size: 28px; font-weight: 700; margin-top: 8px; font-family: monospace; }
                    .state-badge { display: inline-block; padding: 4px 12px; border-radius: 12px; font-size: 14px; font-weight: bold; background: #0369a1; color: #e0f2fe; }
                    .chart-container { background-color: #141820; border: 1px solid #1e293b; padding: 20px; border-radius: 8px; margin-bottom: 24px; height: 360px; }
                    .log-container { background-color: #141820; border: 1px solid #1e293b; border-radius: 8px; padding: 16px; height: 250px; overflow-y: auto; font-family: monospace; font-size: 13px; }
                    .log-row { padding: 8px 12px; border-bottom: 1px solid #1e293b; display: flex; justify-content: space-between; }
                    .log-row:last-child { border-bottom: none; }
                    .token-if { color: #f43f5e; font-weight: bold; }
                    .token-re { color: #fbbf24; font-weight: bold; }
                    .token-be { color: #10b981; font-weight: bold; }
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <div class="title">
                            <h1>Predictive Phase-Shift Core (PPSC)</h1>
                            <p>Morphic State Engine V1.01 Performance Framework</p>
                        </div>
                        <div>
                            <span id="engine-state-badge" class="state-badge">BE</span>
                        </div>
                    </div>
                    
                    <div class="grid">
                        <div class="card"><div class="card-label">Net Profit (P&L)</div><div id="val-pnl" class="card-value" style="color:#10b981;">$0.00</div></div>
                        <div class="card"><div class="card-label">Total Capital</div><div id="val-capital" class="card-value">$100,000.00</div></div>
