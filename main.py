import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# === HOUSE PLAN DATABASE ===
# In a real scenario, this could be a JSON file or a database
PLANS = {
    "1bhk": {"name": "Cozy 1 BHK", "size": "600 sq ft", "desc": "Perfect for bachelors or small families."},
    "2bhk": {"name": "Modern 2 BHK", "size": "1000 sq ft", "desc": "Ideal for a family of 3-4 members."},
    "3bhk": {"name": "Luxury 3 BHK", "size": "1500 sq ft", "desc": "Spacious with a master bedroom."}
}

# === COMMAND HANDLERS ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🏠 1 BHK Plan", callback_data="1bhk")],
        [InlineKeyboardButton("🏡 2 BHK Plan", callback_data="2bhk")],
        [InlineKeyboardButton("🏘️ 3 BHK Plan", callback_data="3bhk")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🏗️ *Welcome to PlanDesignBot!*\nI am your House Plan Assistant.\n\nPlease select a plan type:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Acknowledge the button press

    plan_key = query.data
    plan = PLANS.get(plan_key)

    if plan:
        response = (f"📐 *{plan['name']}*\n"
                    f"📏 *Size:* {plan['size']}\n"
                    f"📝 *Description:* {plan['desc']}\n\n"
                    f"💡 *Tip:* Send /contact to talk to an architect.")
        await query.edit_message_text(response, parse_mode="Markdown")
    else:
        await query.edit_message_text("Sorry, I couldn't find that plan.")

async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📧 Please email us: designs@plandesignbot.com or visit our website.")

# === MAIN FUNCTION ===
def main():
    # Railway will provide the PORT, but the bot uses polling, so we just use the token
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        print("Error: TELEGRAM_BOT_TOKEN not set!")
        return

    app = Application.builder().token(token).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("contact", contact))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
