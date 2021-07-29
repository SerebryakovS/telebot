#!/usr/bin/python
import os
import uuid
import telebot

BOT_TOKEN    = ""; # telegram bot token(given by botFather)
BOT_INTERVAL =  1; # long-pooling check packet interval
BOT_TIMEOUT  = 10; # long-pooling connection timeout
BOT_WELCOME  = ""; # user will see this message first
BOT_NAME     = ""; # (optional) name for the bot

class question(object):
    opts_limit = 4;
    def __init__(self,question_string):
        self.question = str(question_string);
        self.question_id = uuid.uuid4().hex;
        self.options = list();
    def add_option(self,option):
        if len(self.options) < opts_limit:
            self.options.append(option);
        else:
            print("[question:",self.question_id,"] => options limit reached");
    def form_question_simplbuttons(self,markup):
        but_opt = [];
        opt_len = len(self.options);
        if opt_len <= 1:
            print("[question:",self.question_id,"] => options list is not full");
            return;
        for index in range(opt_len):
            but_opt.append(telebot.types.InlineKeyboardButton(
                str(option[index]), callback_data=str(self.question_id)+":"+str(index)));
        if opt_len == 2 or opt_len == 4:
            markup.row(but_opt[0], but_opt[1]);
        if opt_len == 3:
            markup.row(but_opt[2]);
        if opt_len == 4:
            markup.row(but_opt[2], but_opt[3]);

    def form_question_checksbox(self,markup):
        pass;
    def form_question(self,qs_type):
        # HERE ONE FROM ABOVE HANDLERS SELECTED

def telebot_decorators():
    @bot.message_handler(commands=["start"])
    def send_welcome(message):
        # do something with user_id
        user_id = message.from_user.id;
        markup = telebot.types.InlineKeyboardMarkup();
        bot.send_message(message.chat.id,BOT_WELCOME,reply_markup=markup);







def bot_actions(bot):

    @bot.callback_query_handler(func=lambda call: True)
    def handle(call):
        try:
            callback_data = str(call.data).split('_');
            user_id = call.message.chat.id;
            qs_index = int(callback_data[0]);
            if int(qs_index) >= 0:
                USR_STATUS[user_id].update({qs_index:callback_data[1]});
            qs_index+=1;
            markup = telebot.types.InlineKeyboardMarkup();
            if qs_index >= len(QUESTIONS):
                counter = [0 for i in range(len(QUESTIONS)+1)];
                print(str(user_id),":",str(USR_STATUS[user_id]))
                for index in USR_STATUS[user_id].values():
                    counter[int(index)-1] += 1;
                #del USR_STATUS[user_id];
                counter_max = max(counter);
                mini_counter = 0; max_srore = [];
                for elem_idx in range(len(counter)):
                    if counter[elem_idx] == counter_max:
                        mini_counter+=1;
                        max_srore.append(elem_idx+1);
                if (mini_counter == 1):
                    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id);
                    bot.send_message(call.message.chat.id, '%s%s'%(RESPONSES[0][counter.index(counter_max)],
                                                                RESPONSES[1]));
                elif (mini_counter > 1):
                    buttonA = telebot.types.InlineKeyboardButton(max_srore[0], callback_data="6_"+str(max_srore[0]));
                    buttonB = telebot.types.InlineKeyboardButton(max_srore[1], callback_data="6_"+str(max_srore[1]));
                    markup.row(buttonA, buttonB);
                    bot.edit_message_media(chat_id=call.message.chat.id,message_id=call.message.message_id,
                                        media=telebot.types.InputMediaPhoto(open('5.JPG', 'rb')),reply_markup=markup);
                    bot.edit_message_caption(chat_id=call.message.chat.id,message_id=call.message.message_id,
                                            caption=QUESTIONS_ADD[0]["qs"]+
                                            '\n%d. '%(max_srore[0])+QUESTIONS_ADD[0]["opt"][max_srore[0]-1]+
                                            '\n%d. '%(max_srore[1])+QUESTIONS_ADD[0]["opt"][max_srore[1]-1],
                                            reply_markup=markup);
            else:
                form_question(markup,QUESTIONS[qs_index],str(qs_index));
                if (qs_index == 0):
                    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id);
                    bot.send_photo(chat_id=call.message.chat.id,
                                photo=open('0.JPG', 'rb'),
                                caption=QUESTIONS[qs_index]["qs"]+
                                '\n1. '+QUESTIONS[qs_index]["opt"][0]+
                                '\n2. '+QUESTIONS[qs_index]["opt"][1]+
                                '\n3. '+QUESTIONS[qs_index]["opt"][2]+
                                '\n4. '+QUESTIONS[qs_index]["opt"][3],
                                reply_markup=markup);
                    return;
                bot.edit_message_media(chat_id=call.message.chat.id,message_id=call.message.message_id,
                                    media=telebot.types.InputMediaPhoto(open(str(qs_index)+'.JPG', 'rb')),reply_markup=markup);
                bot.edit_message_caption(chat_id=call.message.chat.id,message_id=call.message.message_id,
                                        caption=QUESTIONS[qs_index]["qs"]+
                                        '\n1. '+QUESTIONS[qs_index]["opt"][0]+
                                        '\n2. '+QUESTIONS[qs_index]["opt"][1]+
                                        '\n3. '+QUESTIONS[qs_index]["opt"][2]+
                                        '\n4. '+QUESTIONS[qs_index]["opt"][3],
                                        reply_markup=markup);
        except Exception as ex:
            print(ex);
def bot_pooling():
    while True:
        bot = telebot.TeleBot(B_TOKN);
        print("New bot created");
        bot_actions(bot);
        print("pooling...");
        try:
            bot.polling(none_stop=True, interval=BOT_INTERVAL, timeout=BOT_TIMEOUT);
        except Exception as ex: #Error in polling
            print("Bot polling failed, restarting in {}sec. Error:\n{}".format(BOT_TIMEOUT, ex))
            time.sleep(BOT_TIMEOUT);
        else: #Clean exit
            bot.stop_polling();
            print("Bot polling loop finished");
            break; #End loop
if __name__ == "__main__":
    bot_pooling();
