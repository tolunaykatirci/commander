# Commander Python

Order your commands and execute one by one.

## Usage

1. Make sure you have installed Python on your computer.

2. Run command below.

```bash
python commander.py --script=ionic-cordova.json
```

## Documentation

### Commands Summary

| Command | Description |
|---|---|
| DEFINE_VARIABLE | Define variables to use another commands. |
| COPY_FILE | Copy specified file to destination folder. If destination folder is not exist, it will be automatically created. |
| REPLACE_TEXT | Replace texts in specified file. |
| RUN_SHELL | Run shell command. |
| RUN_COMMANDER_SCRIPT| Run commander script internally. |

### Commands

#### DEFINE_VARIABLE
Define variables to use another commands.

| Parameter | Type | Description |
|---|---|---|
| pairs | object[] | - |

### Global Fields

These fields can be used for any command.

| Parameter | Type | Description |
|---|---|---|
| wait | boolean | Commander stops here and waits an input from user. |


--step
