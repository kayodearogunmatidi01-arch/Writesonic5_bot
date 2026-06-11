def main():
    # Double-check that tokens are loaded
    if not TELEGRAM_TOKEN:
        print("❌ CRITICAL ERROR: TELEGRAM_TOKEN environment variable is missing!", flush=True)
        return
    if not AI_API_KEY:
        print("❌ CRITICAL ERROR: AI_API_KEY environment variable is missing!", flush=True)
        return

    print("🚀 Starting Writesonic5_bot polling...", flush=True)
    
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    application.run_polling()

if __name__ == '__main__':
    main()
