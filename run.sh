#!/bin/bash

cp galaxy.ini galaxy/config
cp tool_conf.xml galaxy/config
cp requirements.txt galaxy/lib/galaxy/dependencies/requirements.txt
rsync -ruv tools/ galaxy/tools/

cd galaxy
./run.sh
