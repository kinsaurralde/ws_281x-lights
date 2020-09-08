SRC_DIR				= src/
BUILD_DIR			= build/
TOOLS_DIR			= tools/
CONTROLLERS_DIR  	= src/controller/
SCRIPTS_DIR			= src/scripts/
WEBAPP_DIR			= src/webapp/
CPP_FLAGS			= -Wno-undef -Wall -Werror

BUILD_RPI_DIR		= ${BUILD_DIR}raspberrypi/
BUILD_RPI_SRC_DIR	= ${BUILD_RPI_DIR}src/

HTML_DIR			= ${WEBAPP_DIR}templates/
CSSJS_DIR 			= ${WEBAPP_DIR}static/
PY_FILES			= ${WEBAPP_DIR}*.py ${WEBAPP_DIR}tests/*.py ${WEBAPP_DIR}python/*.py tools/*

CLANG_FORMAT		= node_modules/clang-format/bin/linux_x64/clang-format --style=Google
ESLINT				= node_modules/eslint/bin/eslint.js
HTML_VALIDATE		= node_modules/html-validate/bin/html-validate.js
PRETTIER			= node_modules/prettier/bin-prettier.js
PRETTIER_CONIG		= --config lint_config/.prettierrc.json
HTML_VALIDATE_CONFG = --config lint_config/.htmlvalidate.json
ESLINT_CONFIG		= --config lint_config/.eslintrc.json
PYLINT_CONFIG		= --rcfile=lint_config/pylintrc

WEBAPP_CONFIG_ARG	= "config/controllers_sample.yaml"

all:
	# Create Directories
	mkdir -p ${BUILD_DIR}esp8266
	mkdir -p ${BUILD_DIR}raspberrypi/src
	mkdir -p ${BUILD_DIR}webapp

	# Copy to raspberrypi
	cp ${CONTROLLERS_DIR}pixels.cpp ${CONTROLLERS_DIR}pixels.h -t ${BUILD_DIR}raspberrypi/src/
	cp ${CONTROLLERS_DIR}structs.cpp ${CONTROLLERS_DIR}structs.h -t ${BUILD_DIR}raspberrypi/src/
	cp ${CONTROLLERS_DIR}extern.cpp -t ${BUILD_DIR}raspberrypi/src/
	cp ${CONTROLLERS_DIR}wrapper.py ${CONTROLLERS_DIR}controller_server.py ${CONTROLLERS_DIR}controller.py ${BUILD_DIR}raspberrypi/
	cp ${SCRIPTS_DIR}rpi_startup.sh ${BUILD_DIR}raspberrypi/
	cp ${TOOLS_DIR}makefiles/rpi_Makefile ${BUILD_DIR}raspberrypi/Makefile

	# Copy to esp8266
	cp ${CONTROLLERS_DIR}pixels.cpp ${CONTROLLERS_DIR}pixels.h -t ${BUILD_DIR}esp8266/
	cp ${CONTROLLERS_DIR}structs.cpp ${CONTROLLERS_DIR}structs.h -t ${BUILD_DIR}esp8266/
	cp ${CONTROLLERS_DIR}controller.ino ${BUILD_DIR}esp8266/
	touch ${BUILD_DIR}esp8266/wifi_controller.h
	printf "#define WIFI_SSID \"ssid\"\n#define WIFI_PASSWORD \"password\"\n" > ${BUILD_DIR}esp8266/wifi_controller.h

	# Copy to webapp
	cp -r ${WEBAPP_DIR} ${BUILD_DIR}

test:
	make test_webapp
	make coverage

test_webapp:
	cd src/webapp && pytest && cd ../../

coverage:
	cd src/webapp && coverage run --source=. -m pytest && coverage report && coverage html && cd ../../

build: all
	g++ -c -fPIC ${BUILD_RPI_SRC_DIR}pixels.cpp -o ${BUILD_RPI_SRC_DIR}pixels.o ${CPP_FLAGS}
	g++ -c -fPIC ${BUILD_RPI_SRC_DIR}structs.cpp -o ${BUILD_RPI_SRC_DIR}structs.o ${CPP_FLAGS}
	g++ -c -fPIC ${BUILD_RPI_SRC_DIR}extern.cpp -o ${BUILD_RPI_SRC_DIR}extern.o ${CPP_FLAGS}
	g++ -shared -o ${BUILD_RPI_DIR}pixels.so ${BUILD_RPI_SRC_DIR}pixels.o ${BUILD_RPI_SRC_DIR}structs.o ${BUILD_RPI_SRC_DIR}extern.o ${CPP_FLAGS}
	rm -f ${BUILD_RPI_SRC_DIR}*.o

run_rpi: build
	cd ${BUILD_RPI_DIR} && python3 controller_server.py --test && cd ../../

run_app:
	cd ${WEBAPP_DIR} && python3 app.py -d --config ${WEBAPP_CONFIG_ARG}

run_app_nosend:
	cd ${WEBAPP_DIR} && python3 app.py -d --nosend --config ${WEBAPP_CONFIG_ARG}

run_local: build
	cd ${TOOLS_DIR} && python3 -i localtest.py

setup:
	sudo apt install nodejs
	sudo apt install npm
	make node_modules
	sudo npm i docsify-cli -g
	sudo apt install pylint
	sudo apt install python3-pip
	sudo pip3 install eventlet
	pip3 install black
	pip3 install pytest-flask
	pip3 install pytest-mock
	pip3 install coverage
	pip3 install setuptools
	sudo pip3 install rpi_ws281x
	sudo apt install screen
	sudo pip3 install Flask
	sudo pip3 install flask_socketio
	sudo pip3 install ruamel.yaml 

node_modules:
	npm install clang-format prettier html-validate eslint eslint-config-defaults eslint-config-google

lint: clean
	${PRETTIER} ${PRETTIER_CONIG} --write ${CSSJS_DIR}*.css
	${PRETTIER} ${PRETTIER_CONIG} --write ${HTML_DIR}*.html
	find src/ -iname *.js | xargs ${CLANG_FORMAT} -i
	${HTML_VALIDATE} ${HTML_VALIDATE_CONFG} ${HTML_DIR}*.html
	${ESLINT} ${ESLINT_CONFIG} ${CSSJS_DIR}*.js
	python3 -m black ${PY_FILES}
	python3 -m pylint ${PYLINT_CONFIG} ${PY_FILES}

upload_rpi: all
	cd tools &&	python3 upload_rpi.py

.PHONY: docs
docs:
	cp -r images/ docs/images
	cp README.md docs/README.md
	docsify serve docs

git:
	make build
	make test
	make clean
	make lint
	git add .
	git status

clean:
	rm -fr ${BUILD_DIR}*
	rm -f ${CONTROLLERS_DIR}*.so
	find . -name __pycache__ -exec rm -rv {} +
	find . -name .pytest_cache -exec rm -rv {} +
	find . -name htmlcov -exec rm -rv {} +
	find . -name .coverage -exec rm -rv {} +
	