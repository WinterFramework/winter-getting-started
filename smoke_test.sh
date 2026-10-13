#!/usr/bin/env bash
# Checks that a running instance of the application answers as expected.
# Usage: ./smoke_test.sh http://localhost:8080
set -euo pipefail

base_url="${1%/}"

# A fresh container or a scaled-to-zero Container App needs time to start.
for attempt in $(seq 1 30); do
  if curl --silent --fail --output /dev/null "$base_url/greeting/"; then
    break
  fi
  if [ "$attempt" = 30 ]; then
    echo "No answer from $base_url/greeting/" >&2
    exit 1
  fi
  sleep 5
done

check() {
  local path="$1" expected_status="$2" expected_body="$3"
  local body status
  body=$(curl --silent --show-error --write-out '\n%{http_code}' "$base_url$path")
  status="${body##*$'\n'}"
  body="${body%$'\n'*}"
  if [ "$status" != "$expected_status" ] || [[ "$body" != *"$expected_body"* ]]; then
    echo "GET $path: expected $expected_status containing '$expected_body', got $status: $body" >&2
    exit 1
  fi
  echo "GET $path: $status"
}

check /greeting/ 200 '"Hello from Winter API!"'
check /greeting/a-name-that-is-way-too-long/ 400 '"detail": "Name must be at most 20 characters long"'
check /openapi.json 200 '"/greeting/{name}/"'
check / 200 'swagger-ui'
