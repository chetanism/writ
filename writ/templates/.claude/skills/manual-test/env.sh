# Point this shell at the manual-test instance. Source it, never execute it.
#
#   . .claude/skills/manual-test/env.sh
#
# **Source it at the top of every shell you run**, because a tool call gets a fresh shell and none
# of these survive from the last one. A command run without it reaches the *development* instance —
# which is the one you are also using — and the failure is silent: everything works, against the
# wrong data.
#
# Shell environment should beat any committed `.env` file. If this project's configuration loader
# prefers the file, that is worth knowing before the first walk, not during it.

# ---------------------------------------------------------------------------
# Where run state lives. Outside the repository, so a run never dirties the worktree and
# `git status` stays readable.
export MT_PROJECT="${MT_PROJECT:-PROJECT-manual}"     # TODO: the project's own name
MT_TMP="${TMPDIR:-/tmp}"; MT_TMP="${MT_TMP%/}"
export MT_HOME="${MT_HOME:-$MT_TMP/$MT_PROJECT}"

# ---------------------------------------------------------------------------
# The isolated instance's addresses. **Every one of these must differ from the development
# defaults**, or the isolation is nominal: same ports means same instance, and the walk quietly
# destroys the state you were working in.
#
# TODO: fill from the project's own configuration — one export per connection string, port or base
# URL a deployable reads. Keep the development value beside it in a comment, so a reader can see at
# a glance that the two do not collide.
#
#   export DATABASE_URL='...'          # dev: ...
#   export PORT="${PORT:-...}"         # dev: ...
#   export APP="http://127.0.0.1:${PORT}"

# Quieter than a debug level would be for a walk that runs hundreds of commands; server logs go to
# files under $MT_HOME and are read on demand, not streamed.
export LOG_LEVEL="${LOG_LEVEL:-info}"

# ---------------------------------------------------------------------------
# Identifiers the current run has discovered — the fixture's ids, its credentials, its handles.
# Appended by the run with `mt_remember` and re-sourced here, so they survive a shell that only
# lives for one command.
mkdir -p "$MT_HOME"
[ -f "$MT_HOME/session.sh" ] && . "$MT_HOME/session.sh"

# Record one identifier for later shells. `mt_remember KEY value`.
mt_remember() {
  printf 'export %s=%q\n' "$1" "$2" >>"$MT_HOME/session.sh"
  export "$1=$2"
}

# Append one line to the run transcript.
mt_log() {
  printf '%s\n' "$*" >>"$MT_HOME/${MT_SEED:-unseeded}/transcript.md"
}
