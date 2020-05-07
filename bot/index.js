var TelegramBot = require('node-telegram-bot-api');
var token = '1104963369:AAEPtyYQb8gwqHmeQ3Ex9Jq9Gae5ZsIh4tA';
var bot = new TelegramBot(token, {polling:true});
bot.onText(/\/echo (.+)/,function(msg,match){
    var chatId = msg.chat.id;
    var echo = match[1];
    bot.sendMessage(chatId,echo);
});