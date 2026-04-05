from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

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

# ====== BUTTON HANDLER ======
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data.startswith("confirm_"):
        booking_id = query.data.split("_")[1]
        await query.edit_message_text(f"✅ Booking {booking_id} Confirmed")

    elif query.data.startswith("cancel_"):
        booking_id = query.data.split("_")[1]
        await query.edit_message_text(f"❌ Booking {booking_id} Cancelled")

    elif query.data.startswith("call_"):
        phone = query.data.split("_")[1]
        await query.answer(f"📞 {phone}", show_alert=True)

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

    # STEP 3: CHECK-IN
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

    # STEP 7: AC (FINAL)
    elif "ac" not in context.user_data:
        if "yes" in text or "no" in text:
            context.user_data["ac"] = text

            data = context.user_data

            # BOOKING ID
            booking_id = len(BOOKINGS) + 1
            data["id"] = booking_id

            BOOKINGS.append(data.copy())

            # 🔘 BUTTONS
            keyboard = [
                [
                    InlineKeyboardButton("✅ Confirm", callback_data=f"confirm_{booking_id}"),
                    InlineKeyboardButton("❌ Cancel", callback_data=f"cancel_{booking_id}")
                ],
                [
                    InlineKeyboardButton("📞 Call", callback_data=f"call_{data['phone']}")
                ]
            ]

            reply_markup = InlineKeyboardMarkup(keyboard)

            # 🔔 OWNER NOTIFICATION
            await context.bot.send_message(
                chat_id=OWNER_ID,
                text=(
                    "🚨🚨 NEW BOOKING ALERT 🚨🚨\n\n"
                    f"🆔 ID: {data['id']}\n"
                    f"👤 {data['name']}\n"
                    f"📱 {data['phone']}\n"
                    f"📅 {data['checkin']} → {data['checkout']}\n"
                    f"👥 {data['members']} Members\n"
                    f"👪 {data['type']}\n"
                    f"❄️ AC: {data['ac']}\n\n"
                    "⚠️ Choose action 👇"
                ),
                reply_markup=reply_markup,
                disable_notification=False
            )

            # CUSTOMER RESPONSE
            await update.message.reply_text(
                "✅ Booking Request Received!\n"
                "🔒 Safe & Trusted Stay\n\n"

                f"🆔 ID: {data['id']}\n"
                f"📅 {data['checkin']} → {data['checkout']}\n"
                f"👥 {data['members']} Members\n"
                f"❄️ AC: {data['ac']}\n\n"

                "🏡 FACILITIES:\n"
                "🧼 Clean Rooms\n"
                "💧 RO Water\n"
                "🔥 24/7 Hot Water (Geyser)\n"
                "🚗 Parking\n"
                "⚡ 24/7 Power\n\n"

                "📍 Tirupati (3-4 KM from railway station)\n\n"

                "⚠️ Limited rooms available\n\n"

                "💰 BOOKING:\n"
                "Advance ₹500\n\n"

                "📲 PAYMENT:\n"
                "GPay / PhonePe
            )
        else:
            await update.message.reply_text("❌ Answer yes or no")

    # ===== AFTER FLOW =====
    # ===== AFTER FLOW =====
else:
    if "location" in text or "where" in text:
        await update.message.reply_text("📍 Tirupati (3-4 KM from railway station)")

    elif "price" in text or "cost" in text:
        await update.message.reply_text("💰 Price depends on availability, our agent will inform you soon")

    elif "clean" in text or "neat" in text:
        await update.message.reply_text("🧼 Rooms are very clean and hygienic")

    elif "room" in text:
        await update.message.reply_text("🏡 Spacious rooms available for family and bachelors")

    elif "geyser" in text:
        await update.message.reply_text("🔥 24/7 hot water available")

    elif "parking" in text:
        await update.message.reply_text("🚗 Parking available")

    elif "water" in text:
        await update.message.reply_text("💧 RO drinking water available")

    elif "safe" in text:
        await update.message.reply_text("🔒 100% safe and secure stay")

    elif "food" in text:
        await update.message.reply_text("🍽️ Food not provided, kitchen available")

    elif "payment" in text or "book" in text:
        await update.message.reply_text(
            "💰 Advance ₹500\n📞 8493592747\nGPay / PhonePe"
        )

    # 🔥 UPDATED EXTRA QUESTIONS

    elif "wifi" in text or "internet" in text:
        await update.message.reply_text("📶 WiFi currently not available")

    elif "ac" in text:
        await update.message.reply_text("❄️ AC rooms available on request")

    elif "time" in text or "check" in text:
        await update.message.reply_text("⏰ 24 hours check-in & check-out available")

    elif "advance" in text:
        await update.message.reply_text("💰 Advance ₹500 required to confirm booking")

    elif "cancel" in text:
        await update.message.reply_text("❌ Advance is non-refundable")

    elif "photo" in text or "pics" in text:
        await update.message.reply_text("📸 Room photos will be shared shortly")

    elif "distance" in text:
        await update.message.reply_text("📍 3-4 KM from Tirupati railway station")

    elif "contact" in text:
        await update.message.reply_text("📞 Call/WhatsApp: 8121451238")

    else:
        await update.message.reply_text("🤖 Please ask like: price, location, rooms, booking")

# ===== /DATA =====
async def data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("❌ Not authorized")
        return

    msg = "📊 BOOKINGS:\n\n"
    for i, b in enumerate(BOOKINGS, 1):
        msg += f"{i}. ID:{b['id']} | {b['name']} | {b['phone']} | AC:{b['ac']}\n"

    await update.message.reply_text(msg)

# ===== RUN =====
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("data", data))
app.add_handler(CallbackQueryHandler(button_handler))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

print("🚀 BOT LIVE...")
app.run_polling()
