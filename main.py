from telegram.ext import Updater, Filters
from telegram.ext import CommandHandler, MessageHandler, CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, InputMediaPhoto, Update,KeyboardButton, ReplyKeyboardMarkup
from db_connect import RecordManager
import threading
import time
from scraper import Scraper


class Bot:
    # Send Delay
    delay = 240

    # Admin ID
    admin_id = 0

    driver_is_busy = False
    _driver = None

    def __init__(self,token = "5058044017:AAE5gy_TTrpIdDHBoJKXb2pjAE8sy6HnrLg"):
        self.updater = Updater(token=token, use_context=True)
        self.bot = self.updater.bot
        # self.manager = RecordManager()
        
    def start(self, update: Update, context: CallbackContext, *args, **kwargs) -> None:
        """Sends a message with three inline buttons attached."""

        sender = update.effective_chat.id
        buttons = [
           [KeyboardButton("SYMBOL"),KeyboardButton("OVERALL INDEX"),KeyboardButton("CLOSED/LAST TRADED PRICE"),]
        ]
        reply_markup = ReplyKeyboardMarkup(buttons)
        self.bot.send_message(sender, 'Please choose:', reply_markup=reply_markup)


    def symbol(self, update) -> None:
        """Sends a message with three inline buttons attached."""
        sender = update.effective_chat
        buttons = [[
            KeyboardButton("Back")
        ]]
        reply_markup = ReplyKeyboardMarkup(buttons)
        self.manager.set_last_command(sender, "symbol")
        self.bot.send_message(sender.id, "نام کامل را وارد کنید", reply_markup=reply_markup)

    def handler(self, update, context):
        self.manager = RecordManager()

        sender = update.effective_chat
        message = update.effective_message.text
        condition = self.manager.get_last_command(sender)
        response = ""
        if condition == "symbol":
            if message == "Back":
                self.manager.set_last_command(sender, "start")
                self.start(update, context)

            else:
                try:
                    response = self.manager.get_symbol_by_name(message)
                    self.manager.set_last_command(sender, "start")
                except:
                    self.manager.set_last_command(sender, "symbol")
                    response = "پیدا نشد دوباره امتحان کنید"
                self.bot.send_message(sender.id, response)

        elif message == "SYMBOL":
            self.symbol(update)
        elif message == "OVERALL INDEX":
            pass
        elif message == "CLOSED/LAST TRADED PRICE":
            pass
        else:
            self.start(update, context)
        self.manager.done()


    def listen(self):
        dispatcher = self.updater.dispatcher
        dispatcher.add_handler(CommandHandler('start', self.start))
        dispatcher.add_handler(MessageHandler(Filters.text, self.handler))


        self.updater.start_polling()
        self.get_new_price()
        self.updater.idle()
    

    def get_new_price(self, *args):
    #این روش توی sqlite جواب نمیده به همین خاطر از روش معمول استفاده میکنم

    #     manager = args[0]
    #     scraper = Scraper()
    #     while True:
    #         new_prices = scraper.update_price()
    #         manager.set_new_records(new_prices)
    #         time.sleep(60)


        # scraper = Scraper()
        # new_prices = scraper.update_price()
        # self.manager.set_new_records(new_prices)
        pass

            



bot = Bot()
#این روش توی sqlite جواب نمیده به همین خاطر از روش معمول استفاده میکنم
# scraping = threading.Thread(target=bot.get_new_price, args=(bot.manager,))
# scraping.start()
bot.listen()
