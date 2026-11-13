#!/bin/bash
# Runs at ApplicationStop. NOTE: CodeDeploy runs this script from the PREVIOUS successful revision.
if systemctl is-active --quiet httpd; then
  systemctl stop httpd
fi
exit 0
