import telebot, asyncdispatch, logging, options, strutils

var L = newConsoleLogger(fmtStr="$levelname, [$time] ")
addHandler(L)

# Remember to strip your secret key to avoid HTTP errors
const API_KEY = strip(slurp("secret.key"))

proc updateHandler(bot: TeleBot, update: Update): Future[bool] {.async.} =
  if not update.message.isNil:
    let response = update.message
    if response.text.len > 0:
      let text = response.text
      # echo "Received message: " & text & " from: " & response.chat.id.string
      discard await bot.sendMessage(response.chat.id, "Echo: " & text, parseMode = "markdown", disableNotification = true, replyParameters = ReplyParameters(messageId: response.messageId))
  return true

proc startCommandHandler(bot: TeleBot, command: Command): Future[bool] {.async.} =
  if not command.message.fromUser.isNil:
    let userName = command.message.fromUser.firstName
    discard await bot.sendMessage(command.message.chat.id, "Hello " & userName & "! Welcome to the Echo Bot. Send me any text and I will echo it back to you.", parseMode = "markdown", disableNotification = true, replyParameters = ReplyParameters(messageId: command.message.messageId))
  return true

when isMainModule:c
  when defined(local):
    let bot = newTeleBot(API_KEY, "http://127.0.0.1:8081") # For local API server testing
  else:
    let bot = newTeleBot(API_KEY)

  # bot.setLogLevel(levelDebug) # Enable debug logging for development

  bot.onUpdate(updateHandler)
  bot.onCommand("start", startCommandHandler) # Register /start command handler

  echo "Bot started. Polling for updates..."
  bot.poll(timeout = 300)
