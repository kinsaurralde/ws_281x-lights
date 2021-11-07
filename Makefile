# Version Information
MAJOR				= 3
MINOR				= 0
PATCH				= 0
LABEL				= development

# Options
LINE_LENGTH = 120

# Directories
CONTROLLER_DIR = src/controller/
CONTROLLER_MODULES = ${CONTROLLER_DIR}src/modules/
WEBAPP_DIR = src/webapp/
WEBAPP_MODULES = ${WEBAPP_DIR}modules/
WEBAPP_STATIC = ${WEBAPP_DIR}static/
WEBAPP_TEMPLATES = ${WEBAPP_DIR}templates/
BUILD_DIR = build/
WEBAPP_BUILD_DIR = ${BUILD_DIR}webapp/
CONTROLLER_BUILD_DIR = ${BUILD_DIR}esp/

# Files
PY_FILES			= ${WEBAPP_DIR}server.py ${WEBAPP_DIR}modules/*
JS_FILES			= ${WEBAPP_STATIC}*.js ${WEBAPP_STATIC}js

# Lint Options
CLANGTIDY_OPTIONS	= -checks=-*,clang-analyzer*,readability*,performance*,portability*,google*,-readability-magic-numbers,-clang-analyzer-valist.Uninitialized
PYLINT_CONFIG		= --rcfile=lint/pylintrc
PRETTIER_CONIG		= --config lint/.prettierrc.json
HTML_VALIDATE_CONFG = --config lint/.htmlvalidate.json
ESLINT_CONFIG		= --config lint/.eslintrc.json

# Linters
PRETTIER			= node_modules/prettier/bin-prettier.js
HTML_VALIDATE		= node_modules/html-validate/bin/html-validate.js
ESLINT				= node_modules/eslint/bin/eslint.js

# Programs
NANOPB_COMPILER		= sdk/nanopb/generator/nanopb_generator.py

# Other
ESP_HASH			= $(shell sha256sum ${CONTROLLER_DIR}controller.ino | head -c 64)
PIXELS_HASH			= $(shell sha256sum ${CONTROLLER_DIR}src/modules/pixels* | sha256sum | head -c 64)


.PHONY: lint

nanopb:
# Create Build Directories
	mkdir -p proto/build/nanopb
	mkdir -p proto/build/py
# Compile for nanopb
# cd proto && ls -al ../sdk/nanopb
	cd proto && ./../${NANOPB_COMPILER} --library-include-format=#include\ \"%s\" --strip-path --output-dir=build/nanopb/. *.proto
# Compile for python
	cd proto && protoc --python_out=build/py/. *.proto
# Move nanopb protos
	mv proto/build/nanopb/*.pb.* src/controller/src/nanopb/
# Move py protos
	mv proto/build/py/*_pb2.py src/webapp/
# Delete build
	rm -rf proto/build/

config-generator:
	cd tools/ && python3 config_generator.py

version:
	touch ${CONTROLLER_DIR}version.h
	printf "// This file was generated by Makefile on $(shell date)\n" > ${CONTROLLER_DIR}version.h
	printf "// DO NOT EDIT THIS FILE\n\n" >> ${CONTROLLER_DIR}version.h
	printf "#ifndef VERSION_H_\n#define VERSION_H_\n\n" >> ${CONTROLLER_DIR}version.h
	printf "#define MAJOR ${MAJOR}\n#define MINOR ${MINOR}\n#define PATCH ${PATCH}\n#define LABEL \"${LABEL}\"\n\n" >> ${CONTROLLER_DIR}version.h
	printf "#define ESP_HASH 0x${ESP_HASH}\n#define PIXELS_HASH 0x${PIXELS_HASH}\n\n" >> ${CONTROLLER_DIR}version.h
	printf "#endif  // VERSION_H_\n\n" >> ${CONTROLLER_DIR}version.h
	touch ${WEBAPP_DIR}version.py
	printf "# This file was generated by Makefile on ${shell date}\n" > ${WEBAPP_DIR}version.py
	printf "# DO NOT EDIT THIS FILE\n\n" >> ${WEBAPP_DIR}version.py
	printf "MAJOR = ${MAJOR}\nMINOR = ${MINOR}\nPATCH = ${PATCH}\nLABEL = \"${LABEL}\"\n\n" >> ${WEBAPP_DIR}version.py
	printf "ESP_HASH = 0x${ESP_HASH}\nPIXELS_HASH = 0x${PIXELS_HASH}" >> ${WEBAPP_DIR}version.py

run-webapp-development:
	cd src/webapp/ && python3 -B server.py --port=5000 --ping-controllers --ping-interval=10 && cd ../../

npm-setup:
	npm install prettier html-validate eslint eslint-config-defaults eslint-config-google

pip-setup:
	pip3 install black
	pip3 install pylint

lint:
# Format c++
	clang-format -i ${CONTROLLER_DIR}controller.ino ${CONTROLLER_MODULES}* -style="{BasedOnStyle: Google, ColumnLimit: ${LINE_LENGTH}}"
# Format python
	python3 -m black --line-length ${LINE_LENGTH} ${PY_FILES}
# Format CSS/JS
	find ${WEBAPP_DIR} -iname *.css | xargs ${PRETTIER} ${PRETTIER_CONIG} --write
	find ${JS_FILES} -iname *.js | xargs ${PRETTIER} ${PRETTIER_CONIG} --write

lint-check: lint-check-cpp lint-check-py lint-check-js

lint-check-cpp: clang
	clang-tidy ${CLANGTIDY_OPTIONS} ${CONTROLLER_MODULES}* ${CONTROLLER_DIR}testing/*.cpp

lint-check-py:
	python3 -m pylint ${PYLINT_CONFIG} ${PY_FILES}

lint-check-js:
	find ${JS_FILES} -iname *.js | xargs ${ESLINT} --fix ${ESLINT_CONFIG}

clang:
	clang++ -Wall -MJ a.o.json -std=c++11 -o build/loggingtest src/controller/testing/main.cpp src/controller/src/nanopb/*.c src/controller/src/modules/*.cpp
	sed -e '1 i\[' -e '$$a\]' *.o.json > compile_commands.json
	rm *.o.json

main-test: clang
	./build/loggingtest

clean:
	rm -rf ${BUILD_DIR}*

build: nanopb version build-copy-only
	

build-copy-only:
	rm -rf ${WEBAPP_BUILD_DIR}
	rm -rf ${CONTROLLER_BUILD_DIR}
	cd tools/ && python3 build.py
