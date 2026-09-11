#!/usr/bin/env bash
set -euo pipefail

DORIS_HOST="${DORIS_HOST:-127.0.0.1}"
DORIS_QUERY_PORT="${DORIS_QUERY_PORT:-9030}"
DORIS_HTTP_PORT="${DORIS_HTTP_PORT:-8030}"
DORIS_USER="${DORIS_USER:-root}"
DORIS_PASSWORD="${DORIS_PASSWORD:-}"
ROWS="${ROWS:-100000}"

python benchmark/doris/generate_events.py --rows "$ROWS"

MYSQL_AUTH=("-h${DORIS_HOST}" "-P${DORIS_QUERY_PORT}" "-u${DORIS_USER}")
if [[ -n "$DORIS_PASSWORD" ]]; then MYSQL_AUTH+=("-p${DORIS_PASSWORD}"); fi

mysql "${MYSQL_AUTH[@]}" < benchmark/doris/schema.sql

curl --fail --show-error --silent \
  -u "${DORIS_USER}:${DORIS_PASSWORD}" \
  -H 'format:csv' \
  -H 'column_separator:,' \
  -H 'expect:100-continue' \
  -T benchmark/doris/events.csv \
  "http://${DORIS_HOST}:${DORIS_HTTP_PORT}/api/velodb_portfolio/agent_events/_stream_load"

echo
printf 'row count: '
mysql "${MYSQL_AUTH[@]}" -N -e 'SELECT COUNT(*) FROM velodb_portfolio.agent_events;'

echo 'running representative queries...'
mysql "${MYSQL_AUTH[@]}" < benchmark/doris/queries.sql
