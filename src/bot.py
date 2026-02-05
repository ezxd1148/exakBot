'''
Unrefined Baseline for exakBot.src.bot (Ugly)

- Today's goal: make it work (Done)
- 5/2 goal: clean up code, modularize, document, also implement logging (In Progress)
'''

# import libraries

import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# analyzer imports

import analyzer.normalize as normalize # normalize.py

# loads .env from current directory

load_dotenv()

## env config

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    raise RuntimeError("Missing TELEGRAM_BOT_TOKEN in Environment Variable")

# main 

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

#temporary for testing
#async def get_link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#    context.user_data['WAITING_FOR_LINK'] = True
#    await update.message.reply_text("Please send me the link you want to analyze.")


async def separate_url(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Docstring for separate_url
    
    :param update: Description
    :type update: Update
    :param context: Description
    :type context: ContextTypes.DEFAULT_TYPE (AI guess)

    """

    #temporary for testing
    #if not context.user_data.get("WAITING_FOR_LINK", False):
    #    return  # ignore messages if not waiting for a link

    if not update.message or not update.message.text:
        return  # ignore non-text messages
    
    entities = update.message.parse_entities(["url", "text_link"])
    
    
    unique_urls = set(entities.values())

    status_msg = await update.message.reply_text(f"Found {len(unique_urls)} link(s)")
    
    # extract URL from entities
    # for entity in entities:
    #    if entity.type == "text_link":
    #        urls.append(entity.url)
    #    if entity.type == "url":
    #        urls.append(update.message.text[entity.offset: entity.offset + entity.length])
    
    # check if URL was found
    # if not urls:
    #    await update.message.reply_text("No valid link found in the message. Please send a valid link.")
    #    return

    await update.message.reply_text("Analyzing the link, please wait...")

    urls = []

    #loop thru all the urls found (usually just one)
    for url_candidate in unique_urls:
        try:
            normalized_link = normalize.normalize_link(url_candidate)
            # await update.message.reply_text(f"Normalized Link: {normalized_link}") - temporary for testing
            urls.append(normalized_link)
        except ValueError as ve:
            await update.message.reply_text(str(ve))

    # Added summary as of now - temporary for testing
    summary = "\n".join(urls)
    await context.bot.edit_message_text(
        chat_id=update.effective_chat.id,
        message_id=status_msg.message_id,
        text=f"Summary:\n{summary}",
        parse_mode=ParseMode.MARKDOWN
    )
    # context.user_data['WAITING_FOR_LINK'] = False - temporary for testing

## bot setup
app = ApplicationBuilder().token(TOKEN).build() # REMINDER TO CHANGE TO ENV (Done)

### command handlers

app.add_handler(CommandHandler("start", start_bot))
#app.add_handler(CommandHandler("scan", get_link)) - temporary for testing
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, separate_url))

### run bot
app.run_polling()