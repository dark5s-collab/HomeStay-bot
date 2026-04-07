from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# ====== CONFIG ======
BOT_TOKEN = "8659430531:AAFzI_6equMZe89CL_Pe-3LpQOUGyzd2cA4"
OWNER_ID = 8493592743

BOOKINGS = []

# ====== START ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        "🙏 Welcome to MEDINI HOME STAY\n\n"
        "Please enter your Name"
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

    elif query.data == "call_owner":
        await query.answer("📞 Call: 8121451238", show_alert=True)

# ====== MAIN FUNCTION ======
async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    # ===== BOOKING FLOW =====

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

    # STEP 6: TYPE (FINAL STEP)
    elif "type" not in context.user_data:
        if "family" in text or "bachelor" in text:
            context.user_data["type"] = text

            data = context.user_data
            booking_id = len(BOOKINGS) + 1
            data["id"] = booking_id
            BOOKINGS.append(data.copy())

            # BUTTONS
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

            # OWNER MESSAGE
            await context.bot.send_message(
                chat_id=OWNER_ID,
                text=(
                    "🚨 NEW BOOKING ALERT 🚨\n\n"
                    f"🆔 ID: {data['id']}\n"
                    f"👤 {data['name']}\n"
                    f"📱 {data['phone']}\n"
                    f"📅 {data['checkin']} → {data['checkout']}\n"
                    f"👥 {data['members']} Members\n"
                    f"👪 {data['type']}"
                ),
                reply_markup=reply_markup
            )

            # USER RESPONSE
            await update.message.reply_text(
                "✅ Booking Request Sent!\n\n"
                "📞 Our agent will contact you soon\n"
                "⚠️ Limited rooms available"
            )

        else:
            await update.message.reply_text("❌ Type Family or Bachelors")

    # ===== AFTER BOOKING (AUTO REPLIES) =====
    else:
        if any(word in text for word in ["location", "where"]):
            await update.message.reply_text("📍 Tirupati (3-4 KM from railway station)")

        elif any(word in text for word in ["price", "cost", "rate"]):
            await update.message.reply_text("💰 Price depends on availability\nAgent will contact you")

        elif "near tirumala" in text:
            await update.message.reply_text("📍 Yes, very close to Tirumala")

        elif "parking" in text:
            await update.message.reply_text("🚗 Parking available")

        elif "geyser" in text or "hot water" in text:
            await update.message.reply_text("🔥 24/7 hot water available")

        elif "clean" in text or "neat" in text:
            await update.message.reply_text("🧼 Clean & hygienic rooms")

        elif "food" in text:
            await update.message.reply_text("🍽️ Kitchen available (self cooking)")

        elif "water" in text:
            await update.message.reply_text("💧 RO drinking water available")

        elif "wifi" in text:
            await update.message.reply_text("📶 WiFi may be available")

        elif "payment" in text or "upi" in text:
            await update.message.reply_text(
                "💰 Advance ₹1000\n"
                "📲 GPay / PhonePe: 8121451238"
            )

        elif "refund" in text or "cancel" in text:
            await update.message.reply_text("❌ Policy will be explained by our agent")

        elif "contact" in text or "call" in text:
            await update.message.reply_text("📞 Call: 8121451238")

        else:
            await update.message.reply_text(
                "🤖 Ask about:\n"
                "price, location, rooms, parking, food, payment"
            )

# ===== DATA (OWNER ONLY) =====
async def data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("❌ Not authorized")
        return

    msg = "📊 BOOKINGS:\n\n"
    for i, b in enumerate(BOOKINGS, 1):
        msg += f"{i}. ID:{b['id']} | {b['name']} | {b['phone']}\n"

    await update.message.reply_text(msg)

# ===== RUN =====
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("data", data))
app.add_handler(CallbackQueryHandler(button_handler))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

print("🚀 BOT LIVE...")
app.run_polling()
