#!/usr/bin/env bash
# Deletes every object version and delete marker in a (small) versioned bucket so it can be deleted.
# Usage: ./empty-versioned-bucket.sh <bucket-name> <region>
# Handles up to 1,000 versions per run (enough for these labs). Run again if more remain.
set -euo pipefail
B="$1"; R="$2"
for kind in Versions DeleteMarkers; do
  json=$(aws s3api list-object-versions --bucket "$B" --region "$R" --output json \
         --query "{Objects: ${kind}[].{Key:Key,VersionId:VersionId}, Quiet: \`true\`}")
  count=$(echo "$json" | python3 -c 'import json,sys; print(len(json.load(sys.stdin)["Objects"] or []))')
  if [ "$count" != "0" ]; then
    aws s3api delete-objects --bucket "$B" --region "$R" --delete "$json" >/dev/null
    echo "deleted $count $kind from $B"
  fi
done
