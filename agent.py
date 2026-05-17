import os
import json
import time
import requests
from datetime import datetime
from dotenv import load_dotenv
from market_data import get_ticker, get_ohlc, paper_buy, paper_sell, get_paper_status

load_dotenv()

# ==========================================
# ZONE 1: THE KRAKEN-VERIFIED ASSET ARSENAL
# ==========================================
CRYPTO_ASSETS = [
"CHZ/USD", "H/USD", "VVV/USD", "INJ/USD", "ZEC/USD", 
    "HYPE/USD", "POL/USD", "EDGEX/USD", "NEAR/USD"
]

OLLAMA_URL = "http://localhost:11434/api/generate"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TELEMETRY_FILE = os.path.join(BASE_DIR, "telemetry.json")
LEDGER_FILE = os.path.join(BASE_DIR, "trade_ledger.json")
SHADOW_LEDGER_FILE = os.path.join(BASE_DIR, "shadow_portfolio.json")

# --- INITIALIZATION GUARDRAILS: Instant Anti-404 Hotfixes ---
if not os.path.exists(LEDGER_FILE):
    with open(LEDGER_FILE, 'w') as f:
        f.write("") # Blank creation instantly silences web server 404 logs

if not os.path.exists(TELEMETRY_FILE):
    default_telemetry = {
        "prices": {},
        "current_target": "INITIALIZING",
        "latest_analysis": "Cognitive uplink initializing... Streaming local telemetry.",
        "balance_history": [10000.0],
        "holdings": {"USD": 10000.0},
        "net_worth": 10000.0
    }
    with open(TELEMETRY_FILE, 'w') as f:
        json.dump(default_telemetry, f, indent=4) # Guardrail prevents initial page-load gaps

# ==========================================
# ZONE 2: SHADOW LEDGER & MEMORY SUBSYSTEMS
# ==========================================
def load_shadow_portfolio() -> dict:
    """Loads the local shadow ledger or auto-seeds a clean sandbox balance."""
    if os.path.exists(SHADOW_LEDGER_FILE):
        try:
            with open(SHADOW_LEDGER_FILE, 'r') as f:
                return json.load(f)
        except Exception: 
            pass
            
    initial_state = {"USD": 10000.0}
    for asset in CRYPTO_ASSETS:
        initial_state[asset.split('/')[0]] = 0.0
        
    with open(SHADOW_LEDGER_FILE, 'w') as f:
        json.dump(initial_state, f, indent=4)
    return initial_state

def save_shadow_portfolio(state: dict):
    """Commits current shadow ledger balances safely to disk."""
    with open(SHADOW_LEDGER_FILE, 'w') as f:
        json.dump(state, f, indent=4)

def get_recent_trades_for_pair(pair: str, limit: int = 3) -> str:
    """Parses execution logs to supply the cognitive matrix with past trade entries."""
    if not os.path.exists(LEDGER_FILE) or os.path.getsize(LEDGER_FILE) == 0:
        return "No prior transaction history recorded for this asset."
    
    matching_trades = []
    try:
        with open(LEDGER_FILE, 'r') as f:
            for line in f:
                if not line.strip(): 
                    continue
                trade = json.loads(line)
                if trade.get("pair") == pair:
                    matching_trades.append(
                        f"  * [{trade['time']}] Action: {trade['action']} at Price: ${float(trade['price']):.4f}"
                    )
        if not matching_trades:
            return "No prior transaction history recorded for this asset."
        return "\n".join(matching_trades[-limit:])
    except Exception as e:
        return f"Memory retrieval exception: {e}"

# ==========================================
# ZONE 3: COGNITIVE NEURAL INFRASTRUCTURE
# ==========================================
def query_local_llm(prompt: str) -> str:
    payload = {
        "model": "deepseek-r1:8b",
        "prompt": prompt,
        "stream": False,
        "think": False
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        return response.json().get("response", "")
    except Exception as e:
        print(f"[!] Local Engine Fault: {e}")
        return "{}"

def analyze_market(ticker_data: dict, ohlc: list[dict], pair: str) -> str:
    recent_candles = ohlc[-8:] if len(ohlc) >= 8 else ohlc
    ohlc_summary = "\n".join(
        f"O:{c.get('open')} H:{c.get('high')} L:{c.get('low')} C:{c.get('close')}"
        for c in recent_candles
    )
    prompt = f"Analyze {pair} market mechanics.\nCurrent: Ask {ticker_data.get('ask')}, Bid {ticker_data.get('bid')}, Last {ticker_data.get('last')}\nCandles: {ohlc_summary}\nOutput a sharp 1-sentence synthesis of direction and velocity."
    return query_local_llm(prompt).strip()



def make_batch_decision(pair: str, analysis: str, inventory: float, virtual_cash: float, trade_memory: str) -> dict:
    """Implements an unbendable HODL bias directive while allowing strategic initial capital deployment."""
    prompt = f"""You are the Master Portfolio Chief Risk Officer analyzing {pair}.
    Market Context Stream: {analysis}
    Active Asset Inventory: {inventory} units.
    Available Buying Power: ${virtual_cash:.2f} USD.
    
    ========================================================================
    YOUR PRIOR TRANSACTION MEMORY LOG FOR {pair}:
    {trade_memory}
    ========================================================================
    
    CRITICAL MANDATE: STRATEGIC DEPLOYMENT & CAPITAL PROTECTION
    Analyze your memory and current inventory before making any move:
    
    1. THE BLANK SLATE PROTOCOL (If Inventory is 0): You have cash to deploy. Do NOT refuse to buy just because you lack a prior cost basis. If the market shows a verified support bounce, a trend reversal, or a strong upward breakout, you are CLEARED TO BUY.
    2. PROTECT THE COST BASIS (If Inventory > 0): Do NOT sell an asset at a lower price than you bought it unless there is a catastrophic macro breakdown.
    3. REJECT EMOTIONAL FOMO: Do NOT buy back into an asset at a higher price than you just sold it minutes ago. Wait for a structural pullback.
    4. DEFAULT TO HOLD: If the price is merely moving sideways with noise, action MUST be HOLD.

    Output strictly in this JSON format and nothing else:
    {{
        "action": "BUY"|"SELL"|"HOLD",
        "conviction": 1, 
        "reasoning": "A concise macro justification."
    }}"""
    try:
        response_text = query_local_llm(prompt)
        clean_json = response_text.replace('```json', '').replace('```', '').strip()
        return json.loads(clean_json)
    except Exception as e:
        return {"action": "HOLD", "conviction": 1, "reasoning": "Memory interface decoding fault. Safe HOLD."}

# ==========================================
# ZONE 4: METRICS & BROADCAST OUTPUTS
# ==========================================
def update_telemetry_matrix(prices: dict, current_target: str, summary: str, net_worth: float, holdings: dict):
    balance_history = [10000.0]
    if os.path.exists(TELEMETRY_FILE):
        try:
            with open(TELEMETRY_FILE, 'r') as f:
                old_data = json.load(f)
                if "balance_history" in old_data:
                    balance_history = old_data["balance_history"]
        except Exception: 
            pass

    if not balance_history or abs(balance_history[-1] - net_worth) > 0.01:
        balance_history.append(net_worth)
        if len(balance_history) > 50: 
            balance_history.pop(0)

    telemetry_data = {
        "prices": prices,
        "current_target": current_target,
        "latest_analysis": summary,
        "balance_history": balance_history,
        "holdings": holdings,
        "net_worth": net_worth
    }
    with open(TELEMETRY_FILE, 'w') as f:
        json.dump(telemetry_data, f, indent=4)

def log_trade_to_ledger(pair: str, action: str, price: float, cash_spent: float):
    log_entry = {
        "time": datetime.now().strftime("%H:%M:%S"),
        "pair": pair,
        "action": f"{action} (${cash_spent:.0f})",
        "price": price
    }
    with open(LEDGER_FILE, 'a') as f:
        f.write(json.dumps(log_entry) + '\n')

# ==========================================
# ZONE 5: MASTER SYNCHRONIZED EXECUTION
# ==========================================
def run_synchronized_pipeline():
    print(f"\n=== STARTING INTEGRATED NEON SHADOW LEDGER LOOP ===")
    portfolio = load_shadow_portfolio()
    
    engine_status = get_paper_status()
    if engine_status and "current_value" in engine_status:
        portfolio["USD"] = float(engine_status["current_value"])
    
    current_cash = portfolio["USD"]
    print(f"Verified Cash Reserves: ${current_cash:.2f} USD")
    
    tracked_prices = {}
    batch_jobs = []
    combined_summaries = []
    
    virtual_cash_pool = current_cash
    true_asset_valuation = 0.0
    display_holdings = {"USD": round(current_cash, 2)}

    # Phase 1: Context Aggregation, Memory Injection & Strategy Sizing
    for asset in CRYPTO_ASSETS:
        ticker = get_ticker(asset)
        ohlc = get_ohlc(asset)
        if not ticker or not ohlc: 
            continue
            
        last_price = float(ticker.get("last", 0.0))
        tracked_prices[asset] = f"{last_price:.4f}"
        
        base_token = asset.split('/')[0]
        token_inventory = float(portfolio.get(base_token, 0.0))
        
        true_asset_valuation += (token_inventory * last_price)
        display_holdings[base_token] = round(token_inventory, 4)
        
        analysis = analyze_market(ticker, ohlc, asset)
        combined_summaries.append(f"{asset}: {analysis}")
        
        # Pull previous ledger transactions for this specific asset
        trade_memory = get_recent_trades_for_pair(asset)
        
        decision = make_batch_decision(asset, analysis, token_inventory, virtual_cash_pool, trade_memory)
        action = decision.get("action", "HOLD")
        
        trade_size = 0.0
        if action == "BUY":
            conviction_rating = min(max(int(decision.get("conviction", 3)), 1), 5)
            trade_size = conviction_rating * 100.0 
            if virtual_cash_pool < trade_size:
                if virtual_cash_pool >= 100.0:
                    trade_size = int(virtual_cash_pool // 100) * 100.0
                else:
                    decision["action"] = "HOLD"
                    trade_size = 0.0
            virtual_cash_pool -= trade_size

        batch_jobs.append({
            "pair": asset, "base_token": base_token, "decision": decision,
            "ticker": ticker, "last_price": last_price, "trade_size": trade_size, "inventory": token_inventory
        })

    total_net_worth = current_cash + true_asset_valuation
    print(f"True Portfolio Net Worth Calculation: ${total_net_worth:.2f} USD")

    # Phase 2: Ordered Order Dispatch & Structural Accounting Updates
    print("\n=== DATA SYNCHRONIZED. DISPATCHING PROTECTED ALLOCATIONS ===")
    for job in batch_jobs:
        pair = job["pair"]
        token = job["base_token"]
        action = job["decision"]["action"]
        reason = job["decision"]["reasoning"]
        price = job["last_price"]
        size = job["trade_size"]
        
        if action == "HOLD":
            print(f"[-] {pair} -> HOLD | Reason: {reason}")
            continue
            
        if action == "BUY":
            volume = round(size / price, 6)
            print(f"[⚡] DISPATCH BUY -> {volume} {token} | Cost basis: ${size:.2f} | Context: {reason}")
            res = paper_buy(pair, volume)
            if res and "error" not in str(res).lower():
                portfolio[token] = portfolio.get(token, 0.0) + volume
                portfolio["USD"] -= size
                display_holdings[token] = round(portfolio[token], 4)
                log_trade_to_ledger(pair, action, price, size)
            else:
                print(f"    [!] Order Rejected by exchange layer binary.")
                
        elif action == "SELL":
            volume = job["inventory"]
            print(f"[💥] DISPATCH LIQUIDATION -> Selling entire {volume} {token} position | Context: {reason}")
            res = paper_sell(pair, volume)
            if res and "error" not in str(res).lower():
                revenue = volume * price
                portfolio[token] = 0.0
                portfolio["USD"] += revenue
                display_holdings[token] = 0.0
                log_trade_to_ledger(pair, action, price, revenue)
            else:
                print(f"    [!] Liquidation order rejected by exchange layer binary.")

    display_holdings["USD"] = round(portfolio["USD"], 2)
    save_shadow_portfolio(portfolio)

    # Phase 3: Telemetry Stream Delivery
    master_summary = "\n".join(combined_summaries)
    update_telemetry_matrix(tracked_prices, "SHADOW_RUN_NOMINAL", master_summary, total_net_worth, display_holdings)
    print("=== PIPELINE COMPUTATION METRICS COMMITTED TO FRONTEND ===")

if __name__ == "__main__":
    while True:
        try: 
            run_synchronized_pipeline()
        except Exception as e: 
            print(f"[CRITICAL FAULT]: {e}")
        time.sleep(60)
