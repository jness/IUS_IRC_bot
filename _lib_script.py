import os, subprocess

def run(command, subcommand):
    scriptdir = './scripts'
    file = scriptdir + '/' + command
    if os.path.exists(file):
        process = subprocess.Popen(['./' + file, subcommand], shell=False, stdout=subprocess.PIPE)
        if process:
            return process
    else:
        return False
