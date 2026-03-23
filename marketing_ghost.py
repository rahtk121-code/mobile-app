import asyncio
import os
from pyrogram import Client, enums
from pyrogram.errors import FloodWait

# --- بيانات الحسابات (تأكد من وضع الـ String Sessions الخاصة بك) ---
ACCOUNTS = [
    {
        "name": "Saudi_Alpha",
        "session": "STRING_SESSION_1_HERE",
        "api_id": "API_ID_1",
        "api_hash": "API_HASH_1",
        "targets": ["@WhalePool", "@CryptoWhalePump", "@BinanceArabic"]
    },
    {
        "name": "Saudi_Beta",
        "session": "STRING_SESSION_2_HERE",
        "api_id": "API_ID_2",
        "api_hash": "API_HASH_2",
        "targets": ["@otcru", "@cryptochina", "@KuCoin_Exchange"]
    }
]

# الرابط الاحترافي الذي أنشأته أنت
TELEGRAPH_LINK = "https://telegra.ph/ShadowMix-V65--The-Invisible-Crypto-Shield-03-23"

# نص الرسالة المنسق بـ HTML لجذب الحيتان
MARKETING_MSG = (
    f"<a href='{TELEGRAPH_LINK}'>&#8203;</a>" # خدعة الرابط المخفي لإظهار المعاينة
    f"<b>🛡️ ShadowMix V6.5 | The Ultimate Ghost Protocol</b>\n\n"
    f"Stop being tracked by surveillance firms. Shred your crypto now with the most advanced mixer.\n\n"
    f"✅ <b>Liquidity Shredding</b> (250+ Splits)\n"
    f"✅ <b>Zero-Trace</b> (RAM-only Servers)\n"
    f"✅ <b>Cross-Chain</b> (Safe Hopping)\n\n"
    f"🚀 <b>START MIXING:</b> <a href='https://t.me/YourBotUser'>@YourBotUser</a>\n" # استبدل YourBotUser بمعرف بوتك
    f"<i>In a world of surveillance, be a shadow.</i>"
)

async def run_account(acc):
    async with Client(acc["name"], session_string=acc["session"], api_id=acc["api_id"], api_hash=acc["api_hash"]) as app:
        print(f"✅ {acc['name']} is ONLINE and targeting whales...")
        while True:
            for group in acc["targets"]:
                try:
                    # إرسال الرسالة بتنسيق HTML
                    await app.send_message(group, MARKETING_MSG, parse_mode=enums.ParseMode.HTML)
                    print(f"🚀 {acc['name']} posted successfully in {group}")
                    await asyncio.sleep(1800) # انتظار 30 دقيقة (أكثر أماناً للأرقام الوهمية)
                except FloodWait as e:
                    await asyncio.sleep(e.value)
                except Exception as e:
                    print(f"❌ Error in {group}: {e}")

async def main():
    await asyncio.gather(*[run_account(a) for a in ACCOUNTS])

if __name__ == "__main__":
    asyncio.run(main())
