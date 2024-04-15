#!/bin/bash
sleep 2;

curl -X PUT localhost:8888/api/scenes -d '{"id":"baseocean","action":"activate"}';
