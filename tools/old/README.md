# ws_281x-lights/tools

This folder contains various tools that can help main project.

## gen_config.py

This python script asks questions to generate a config file

### Usage

```bash
./gen_config.py <mode> [filename]
```

#### Command line arguments:

Mode: (Required)
* new: start from blank file
    * Will delete and replace file at filename if it already exists

Filename: (Optional)
* Default: config.json
* Path to output config file
* Must have .json extension

## send_json.py

This python script sends to given json file to the given url in a POST request

### Usage

```bash
./send_json.py <file_name> <url>
```

#### Command line arguments:

Filename: (Required)
* Path to json file

Url: (Required)
* URL to send to
* Should include port if not 80
* http:// not necessary 

## secondary.py

This python script makes the folder containing the files the remote controllers use

### Usage

```bash
./secondary.py <mode> <path>
```

#### Command line arguments:

Mode: (required)
* new: makes a new folder from config files in given folder
* update: updates python files in given folder

## put_files.py

This python script updates remote controllers through sftp

### Usage
```bash
./put_files.py <filename>
```

#### Command line arguments:

Filename: (required)
* Path to file which contains address of remote controllers and their file paths
    * A sample file is given at sample/sample_sftp.txt
