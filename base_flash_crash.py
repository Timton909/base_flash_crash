import requests, time

def flash_crash():
    print("Base — Flash Crash Detector (>50% drop in <60 sec)")
    history = {}

    while True:
        try:
            r = requests.get("https://api.dexscreener.com/latest/dex/pairs/base")
            now = time.time()

            for pair in r.json().get("pairs", []):
                addr = pair["pairAddress"]
                price = float(pair.get("priceUsd", 0))
                change_1m = pair.get("priceChange", {}).get("m1", 0)

                if addr not in history:
                    history[addr] = (now, price)
                    continue

                last_t, last_p = history[addr]
                if now - last_t > 60:
                    history[addr] = (now, price)
                    continue

                if change_1m <= -50:
                    token = pair["baseToken"]["symbol"]
                    print(f"FLASH CRASH\n"
                          f"{token} {change_1m:.0f}% in 1 min\n"
                          f"Price: ${price:.10f}\n"
                          f"https://dexscreener.com/base/{addr}\n"
                          f"→ Panic sell or rug — buy dip or run\n"
                          f"{'CRASH'*25}")
                    del history[addr]

                history[addr] = (now, price)

        except:
            pass
        time.sleep(3.1)

if __name__ == "__main__":
    flash_crash()
