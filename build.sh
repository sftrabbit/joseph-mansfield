#!/bin/sh

BUILD_DIR=.
PUBLIC_DIR=${BUILD_DIR}/pub
PROJECT_DIR=$(dirname $0)

echo "Compiling HTML pages"
${PROJECT_DIR}/compile.py

BUILD_DIR_REGEX="s/\${BUILD_DIR}/${BUILD_DIR}/"
PROJECT_DIR_REGEX="s/\${PROJECT_DIR}/${PROJECT_DIR}/"
CONFIG_FILE_IN=${PROJECT_DIR}/config.rb.in
CONFIG_FILE=${BUILD_DIR}/config.rb
sed -e $BUILD_DIR_REGEX -e $PROJECT_DIR_REGEX $CONFIG_FILE_IN > $CONFIG_FILE

echo "Compiling compass stylesheets"
compass compile

echo "Copying assets"
cp -r ${PROJECT_DIR}/assets/images $PUBLIC_DIR/
