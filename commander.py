import json
import shutil
from pathlib import Path
import subprocess
import sys
from termcolor import colored
import time
import os
import zipfile
import re
import argparse


class Commander:
    def __init__(self, json_path, stepper=False, constants=None):
        self.constants = {}
        self.json_path = json_path
        self.command_json = self.read_commands(json_path)
        self.stepper = stepper

        if constants is not None:
            self.constants = constants

    def read_commands(self, json_path: str):
        f = open(json_path)
        commands = json.load(f)
        return commands

    def parse_and_execute_command(self, command):
        current_command = command['operation']

        if 'skip' in command and command['skip']:
            print_info('Command is skipping.. {}'.format(current_command))
            return

        print_info('\nCommand is executing.. {}'.format(current_command))

        if current_command == 'DEFINE_CONSTANT':
            if 'pairs' not in command:
                raise Exception('pairs field could not found')

            pairs = command['pairs']
            for pair in pairs:
                key = self.__replace_constants(pair['key'])
                value = self.__replace_constants(pair['value'])
                self.constants[key] = value
                print('\t\t{}: {}'.format(key, value))

        elif current_command == 'COPY':
            source = self.__replace_constants(command['source'])
            destination = self.__replace_constants(command['destination'])

            print('\t\tSource: {}'.format(source))
            print('\t\tDestination: {}'.format(destination))

            pass_if_exists = False
            if 'passIfExists' in command:
                pass_if_exists = command['passIfExists']
                print('\t\tPass if exists: {}'.format(pass_if_exists))

            self.__copy(source, destination, pass_if_exists=pass_if_exists)

        elif current_command == 'REPLACE_TEXT':
            file_path = self.__replace_constants(command['filePath'])
            old_value = self.__replace_constants(command['oldValue'])
            new_value = self.__replace_constants(command['newValue'])

            print('\t\tFile path: {}'.format(file_path))
            print('\t\tOld value: {}'.format(old_value))
            print('\t\tNew value: {}'.format(new_value))

            self.__replace_text(file_path, old_value, new_value)

        elif current_command == 'RUN_SHELL':
            shell_command = self.__replace_constants(command['command'])
            print('\t\tShell command: {}'.format(shell_command))

            working_directory = None
            if 'workingDirectory' in command:
                working_directory = self.__replace_constants(command['workingDirectory'])
                print('\t\tWorking Directory: {}'.format(working_directory))

            self.__run_shell(shell_command, working_directory=working_directory)

        elif current_command == 'RUN_COMMANDER_SCRIPT':
            file_path = self.__replace_constants(command['filePath'])
            inside_commander = Commander(file_path, constants=self.constants)
            inside_commander.execute()

        elif current_command == 'EXTRACT_ZIP':
            source = self.__replace_constants(command['source'])
            destination = self.__replace_constants(command['destination'])

            print('\t\tSource: {}'.format(source))
            print('\t\tDestination: {}'.format(destination))

            self.__extract_zip(source, destination)

        elif current_command == 'REGEX':
            source = self.__replace_constants(command['source'])
            regex_pattern = self.__replace_constants(command['regexPattern'])
            text = self.__replace_constants(command['text'])
            is_append = True if 'append' in command and command['append'] is True else False

            print('\t\tSource: {}'.format(source))
            print('\t\tRegex Pattern: {}'.format(regex_pattern))
            print('\t\tText: {}'.format(text))
            print('\t\tAppend: {}'.format(is_append))

            self.__regex(source, regex_pattern, text, is_append=is_append)

        else:
            raise ValueError('Command not found: {}'.format(current_command))

        print_success('Command is executed successfully.. {}'.format(current_command))

        if self.stepper or ('wait' in command and command['wait'] is True):
            val = input('Press Enter to continue..')

    def execute(self):
        for command in self.command_json:
            try:
                self.parse_and_execute_command(command)
            except Exception as e:
                print_error('Command could not executed: {}'.format(command['operation']))
                print_error(e)
                return

    def __run_shell(self, command, working_directory=None):
        if working_directory is None:
            subprocess.run(command, shell=True, stderr=sys.stderr, stdout=sys.stdout)
        else:
            subprocess.run(command, shell=True, cwd=working_directory, stderr=sys.stderr, stdout=sys.stdout)

    def __replace_constants(self, text: str):
        for k, v in self.constants.items():
            k_covered = '${' + k + '}'
            text = text.replace(k_covered, v)
        return text

    def __replace_text(self, file_path, old_value, new_value):
        with open(file_path, "rt") as fin:
            with open("cp.temp", "wt") as fout:
                for line in fin:
                    fout.write(line.replace(old_value, new_value))

        shutil.move("cp.temp", file_path)

    def __copy(self, source, destination, pass_if_exists=False):

        if pass_if_exists and os.path.exists(destination):
            print_info('\t\tFile exists: {}'.format(destination))
            return

        if os.path.isdir(source):
            # copy directory
            shutil.copytree(source, destination)
        else:
            if not os.path.exists(destination):
                os.makedirs(os.path.dirname(destination), exist_ok=True)
            shutil.copy(source, destination)

    def __extract_zip(self, source, destination):
        with zipfile.ZipFile(source, 'r') as zip_ref:
            zip_ref.extractall(destination)

    def __regex(self, source, regex_pattern, text, is_append=False):

        f = open(source, 'r')
        source_text = f.read()

        if is_append:
            def __append(m):
                return m.group(0) + text
            source_text = re.sub(regex_pattern, __append, source_text)
        else:
            source_text = re.sub(regex_pattern, text, source_text)

        f = open(source, 'w')
        f.write(source_text)


def print_info(text):
    print(colored(text, 'cyan'))


def print_success(text):
    print(colored(text, 'green'))


def print_error(text):
    print(colored(text, 'red'))


if __name__ == '__main__':
    help_message = 'Commander - Python Command Sequence Tool'

    parser = argparse.ArgumentParser(description=help_message)
    parser.add_argument('file', help='Input file path')

    parser.add_argument('--stepper', action="store_true",
                        help='Runs commands step by step')

    args = parser.parse_args()

    if not os.path.isfile(args.file):
        print_error('Specified file could not found!')
        sys.exit()

    stepper = False
    if args.stepper:
        stepper = True
        print_info('Stepper is active')

    start = time.time()
    commander = Commander(args.file, stepper=stepper)
    commander.execute()

    end = time.time()
    hours, rem = divmod(end - start, 3600)
    minutes, seconds = divmod(rem, 60)
    print_info('\nElapsed time: {:0>2}:{:0>2}:{:05.2f}'.format(int(hours), int(minutes), seconds))
