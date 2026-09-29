#!/usr/bin/env python3
"""The design system's tokens, compiled to CSS and held to what the design spec says of them.

    python3 scripts/design_tokens.py build              # write every output the config names from the tokens
    python3 scripts/design_tokens.py check              # the gate: every rule below; exits 1 on a finding
    python3 scripts/design_tokens.py extract            # the literal values the code already uses, grouped
    python3 scripts/design_tokens.py extract --json     # the same, for a skill to read

**A design system written down and not checked is a style guide, and a style guide is decoration
within a quarter.** Somebody needs a grey that is not quite any of the greys, writes `#6b6f76`
into a component, and nothing says a word; a year later there are forty greys and the dark theme
works on half the screens. The tokens file is the one place a value is decided, and `check` is
what makes that true rather than aspirational:

  1. **The tokens parse and resolve.** Every `{group.name}` reference names a token that exists,
     no chain of references loops, every colour parses, and every dimension has a unit.
  2. **Every output is what the tokens say.** Each generated file is rebuilt in memory and
     compared, so an edit to an output instead of the source fails — the same freshness rule as
     the ledger.
  3. **Every declared contrast pair passes, in every theme.** `$contrast` names foreground and
     background tokens and a minimum ratio, WCAG 2 by default at 4.5. A dark theme that quietly
     puts grey text on a grey surface fails here rather than in an accessibility complaint.
  4. **No raw colour or length is written in the source.** A hex, an `rgb()` or `oklch()`, a named
     colour, a `px`, `rem` or `em` in a stylesheet or component, inside the `design_values` perimeter, is a value
     decided somewhere other than the tokens. The perimeter is `enforce` in `ledger.config.json`,
     so an existing codebase turns this on one directory at a time, exactly as it does every other
     rule. A line carrying the exemption marker and a reason is let through, and stays greppable.

`extract` runs the fourth rule's scan backwards, over the whole source tree and ignoring the
perimeter: every literal colour and length the code uses today, counted, with colours that are
indistinguishable to the eye grouped together. It is where a design system for a codebase that
already exists starts — from what was built, not from a blank page.

**The tokens file** is JSON in the shape of the W3C design tokens format: nested groups, a leaf is
any object with `$value`, `$type` is inherited from the nearest group that sets it. Two top-level
keys are this tool's own:

  - `$themes` — `{"dark": {"color.bg.default": "{color.gray.950}"}}`. A theme overrides tokens
    that exist; it never adds one, so every theme has the same names and a component cannot
    reference a token one theme forgot.
  - `$contrast` — `[{"fg": "color.text.default", "bg": "color.bg.default", "min": 4.5}]`.

**The outputs** are named in `design.outputs`, each a path or empty for off:

  - `css` — custom properties on `:root`, one block per theme, and the system's dark preference
    where the page has not chosen. What every other output reads at runtime.
  - `tailwind` — a Tailwind v4 `@theme inline` block mapping tokens onto Tailwind's namespaces, so
    `bg-bg-surface` and `var(--ds-color-bg-surface)` are one token rather than two systems. It
    resets Tailwind's default palette, so a class for a colour the tokens do not have does not
    exist. Needs `design.prefix`, because Tailwind's own names (`--color-*`) are what the tokens
    would otherwise be called.
  - `ts` — `tokens`, each a `var()` for styling that follows the theme, and `values`, each theme's
    literals for code that cannot read CSS: a chart, a canvas, an animation library.

Off until a project sets `design.tokens` in the config: `check` then says so and passes, so a
project with no interface is not failed for a file it has no reason to have.

Standard library only, Python 3.9+, like `ledger.py`.
"""

from __future__ import annotations

import argparse
import io
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ledger as L  # noqa: E402 — the config loader and the perimeter, so the two cannot disagree

DEFAULTS = {
    "tokens": "",
    "outputs": {"css": "", "tailwind": "", "ts": ""},
    # Put in front of every custom property: `ds` makes `--ds-color-bg-surface`. Required with the
    # Tailwind output; harmless without it.
    "prefix": "",
    # Skills the project chose for aesthetic direction — read by `/design-system` and by UI work,
    # never by this tool. Recorded here so the choice is one place somebody can find.
    "taste": [],
    "sources": {
        "globs": ["**/*.css", "**/*.scss", "**/*.less", "**/*.tsx", "**/*.jsx", "**/*.vue", "**/*.svelte"],
        "exclude": ["**/node_modules/**", "**/dist/**", "**/build/**", "**/.next/**"],
    },
    # Values too universal to be a decision. `0` needs no unit and `1px` is a hairline in every
    # system anybody has shipped; add to this list in the config rather than tokenising them.
    "allow": ["0px", "1px", "100%"],
    "exempt": "design-exempt:",
    "default_contrast": 4.5,
    # Two colours closer than this in OKLab read as one colour to almost everybody. 0.02 is about
    # one just-noticeable difference.
    "cluster": 0.02,
}

REFERENCE = re.compile(r"\{([A-Za-z0-9_$.-]+)\}")
WHOLE_REFERENCE = re.compile(r"^\{([A-Za-z0-9_$.-]+)\}$")
DIMENSION = re.compile(r"^-?\d*\.?\d+(px|rem|em|%|vh|vw|vmin|vmax|ch|ex|dvh|svh|lvh)$")
DURATION = re.compile(r"^\d*\.?\d+(ms|s)$")

# The raw values the scan looks for. Hex is bounded by what cannot precede it — `&#123;` is an
# entity and `a#b` is a selector — and by the lengths CSS accepts, so `#abcde` is not a colour.
HEX = re.compile(r"(?<![\w&#/-])#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{3,4})(?![\w-])")
COLOR_FUNCTION = re.compile(r"(?<![\w-])(?:rgba?|hsla?|hwb|lab|lch|oklab|oklch|color)\([^()]*\)", re.IGNORECASE)
LENGTH = re.compile(r"(?<![\w.#$-])-?(\d*\.?\d+)(px|rem|em)(?![\w-])")
# Named colours, by the CSS list. Looked for only where a colour is being set — a stylesheet
# declaration or a style property in a component — because `white` and `red` are ordinary words in
# the text of an interface. `transparent`, `currentColor` and `inherit` are not decisions.
NAMED_COLOURS = frozenset("""
aliceblue antiquewhite aqua aquamarine azure beige bisque black blanchedalmond blue blueviolet brown
burlywood cadetblue chartreuse chocolate coral cornflowerblue cornsilk crimson cyan darkblue darkcyan
darkgoldenrod darkgray darkgreen darkgrey darkkhaki darkmagenta darkolivegreen darkorange darkorchid
darkred darksalmon darkseagreen darkslateblue darkslategray darkslategrey darkturquoise darkviolet
deeppink deepskyblue dimgray dimgrey dodgerblue firebrick floralwhite forestgreen fuchsia gainsboro
ghostwhite gold goldenrod gray green greenyellow grey honeydew hotpink indianred indigo ivory khaki
lavender lavenderblush lawngreen lemonchiffon lightblue lightcoral lightcyan lightgoldenrodyellow
lightgray lightgreen lightgrey lightpink lightsalmon lightseagreen lightskyblue lightslategray
lightslategrey lightsteelblue lightyellow lime limegreen linen magenta maroon mediumaquamarine
mediumblue mediumorchid mediumpurple mediumseagreen mediumslateblue mediumspringgreen
mediumturquoise mediumvioletred midnightblue mintcream mistyrose moccasin navajowhite navy oldlace
olive olivedrab orange orangered orchid palegoldenrod palegreen paleturquoise palevioletred
papayawhip peachpuff peru pink plum powderblue purple rebeccapurple red rosybrown royalblue
saddlebrown salmon sandybrown seagreen seashell sienna silver skyblue slateblue slategray slategrey
snow springgreen steelblue tan teal thistle tomato turquoise violet wheat white whitesmoke yellow
yellowgreen
""".split())
# The properties that take a colour, in both spellings: `background-color` in a stylesheet and
# `backgroundColor` in a style object.
COLOUR_PROPERTY = re.compile(
    r"(?<![\w-])(?:(?:background|border(?:-?(?:top|right|bottom|left|block|inline))?|outline|text-?decoration|"
    r"caret|accent|column-?rule|flood|lighting|stop)-?color|color|background|border(?:-?(?:top|right|bottom|left))?|"
    r"outline|fill|stroke|box-?shadow|text-?shadow)\s*[:=]\s*\{?\s*[\"'`]?(?P<value>[^;{}\"'`\n]*)",
    re.IGNORECASE,
)
WORD = re.compile(r"[A-Za-z]+")
# What a stylesheet line looks like before its declarations: a selector and its brace. An id
# selector is spelled like a hex colour often enough (`#fab`, `#bed`, `#cafe`) to matter.
SELECTOR = re.compile(r"[^{};]*\{")
# A `#` that is a link target or a fragment rather than a colour: `href="#add"`, `url(#fade)`.
FRAGMENT = re.compile(r"(?:(?:href|to|id|for|xlink:href)\s*=\s*\{?\s*[\"'`]|url\(\s*[\"']?)$", re.IGNORECASE)
STYLESHEET = (".css", ".scss", ".sass", ".less", ".pcss")

# Custom properties cannot be read inside a media or container query, so a breakpoint written
# there is the only place a literal is the correct way to spell a token.
AT_QUERY = re.compile(r"^\s*@(media|container|custom-media)\b")


class TokenError(Exception):
    pass


# --------------------------------------------------------------------------------------------
# Colour
# --------------------------------------------------------------------------------------------


def _channel(text: str, scale: float) -> float:
    text = text.strip()
    if text.endswith("%"):
        return float(text[:-1]) / 100.0 * scale
    return float(text)


def _split_function(body: str) -> "tuple[list, float]":
    """`255 0 0 / 50%` and `255, 0, 0, 0.5` alike, as the channels and the alpha."""
    alpha = 1.0
    if "/" in body:
        body, raw = body.split("/", 1)
        alpha = _channel(raw, 1.0)
    parts = [p for p in re.split(r"[\s,]+", body.strip()) if p]
    if len(parts) == 4:
        alpha = _channel(parts.pop(), 1.0)
    return parts, alpha


def _hue(text: str) -> float:
    text = text.strip().lower()
    for unit, factor in (("deg", 1.0), ("turn", 360.0), ("grad", 0.9), ("rad", 180.0 / math.pi)):
        if text.endswith(unit):
            return float(text[: -len(unit)]) * factor
    return float(text)


def _linear(c: float) -> float:
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _clamp(value: float) -> float:
    return min(1.0, max(0.0, value))


def parse_color(text: str) -> "tuple[tuple, float]":
    """A CSS colour as **linear** sRGB channels in 0..1, and its alpha.

    Linear because both things done with a colour here are done in linear light: WCAG luminance,
    and the conversion to OKLab. Out-of-gamut `oklch()` is clamped, which is what a browser shows.
    Named colours are not parsed; a design system that means white writes it down."""
    raw = text.strip()
    lower = raw.lower()
    if lower.startswith("#"):
        digits = lower[1:]
        if len(digits) in (3, 4):
            digits = "".join(ch * 2 for ch in digits)
        if len(digits) not in (6, 8) or not re.fullmatch(r"[0-9a-f]+", digits):
            raise TokenError("not a colour: " + raw)
        rgb = tuple(_linear(int(digits[i : i + 2], 16) / 255.0) for i in (0, 2, 4))
        alpha = int(digits[6:8], 16) / 255.0 if len(digits) == 8 else 1.0
        return rgb, alpha
    match = re.fullmatch(r"(rgba?|hsla?|oklch|oklab)\((.*)\)", lower)
    if not match:
        raise TokenError("not a colour this tool reads (hex, rgb(), hsl(), oklch(), oklab()): " + raw)
    kind, body = match.groups()
    try:
        parts, alpha = _split_function(body)
        if len(parts) != 3:
            raise ValueError
        if kind.startswith("rgb"):
            rgb = tuple(_linear(_clamp(_channel(p, 255.0) / 255.0)) for p in parts)
        elif kind.startswith("hsl"):
            h = _hue(parts[0]) % 360.0
            s, lightness = _channel(parts[1], 1.0), _channel(parts[2], 1.0)
            if not parts[1].strip().endswith("%"):
                s /= 100.0
            if not parts[2].strip().endswith("%"):
                lightness /= 100.0
            k = lambda n: (n + h / 30.0) % 12  # noqa: E731
            a = s * min(lightness, 1 - lightness)
            f = lambda n: lightness - a * max(-1, min(k(n) - 3, 9 - k(n), 1))  # noqa: E731
            rgb = tuple(_linear(_clamp(f(n))) for n in (0, 8, 4))
        else:
            lightness = _channel(parts[0], 1.0)
            if kind == "oklch":
                chroma = _channel(parts[1], 0.4)
                h = math.radians(_hue(parts[2]))
                a, b = chroma * math.cos(h), chroma * math.sin(h)
            else:
                a, b = _channel(parts[1], 0.4), _channel(parts[2], 0.4)
            rgb = tuple(_clamp(c) for c in oklab_to_linear(lightness, a, b))
    except (ValueError, ZeroDivisionError):
        raise TokenError("not a colour: " + raw)
    return rgb, _clamp(alpha)


def oklab_to_linear(lightness: float, a: float, b: float) -> tuple:
    l_ = (lightness + 0.3963377774 * a + 0.2158037573 * b) ** 3
    m_ = (lightness - 0.1055613458 * a - 0.0638541728 * b) ** 3
    s_ = (lightness - 0.0894841775 * a - 1.2914855480 * b) ** 3
    return (
        4.0767416621 * l_ - 3.3077115913 * m_ + 0.2309699292 * s_,
        -1.2684380046 * l_ + 2.6097574011 * m_ - 0.3413193965 * s_,
        -0.0041960863 * l_ - 0.7034186147 * m_ + 1.7076147010 * s_,
    )


def linear_to_oklab(rgb: tuple) -> tuple:
    r, g, b = rgb
    l_ = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m_ = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s_ = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l_, m_, s_ = (math.copysign(abs(v) ** (1.0 / 3.0), v) for v in (l_, m_, s_))
    return (
        0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_,
        1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_,
        0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_,
    )


def luminance(rgb: tuple) -> float:
    r, g, b = rgb
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(fg: tuple, bg: tuple) -> float:
    """The WCAG 2 contrast ratio of two opaque colours, 1 to 21."""
    hi, lo = sorted((luminance(fg), luminance(bg)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


# --------------------------------------------------------------------------------------------
# Tokens
# --------------------------------------------------------------------------------------------


def flatten(tree: dict) -> dict:
    """`{"color.text.default": {"$value": …, "$type": "color"}}`, with `$type` inherited."""
    found = {}

    def walk(node: dict, path: list, inherited):
        kind = node.get("$type", inherited)
        if "$value" in node:
            found[".".join(path)] = {"$value": node["$value"], "$type": kind}
            return
        for key, child in node.items():
            if key.startswith("$"):
                continue
            if not isinstance(child, dict):
                raise TokenError(".".join(path + [key]) + ": a group holds groups and tokens, not a bare value")
            walk(child, path + [key], kind)

    walk({k: v for k, v in tree.items() if k not in ("$themes", "$contrast")}, [], None)
    return found


def css_name(path: str, prefix: str = "") -> str:
    return "--" + (prefix + "-" if prefix else "") + re.sub(r"[^A-Za-z0-9_-]", "-", path.replace(".", "-"))


def resolve(path: str, tokens: dict, overrides: dict, seen=()) -> object:
    """A token's literal value in one theme, following references to the end."""
    if path in seen:
        raise TokenError(" -> ".join(seen + (path,)) + ": references loop")
    if path not in tokens:
        raise TokenError((seen[-1] + ": " if seen else "") + "{" + path + "} names no token")
    value = overrides.get(path, tokens[path]["$value"])
    if isinstance(value, str):
        whole = WHOLE_REFERENCE.match(value.strip())
        if whole:
            return resolve(whole.group(1), tokens, overrides, seen + (path,))
        for ref in REFERENCE.findall(value):
            resolve(ref, tokens, overrides, seen + (path,))
    return value


def to_css(value: object, kind, prefix: str = "") -> str:
    """One token value as CSS, with every reference kept as `var()` so the chain survives."""
    if isinstance(value, str):
        return REFERENCE.sub(lambda m: "var(" + css_name(m.group(1), prefix) + ")", value)
    if isinstance(value, bool):
        raise TokenError("a boolean is not a CSS value")
    if isinstance(value, (int, float)):
        return repr(value) if isinstance(value, float) else str(value)
    if isinstance(value, list):
        if kind == "cubicBezier" and len(value) == 4:
            return "cubic-bezier(" + ", ".join(to_css(v, None, prefix) for v in value) + ")"
        if kind == "fontFamily":
            return ", ".join(('"%s"' % v) if " " in str(v) and not str(v).startswith('"') else str(v) for v in value)
        if kind == "shadow":
            return ", ".join(to_css(v, kind, prefix) for v in value)
        return " ".join(to_css(v, None, prefix) for v in value)
    if isinstance(value, dict):
        if set(value) == {"value", "unit"}:
            return to_css(value["value"], None, prefix) + str(value["unit"])
        if kind == "shadow":
            parts = ["inset"] if value.get("inset") else []
            for key in ("offsetX", "offsetY", "blur", "spread"):
                parts.append(to_css(value.get(key, "0px"), None, prefix))
            parts.append(to_css(value.get("color", "transparent"), None, prefix))
            return " ".join(parts)
    raise TokenError("a composite value this tool does not compile; write it as a string: " + json.dumps(value))


def validate(path: str, value: object, kind) -> list:
    """The literal a token resolves to is the kind of thing its `$type` says."""
    if isinstance(value, str) and REFERENCE.search(value) and not WHOLE_REFERENCE.match(value.strip()):
        return []  # a composite string such as a shadow; its references were resolved already
    try:
        if kind == "color":
            parse_color(str(value))
        elif kind == "dimension":
            text = to_css(value, kind)
            if text != "0" and not DIMENSION.match(text):
                return [path + ": a dimension needs a unit: " + text]
        elif kind == "duration":
            text = to_css(value, kind)
            if not DURATION.match(text):
                return [path + ": a duration is in ms or s: " + text]
    except TokenError as err:
        return [path + ": " + str(err)]
    return []


def load_tokens(root: str, design: dict) -> dict:
    full = os.path.join(root, design["tokens"])
    if not os.path.exists(full):
        raise TokenError(design["tokens"] + ": the tokens file the config names is not there")
    with io.open(full, encoding="utf-8") as handle:
        try:
            return json.load(handle)
        except ValueError as err:
            raise TokenError(design["tokens"] + ": does not parse: " + str(err))


HEADER = "Generated by scripts/design_tokens.py from %s. Edit the tokens, then run build."


def _names(tokens: dict, prefix: str) -> dict:
    """Custom property name to token path, refusing two paths that compile to one name."""
    names = {}
    for path in tokens:
        name = css_name(path, prefix)
        if name in names:
            raise TokenError("%s and %s both compile to %s" % (names[name], path, name))
        names[name] = path
    return names


def _themes(tree: dict, tokens: dict) -> dict:
    themes = tree.get("$themes") or {}
    for theme, overrides in themes.items():
        for path in overrides:
            if path not in tokens:
                raise TokenError("$themes.%s: %s overrides a token that does not exist" % (theme, path))
    return themes


def build_css(tree: dict, source: str, prefix: str = "") -> str:
    tokens = flatten(tree)
    _names(tokens, prefix)
    themes = _themes(tree, tokens)

    def block(selector: str, entries: dict, indent: str = "") -> list:
        out = [indent + selector + " {"]
        for path in sorted(entries):
            value = to_css(entries[path], tokens[path]["$type"], prefix)
            out.append(indent + "  " + css_name(path, prefix) + ": " + value + ";")
        out.append(indent + "}")
        return out

    lines = ["/* " + HEADER % source + " */", ""]
    lines += block(":root", {p: t["$value"] for p, t in tokens.items()})
    for theme in sorted(themes):
        overrides = themes[theme]
        lines.append("")
        lines += block('[data-theme="%s"]' % theme, overrides)
        # The system preference applies only where the page has not chosen, so an explicit
        # `data-theme="light"` still wins over a dark operating system.
        if theme == "dark":
            lines.append("")
            lines.append("@media (prefers-color-scheme: dark) {")
            lines += block(":root:not([data-theme])", overrides, "  ")
            lines.append("}")
    return "\n".join(lines) + "\n"


# Which Tailwind v4 namespace a token lands in. By its group's name first — `font.family` and
# `font.weight` are both fonts, and a dimension could be a space, a radius, a type size or a
# breakpoint — then by `$type` for the groups that are named for their type anyway.
TAILWIND_BY_GROUP = {"space": "spacing", "spacing": "spacing", "radius": "radius", "breakpoint": "breakpoint",
                     "breakpoints": "breakpoint", "text": "text", "font.size": "text", "font.family": "font",
                     "font.weight": "font-weight", "container": "container", "shadow": "shadow", "ease": "ease"}
TAILWIND_BY_TYPE = {"color": "color", "fontFamily": "font", "fontWeight": "font-weight", "shadow": "shadow",
                    "cubicBezier": "ease"}


def tailwind_name(path: str, kind) -> "str | None":
    """`color.bg.surface` → `--color-bg-surface`: the namespace, then the path below its group."""
    parts = path.split(".")
    namespace, rest = None, []
    for depth in (2, 1):
        group = ".".join(parts[:depth])
        if group in TAILWIND_BY_GROUP and len(parts) > depth:
            namespace, rest = TAILWIND_BY_GROUP[group], parts[depth:]
            break
    if namespace is None and kind != "dimension":
        namespace, rest = TAILWIND_BY_TYPE.get(kind), parts[1:]
    if namespace is None or not rest:
        return None
    return "--" + namespace + "-" + re.sub(r"[^A-Za-z0-9_-]", "-", "-".join(rest))


def build_tailwind(tree: dict, source: str, prefix: str = "") -> str:
    """A Tailwind v4 `@theme inline` block pointing Tailwind's names at the tokens' properties.

    `inline`, so a utility reads the token's property directly and a theme override reaches it.
    Breakpoints are the exception and are written as literals: a media query cannot read a
    property. The default palette is reset, so `bg-red-500` stops existing unless a token is it."""
    if not prefix:
        raise TokenError(
            "the Tailwind output needs design.prefix — without one the tokens' own properties are "
            "Tailwind's names, and every mapping would point at itself"
        )
    tokens = flatten(tree)
    names = _names(tokens, prefix)
    lines = ["/* " + HEADER % source + " */", "", "@theme inline {", "  --color-*: initial;"]
    mapped = {}
    for path in sorted(tokens):
        kind = tokens[path]["$type"]
        name = tailwind_name(path, kind)
        if name is None:
            continue
        if name in mapped:
            raise TokenError("%s and %s both map to Tailwind's %s" % (mapped[name], path, name))
        if name in names:
            raise TokenError("%s: Tailwind's %s is also a token property; choose another prefix" % (path, name))
        mapped[name] = path
        if name.startswith("--breakpoint-"):
            value = literal(path, tokens, {}, prefix)
        else:
            value = "var(" + css_name(path, prefix) + ")"
        lines.append("  " + name + ": " + value + ";")
    lines.append("}")
    return "\n".join(lines) + "\n"


VAR = re.compile(r"var\((--[A-Za-z0-9_-]+)\)")


def literal(path: str, tokens: dict, overrides: dict, prefix: str = "") -> str:
    """A token as CSS with every reference replaced by what it resolves to in one theme."""
    names = {css_name(p, prefix): p for p in tokens}
    value = resolve(path, tokens, overrides)
    text = to_css(value, tokens[path]["$type"], prefix)
    return VAR.sub(lambda m: literal(names[m.group(1)], tokens, overrides, prefix) if m.group(1) in names
                   else m.group(0), text)


def build_ts(tree: dict, source: str, prefix: str = "") -> str:
    """`tokens` for styling that follows the theme; `values` for code that needs the literal."""
    tokens = flatten(tree)
    _names(tokens, prefix)
    themes = _themes(tree, tokens)
    lines = ["// " + HEADER % source, "", "export const tokens = {"]
    for path in sorted(tokens):
        lines.append("  %s: %s," % (json.dumps(path), json.dumps("var(" + css_name(path, prefix) + ")")))
    lines += ["} as const;", "", "export type Token = keyof typeof tokens;", "", "export const values = {"]
    for theme, overrides in [("default", {})] + sorted(themes.items()):
        lines.append("  %s: {" % json.dumps(theme))
        for path in sorted(tokens):
            lines.append("    %s: %s," % (json.dumps(path), json.dumps(literal(path, tokens, overrides, prefix))))
        lines.append("  },")
    lines += ["} as const satisfies Record<string, Record<Token, string>>;", ""]
    return "\n".join(lines)


BUILDERS = {"css": build_css, "tailwind": build_tailwind, "ts": build_ts}


def outputs(design: dict) -> dict:
    """Format to path, for the outputs switched on."""
    return {fmt: path for fmt, path in (design.get("outputs") or {}).items() if path and fmt in BUILDERS}


# --------------------------------------------------------------------------------------------
# The checks
# --------------------------------------------------------------------------------------------


def settings(config: dict) -> dict:
    design = json.loads(json.dumps(DEFAULTS))
    for key, value in (config.get("design") or {}).items():
        if isinstance(value, dict) and isinstance(design.get(key), dict) and value:
            design[key].update(value)
        else:
            design[key] = value
    # `css` sat at the top level before there was more than one output; still honoured.
    if design.get("css") and not design["outputs"].get("css"):
        design["outputs"]["css"] = design["css"]
    return design


def check_tokens(tree: dict, design: dict) -> list:
    errors = []
    try:
        tokens = flatten(tree)
    except TokenError as err:
        return [str(err)]
    themes = tree.get("$themes") or {}
    if not isinstance(themes, dict):
        return ["$themes: an object of theme name to overrides"]
    for theme, overrides in [("", {})] + sorted(themes.items()):
        where = ("$themes." + theme + ": ") if theme else ""
        for path in overrides:
            if path not in tokens:
                errors.append(where + path + " overrides a token that does not exist")
        for path, token in sorted(tokens.items()):
            if theme and path not in overrides and not _depends_on(path, tokens, overrides):
                continue
            try:
                value = resolve(path, tokens, overrides)
            except TokenError as err:
                errors.append(where + str(err))
                continue
            errors += [where + e for e in validate(path, value, token["$type"])]
    for number, pair in enumerate(tree.get("$contrast") or [], start=1):
        errors += check_pair(number, pair, tokens, themes, design)
    return sorted(set(errors))


def _depends_on(path: str, tokens: dict, overrides: dict) -> bool:
    try:
        value = tokens[path]["$value"]
        refs = REFERENCE.findall(value) if isinstance(value, str) else []
        return any(r in overrides or _depends_on(r, tokens, overrides) for r in refs if r in tokens)
    except RecursionError:
        return True


def check_pair(number: int, pair: dict, tokens: dict, themes: dict, design: dict) -> list:
    label = "$contrast[%d]" % number
    if not isinstance(pair, dict) or "fg" not in pair or "bg" not in pair:
        return [label + ": a pair names fg and bg"]
    minimum = float(pair.get("min", design["default_contrast"]))
    errors = []
    for theme, overrides in [("default", {})] + sorted(themes.items()):
        try:
            fg, fg_alpha = parse_color(str(resolve(pair["fg"], tokens, overrides)))
            bg, bg_alpha = parse_color(str(resolve(pair["bg"], tokens, overrides)))
        except TokenError as err:
            errors.append("%s %s: %s" % (label, theme, err))
            continue
        if fg_alpha < 1 or bg_alpha < 1:
            errors.append(
                "%s %s: %s on %s is translucent, and its contrast depends on what is beneath it — "
                "pair the opaque colours it composites to" % (label, theme, pair["fg"], pair["bg"])
            )
            continue
        ratio = contrast(fg, bg)
        if ratio + 1e-9 < minimum:
            errors.append(
                "%s %s: %s on %s is %.2f:1, below %.1f:1" % (label, theme, pair["fg"], pair["bg"], ratio, minimum)
            )
    return errors


def source_files(root: str, design: dict) -> list:
    sources = design["sources"]
    skip = {os.path.normpath(p) for p in [design.get("tokens")] + list(outputs(design).values()) if p}
    found = []
    for path in L.iter_files(root, sources.get("globs") or [], sources.get("exclude") or []):
        rel = os.path.relpath(path, root).replace(os.sep, "/")
        if os.path.normpath(rel) not in skip and os.path.isfile(path):
            found.append((path, rel))
    return found


def raw_values(line: str, stylesheet: bool = False) -> list:
    """Every literal colour and length on one line, as written.

    In a stylesheet only the declarations are read, so an id selector spelled like a hex colour is
    not one. Anywhere, a `#` that is a link target or an SVG fragment is not a colour."""
    if AT_QUERY.match(line):
        return []
    if stylesheet:
        line = SELECTOR.sub(" ", line)
        if ":" not in line:
            return []  # a selector list continued onto its own line, or a closing brace
    hits = [m.group(0) for m in HEX.finditer(line) if not FRAGMENT.search(line[: m.start()])]
    hits += [m.group(0) for m in COLOR_FUNCTION.finditer(line)]
    hits += [m.group(0) for m in LENGTH.finditer(line)]
    for match in COLOUR_PROPERTY.finditer(line):
        value = VAR.sub(" ", match.group("value"))  # `var(--color-gray-500)` names a token, not grey
        hits += [w for w in WORD.findall(value) if w.lower() in NAMED_COLOURS]
    return hits


def check_sources(root: str, config: dict, design: dict) -> list:
    fence = L.perimeter(config, "design_values")
    if not fence:
        return []
    allowed = set(design.get("allow") or [])
    marker = design.get("exempt") or ""
    errors = []
    for path, rel in source_files(root, design):
        if not L.within(rel, fence):
            continue
        with io.open(path, encoding="utf-8", errors="replace") as handle:
            for number, line in enumerate(handle, start=1):
                if marker and marker in line:
                    continue
                for hit in raw_values(line, rel.endswith(STYLESHEET)):
                    if hit not in allowed:
                        errors.append("%s:%d: %s is a raw value; use a token" % (rel, number, hit))
    return errors


def check(root: str, config: dict) -> "tuple[list, str]":
    design = settings(config)
    if not design.get("tokens"):
        return [], "design: off — design.tokens is empty in ledger.config.json"
    try:
        tree = load_tokens(root, design)
    except TokenError as err:
        return [str(err)], ""
    errors = check_tokens(tree, design)
    for fmt, path in sorted(outputs(design).items()) if not errors else []:
        try:
            want = BUILDERS[fmt](tree, design["tokens"], design.get("prefix") or "")
        except TokenError as err:
            errors.append(fmt + ": " + str(err))
            continue
        full = os.path.join(root, path)
        have = None
        if os.path.exists(full):
            with io.open(full, encoding="utf-8") as handle:
                have = handle.read()
        if have != want:
            errors.append(path + ": not what the tokens compile to; run scripts/design_tokens.py build")
    errors += check_sources(root, config, design)
    tokens = len(flatten(tree)) if not errors else 0
    return errors, "design: %d tokens, %d contrast pairs, every check passes" % (
        tokens,
        len(tree.get("$contrast") or []),
    )


# --------------------------------------------------------------------------------------------
# Extract
# --------------------------------------------------------------------------------------------


def to_px(text: str) -> "float | None":
    match = LENGTH.fullmatch(text)
    if not match:
        return None
    number, unit = float(match.group(1)), match.group(2)
    return number * (16.0 if unit in ("rem", "em") else 1.0) * (-1 if text.startswith("-") else 1)


def extract(root: str, config: dict) -> dict:
    """Every literal the source uses, counted; colours grouped where the eye cannot tell them apart."""
    design = settings(config)
    colours, lengths, places = {}, {}, {}
    for path, rel in source_files(root, design):
        with io.open(path, encoding="utf-8", errors="replace") as handle:
            for line in handle:
                for hit in raw_values(line, rel.endswith(STYLESHEET)):
                    key = hit.lower().replace(" ", "")
                    bucket = lengths if to_px(hit) is not None else colours
                    bucket[key] = bucket.get(key, 0) + 1
                    places.setdefault(key, set()).add(rel)
    groups = []
    parsed = {}
    for key in colours:
        try:
            rgb, alpha = parse_color(key)
            parsed[key] = (linear_to_oklab(rgb), alpha)
        except TokenError:
            continue
    # Greedy, most-used first: the value a codebase uses most is the one it most likely meant.
    for key in sorted(parsed, key=lambda k: (-colours[k], k)):
        lab, alpha = parsed[key]
        for group in groups:
            centre, centre_alpha = parsed[group["value"]]
            if abs(alpha - centre_alpha) < 0.01 and math.dist(lab, centre) < float(design["cluster"]):
                group["variants"].append(key)
                group["uses"] += colours[key]
                break
        else:
            groups.append({"value": key, "variants": [], "uses": colours[key], "lightness": round(lab[0], 3)})
    for group in groups:
        group["files"] = len(set().union(*(places[k] for k in [group["value"]] + group["variants"])))
    unparsed = sorted(k for k in colours if k not in parsed)
    scale = sorted(
        (
            {"px": to_px(k), "as_written": k, "uses": n, "on_4px_grid": to_px(k) % 4 == 0, "files": len(places[k])}
            for k, n in lengths.items()
        ),
        key=lambda row: (row["px"], row["as_written"]),
    )
    return {
        "colours": sorted(groups, key=lambda g: (-g["uses"], g["value"])),
        "unparsed_colours": unparsed,
        "lengths": scale,
        "files_scanned": len(source_files(root, design)),
    }


def render_extract(found: dict) -> str:
    out = ["# What the code already uses", ""]
    out.append("%d files scanned." % found["files_scanned"])
    out.append("")
    out.append("## Colours, grouped where the eye cannot tell them apart")
    out.append("")
    out.append("| Colour | Uses | Files | OKLab L | Also written as |")
    out.append("|---|---|---|---|---|")
    for g in found["colours"]:
        out.append(
            "| `%s` | %d | %d | %.3f | %s |"
            % (g["value"], g["uses"], g["files"], g["lightness"], ", ".join("`%s`" % v for v in g["variants"]) or "—")
        )
    if found["unparsed_colours"]:
        out.append("")
        out.append("Not read as colours: " + ", ".join("`%s`" % v for v in found["unparsed_colours"]))
    out.append("")
    out.append("## Lengths")
    out.append("")
    out.append("| px | As written | Uses | Files | On a 4px grid |")
    out.append("|---|---|---|---|---|")
    for row in found["lengths"]:
        out.append(
            "| %g | `%s` | %d | %d | %s |"
            % (row["px"], row["as_written"], row["uses"], row["files"], "yes" if row["on_4px_grid"] else "no")
        )
    return "\n".join(out) + "\n"


# --------------------------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------------------------


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("command", choices=("build", "check", "extract"))
    parser.add_argument("--root", default=".", help="project root")
    parser.add_argument("--config", default="scripts/ledger.config.json")
    parser.add_argument("--json", action="store_true", help="extract: print JSON rather than Markdown")
    args = parser.parse_args(argv)
    root = os.path.abspath(args.root)
    config = L.load_config(root, args.config)

    if args.command == "extract":
        found = extract(root, config)
        print(json.dumps(found, indent=2) if args.json else render_extract(found), end="" if not args.json else "\n")
        return 0

    if args.command == "build":
        design = settings(config)
        if not design.get("tokens") or not outputs(design):
            print("design: set design.tokens and at least one of design.outputs in ledger.config.json first",
                  file=sys.stderr)
            return 1
        try:
            tree = load_tokens(root, design)
            errors = check_tokens(tree, design)
            if errors:
                raise TokenError("\n".join(errors))
            built = {path: BUILDERS[fmt](tree, design["tokens"], design.get("prefix") or "")
                     for fmt, path in outputs(design).items()}
        except TokenError as err:
            print(str(err), file=sys.stderr)
            return 1
        for path, text in sorted(built.items()):
            full = os.path.join(root, path)
            os.makedirs(os.path.dirname(full) or ".", exist_ok=True)
            with io.open(full, "w", encoding="utf-8") as handle:
                handle.write(text)
            print("design: wrote " + path)
        return 0

    errors, summary = check(root, config)
    for error in errors:
        print(error, file=sys.stderr)
    if errors:
        print("design: %d finding(s)" % len(errors), file=sys.stderr)
        return 1
    print(summary)
    return 0


if __name__ == "__main__":
    sys.exit(main())
