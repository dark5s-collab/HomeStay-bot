from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🙏 Welcome to Tirupati Homestay\n\n"
        "Please follow steps to check availability:\n\n"
        "1. Enter your Name\n"
        "2. Enter Phone Number\n"
        "3. Enter Check-in Date (DD/MM/YYYY)\n"
        "4. Enter Check-out Date (DD/MM/YYYY)\n\n"
        "After that you can ask about price, location, facilities."
    )

# MAIN
async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    # BASIC VALIDATION
    if len(text) < 2:
        await update.message.reply_text("❌ Please enter valid input")

    # NAME
    elif text.isalpha():
        context.user_data["name"] = text
        await update.message.reply_text("📱 Enter your Phone Number")

    # PHONE
    elif text.isdigit() and len(text) == 10:
        context.user_data["phone"] = text
        await update.message.reply_text("📅 Enter Check-in Date (DD/MM/YYYY)")

    # CHECK-IN
    elif "/" in text and "checkin" not in context.user_data:
        context.user_data["checkin"] = text
        await update.message.reply_text("📅 Enter Check-out Date (DD/MM/YYYY)")

    # CHECK-OUT
    elif "/" in text and "checkin" in context.user_data:
        context.user_data["checkout"] = text
        await update.message.reply_text(
            "✅ Details received!\n\n"
            "Now you can ask about:\n"
            "Price, Location, Facilities, Payment"
        )

    # LOCATION
    elif "where" in text or "location" in text or "tirupati" in text:
        await update.message.reply_text("📍 Homestay is in Tirupati (3-4 KM from railway station)")

    # CLEAN / NEAT
    elif "clean" in text:
        await update.message.reply_text("🧼 Yes, homestay is clean")

    elif "neat" in text:
        await update.message.reply_text("✨ Rooms are neat and well maintained")

    # FACILITIES
    elif "water" in text:
        await update.message.reply_text("💧 RO Drinking Water available")

    elif "geyser" in text or "hot water" in text:
        await update.message.reply_text("🔥 Geyser available")

    elif "parking" in text or "car" in text:
        await update.message.reply_text("🚗 Car parking available")

    elif "kitchen" in text:
        await update.message.reply_text("🍳 Kitchen available")

    # WIFI / ELECTRICITY
    elif "wifi" in text:
        await update.message.reply_text("📶 WiFi not available")

    elif "electricity" in text or "power" in text:
        await update.message.reply_text("⚡ 24/7 electricity available")

    # FOOD
    elif "food" in text:
        await update.message.reply_text("🍽️ Food not provided, kitchen available")

    # DISTANCE
    elif "distance" in text or "far" in text:
        await update.message.reply_text("📍 3-4 KM from Tirupati railway station")

    # SAFETY
    elif "safe" in text:
        await update.message.reply_text("🔒 100% safe for family")

    # PETS
    elif "pet" in text:
        await update.message.reply_text("❌ Pets not allowed")

    # LIFT
    elif "lift" in text:
        await update.message.reply_text("❌ Lift not available")

    # DISCOUNT
    elif "discount" in text:
        await update.message.reply_text("💸 Discount available for longer stay")

    # REFUND
    elif "refund" in text or "cancel" in text:
        await update.message.reply_text("❌ Advance is non-refundable")

    # ID
    elif "id" in text:
        await update.message.reply_text("🪪 ID proof not required")

    # TIME
    elif "time" in text or "check" in text:
        await update.message.reply_text("⏰ 24 hours check-in/check-out")

    # PHOTOS
    elif "photo" in text:
        await update.message.reply_text("📸 We will send photos within 5 minutes")

    # PAYMENT
    elif "payment" in text or "price" in text or "pay" in text:
        await update.message.reply_text(
            "💰 Payment Details:\n"
            "Advance: ₹500\n"
            "Pay via PhonePe / GPay\n"
            "📞 8493592747\n\n"
            "Remaining amount can be paid after reaching"
        )

    # DEFAULT (IMPORTANT)
    else:
        await update.message.reply_text(
            "🤖 I didn't understand.\n\n"
            "Please ask about:\n"
            "Location, Price, Facilities, Payment"
        )

# RUN
app = ApplicationBuilder().token("8493592743:AAEE1y83vrcPE5uDk0l5VFvRcuZ4R9q2RWE").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, reply))

app.run_polling()
