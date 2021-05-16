## ----------------------------------------------------------------------------
## This Makefile handles installing dependencies and starting several 
## configurations of the webserver. Some variables can be changed for
## certain targets.
## ----------------------------------------------------------------------------
## Changeable variables with default value:
## 
CONFIG_PATH_ARG="config/controllers_sample.yaml"	## 
PORT_ARG=5000	## 

## ----------------------------------------------------------------------------
## Targets
## 

help:			## Show this help
	@sed -n '/@sed/!s/## //p' $(MAKEFILE_LIST)

setup:			## Install python3, pip3, and screen through apt
	sudo apt update --fix-missing
	sudo apt install python3
	sudo apt install python3-pip
	sudo apt install screen

install:		## Install dependencies of webserver through pip3
	pip3 install -r requirements.txt

.PHONY: venv
venv:			## Print command to activate virtual enviroment
	@echo Run the following line to activate virtual enviroment
	@echo source venv/bin/activate

run_app:		## Run webapp. If CONFIG_PATH_ARG and PORT_ARG not specified, use default
	python3 app.py --config ${CONFIG_PATH_ARG} --port ${PORT_ARG}

run_interactive:	## Run webapp setup with interactive mode (does not start webserver)
	python3 -i app.py --nostart --noschedule

