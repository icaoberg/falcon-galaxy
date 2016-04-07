#!/bin/bash

cp galaxy.ini galaxy/config
cp tool_conf.xml galaxy/config
rsync -ruv tools/ galaxy/tools/

cd galaxy
./run.sh
