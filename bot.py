from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text("🙏 Welcome to Medini Homestay\n\nPlease enter your Name")

# MAIN LOGIC
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
            await update.message.reply_text("📅 Enter Check-in Date (DD/MM/YYYY)")
        else:
            await update.message.reply_text("❌ Enter valid 10-digit phone number")

    # STEP 3: CHECK-IN
    elif "checkin" not in context.user_data:
        if "/" in text:
            context.user_data["checkin"] = text
            await update.message.reply_text("📅 Enter Check-out Date (DD/MM/YYYY)")
        else:
            await update.message.reply_text("❌ Use format DD/MM/YYYY")

    # STEP 4: CHECK-OUT
    elif "checkout" not in context.user_data:
        if "/" in text:
            context.user_data["checkout"] = text
            await update.message.reply_text("👨‍👩‍👧 Enter number of members")
        else:
            await update.message.reply_text("❌ Use format DD/MM/YYYY")

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

            # FINAL RESPONSE
            await update.message.reply_text(
                "✅ Booking Details Received!\n\n"
                f"👤 Name: {context.user_data['name']}\n"
                f"📱 Phone: {context.user_data['phone']}\n"
                f"📅 Check-in: {context.user_data['checkin']}\n"
                f"📅 Check-out: {context.user_data['checkout']}\n"
                f"👥 Members: {context.user_data['members']}\n"
                f"🏠 Type: {context.user_data['type']}\n"
                f"❄️ AC: {context.user_data['ac']}\n\n"
                
                "📍 Location: Tirupati (3-4 KM from railway station)\n"
                "🧼 Clean & Neat Rooms\n"
                "💧 RO Water Available\n"
                "🔥 Geyser Available\n"
                "🚗 Parking Available\n"
                "🍳 Kitchen Available\n"
                "⚡ 24/7 Electricity\n"
                "🔒 Safe for Family\n\n"
                
                "💰 Payment:\n"
                "Advance: ₹500\n"
                "📞 8493592747 (PhonePe / GPay)\n"
                "Remaining pay after reaching"
            )

        else:
            await update.message.reply_text("❌ Answer yes or no")

    # AFTER FLOW → QUESTIONS
    else:

        # LOCATION
        if "location" in text or "where" in text:
            await update.message.reply_text("📍 Tirupati (3-4 KM from railway station)")

        elif "clean" in text or "neat" in text:
            await update.message.reply_text("🧼 Rooms are clean and neat")

        elif "wifi" in text:
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

        elif "payment" in text or "price" in text:
            await update.message.reply_text(
                "💰 Advance ₹500\n📞 8493592747\nPay via GPay / PhonePe"
            )

        else:
            await update.message.reply_text("🤖 I didn't understand, please ask clearly")

# RUN
app = ApplicationBuilder().token("8493592743:AAEE1y83vrcPE5uDk0l5VFvRcuZ4R9q2RWE").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, reply))

app.run_polling()
