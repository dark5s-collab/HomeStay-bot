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

    elif query.data == "call_owner":
        await query.answer("📞 8121451238", show_alert=True)

# ====== MAIN REPLY FUNCTION ======
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

    # STEP 7: AC
    elif "ac" not in context.user_data:
        if "yes" in text or "no" in text:
            context.user_data["ac"] = text

            data = context.user_data
            booking_id = len(BOOKINGS) + 1
            data["id"] = booking_id
            BOOKINGS.append(data.copy())

            # ✅ BUTTONS (WITH CALL)
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

            # OWNER NOTIFICATION
            await context.bot.send_message(
                chat_id=OWNER_ID,
                text=(
                    "🚨🚨 NEW BOOKING ALERT 🚨🚨\n\n"
                    f"🆔 ID: {data['id']}\n"
                    f"👤 {data['name']}\n"
                    f"📅 {data['checkin']} → {data['checkout']}\n"
                    f"👥 {data['members']} Members\n"
                    f"👪 {data['type']}\n"
                    f"❄️ AC: {data['ac']}\n\n"
                    "⚠️ Choose action 👇"
                ),
                reply_markup=reply_markup
            )

            # USER RESPONSE
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
                "Advance ₹1000\n\n"
                "📲 PAYMENT:\n"
                "GPay / PhonePe / Cash"
            )
        else:
            await update.message.reply_text("❌ Answer yes or no")

    # ===== AFTER FLOW =====
    else:
        if "location" in text or "where" in text:
            await update.message.reply_text("📍 Tirupati (3-4 KM from railway station)")
        elif "price" in text or "cost" or "rate" in text:
            await update.message.reply_text("📍 Tirupati (3-4 KM from railway station)")
        elif "near tirumala" in text:
            await update.message.reply_text("Yes, very close to Tirumala")
        elif "quiet area" in text:
            await update.message.reply_text("Yes, the area is quiet and safe")
        elif "road access" in text:
            await update.message.reply_text("Yes, easily accessible by road")
        elif "shops nearby" in text:
            await update.message.reply_text("Yes, grocery stores and restaurants are nearby")
        elif "public transport" in text:
            await update.message.reply_text("Public transport is very easy to find nearby")
        elif "easy to find" in text:
            await update.message.reply_text("Yes, homestay is easy to locate with landmarks")
        elif "parking outside" in text:
            await update.message.reply_text("Yes, parking is available near the homestay")
        elif "security" in text:
            await update.message.reply_text("Don't know about security")
        elif "night access" in text:
            await update.message.reply_text("Don't know if safe at night")
        elif "homestay neat" in text or "clean" in text:
            await update.message.reply_text("🧼 Rooms are very clean and neat")
        elif "rooms clean" in text:
            await update.message.reply_text("Yes, rooms are clean and tidy")
        elif "bathroom clean" in text:
            await update.message.reply_text("Yes, bathrooms are clean and hygienic")
        elif "wifi" in text:
            await update.message.reply_text("Depends on the homestay, WiFi availability may vary")
        elif "geyser" in text:
            await update.message.reply_text("🔥 24/7 hot water available")
        elif "cooking" in text:
            await update.message.reply_text("Induction stove is available for cooking")
        elif "drinking water" in text or "water" in text:
            await update.message.reply_text("💧 RO filtered drinking water is available")
        elif "dining clean" in text:
            await update.message.reply_text("Yes, dining tables and chairs are clean")
        elif "breakfast" in text or "lunch" in text or "dinner" in text or "food" in text:
            await update.message.reply_text("🍽️ Kitchen available; food not included")
        elif "fans" in text:
            await update.message.reply_text("Yes, fans are available in all rooms")
        elif "ac" in text:
            await update.message.reply_text("Yes, AC is available if AC room is booked")
        elif "bed sheets" in text:
            await update.message.reply_text("Yes, bed sheets are clean and changed regularly")
        elif "towels" in text:
            await update.message.reply_text("No, towels are not provided")
        elif "garden" in text:
            await update.message.reply_text("No, there is no garden or outdoor space")
        elif "balcony" in text:
            await update.message.reply_text("No, there is no balcony or terrace")
        elif "pets" in text:
            await update.message.reply_text("No, pets are not allowed")
        elif "smoking" in text:
            await update.message.reply_text("Smoking is not allowed")
        elif "parking inside" in text or "parking" in text:
            await update.message.reply_text("🚗 Parking inside the homestay compound is available")
        elif "payment methods" in text:
            await update.message.reply_text("Payment can be made via Cash, UPI, or Paytm")
        elif "advance payment" in text or "advance" in text:
            await update.message.reply_text("Advance payment of ₹1000 is required")
        elif "refund" in text:
            await update.message.reply_text("Refund policy depends on the homestay rules")
        elif "upi" in text:
            await update.message.reply_text("You can pay via UPI using PhonePe or Google Pay")
        elif "cash payment" in text:
            await update.message.reply_text("Cash payment is accepted at check-in")
        elif "partial payment" in text:
            await update.message.reply_text("Partial payment is accepted if agreed with the homestay")
        elif "online payment" in text:
            await update.message.reply_text("Online payment via UPI or bank transfer is accepted")
        elif "payment confirmation" in text:
            await update.message.reply_text("Payment confirmation will be provided immediately after payment")
        elif "no advance" in text:
            await update.message.reply_text("Advance payment of ₹1000 is required; rest can be paid on arrival")
        elif "payment help" in text or "book" in text:
            await update.message.reply_text("For payment assistance, contact the homestay directly")
        else:
            await update.message.reply_text("🤖 Ask me about: price, location, rooms, AC, WiFi, geyser, parking, food, payment")

# ===== DATA =====
async def data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("❌ Not authorized")
        return

    msg = "📊 BOOKINGS:\n\n"
    for i, b in enumerate(BOOKINGS, 1):
        msg += f"{i}. ID:{b['id']} | {b['name']} | AC:{b['ac']}\n"

    await update.message.reply_text(msg)

# ===== RUN =====
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("data", data))
app.add_handler(CallbackQueryHandler(button_handler))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

print("🚀 BOT LIVE...")
app.run_polling()
