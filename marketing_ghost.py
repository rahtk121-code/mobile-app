import asyncio
import os
from pyrogram import Client
from pyrogram.errors import FloodWait, RPCError

# --- إعدادات الحسابات (يتم سحبها من Environment Variables للأمان) ---
# ملاحظة: إذا كنت ستشغله محلياً، يمكنك استبدال os.getenv بالقيم مباشرة بين " "
ACCOUNTS = [
    {
        "name": "Saudi_Alpha",
        "session": os.getenv("SESSION_1"),
        "api_id": os.getenv("API_ID_1"),
        "api_hash": os.getenv("API_HASH_1"),
        "targets": ["@WhalePool", "@CryptoWhalePump", "@BinanceArabic", "@DeFi_Whales"]
    },
    {
        "name": "Saudi_Beta",
        "session": os.getenv("SESSION_2"),
        "api_id": os.getenv("API_ID_2"),
        "api_hash": os.getenv("API_HASH_2"),
        "targets": ["@otcru", "@cryptochina", "@KuCoin_Exchange", "@Mixer_Community"]
    }
]

# الرسالة الاحترافية الموحدة (يمكنك تغييرها لاحقاً حسب اللغة)
MARKETING_MSG = """
🛡️ **ShadowMix V6.5 | The Ultimate Ghost Protocol**

Tired of surveillance? Hide your crypto trails with the most advanced mixer.
✅ **Liquidity Shredding:** Automatic split into 250+ transactions.
✅ **Zero-Trace:** RAM-only servers, no logs ever.
✅ **Multi-Chain:** Polygon, ETH, and BNB supported.

🚀 **Start Now:** [رابط_بوتك_هنا]
*In a world of surveillance, be a shadow.*
"""

async def run_marketing_machine(acc):
    if not acc["session"]:
        print(f"⚠️ Skipping {acc['name']}: No Session String found.")
        return

    try:
        async with Client(
            name=acc["name"],
            session_string=acc["session"],
            api_id=int(acc["api_id"]),
            api_hash=acc["api_hash"]
        ) as app:
            print(f"✅ {acc['name']} is ONLINE and ready for deployment.")
            
            while True:
                for group in acc["targets"]:
                    try:
                        await app.send_message(group, MARKETING_MSG)
                        print(f"🚀 SUCCESS: {acc['name']} posted in {group}")
                        
                        # انتظار 25 دقيقة (1500 ثانية) بين كل منشور لتجنب الحظر
                        await asyncio.sleep(1500) 
                        
                    except FloodWait as e:
                        print(f"⏳ FloodWait for {acc['name']}: Waiting {e.value} seconds...")
                        await asyncio.sleep(e.value)
                    except RPCError as e:
                        print(f"❌ RPC Error for {acc['name']} in {group}: {e}")
                        continue
                    except Exception as e:
                        print(f"❌ Unexpected Error: {e}")
                        continue
    except Exception as e:
        print(f"❌ Critical Error starting {acc['name']}: {e}")

async def main():
    print("🛰️ ShadowMix Global Marketing Army Initializing...")
    # تشغيل الحسابين بالتوازي
    await asyncio.gather(*[run_marketing_machine(acc) for acc in ACCOUNTS])

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Marketing Army Disengaged.")