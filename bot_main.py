#!/usr/bin/python
import os
import uuid
import telebot
# telegram bot token(given by botFather)
BOT_TOKEN    = "1945088632:AAF5TokYX_nddT-9QBhg2avL-8fVjZeTXMg";
# (optional) name for the bot
BOT_NAME     = "@gentemplate_bot";

class question(object):
    opts_limit = 4;
    def __init__(self,question_string,input_type):
        self.question = str(question_string);
        self.question_id = uuid.uuid4().hex;
        self.options = list();
        self.form_controls = {
            'IB':self.form_question_simplbuttons,
            'IT':self.form_question_text_field,
            'IC':self.form_question_checksbox
        }[input_type];
    @staticmethod
    def generate_questions(filepath):
        questions = list();
        with open(filepath,'r') as qs_file:
            lines = qs_file.readlines();
            for line in lines:
                line = line.split(':');
                if len(line) == 1:
                    questions[-1]['input_type'] = line[0].strip();
                else:
                    if line[0] == 'W':
                        questions.append({'BOT_WELCOME':line[1]});
                    elif line[0] == 'Q':
                        questions.append({'qs':line[1],'opts':[],'input_type':''});
                    elif line[0] == 'O':
                        questions[-1]['opts'].append(line[1]);
        return questions;
    def add_option(self,option):
        if len(self.options) < question.opts_limit:
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
    def form_question_text_field(self,markup):
        pass;

def telebot_decorators(bot,QUESTIONS):
    @bot.message_handler(commands=["start"])
    def send_welcome(message):
        # do something with user_id
        user_id = message.from_user.id;
        markup = telebot.types.InlineKeyboardMarkup();
        button_to_begin = telebot.types.InlineKeyboardButton('НАЧАТЬ', callback_data=str('0'));
        markup.add(button_to_begin);
        bot.send_message(message.chat.id,QUESTIONS[0]['BOT_WELCOME'],reply_markup=markup);

    #@bot.callback_query_handler(func=lambda call: True)
    #def handle(call):
        #try:
            #callback_data = str(call.data).split('_');
            #user_id = call.message.chat.id;


            #qs_index = int(callback_data[0]);
            #if int(qs_index) >= 0:
                #USR_STATUS[user_id].update({qs_index:callback_data[1]});
            #qs_index+=1;

            #markup = telebot.types.InlineKeyboardMarkup();





                #if (mini_counter == 1):
                    #bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id);
                    #bot.send_message(call.message.chat.id, '%s%s'%(RESPONSES[0][counter.index(counter_max)],
                                                                #RESPONSES[1]));
                #elif (mini_counter > 1):
                    #buttonA = telebot.types.InlineKeyboardButton(max_srore[0], callback_data="6_"+str(max_srore[0]));
                    #buttonB = telebot.types.InlineKeyboardButton(max_srore[1], callback_data="6_"+str(max_srore[1]));
                    #markup.row(buttonA, buttonB);
                    #bot.edit_message_media(chat_id=call.message.chat.id,message_id=call.message.message_id,
                                        #media=telebot.types.InputMediaPhoto(open('5.JPG', 'rb')),reply_markup=markup);
                    #bot.edit_message_caption(chat_id=call.message.chat.id,message_id=call.message.message_id,
                                            #caption=QUESTIONS_ADD[0]["qs"]+
                                            #'\n%d. '%(max_srore[0])+QUESTIONS_ADD[0]["opt"][max_srore[0]-1]+
                                            #'\n%d. '%(max_srore[1])+QUESTIONS_ADD[0]["opt"][max_srore[1]-1],
                                            #reply_markup=markup);
            #else:
                #form_question(markup,QUESTIONS[qs_index],str(qs_index));
                #if (qs_index == 0):
                    #bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id);
                    #bot.send_photo(chat_id=call.message.chat.id,
                                #photo=open('0.JPG', 'rb'),
                                #caption=QUESTIONS[qs_index]["qs"]+
                                #'\n1. '+QUESTIONS[qs_index]["opt"][0]+
                                #'\n2. '+QUESTIONS[qs_index]["opt"][1]+
                                #'\n3. '+QUESTIONS[qs_index]["opt"][2]+
                                #'\n4. '+QUESTIONS[qs_index]["opt"][3],
                                #reply_markup=markup);
                    #return;
                #bot.edit_message_media(chat_id=call.message.chat.id,message_id=call.message.message_id,
                                    #media=telebot.types.InputMediaPhoto(open(str(qs_index)+'.JPG', 'rb')),reply_markup=markup);
                #bot.edit_message_caption(chat_id=call.message.chat.id,message_id=call.message.message_id,
                                        #caption=QUESTIONS[qs_index]["qs"]+
                                        #'\n1. '+QUESTIONS[qs_index]["opt"][0]+
                                        #'\n2. '+QUESTIONS[qs_index]["opt"][1]+
                                        #'\n3. '+QUESTIONS[qs_index]["opt"][2]+
                                        #'\n4. '+QUESTIONS[qs_index]["opt"][3],
                                        #reply_markup=markup);

class bot_runner(object):
    BOT_INTERVAL =  1; # long-pooling check packet interval
    BOT_TIMEOUT  = 10; # long-pooling connection timeout
    def __init__(self,bot_token):
        self.bot_token = bot_token;
    def bot_pooling(self,questions):
        import time;
        while True:
            bot = telebot.TeleBot(self.bot_token);
            print("[OK]: New bot created");
            telebot_decorators(bot,questions);
            print("[..]: Decorators initialized. pooling started");
            try:
                bot.polling(none_stop=True,
                            interval=bot_runner.BOT_INTERVAL,
                            timeout=bot_runner.BOT_TIMEOUT);
            except Exception as ex: #Error in polling
                print("[FAILED]: Restarting in {}sec. Error:\n{}".format(BOT_TIMEOUT, ex))
                time.sleep(BOT_TIMEOUT);
            else: # clean, before exit
                bot.stop_polling();
                print("[OK]: Bot polling loop finished");
                break; #end loop
    def bot_hooking(self):
        pass;
    def bot_spamming(self):
        pass;

if __name__ == "__main__":
    import sys;
    try:
        mode = sys.argv[1];
        _bot_runner = bot_runner(BOT_TOKEN);
        if mode == 'collect':
            qs_raw = question.generate_questions('bot_constructor');
            BOT_QUESTIONS = list();
            for item in qs_raw:
                if 'BOT_WELCOME' in item:
                    BOT_QUESTIONS.append({'BOT_WELCOME':item['BOT_WELCOME']});
                    continue;
                BOT_QUESTIONS.append(question(item['qs'],item['input_type']));
                for opt in item['opts']:
                    BOT_QUESTIONS[-1].add_option(opt);
            _bot_runner.bot_pooling(BOT_QUESTIONS); # or _bot_runner.bot_hooking(); for WebHooks
        elif mode == 'spam':
            _bot_runner.bot_spamming();
    except Exception as ex:
        print("[FAILED]:",ex);
        exit();
    if 'help' in sys.argv[1]:
        pass;
    else:
        print("[FAILED]: wrong options. Please type: %s %s , for more info"%(
            sys.executable,sys.argv[0]));


