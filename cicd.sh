#!/bin/bash

# args:
# 1. --dry-run
# if used, only prints configuration files
# else upload the connectors configuration files

URL=http://localhost:8083
CONNECTOR_PATH=./connectors

CYAN="\033[1;36m"
RESET="\033[0m"
NOTICE_FLAG="${CYAN}❯"

echo -e "${NOTICE_FLAG} List connectors ${RESET}"
echo $(curl -s -X GET $URL/connectors)

echo -e "${NOTICE_FLAG} Begin upserting connectors ${RESET}"
for FILENAME in "$CONNECTOR_PATH"/*.json; do
    CONNECTOR=${FILENAME##*/}
    echo -e "${CYAN}$CONNECTOR${RESET}"
    if [ "$1" == "--dry-run" ]; then
        cat "$FILENAME"
    else
        curl -i -X PUT -H "Accept:application/json" -H "Content-Type:application/json" "$URL/connectors/${CONNECTOR%.*}/config" -d "@$FILENAME"
    fi
    echo
done

echo -e "${NOTICE_FLAG} Finished.${RESET}"
