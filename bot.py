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

    # ===== BOOKING FLOW =====
    if "done" not in context.user_data:

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
                        f"Name: {data['name']}\n"
                        f"Phone: {data['phone']}\n"
                        f"{data['checkin']} → {data['checkout']}\n"
                        f"{data['members']} Members\n"
                        f"{data['type']}\n"
                        f"AC: {data['ac']}"
                    ),
                    reply_markup=reply_markup
                )

                await update.message.reply_text("✅ Booking sent successfully")
                context.user_data["done"] = True

            else:
                await update.message.reply_text("❌ Answer yes or no")

    # ===== SMART + ELIF COMBINED SYSTEM =====
    else:

        words = text.split()

        ask_price = any(w in words for w in ["price","cost","rent","charge"])
        ask_location = any(w in words for w in ["location","where","address","place"])
        ask_time = any(w in words for w in ["time","checkin","checkout"])
        ask_availability = any(w in words for w in ["available","vacant","rooms","free"])
        ask_payment = any(w in words for w in ["pay","payment","upi","gpay","phonepe"])
        ask_facility = any(w in words for w in ["wifi","parking","food","water","lift","ac"])
        ask_distance = any(w in words for w in ["distance","near","far"])
        ask_quality = any(w in words for w in ["clean","neat","hygiene"])
        ask_urgency = any(w in words for w in ["today","now","urgent","fast"])
        ask_people = any(w in words for w in ["family","bachelor","friends"])

        if ask_price:
            if "ac" in words:
                await update.message.reply_text("💰 AC rooms cost higher than Non-AC.")
            else:
                await update.message.reply_text("💰 Price depends on members & availability.")

        elif ask_availability:
            if ask_urgency:
                await update.message.reply_text("⚡ Few rooms left today!")
            else:
                await update.message.reply_text("📊 Rooms available based on demand.")

        elif ask_location:
            await update.message.reply_text("📍 Tirupati (3-4 KM from railway station)")

        elif ask_time:
            await update.message.reply_text("🕒 24-hour check-in/check-out system.")

        elif ask_payment:
            await update.message.reply_text("📲 UPI / Cash accepted")

        elif ask_facility:
            await update.message.reply_text("🏨 AC / Parking / Water available")

        elif ask_distance:
            await update.message.reply_text("📍 3-4 KM from station")

        elif ask_quality:
            await update.message.reply_text("✨ Clean and neat rooms")

        elif ask_people:
            await update.message.reply_text("👨‍👩‍👧‍👦 Family & Bachelors allowed")

        # ===== FALLBACK OLD RESPONSES =====
        elif "parking" in text:
            await update.message.reply_text("🚗 Parking available")

        elif "wifi" in text:
            await update.message.reply_text("📶 WiFi may be available")

        elif "food" in text:
            await update.message.reply_text("Food not available, kitchen available")

        elif "water" in text:
            await update.message.reply_text("RO drinking water available")

        else:
            await update.message.reply_text("🤖 Ask something like price, location, rooms, etc.")

# ===== RUN =====
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

print("🚀 BOT LIVE...")
app.run_polling()
