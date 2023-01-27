from Credentials import BOT_TOKEN
from Lib.handlers import *
import logging
from telegram.ext import ApplicationBuilder

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)


if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handlers(handlers)
    application.run_polling()
