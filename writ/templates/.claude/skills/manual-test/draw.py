#!/usr/bin/env python3
"""Deterministic choice, so a seed is the run and not a decoration.

  python3 draw.py <seed> <counter> --int <n>       one integer in [0, n)
  python3 draw.py <seed> <counter> --pick          one line from stdin
  python3 draw.py <seed> <counter> --sample <k>    k distinct lines from stdin
  python3 draw.py <seed> <counter> --shuffle       every line, permuted
  python3 draw.py --seed                           a fresh seed to record

Why this exists rather than "choose randomly": a model asked to be random revisits the same three
creative cases, and `shuf --random-source` is GNU — absent on macOS. This is a hash, not a stream,
so there is no PRNG state to thread through a driver that gets a new shell for every command: the
same (seed, counter) is the same answer for ever, on any machine, in any order.

`counter` is the step number. Reusing one is how two draws collide, so a walk increments it every
draw and records it in the transcript beside the choice — which is what makes a replay a replay
and not a second run.

Stdlib only, Python 3.9+, matching `scripts/ledger.py`: this kit asks for one runtime, not two.
"""

import hashlib
import random
import sys
import time


def _h(seed: str, counter: str, salt) -> int:
    """A uniform-enough 32-bit value from (seed, counter, salt)."""
    digest = hashlib.sha256("{}:{}:{}".format(seed, counter, salt).encode("utf-8")).digest()
    return int.from_bytes(digest[:4], "big")


def _lines() -> list:
    return [
        line.strip()
        for line in sys.stdin.read().split("\n")
        if line.strip() and not line.strip().startswith("#")
    ]


def _shuffled(seed: str, counter: str, items: list) -> list:
    """Fisher-Yates, drawing each swap from its own hash."""
    out = list(items)
    for i in range(len(out) - 1, 0, -1):
        j = _h(seed, counter, i) % (i + 1)
        out[i], out[j] = out[j], out[i]
    return out


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)

    if argv[:1] == ["--seed"]:
        # Six words of hex is enough to name a run and short enough to retype.
        raw = "{}:{}".format(int(time.time() * 1000), random.random())
        sys.stdout.write(hashlib.sha256(raw.encode("utf-8")).hexdigest()[:12] + "\n")
        return 0

    if len(argv) < 3:
        sys.stderr.write("usage: draw.py <seed> <counter> <--int n|--pick|--sample k|--shuffle>\n")
        return 1

    seed, counter, mode = argv[0], argv[1], argv[2]
    arg = argv[3] if len(argv) > 3 else None

    if mode == "--int":
        try:
            n = int(arg)
        except (TypeError, ValueError):
            n = 0
        if n <= 0:
            sys.stderr.write("--int needs a positive integer\n")
            return 1
        sys.stdout.write(str(_h(seed, counter, "int") % n) + "\n")
        return 0

    if mode == "--pick":
        items = _lines()
        if not items:
            return 1
        sys.stdout.write(items[_h(seed, counter, "pick") % len(items)] + "\n")
        return 0

    if mode == "--sample":
        try:
            k = int(arg)
        except (TypeError, ValueError):
            k = 0
        if k <= 0:
            sys.stderr.write("--sample needs a positive integer\n")
            return 1
        sys.stdout.write("\n".join(_shuffled(seed, counter, _lines())[:k]) + "\n")
        return 0

    if mode == "--shuffle":
        sys.stdout.write("\n".join(_shuffled(seed, counter, _lines())) + "\n")
        return 0

    sys.stderr.write("draw: unknown mode " + mode + "\n")
    return 1


if __name__ == "__main__":
    sys.exit(main())
