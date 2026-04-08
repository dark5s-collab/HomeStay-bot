from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# ===== CONFIG =====
BOT_TOKEN = "8493592743:AAF4br9f4MhKsTqBvs8GE8GN2xkmSSRwLSU"
OWNER_ID = 6681431665

BOOKINGS = []

# ===== START =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        "🙏 Welcome to MEDINI HOME STAY\n\nPlease enter your Name"
    )

# ===== BUTTON HANDLER =====
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data.startswith("confirm_"):
        booking_id = query.data.split("_")[1]
        await query.edit_message_text(f"✅ Booking {booking_id} Confirmed")

    elif query.data.startswith("cancel_"):
        booking_id = query.data.split("_")[1]
        await query.edit_message_text(f"❌ Booking {booking_id} Cancelled")

    elif query.data == "call_owner":
        await query.answer("📞 8121451238", show_alert=True)

# ===== MAIN =====
async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower().strip()

    if "name" not in context.user_data:
        if len(text) < 3:
            await update.message.reply_text("❌ Enter valid name")
        else:
            context.user_data["name"] = text
            await update.message.reply_text("📱 Enter your Phone Number")

    elif "phone" not in context.user_data:
        if text.isdigit() and len(text) == 10:
            context.user_data["phone"] = text
            await update.message.reply_text("📅 Enter Check-in Date")
        else:
            await update.message.reply_text("❌ Enter valid 10-digit phone number")

    elif "checkin" not in context.user_data:
        context.user_data["checkin"] = text
        await update.message.reply_text("📅 Enter Check-out Date")

    elif "checkout" not in context.user_data:
        context.user_data["checkout"] = text
        await update.message.reply_text("👥 Enter number of members")

    elif "members" not in context.user_data:
        if text.isdigit():
            context.user_data["members"] = text
            await update.message.reply_text("👨‍👩‍👧‍👦 Family or Bachelors?")
        else:
            await update.message.reply_text("❌ Enter number only")

    elif "type" not in context.user_data:
        if "family" in text or "bachelor" in text:
            context.user_data["type"] = text
            await update.message.reply_text("❄️ Do you want AC room? (yes/no)")
        else:
            await update.message.reply_text("❌ Type Family or Bachelors")

    elif "ac" not in context.user_data:
        if text in ["yes", "no", "y", "n"]:
            context.user_data["ac"] = "yes" if text in ["yes", "y"] else "no"

            data = context.user_data
            booking_id = len(BOOKINGS) + 1
            data["id"] = booking_id
            BOOKINGS.append(data.copy())

            keyboard = [
                [
                    InlineKeyboardButton("✅ Confirm", callback_data=f"confirm_{booking_id}"),
                    InlineKeyboardButton("❌ Cancel", callback_data=f"cancel_{booking_id}")
                ],
                [
                    InlineKeyboardButton("📞 Call", callback_data="call_owner")
                ]
            ]

            reply_markup = InlineKeyboardMarkup(keyboard)

            await context.bot.send_message(
                chat_id=OWNER_ID,
                text=(
                    "🚨 NEW BOOKING\n\n"
                    f"ID: {data['id']}\n"
                    f"{data['name']}\n"
                    f"{data['checkin']} → {data['checkout']}\n"
                    f"{data['members']} Members\n"
                    f"{data['type']}\n"
                    f"AC: {data['ac']}"
                ),
                reply_markup=reply_markup
            )

            await update.message.reply_text("✅ Booking sent successfully")
            context.user_data.clear()

        else:
            await update.message.reply_text("❌ Answer yes or no")

    # ===== AFTER FLOW =====
    else:
        if "location" in text:
            await update.message.reply_text("📍 Tirupati (3-4 KM from railway station)")

        elif "price" in text:
            await update.message.reply_text("💰 Price depends on availability")

        elif "parking" in text:
            await update.message.reply_text("🚗 Parking available")

        elif "wifi" in text:
            await update.message.reply_text("📶 WiFi may be available")

        elif "geyser" in text:
            await update.message.reply_text("🔥 24/7 hot water available")

        elif "payment" in text:
            await update.message.reply_text("📲 GPay / PhonePe / Cash")

        elif "advance booking" in text:
            await update.message.reply_text("Advance booking is required ₹500/-")

        elif "booking number" in text:
            await update.message.reply_text("📞 8121451238")

        elif "phonepe" in text:
            await update.message.reply_text("Our agent will give you soon")

        elif "gpay" in text:
            await update.message.reply_text("Our agent will give you soon")

        elif "upi" in text:
            await update.message.reply_text("UPI available, agent will provide details")

        elif "rooms available" in text:
            await update.message.reply_text("Our agent will tell you soon")

        elif "rooms left" in text:
            await update.message.reply_text("Few rooms left")

        elif "checkin time" in text:
            await update.message.reply_text("Check-in and check-out is based on 24 hours")

        elif "checkout time" in text:
            await update.message.reply_text("Check-out and check-in is based on 24 hours")

        elif "early checkin" in text:
            await update.message.reply_text("Depends on availability")

        elif "late checkout" in text:
            await update.message.reply_text("Extra charges may apply")

        elif "extra bed" in text:
            await update.message.reply_text("Extra bed available")

        elif "lift" in text:
            await update.message.reply_text("No lift available")

        elif "clean" in text and "neat" in text:
            await update.message.reply_text("Yes, the rooms are clean and neat")

        elif "clean" in text:
            await update.message.reply_text("Rooms are clean")

        elif "distance" in text:
            await update.message.reply_text("3-4 KM from station")

        elif "tirumala" in text and "near" in text:
            await update.message.reply_text("Near to Tirumala")

        elif "bus stand" in text:
            await update.message.reply_text("Near bus stand")

        elif "temple distance" in text:
            await update.message.reply_text("Close to temple")

        elif "hot water" in text:
            await update.message.reply_text("24/7 hot water")

        elif "power backup" in text:
            await update.message.reply_text("Power backup not available")

        elif "electricity" in text:
            await update.message.reply_text("24/7 electricity")

        elif "cleaning" in text:
            await update.message.reply_text("Rooms cleaned daily")

        elif "staff" in text:
            await update.message.reply_text("Staff available")

        elif "neat" in text:
            await update.message.reply_text("Yes, the rooms are neat")

        elif "food" in text:
            await update.message.reply_text("Food not available, kitchen available if needed")

        elif "water" in text:
            await update.message.reply_text("RO drinking water available")

        else:
            await update.message.reply_text("🤖 Ask something relevant")

# ===== RUN =====
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

print("🚀 BOT LIVE...")
app.run_polling()
