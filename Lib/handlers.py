from Credentials import TRUSTED_USERS_ID
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from Lib.job_manager import Manager

manager = Manager()
myVars = locals()


def security_decorator(any_func):
    async def check_username(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = str(update.message.from_user.username)
        if user in TRUSTED_USERS_ID:
            await any_func(update, context)
        else:
            await answer(update, context)

    return check_username


async def helper(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        command_name = context.args[0].strip('/') + '_help'
        output = '/{} => {}'.format(context.args[0].strip('/'), myVars[command_name])
        await context.bot.send_message(chat_id=update.effective_chat.id, text=output)
    except KeyError:
        output = '/{} => Wrong command name or help currently unavaliable'.format(context.args[0].strip('/'))
        await context.bot.send_message(chat_id=update.effective_chat.id, text=output)


helper_handler = CommandHandler('help', helper)


async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="You are not allowed to send command.")


answer_handler = CommandHandler('start', answer)


async def list_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_list = ''
    for i in handlers:
        x, = i.commands
        help_list += '/{command} \n'.format(command=x)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=help_list)


list_handler = CommandHandler('list', list_command)
list_help = 'Команда, позволяющая выводить список доступных команд для бота'


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Type /list for list of commands.")


start_handler = CommandHandler('start', start)
start_help = 'Стартуем.'


async def ls(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=manager.ls())


ls_handler = CommandHandler('ls', ls)
ls_help = 'Выводит список файлов в текущей директории'


async def curdir(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=manager.curdir())


curdir_handler = CommandHandler('curdir', curdir)
curdir_help = 'Выводит текущий путь.'


@security_decorator
async def cd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=manager.cd(context.args[0]))


cd_handler = CommandHandler('cd', cd)
cd_help = 'команда, позволяющая перемещаться между каталогами.'

@security_decorator
async def mail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    manager.mail(context.args[0])
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Done')


mail_handler = CommandHandler('mail', mail)
mail_help = 'отправить заданый файл(ы) на почту'

@security_decorator
async def launch(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Protocol ' + context.args[0] + ' launched')
    manager.launch(context.args[0])
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Protocol ' + context.args[0] + ' completed')


launch_handler = CommandHandler('launch', launch)
launch_help = 'команда запуска протокола. /launch <имя_протокола>. С помощью команды /curdir проверьте, что файл протокола' \
              'доступен к исполнению'

@security_decorator
async def comm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    output = str(manager.command(context.args))
    if output != '':
        await context.bot.send_message(chat_id=update.effective_chat.id, text=output)
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Done: ' + ' '.join(context.args))


comm_handler = CommandHandler('comm', comm)
comm_help = 'запускает команду, введёную после /comm. Учтите, что набор команд зависит от ОС в которой развернут бот.'


@security_decorator
async def listen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=manager.listen())


listen_handler = CommandHandler('listen', listen)
listen_help = 'Выводит информацию, о запущенном процессе'


'''Список комманд'''
handlers = [
    start_handler,
    ls_handler,
    curdir_handler,
    cd_handler,
    mail_handler,
    launch_handler,
    comm_handler,
    listen_handler,
    helper_handler,
    list_handler
]
