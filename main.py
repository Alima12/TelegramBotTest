from telegram.ext import Updater, Filters
from telegram.ext import CommandHandler, MessageHandler, CallbackContext
from telegram import Update,KeyboardButton, ReplyKeyboardMarkup
from db_connect import RecordManager
from scraper import Scraper


class Bot:
    def __init__(self,token = "5058044017:AAE5gy_TTrpIdDHBoJKXb2pjAE8sy6HnrLg"):
        self.updater = Updater(token=token, use_context=True)
        self.bot = self.updater.bot
        self.manager = RecordManager()
        
    def start(self, update: Update, context: CallbackContext, *args, **kwargs) -> None:
        sender = update.effective_chat.id
        buttons = [
           [KeyboardButton("SYMBOL"),KeyboardButton("OVERALL INDEX"),KeyboardButton("CLOSED/LAST TRADED PRICE"),]
        ]
        reply_markup = ReplyKeyboardMarkup(buttons)
        self.bot.send_message(sender, 'Please choose:', reply_markup=reply_markup)


    def symbol(self, update) -> None:
        sender = update.effective_chat
        buttons = [[
            KeyboardButton("Back")
        ]]
        reply_markup = ReplyKeyboardMarkup(buttons)
        self.manager.set_last_command(sender, "symbol")
        self.bot.send_message(sender.id, "نام کامل را وارد کنید", reply_markup=reply_markup)

    def price(self, update) -> None:
        sender = update.effective_chat
        buttons = [[
            KeyboardButton("Back")
        ]]
        reply_markup = ReplyKeyboardMarkup(buttons)
        self.manager.set_last_command(sender, "price")
        self.bot.send_message(sender.id, " لطفا نماد را وارد کنید", reply_markup=reply_markup)

    def handler(self, update, context):
        self.manager = RecordManager()

        sender = update.effective_chat
        message = update.effective_message.text
        condition = self.manager.get_last_command(sender)
        response = ""

        # میشد از switch case استفاده کرد ولی بخاطر نصب نبودن پایتون 3.10  امکان استفاده نداشتم
        if condition == "symbol":
            if message == "Back":
                self.manager.set_last_command(sender, "start")
                self.start(update, context)
            else:
                try:
                    response = self.manager.get_symbol_by_name(message)
                except:
                    self.manager.set_last_command(sender, "symbol")
                    response = "پیدا نشد دوباره امتحان کنید"
                self.bot.send_message(sender.id, response)

        elif condition == "price":
            if message == "Back":
                self.manager.set_last_command(sender, "start")
                self.start(update, context)
            else:
                try:
                    response = self.manager.get_price_by_symbol(message)
                    self.bot.send_message(sender.id, f"""نماد: {response["Symbol"]}
نام کامل: {response["FullName"]}
آخرین قیمت: {response["LastPrice"]}
قیمت پایانی: {response["ClosedPrice"]}
                """)

                except:
                    self.manager.set_last_command(sender, "price")
                    response = "پیدا نشد دوباره امتحان کنید"
                    self.bot.send_message(sender.id, response)



        elif message == "SYMBOL":
            self.symbol(update)
        elif message == "OVERALL INDEX":
            response = self.manager.get_last_overall()
            self.bot.send_message(sender.id, f"""{response["count"]}
درصد : {response["percent"]}
            """)
        elif message == "CLOSED/LAST TRADED PRICE":
            self.price(update)
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


        scraper = Scraper()
        new_prices = scraper.update_price()
        new_overall = scraper.get_overall()
        self.manager.set_overall(new_overall["count"], new_overall["percent"])
        self.manager.set_new_records(new_prices)
        self.manager.done()
        

            



bot = Bot()
#این روش توی sqlite جواب نمیده به همین خاطر از روش معمول استفاده میکنم
# scraping = threading.Thread(target=bot.get_new_price, args=(bot.manager,))
# scraping.start()
bot.listen()
