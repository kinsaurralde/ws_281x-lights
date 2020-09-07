# Webapp

The webapp hosts the control webpage used to easily send commands to some or multiple controllers. 
It also provides predictions of what each strip should look like (PLANNED).

## Routes

### /
**GET**

Serves the web control panel

Return: HTML page

### /data
**POST**

Recieves array of commands and sends them to the correct controllers.
The format of a single command can be found [here](controller/controller.md#data)

Return: array of connection fails

### /docs
**GET**

Serves web page with these docs

Return: HTML page

### /getanimations
**GET**

Gets animation config

Return: JSON Object

### /getcolors
**GET**

Gets color config

Return: JSON Object

### /getcontrollers
**GET**

Gets controller config

Return: JSON Object

## SocketIO Messages

### connect
Called when a client connects to this server

### disconnect
Called when a client disconnects from this server
