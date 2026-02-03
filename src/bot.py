'''
Unrefined Baseline for exakBot.src.bot (Ugly)

- Today's goal: make it work (Done)
'''

# import libraries

import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# analyzer imports

# import analyzer.normalize as normalize -- placeholder for actual normalization module

# loads .env from current directory

load_dotenv()

## env config

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    raise RuntimeError("Missing TELEGRAM_BOT_TOKEN in Environment Variable")

# main 

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

async def get_link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data['WAITING_FOR_LINK'] = True
    await update.message.reply_text("Please send me the link you want to analyze.")


async def separate_url(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.user_data.get("WAITING_FOR_LINK", False):
        return  # ignore messages if not waiting for a link

    if update.message is None:
        return
    
    if update.message.text is None:
        await update.message.reply_text("Send a text link (http/https).")
        return
    
    entities = update.message.entities or []
    url_candidate = None
    
    # extract URL from entities
    for entity in entities:
        if entity.type == "text_link":
            url_candidate = entity.url
            break
        if entity.type == "url":
            url_candidate = update.message.text[entity.offset: entity.offset + entity.length]
            break
    
    # check if URL was found
    if url_candidate is None:
        await update.message.reply_text("No valid link found in the message. Please send a valid link.")
        return
    
    await update.message.reply_text("Analyzing the link, please wait...")
    
    # normalized_link = normalize.normalize_link(url_candidate) -- placeholder for actual normalization
    # await update.message.reply_text(normalized_link) -- only after normalize is implemented
    
    await update.message.reply_text(f"Received link: {url_candidate}")
    context.user_data['WAITING_FOR_LINK'] = False

## bot setup
app = ApplicationBuilder().token(TOKEN).build() # REMINDER TO CHANGE TO ENV (Done)

### command handlers

app.add_handler(CommandHandler("start", start_bot))
app.add_handler(CommandHandler("scan", get_link))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, separate_url))

### run bot
app.run_polling()