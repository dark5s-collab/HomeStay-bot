from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8493592743:AAEE1y83vrcPE5uDk0l5VFvRcuZ4R9q2RWE"

users = {}

# ================= BOOKING STEPS =================
steps = ["name", "phone", "checkin", "checkout", "members", "type", "room"]

questions = [
    "👤 What should I call you?",
    "📞 Enter your phone number:",
    "📅 Enter check-in date (DD-MM-YYYY):",
    "📅 Enter check-out date (DD-MM-YYYY):",
    "👥 Number of members:",
    "👪 Family or Bachelors?",
    "🏨 AC or Non-AC?"
]

# ================= SMART RESPONSES =================
responses = {
    ("where", "location", "near", "tirupati"): "📍 Homestay is in Tirupati near Tirumala",

    ("clean",): "✨ Yes, homestay is clean",
    ("neat",): "✨ Yes, homestay is neat",
    ("clean", "neat"): "✨ Yes, homestay is clean and neat",
    ("room clean", "rooms clean"): "🛏️ Rooms are clean and neat",

    ("kitchen",): "🍳 Yes, kitchen is available",

    ("water",): "💧 RO drinking water available",
    ("geyser",): "♨️ Geyser available",
    ("parking",): "🚗 Car parking available",

    ("facilities",): "🏠 Facilities:\n✔️ RO Water\n✔️ Geyser\n✔️ Parking\n✔️ Kitchen\n✔️ Clean & Neat Rooms",

    ("1", "2", "1bhk"): "🏠 1-2 persons → 1BHK",
    ("3", "4", "2bhk"): "🏠 3-4 persons → 2BHK",
    ("5", "6", "3bhk"): "🏠 5-6 persons → 3BHK",

    ("7", "8", "9", "10", "more"): "📞 For more members, I will connect you with agent",

    ("price", "cost"): "💰 Price depends on room type"
}

# ================= SMART MATCH =================
async def smart_reply(update, text):
    for keys, reply in responses.items():
        if any(word in text for word in keys):
            await update.message.reply_text(reply)
            return True
    return False

# ================= START =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id
    users[user_id] = {"step": 0, "data": {}}

    await update.message.reply_text("👋 Welcome to Homestay Booking")
    await update.message.reply_text("👉 Please follow steps to check availability")
    await update.message.reply_text(questions[0])

# ================= MAIN =================
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if not update.message or not update.message.text:
            return

        user_id = update.effective_chat.id
        text = update.message.text.lower().strip()

        if user_id not in users:
            users[user_id] = {"step": 0, "data": {}}

        user = users[user_id]

        # ================= AFTER BOOKING =================
        if user["step"] >= len(steps):

            handled = await smart_reply(update, text)

            if not handled:
                await update.message.reply_text(
                    "❌ I can't understand\n👉 Ask: location / clean / facilities / price"
                )
            return

        step = user["step"]

        # 🚫 FORCE FIRST STEPS
        if step < 4:
            if any(w in text for w in ["price","where","facility","clean","neat"]):
                await update.message.reply_text("⚠️ Please complete booking first")
                return

        # SAVE DATA
        user["data"][steps[step]] = text
        user["step"] += 1

        # NEXT QUESTION
        if user["step"] < len(steps):
            await update.message.reply_text(questions[user["step"]])

        else:
            data = user["data"]

            await update.message.reply_text(
                f"✅ BOOKING COMPLETED\n\n"
                f"👤 Name: {data['name']}\n"
                f"📞 Phone: {data['phone']}\n"
                f"📅 Stay: {data['checkin']} → {data['checkout']}\n"
                f"👥 Members: {data['members']}\n"
                f"🏠 Type: {data['type']} | {data['room']}\n\n"
                "💰 Advance: ₹500\n"
                "📲 GPay / PhonePe available\n"
                "📞 Contact: 8493592747\n\n"
                "👉 After payment send screenshot\n\n"
                "👉 Now ask: location / facilities / price"
            )

    except Exception as e:
        print("ERROR:", e)
        await update.message.reply_text("⚠️ Error but bot still running")

# ================= RUN =================
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

print("🚀 FINAL BOT RUNNING")
app.run_polling()
