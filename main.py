import json
import shutil
from pathlib import Path
import subprocess
import sys
from termcolor import colored
import time


class Commander:
    def __init__(self, json_path):
        self.vars = {}
        self.json_path = json_path
        self.command_json = self.read_commands(json_path)

    def read_commands(self, json_path: str):
        f = open(json_path)
        commands = json.load(f)
        return commands

    def __check_for_variables(self, text: str):
        for k, v in self.vars.items():
            k_covered = '${' + k + '}'
            text = text.replace(k_covered, v)
        return text

    def parse_command(self, command):
        current_command = command['operation']
        print_info('\nCommand is executing.. {}'.format(current_command))

        if current_command == 'DEFINE_VARIABLE':
            if 'pairs' not in command:
                raise Exception('pairs field could not found')

            pairs = command['pairs']
            for pair in pairs:
                key = pair['key']
                value = pair['value']
                self.vars[key] = value
                print('\t\t{}: {}'.format(key, value))

        elif current_command == 'COPY_FILE':
            source_file = self.__check_for_variables(command['sourceFile'])
            destination_folder = self.__check_for_variables(command['destinationFolder'])

            print('\t\tSource file: {}'.format(source_file))
            print('\t\tDestination folder: {}'.format(destination_folder))

            rename = None
            if 'rename' in command:
                rename = self.__check_for_variables(command['rename'])
                print('\t\tRename: {}'.format(rename))

            self.__copy_file(source_file, destination_folder, rename=rename)

        elif current_command == 'REPLACE_TEXT':
            file_path = self.__check_for_variables(command['filePath'])
            old_value = self.__check_for_variables(command['oldValue'])
            new_value = self.__check_for_variables(command['newValue'])

            print('\t\tFile path: {}'.format(file_path))
            print('\t\tOld value: {}'.format(old_value))
            print('\t\tNew value: {}'.format(new_value))

            self.__replace_text(file_path, old_value, new_value)

        elif current_command == 'RUN_SHELL':
            shell_command = self.__check_for_variables(command['command'])
            print('\t\tShell command: {}'.format(shell_command))

            working_directory = None
            if 'workingDirectory' in command:
                working_directory = self.__check_for_variables(command['workingDirectory'])
                print('\t\tWorking Directory: {}'.format(working_directory))

            self.__run_shell(shell_command, working_directory=working_directory)

        elif current_command == 'RUN_COMMANDER_SCRIPT':
            file_path = self.__check_for_variables(command['filePath'])
            inside_commander = Commander(file_path)
            inside_commander.execute()
        else:
            raise Exception('Command not found: {}'.format(current_command))

        print_success('Command is executed successfully.. {}'.format(current_command))

        if 'wait' in command and command['wait'] is True:
            val = input('Press any key to continue..')

    def __run_shell(self, command, working_directory=None):
        if working_directory is None:
            subprocess.run(command, shell=True, stderr=sys.stderr, stdout=sys.stdout)
        else:
            subprocess.run(command, shell=True, cwd=working_directory, stderr=sys.stderr, stdout=sys.stdout)

    def __replace_text(self, file_path, old_value, new_value):
        with open(file_path, "rt") as fin:
            with open("cp.temp", "wt") as fout:
                for line in fin:
                    fout.write(line.replace(old_value, new_value))

        shutil.move("cp.temp", file_path)

    def __copy_file(self, source_file, destination_folder, rename=None):
        Path(destination_folder).mkdir(parents=True, exist_ok=True)
        dst = destination_folder
        if rename is not None:
            dst += '\\' + rename

        shutil.copy(source_file, dst)

    def execute(self):
        for command in self.command_json:
            try:
                self.parse_command(command)
            except Exception as e:
                print_error('Command could not executed: {}'.format(command['operation']))
                print_error(e)
                raise Exception(e)


def print_info(text):
    print(colored(text, 'cyan'))


def print_success(text):
    print(colored(text, 'green'))


def print_error(text):
    print(colored(text, 'red'))


if __name__ == '__main__':
    commander = Commander('test.json')
    try:
        start = time.time()
        commander.execute()
    except Exception:
        pass

    end = time.time()
    hours, rem = divmod(end - start, 3600)
    minutes, seconds = divmod(rem, 60)
    print_info('\nElapsed time: {:0>2}:{:0>2}:{:05.2f}'.format(int(hours), int(minutes), seconds))
