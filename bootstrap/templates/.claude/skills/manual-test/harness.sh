#!/usr/bin/env bash
# The manual-test harness. **Everything that touches a container or a long-running process goes
# through here**, so a walk has no reason to type `docker compose` (or the project's own dev
# command) — and therefore no way to type it against the development instance.
#
#   harness.sh up [--fresh]        bring the isolated instance up, migrate, seed schema
#   harness.sh down [--keep-data]  stop it (and by default destroy its data)
#   harness.sh servers <start|stop|status|logs> [name]
#   harness.sh status              one line per moving part
#   harness.sh surface             what the system says about itself, right now
#   harness.sh drift               do the written oracles still name things that exist?
#
# TODO markers below are what bootstrap could not know. `SKILL.md` §0 refuses to walk while any
# of them survives — an unfilled harness is not a broken build, it is a blocked session.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/../../.." && pwd)"
# shellcheck source=env.sh
. "$HERE/env.sh"
cd "$REPO"

# --------------------------------------------------------------------------
# The isolated instance.
#
# `up` is idempotent, so calling it on an instance that already exists is a no-op — which is what
# makes a seeded replay cheap. `up --fresh` destroys the data first, which is what makes it a
# replay at all.
#
# Readiness is **the application's own readiness check**, not the container's: a healthy container
# says the dependency is listening, not that the schema is there.

up() {
  if [ "${1:-}" = "--fresh" ]; then
    echo "mt: destroying $MT_PROJECT and its data"
    # TODO: tear down the isolated instance, volumes and all.
    rm -f "$MT_HOME/session.sh"
  fi
  # TODO: bring the isolated instance up and wait for it, then migrate and seed the schema.
  #       Every command here must name $MT_PROJECT or the isolated addresses from env.sh.
  echo "mt: TODO — harness.sh up is not implemented yet"
  return 1
}

down() {
  if [ "${1:-}" = "--keep-data" ]; then
    : # TODO: stop the instance, keep its data
  else
    : # TODO: stop the instance and destroy its data
    rm -f "$MT_HOME/session.sh"
  fi
  echo "mt: TODO — harness.sh down is not implemented yet"
  return 1
}

# --------------------------------------------------------------------------
# Long-running processes. Each gets a pidfile and a logfile under $MT_HOME, so a later shell —
# which has none of this one's state — can still stop what this one started.

pidfile() { echo "$MT_HOME/$1.pid"; }
logfile() { mkdir -p "$MT_HOME/logs"; echo "$MT_HOME/logs/$1.log"; }

alive() { local p; p="$(pidfile "$1")"; [ -f "$p" ] && kill -0 "$(cat "$p")" 2>/dev/null; }

start_one() {
  local name="$1" cmd="$2" port="${3:-}"
  if alive "$name"; then echo "mt: $name already running ($(cat "$(pidfile "$name")"))"; return 0; fi
  # A wait on a health endpoint can be answered by a process built three slices ago, which then
  # dies with EADDRINUSE *after* the wait returned. These ports are ours alone, so anything holding
  # one is a leftover and is killed rather than waited for.
  if [ -n "$port" ]; then
    local held; held="$(lsof -ti "tcp:$port" 2>/dev/null || true)"
    [ -n "$held" ] && kill -9 $held 2>/dev/null || true
  fi
  : >"$(logfile "$name")"
  # shellcheck disable=SC2086
  nohup $cmd >>"$(logfile "$name")" 2>&1 &
  echo $! >"$(pidfile "$name")"
  if [ -n "$port" ]; then
    local i=0
    until curl -sf "http://127.0.0.1:$port/health" >/dev/null 2>&1; do
      i=$((i + 1))
      [ "$i" -gt 60 ] && { echo "mt: $name did not become healthy" >&2; tail -20 "$(logfile "$name")" >&2; return 1; }
      sleep 0.5
    done
  else
    sleep 1
    alive "$name" || { echo "mt: $name exited immediately" >&2; tail -20 "$(logfile "$name")" >&2; return 1; }
  fi
  echo "mt: $name up${port:+ on $port} (pid $(cat "$(pidfile "$name")"))"
}

stop_one() {
  local name="$1" p; p="$(pidfile "$1")"
  [ -f "$p" ] || { echo "mt: $name not running"; return 0; }
  # SIGTERM first, because the shutdown hook is part of what is under test.
  local pid; pid="$(cat "$p")"
  pkill -TERM -P "$pid" 2>/dev/null || true
  kill -TERM "$pid" 2>/dev/null || true
  sleep 1
  pkill -9 -P "$pid" 2>/dev/null || true
  kill -9 "$pid" 2>/dev/null || true
  rm -f "$p"
  echo "mt: $name stopped"
}

# TODO: name this project's long-running processes, in **dependency order** — the one that acts on
# what the others wrote goes last, or a walk never sees it act on work done before it was
# listening. One line each: `<name> <command> [port]`.
#
#   PROCESSES=("api:npm run start:api:3900" "worker:npm run start:worker:")
PROCESSES=()

servers() {
  local verb="${1:-status}" who="${2:-all}"
  # `${arr[@]}` on an empty array is an unbound variable under `set -u` in bash 3.2, which is
  # what macOS ships. `${arr[@]+"${arr[@]}"}` is the portable spelling, and it is used below.
  if [ "${#PROCESSES[@]+${#PROCESSES[@]}}" = "" ] || [ "${#PROCESSES[@]}" -eq 0 ]; then
    [ "$verb" = status ] && { echo "mt: no processes declared"; return 0; }
    echo "mt: TODO — no processes declared in harness.sh" >&2; return 1
  fi
  case "$verb" in
    start)
      for entry in ${PROCESSES[@]+"${PROCESSES[@]}"}; do
        local name="${entry%%:*}" rest="${entry#*:}"
        [ "$who" = all ] || [ "$who" = "$name" ] || continue
        start_one "$name" "${rest%:*}" "${rest##*:}"
      done ;;
    stop)
      for entry in ${PROCESSES[@]+"${PROCESSES[@]}"}; do
        local name="${entry%%:*}"
        [ "$who" = all ] || [ "$who" = "$name" ] || continue
        stop_one "$name"
      done ;;
    logs)  tail -n "${3:-50}" "$(logfile "$who")" ;;
    status)
      for entry in ${PROCESSES[@]+"${PROCESSES[@]}"}; do
        local name="${entry%%:*}"
        if alive "$name"; then echo "$name  running  pid $(cat "$(pidfile "$name")")"
        else echo "$name  stopped"; fi
      done ;;
    *) echo "mt: servers <start|stop|status|logs>" >&2; return 1 ;;
  esac
}

# --------------------------------------------------------------------------
# What the system says about itself, right now.
#
# Read this rather than trusting `reference/areas.md` for anything **enumerable**. That file is
# hand-written, and a hand-written copy of a moving surface goes stale. The reference keeps the
# reasoning, which cannot be queried; the enumerations come from here, which cannot be stale. Where
# the two disagree, this wins, and the disagreement is a drift finding.

surface() {
  # TODO: print this project's enumerable surface — its routes and what each requires, its error
  #       catalogue, its capability descriptors, its data classes. Every entry here is one the
  #       oracles no longer have to hand-copy. Nothing yet? Say so, and add to it each slice.
  echo "mt: TODO — harness.sh surface enumerates nothing yet"
}

status() {
  # TODO: one line per moving part of the isolated instance.
  echo "instance: TODO"
  echo
  servers status || true
  echo
  echo "MT_HOME   $MT_HOME"
  echo "seed      ${MT_SEED:-<unset>}"
}

case "${1:-status}" in
  up)      shift; up "$@" ;;
  down)    shift; down "$@" ;;
  servers) shift; servers "$@" ;;
  surface) shift; surface "$@" ;;
  drift)   python3 "$HERE/drift.py" ;;
  status)  status ;;
  *) sed -n '2,12p' "$0"; exit 1 ;;
esac
