# Commander Python

Order your commands and execute one by one.

## Pre-Installation

You can add repository path to environment variables as `Path` environment after download. 
In this way, you can call `commander` executable in any directory.

1. Open **Environment Variables**.
2. Select `Path` environment variable and click **Edit**.
3. Click **New** and specify the repository path.
4. Close all windows by clicking **OK**.

## Usage

**Option 1.** Run executable below.

```bash
commander <file_path.json> <--stepper>
```

**Option 2.** Run python file below. You don't need to add environment variable for this option.

```bash
python commander.py <file_path.json> <--stepper>
```

## Documentation

### Arguments

| Argument | Description |
|---|---|
| file_path | **Mandatory.** JSON config file to execute commands. |
| --help | Shows an help menu for arguments.|
| --stepper | Program waits an input from user after each command executed. |

### Commands Summary

| Command | Description |
|---|---|
| [DEFINE_CONSTANT](#DEFINE_CONSTANT) | Define constants to use in another commands. |
| [COPY](#COPY) | Copy specified file to destination folder. If destination folder does not exist, it will be automatically created. |
| [REPLACE_TEXT](#REPLACE_TEXT) | Replace texts in specified file. |
| [RUN_SHELL](#RUN_SHELL) | Run shell command. |
| [RUN_COMMANDER_SCRIPT](#RUN_COMMANDER_SCRIPT)| Run commander script internally. |
| [EXTRACT_ZIP](#EXTRACT_ZIP) | Extract content of specified zip file to destination folder. |
| [REGEX](#REGEX) | Apply regular expression to specified file. |

### Commands

#### DEFINE_CONSTANT

Define constants to use in another commands. These keys will be automatically changed with the value.

| Parameter | Type | Description |
|---|---|---|
| pairs | [key: string]: value: string | Key-value pair for custom constants. |

*Example:*

```json
[
  {
    "operation": "DEFINE_CONSTANT",
    "pairs": [
      {
        "key": "project_root",
        "value": ".\\demos\\cordova"
      },
      {
        "key": "project_id",
        "value": "com.hms.nearby.cordova.release"
      }
    ]
  },
  {
    "operation": "RUN_SHELL",
    "command": "echo ${project_id} ${project_root}",
    "workingDirectory": "..\\"
  }
]
```

#### COPY

Copy specified file to destination folder. If destination folder does not exist, it will be automatically created.

| Parameter | Type | Description |
|---|---|---|
| source | string | Source file/folder. |
| destination | string | Destination file/folder. |
| passIfExists | boolean | **Optional parameter.** If destination path is exist, pass this command. |

*Example:*

```json
[
  {
    "operation": "COPY",
    "source": "test.txt",
    "destination": "new-folder/test_renamed.txt",
    "passIfExists": true
  },
  {
    "operation": "COPY",
    "source": "test.txt",
    "destination": "new-folder"
  }
]
```

#### REPLACE_TEXT

Replace texts in specified file.

| Parameter | Type | Description |
|---|---|---|
| filePath | string | Source file. |
| oldValue | string | Value to be changed. |
| newValue | string | New value. |

*Example:*

```json
[
  {
    "operation": "REPLACE_TEXT",
    "filePath": "test.txt",
    "oldValue": "vel",
    "newValue": "REPLACED"
  }
]
```

#### RUN_SHELL

Run shell command.

| Parameter | Type | Description |
|---|---|---|
| command | string | Source file. |
| workingDirectory | string | **Optional parameter.** Working directory to run shell can be set relatively. |

*Example:*

```json
[
  {
    "operation": "RUN_SHELL",
    "command": "echo Test Message!!!",
    "workingDirectory": ".\\"
  },
  {
    "operation": "RUN_SHELL",
    "command": "echo Current Working Directory: %cd%",
    "workingDirectory": "..\\"
  }
]
```

#### RUN_COMMANDER_SCRIPT

Run commander script internally. Constants defined in parent script are transferred to the inner commander
script.

| Parameter | Type | Description |
|---|---|---|
| filePath | string | Source file. |

*Example:*

```json
[
  {
    "operation": "RUN_COMMANDER_SCRIPT",
    "filePath": ".\\copy.json"
  },
  {
    "operation": "RUN_COMMANDER_SCRIPT",
    "filePath": ".\\run_shell.json"
  }
]
```

#### EXTRACT_ZIP

Extract content of specified zip file to destination folder.

| Parameter | Type | Description |
|---|---|---|
| source | string | Source zip file. |
| destination | string | Destination folder. |

*Example:*

```json
[
  {
    "operation": "EXTRACT_ZIP",
    "source": "test.zip",
    "destination": "extracted_zip"
  }
]
```

#### REGEX

Apply regular expression to specified file.

| Parameter | Type | Description |
|---|---|---|
| source | string | Source file. |
| regexPattern | string | Regex pattern to be applied. |
| text | string | New text for matched strings. |
| append | boolean | **Optional parameter.** If this value is true, new text will be appended to text after each match. |

*Example:*

```json
[
  {
    "operation": "EXTRACT_ZIP",
    "source": "test.zip",
    "destination": "extracted_zip"
  }
]
```

### Global Fields

These fields can be used for any command.

| Parameter | Type | Description |
|---|---|---|
| wait | boolean | Commander stops here and waits an input from user. |
| skip | boolean | Commander skips current command without executing it. |

## Creating Executable

You can install `pyinstaller` library and create executable with command below.

```bash
pyinstaller --onefile commander.py
```
