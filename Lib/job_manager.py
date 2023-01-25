import os
import subprocess
import shlex
from Credentials import HOME_DIRECTORY, ENCODING_TERMINAL
from Lib.mail import mail


class Manager:
    home_dir = HOME_DIRECTORY
    job = ''
    os.chdir(home_dir)
    # Просмотр текущего каталога

    def ls(self):
        list_dir = ''
        for filename in os.listdir(os.getcwd()):
            list_dir = list_dir + filename + '\n'
        return list_dir

    def curdir(self):
        return os.getcwd()

    # Переход в другую папку
    def cd(self,path):
        os.chdir(path)
        return os.getcwd()

    # Отправить на почту файл
    def mail(self,mail_name:str, filename=''):
        mail(mail_name,filename)

    def launch(self, protocol_file:str):
        logError = open('Manager_errors.txt','w')
        logOutput = open('Manager_output.txt', 'w')
        protocol = open(protocol_file,'r')
        for lines in protocol:
            command = shlex.split(lines.strip('\n'))
            self.job = subprocess.Popen(command, shell=True,stdout=logOutput,stderr=logError)
        protocol.close()
        logOutput.close()
        logError.close()

    def command(self, args):
        p = subprocess.Popen(args, stdout=subprocess.PIPE, shell=True)
        comm = p.communicate()[0].decode(encoding=ENCODING_TERMINAL)
        return comm

    def listen(self):
        output = 'No launched processes'
        if self.job != '':
            output = str(self.job.communicate(timeout=1)[0].decode())
        return output
