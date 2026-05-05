import os
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, 
    filters, ContextTypes, CallbackQueryHandler
)

# Core & Config
from config import BOT_TOKEN, LEADERBOARD_POST_TIME, GROUP_ID
from database import init_db

# Features
from features.verification import new_member_handler, verification_callback
from features.karma import karma_handler, my_karma, leaderboard, shop, buy
from features.moderation import moderation_filter, mute, unmute, ban, lockdown, unlock
from features.insights import track_message_for_insights, activityreport, moodreport
from features.utility import poll, remind, tldr, faq_auto_responder

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Basic start command."""
    if update.message:
        await update.message.reply_text("🤖 **AI Group Manager is Online!**\nUse /help to see available commands.", parse_mode="Markdown")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Help command outlining features."""
    help_text = (
        "🛠 **Commands Available:**\n\n"
        "**Economy:**\n"
        "/karma - Check your Karma & Badges\n"
        "/leaderboard - See the top 5 members\n"
        "/shop - View the Karma shop\n"
        "/buy - Purchase items from the shop\n\n"
        "**Utility:**\n"
        "/tldr [N] - Get an AI summary of the last N messages\n"
        "/poll \"Q\" \"Opt1\" \"Opt2\" - Create a poll (Admins)\n"
        "/remind <sec> <msg> - Schedule a reminder (Admins)\n\n"
        "**Moderation (Admins):**\n"
        "/lockdown & /unlock - Freeze the chat\n"
        "/mute, /unmute, /ban - Message replies\n\n"
        "**Insights (Admins):**\n"
        "/activityreport - View top member analytics\n"
        "/moodreport - AI analysis of current group mood"
    )
    if update.message:
        await update.message.reply_text(help_text, parse_mode="Markdown")

async def main_message_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Master router for all standard text messages. 
    Order: Moderation -> Tracking -> FAQ -> Karma AI
    """
    # 1. Moderation & Anti-Spam (Stops execution if deleted)
    was_deleted = await moderation_filter(update, context)
    if was_deleted:
        return
        
    # 2. Track message for insights buffer & activity count
    track_message_for_insights(update)
    
    # 3. FAQ Auto-Responder Check
    await faq_auto_responder(update, context)
    
    # 4. Karma AI Analysis
    await karma_handler(update, context)

async def post_daily_leaderboard(context: ContextTypes.DEFAULT_TYPE):
    """JobQueue function to automatically post the leaderboard."""
    if not GROUP_ID:
        return
        
    from features.karma import get_top_users
    top_users = get_top_users(5)
    if not top_users:
        return
        
    msg = "🏆 **Daily Leaderboard Update** 🏆\n\n"
    for i, (username, karma) in enumerate(top_users, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "🏅"
        msg += f"{medal} {i}. {username or 'Unknown'} — {karma} Karma\n"
        
    try:
        await context.bot.send_message(chat_id=GROUP_ID, text=msg, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Failed to post daily leaderboard: {e}")

def main():
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN is missing! Please set it in your .env file.")
        return

    # Initialize SQLite Database
    init_db()
    
    # Build Application
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # 1. Joins & Verification
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, new_member_handler))
    app.add_handler(CallbackQueryHandler(verification_callback, pattern="^verify_"))

    # 2. Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    
    # Economy
    app.add_handler(CommandHandler("karma", my_karma))
    app.add_handler(CommandHandler("leaderboard", leaderboard))
    app.add_handler(CommandHandler(["shop", "store"], shop))
    app.add_handler(CommandHandler("buy", buy))
    
    # Moderation
    app.add_handler(CommandHandler("mute", mute))
    app.add_handler(CommandHandler("unmute", unmute))
    app.add_handler(CommandHandler("ban", ban))
    app.add_handler(CommandHandler("lockdown", lockdown))
    app.add_handler(CommandHandler("unlock", unlock))
    
    # Insights
    app.add_handler(CommandHandler("activityreport", activityreport))
    app.add_handler(CommandHandler("moodreport", moodreport))
    
    # Utility
    app.add_handler(CommandHandler("poll", poll))
    app.add_handler(CommandHandler("remind", remind))
    app.add_handler(CommandHandler("tldr", tldr))

    # 3. Main Text Router (Filters ALL messages)
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), main_message_router))

    # 4. Scheduled Jobs (JobQueue)
    # Post leaderboard every day at the configured time
    if app.job_queue:
        try:
            from datetime import time
            hour, minute = map(int, LEADERBOARD_POST_TIME.split(':'))
            run_time = time(hour=hour, minute=minute)
            app.job_queue.run_daily(post_daily_leaderboard, time=run_time)
            logger.info(f"Scheduled daily leaderboard at {LEADERBOARD_POST_TIME}")
        except Exception as e:
            logger.error(f"Failed to schedule leaderboard job: {e}")

    # Start Polling
    logger.info("Bot is starting...")
    app.run_polling()

if __name__ == "__main__":
    main()
