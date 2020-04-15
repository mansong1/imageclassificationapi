#!/bin/bash
SCRIPT_PATH="./tfserver/tfserver_img.sh"

OUTPUT=`"$SCRIPT_PATH"`

[ $? -eq 0 ] ; docker-compose up
