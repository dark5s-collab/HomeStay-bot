from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# ====== CONFIG ======
BOT_TOKEN = "8493592743:AAF4br9f4MhKsTqBvs8GE8GN2xkmSSRwLSU"
OWNER_ID = 6681431665

BOOKINGS = []

# ====== START ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        "🙏 Welcome to MEDINI HOME STAY\n\nPlease enter your Name"
    )

# ====== MAIN ======
async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    # STEP 1: NAME
    if "name" not in context.user_data:
        if len(text) < 3:
            await update.message.reply_text("❌ Enter valid name")
        else:
            context.user_data["name"] = text
            await update.message.reply_text("📱 Enter your Phone Number")

    # STEP 2: PHONE
    elif "phone" not in context.user_data:
        if text.isdigit() and len(text) == 10:
            context.user_data["phone"] = text
            await update.message.reply_text("📅 Enter Check-in Date")
        else:
            await update.message.reply_text("❌ Enter valid 10-digit phone number")

    # STEP 3: CHECK-IN (NO FORMAT)
    elif "checkin" not in context.user_data:
        context.user_data["checkin"] = text
        await update.message.reply_text("📅 Enter Check-out Date")

    # STEP 4: CHECK-OUT
    elif "checkout" not in context.user_data:
        context.user_data["checkout"] = text
        await update.message.reply_text("👥 Enter number of members")

    # STEP 5: MEMBERS
    elif "members" not in context.user_data:
        if text.isdigit():
            context.user_data["members"] = text
            await update.message.reply_text("👨‍👩‍👧‍👦 Family or Bachelors?")
        else:
            await update.message.reply_text("❌ Enter number only")

    # STEP 6: TYPE
    elif "type" not in context.user_data:
        if "family" in text or "bachelor" in text:
            context.user_data["type"] = text
            await update.message.reply_text("❄️ Do you want AC room? (yes/no)")
        else:
            await update.message.reply_text("❌ Type Family or Bachelors")

    # STEP 7: AC
    elif "ac" not in context.user_data:
        if "yes" in text or "no" in text:
            context.user_data["ac"] = text

            data = context.user_data

            # SAVE BOOKING
            BOOKINGS.append(data.copy())

            # NOTIFY OWNER
            await context.bot.send_message(
                chat_id=OWNER_ID,
                text=(
                    "🔥 NEW BOOKING!\n\n"
                    f"👤 Name: {data['name']}\n"
                    f"📱 Phone: {data['phone']}\n"
                    f"📅 {data['checkin']} → {data['checkout']}\n"
                    f"👥 Members: {data['members']}\n"
                    f"👪 Type: {data['type']}\n"
                    f"❄️ AC: {data['ac']}"
                )
            )

            # CUSTOMER RESPONSE
            await update.message.reply_text(
                "✅ Booking Confirmed!\n\n"
                "💰 Advance: ₹500\n"
                "📞 8493592747\n"
                "Pay via PhonePe / GPay\n\n"
                "📍 Tirupati (3-4 KM)\n"
                "🧼 Clean Rooms | 🚗 Parking | ⚡ 24/7 Power"
            )
        else:
            await update.message.reply_text("❌ Answer yes or no")

    # ===== AFTER FLOW =====
    else:
        if "location" in text or "where" in text:
            await update.message.reply_text("📍 Tirupati (3-4 KM from railway station)")

        elif "clean" in text or "neat" in text:
            await update.message.reply_text("🧼 Rooms are clean and neat")

        elif "price" in text or "cost" in text:
            await update.message.reply_text("our agent will tell you soon because it is based on availability")

        elif "wifi" in text:
            await update.message.reply_text("📶 WiFi not available")

        elif "1bhk" in text or "2bhk" in text or "3bhk" in text:
            await update.message.reply_text("📶 WiFi not available")

        elif "food" in text:
            await update.message.reply_text("🍽️ Food not provided, kitchen available")

        elif "parking" in text:
            await update.message.reply_text("🚗 Parking available")

        elif "water" in text:
            await update.message.reply_text("💧 RO water available")

        elif "safe" in text:
            await update.message.reply_text("🔒 100% safe")

        elif "pet" in text:
            await update.message.reply_text("❌ Pets not allowed")

        elif "lift" in text:
            await update.message.reply_text("❌ Lift not available")

        elif "discount" in text:
            await update.message.reply_text("💸 Discount available for long stay")

        elif "refund" in text:
            await update.message.reply_text("❌ No refund on advance")

        elif "time" in text:
            await update.message.reply_text("⏰ 24 hours check-in/check-out")

        elif "photo" in text:
            await update.message.reply_text("📸 Photos will be sent in 5 minutes")

        elif "payment" in text or "booking" in text or "book" in text:
            await update.message.reply_text(
                "💰 Advance ₹500\n📞 8493592747\nPay via GPay / PhonePe"
            )

        else:
            await update.message.reply_text("🤖 I didn't understand, please ask clearly")

# ===== /DATA COMMAND =====
async def data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("❌ Not authorized")
        return

    if not BOOKINGS:
        await update.message.reply_text("No bookings yet")
        return

    msg = "📊 BOOKINGS:\n\n"
    for i, b in enumerate(BOOKINGS, 1):
        msg += f"{i}. {b['name']} - {b['phone']} ({b['members']} people)\n"

    await update.message.reply_text(msg)

# ===== RUN =====
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("data", data))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

print("🚀 BOT LIVE...")
app.run_polling()
