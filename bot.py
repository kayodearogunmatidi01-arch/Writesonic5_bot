import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI

# Load environment variables
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
AI_API_KEY = os.getenv("AI_API_KEY")

# Initialize AI Client (Using OpenAI as an example)
ai_client = OpenAI(api_key=AI_API_KEY)

# Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "🤖 **Welcome to Writesonic5_bot!**\n\n"
        "I am your AI writing assistant. I can help you:\n"
        "✨ Generate content & SEO articles\n"
        "✍️ Rewrite & paraphrase text\n"
        "📝 Summarize documents\n"
        "🛠️ Fix grammar, write emails, ads, and social posts!\n\n"
        "Just type what you want me to do (e.g., 'Write an email asking for a day off' or 'Fix the grammar of this sentence: ...')."
    )
    await update.message.reply_text(welcome_text, parse_mode="Markdown")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    # Send a typing action so the user knows the bot is working
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    try:
        # AI Prompt engineering to fit your bot's personality
        response = ai_client.chat.completions.create(
            model="gpt-4o-mini", # Or your preferred model
            messages=[
                {"role": "system", "content": "You are Writesonic5_bot, an expert AI writing assistant. You generate high-quality content, rewrite text, paraphrase, summarize, fix grammar, and create SEO-friendly articles, emails, ads, and social media posts instantly."},
                {"role": "user", "content": user_text}
            ]
        )
        bot_response = response.choices[0].message.content
    except Exception as e:
        bot_response = "Sorry, I ran into an error processing your request. Please try again later."
        logging.error(f"Error: {e}")

    await update.message.reply_text(bot_response)

def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Run the bot using polling
    application.run_polling()

if __name__ == '__main__':
    main()
