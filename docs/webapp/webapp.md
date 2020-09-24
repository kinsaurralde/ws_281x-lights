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

### /getversioninfo
**GET**

Gets version of controllers

Return: JSON Object

### /getinitialized
**GET**

Gets whether controllers are initialized

Return: JSON Object

### /enable
**GET**

Query Parameters:
    - String name (required): Name of strip to enable

Return: JSON Object

### /disable
**GET**

Query Parameters:
    - String name (required): Name of strip to disable

Return: JSON Object

### /update
**GET**

Emit updated data (version info, initialzied, ping)

## SocketIO Messages

### connect
Called when a client connects to this server

### disconnect
Called when a client disconnects from this server

### webpage_loaded
Emits updated data and brightness.
Called when webapge loads.

### set_brightness
Sets the brightness of controllers in request and resends to all connected clients

## SocketIO Emits

### connection_response
Responds to newly connected client

### brightness
Sends brightness values for some or all controllers

## update
Sends data (ping, version info, initialzied)
