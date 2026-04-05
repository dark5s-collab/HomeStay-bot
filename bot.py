from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# ====== CONFIG ======
BOT_TOKEN = "YOUR_BOT_TOKEN"
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
                "GPay / PhonePe: 8493592747\n\n"

                "📸 Photos will be sent in 5 minutes"
            )
        else:
            await update.message.reply_text("❌ Answer yes or no")

    # ===== AFTER FLOW =====
    else:
        if "geyser" in text:
            await update.message.reply_text("🔥 24/7 hot water available")

        elif "payment" in text or "book" in text:
            await update.message.reply_text(
                "💰 Advance ₹500\n📞 8493592747\nGPay / PhonePe"
            )

        else:
            await update.message.reply_text("🤖 Ask clearly")

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
