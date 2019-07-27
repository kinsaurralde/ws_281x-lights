# ws_281x-lights/tools

This folder contains various tools that can help main project.

## gen_config.py

This python script asks questions to generate a config file

### Usage

```bash
./gen_config.py [mode] <filename>
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
./send_json.py [file_name] [url]
```

#### Command line arguments:

Filename: (Required)
* Path to json file

Url: (Required)
* URL to send to
* Should include port if not 80
* http:// not necessary 
