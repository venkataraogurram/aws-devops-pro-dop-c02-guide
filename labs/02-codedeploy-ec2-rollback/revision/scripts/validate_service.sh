#!/bin/bash
# Health check: exit 0 = healthy, non-zero = deployment fails on this instance.
for i in $(seq 1 10); do
  if curl -sf http://localhost/ | grep -q "Version"; then
    echo "service healthy"
    exit 0
  fi
  sleep 3
done
echo "service did not become healthy"
exit 1
