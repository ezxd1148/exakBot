'''
Unrefined Baseline for exakBot.src.bot (Ugly)

- Today's goal: make it work (Done)
- 5/2 goal: clean up code, modularize, document, also implement logging (In Progress)
'''

# import libraries

import logging
import config
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# analyzer imports

import analyzer.normalize as normalize # normalize.py
import analyzer.resolver as resolver # resolver.py 
import analyzer.scoring as scoring # scoring.py
# get token from config (REMINDER TO CHANGE TO ENV)
TOKEN = config.TELEGRAM_BOT_TOKEN

# main 

results = []

## logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s' ,
    level=logging.INFO
)

## functions

async def start_bot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        '''
        Welcome to exakbot.
Paste a link you don’t trust, and I’ll tell you how sketchy it looks.

Send one of these:

A link (example: https://…)

A forwarded message containing a link

I’ll reply with a risk score, the real destination after redirects, and the main red flags.
If it looks risky, I’ll also tell you what to do next.

Triage only. No “100% safe” promises, because reality doesn’t work like that.
        '''
    )

async def separate_url(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Docstring for separate_url
    
    :param update: Description
    :type update: Update
    :param context: Description
    :type context: ContextTypes.DEFAULT_TYPE (AI guess)

    """

    if not update.message or not update.message.text:
        return  # ignore non-text messages
    
    entities = update.message.parse_entities(["url", "text_link"])
    
    
    unique_urls = set(entities.values())

    status_msg = await update.message.reply_text(f"Found {len(unique_urls)} link(s)")

    await update.message.reply_text("Analyzing the link, please wait...")

    urls = []

    #loop thru all the urls found (usually just one)
    for url_candidate in unique_urls:
        try:
            normalized_link = normalize.normalize_link(url_candidate)
            urls.append(normalized_link)
        except ValueError as ve:
            await update.message.reply_text(str(ve))

    # risk scoring here
    for url in urls:
        score = scoring.score_url(url)
        results.append(f"URL: {url}\nRisk Score: {score}/60")

    # Added summary 
    summary = "\n".join(results)
    await context.bot.edit_message_text(
        chat_id=update.effective_chat.id,
        message_id=status_msg.message_id,
        text=f"Summary:\n{summary}",
        parse_mode=ParseMode.MARKDOWN
    )

## bot setup
app = ApplicationBuilder().token(TOKEN).build()

### command handlers

app.add_handler(CommandHandler("start", start_bot))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, separate_url))

### run bot
app.run_polling()