import asyncio
import random
import datetime
import os
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait, RPCError
from langdetect import detect
from googletrans import Translator

# ================== [ قسم الإعدادات - SETTINGS ] ==================
API_ID = "YOUR_API_ID"        # ضع الـ API ID الخاص بك هنا
API_HASH = "YOUR_API_HASH"    # ضع الـ API HASH الخاص بك هنا
SESSION_STRING = "YOUR_STRING" # ضع الـ String Session هنا
MY_PERSONAL_ID = 123456789     # ضع الـ ID الخاص بحسابك الشخصي لاستلام التقارير

# الرابط الاحترافي للمعاينة (Telegraph)
TELEGRAPH_LINK = "https://telegra.ph/ShadowMix-V65--The-Invisible-Crypto-Shield-03-23"

# الكلمات المفتاحية العالمية للصيد والقنص
GLOBAL_SEARCH_QUERIES = ["Crypto Russia", "Bitcoin China", "Crypto Brasil P2P", "Whale Alert", "Binance Arabic", "Crypto India"]
SNIPER_KEYWORDS = ["mixer", "privacy", "anonymity", "خلط", "خصوصية", "تتبع", "scam", "safe"]

# الرسالة الأساسية (المصدر)
BASE_TEXT = """
🛡️ ShadowMix V8.0 | The Invisible Crypto Shield.
Advanced liquidity shredding for whales. No traces, no logs, pure privacy.
Join the shadow: @YourBotUser
"""
# =================================================================

translator = Translator()
stats = {"posts": 0, "whales": 0, "langs": set()}

async def get_localized_msg(text, target_lang):
    try:
        translated = translator.translate(text, dest=target_lang).text
        return f"<b><a href='{TELEGRAPH_LINK}'>&#8203;</a>{translated}</b>"
    except:
        return f"<b><a href='{TELEGRAPH_LINK}'>&#8203;</a>{text}</b>"

async def get_chat_lang(app, chat_id):
    try:
        msgs = []
        async for m in app.get_chat_history(chat_id, limit=5):
            if m.text: msgs.append(m.text)
        return detect(" ".join(msgs)) if msgs else "en"
    except: return "en"

# --- محرك القناص (Sniper & Auto-Reply) ---
app = Client("ShadowMix_Saudi", session_string=SESSION_STRING, api_id=API_ID, api_hash=API_HASH)

@app.on_message(filters.text & filters.group)
async def sniper_handler(client, message):
    global stats
    if message.from_user and message.from_user.is_self: return
    
    msg_text = message.text.lower()
    if any(word in msg_text for word in SNIPER_KEYWORDS):
        stats["whales"] += 1
        lang = await get_chat_lang(client, message.chat.id)
        reply_text = await get_localized_msg("We offer the best privacy solution. Check our bot for safe mixing.", lang)
        await asyncio.sleep(random.randint(15, 40))
        try:
            await message.reply_text(reply_text, parse_mode=enums.ParseMode.HTML)
            print(f"🎯 Sniper hit in {message.chat.title}")
        except: pass

# --- محرك النشر والبحث العالمي ---
async def global_marketing_task():
    global stats
    while True:
        query = random.choice(GLOBAL_SEARCH_QUERIES)
        print(f"📡 Searching for: {query}")
        try:
            async for dialog in app.search_global_queries(query, limit=5):
                if dialog.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
                    lang = await get_chat_lang(app, dialog.chat.id)
                    stats["langs"].add(lang)
                    final_msg = await get_localized_msg(BASE_TEXT, lang)
                    
                    try:
                        await app.send_message(dialog.chat.id, final_msg, parse_mode=enums.ParseMode.HTML)
                        stats["posts"] += 1
                        print(f"🚀 Posted to {dialog.chat.title} in {lang}")
                    except FloodWait as e: await asyncio.sleep(e.value)
                    except: continue
                    
                    # انتظار بشري (35-55 دقيقة) لتجنب الحظر
                    await asyncio.sleep(random.randint(2100, 3300))
        except Exception as e:
            print(f"❌ Error in Search: {e}")
            await asyncio.sleep(300)

# --- نظام التقارير اليومية ---
async def daily_report_task():
    while True:
        now = datetime.datetime.now()
        # إرسال التقرير الساعة 11:50 مساءً
        if now.hour == 23 and now.minute == 50:
            report = (
                f"📊 **تقرير ShadowMix اليومي (CTO Dashboard)**\n\n"
                f"🚀 إجمالي النشر العالمي: {stats['posts']}\n"
                f"🎯 حيتان تم اصطيادهم: {stats['whales']}\n"
                f"🌍 لغات تم استهدافها: {len(stats['langs'])}\n"
                f"🛡️ حالة النظام: مستقر 100%"
            )
            try:
                await app.send_message(MY_PERSONAL_ID, report)
                stats["posts"] = 0; stats["whales"] = 0; stats["langs"].clear()
            except: pass
            await asyncio.sleep(60)
        await asyncio.sleep(30)

async def main():
    print("💎 ShadowMix Global Army Starting...")
    await app.start()
    await asyncio.gather(global_marketing_task(), daily_report_task())

if __name__ == "__main__":
    app.run(main())
