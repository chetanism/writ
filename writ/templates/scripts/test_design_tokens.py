#!/usr/bin/env python3
"""The design token tool's own suite.

    python3 scripts/test_design_tokens.py

Each test writes the smallest tree that shows one rule holding or one finding being made, and runs
the tool against it the way the gate does. Standard library only.
"""

from __future__ import annotations

import contextlib
import io
import json
import os
import shutil
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import design_tokens as D  # noqa: E402

TOKENS = {
    "color": {
        "$type": "color",
        "gray": {
            "0": {"$value": "#ffffff"},
            "500": {"$value": "#737373"},
            "900": {"$value": "#171717"},
            "950": {"$value": "oklch(14.5% 0 0)"},
        },
        "bg": {"default": {"$value": "{color.gray.0}"}},
        "text": {"default": {"$value": "{color.gray.900}"}, "muted": {"$value": "{color.gray.500}"}},
    },
    "space": {"$type": "dimension", "1": {"$value": "4px"}, "2": {"$value": {"value": 8, "unit": "px"}}},
    "font": {"family": {"$type": "fontFamily", "sans": {"$value": ["Inter Variable", "system-ui", "sans-serif"]}}},
    "motion": {
        "$type": "duration",
        "fast": {"$value": "120ms"},
        "ease": {"$type": "cubicBezier", "$value": [0.2, 0, 0, 1]},
    },
    "shadow": {"$type": "shadow", "sm": {"$value": "0 1px 2px {color.gray.900}"}},
    "radius": {"$type": "dimension", "md": {"$value": "8px"}},
    "breakpoint": {"$type": "dimension", "md": {"$value": "768px"}},
    "$themes": {"dark": {"color.bg.default": "{color.gray.950}", "color.text.default": "{color.gray.0}"}},
    "$contrast": [{"fg": "color.text.default", "bg": "color.bg.default"}],
}


class Tree:
    """A throwaway project: a config, a tokens file, and whatever source a test writes."""

    def __init__(self, tokens=None, design=None, enforce=None):
        self.root = tempfile.mkdtemp(prefix="design-")
        design = dict({"tokens": "design/tokens.json", "outputs": {"css": "src/styles/tokens.css"}}, **(design or {}))
        config = {"design": design}
        if enforce is not None:
            config["enforce"] = enforce
        self.write("scripts/ledger.config.json", json.dumps(config))
        if tokens is not False:
            self.write("design/tokens.json", json.dumps(TOKENS if tokens is None else tokens))

    def write(self, rel, text):
        path = os.path.join(self.root, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with io.open(path, "w", encoding="utf-8") as handle:
            handle.write(text)

    def read(self, rel):
        with io.open(os.path.join(self.root, rel), encoding="utf-8") as handle:
            return handle.read()

    def run(self, *argv):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = D.main(list(argv) + ["--root", self.root])
        return code, out.getvalue(), err.getvalue()

    def close(self):
        shutil.rmtree(self.root, ignore_errors=True)


class Base(unittest.TestCase):
    def tree(self, *args, **kwargs):
        tree = Tree(*args, **kwargs)
        self.addCleanup(tree.close)
        return tree


class ColourTest(unittest.TestCase):
    def test_white_on_black_is_twenty_one_to_one(self):
        white, _ = D.parse_color("#fff")
        black, _ = D.parse_color("rgb(0 0 0)")
        self.assertAlmostEqual(D.contrast(white, black), 21.0, places=2)

    def test_the_forms_a_css_author_writes_agree(self):
        want, _ = D.parse_color("#336699")
        for form in ("rgb(51, 102, 153)", "rgb(20% 40% 60%)", "hsl(210 50% 40%)", "hsl(210, 50%, 40%)"):
            got, alpha = D.parse_color(form)
            self.assertEqual(alpha, 1.0, form)
            for a, b in zip(got, want):
                self.assertAlmostEqual(a, b, places=2, msg=form)

    def test_oklch_round_trips_through_oklab(self):
        rgb, _ = D.parse_color("oklch(62.8% 0.2577 29.23)")  # sRGB red, as oklch writes it
        red, _ = D.parse_color("#ff0000")
        for a, b in zip(rgb, red):
            self.assertAlmostEqual(a, b, places=2)
        lab = D.linear_to_oklab(red)
        self.assertAlmostEqual(lab[0], 0.628, places=2)

    def test_alpha_is_read_in_every_form(self):
        self.assertAlmostEqual(D.parse_color("#00000080")[1], 0.5, places=2)
        self.assertAlmostEqual(D.parse_color("rgb(0 0 0 / 25%)")[1], 0.25)
        self.assertAlmostEqual(D.parse_color("rgba(0, 0, 0, 0.3)")[1], 0.3)

    def test_a_named_colour_is_refused_rather_than_guessed(self):
        with self.assertRaises(D.TokenError):
            D.parse_color("rebeccapurple")
        with self.assertRaises(D.TokenError):
            D.parse_color("#abcde")


class BuildTest(Base):
    def test_build_writes_every_token_and_keeps_references_as_var(self):
        tree = self.tree()
        code, out, err = tree.run("build")
        self.assertEqual(code, 0, err)
        css = tree.read("src/styles/tokens.css")
        self.assertIn("--color-gray-0: #ffffff;", css)
        self.assertIn("--color-text-default: var(--color-gray-900);", css)
        self.assertIn("--space-2: 8px;", css)
        self.assertIn('--font-family-sans: "Inter Variable", system-ui, sans-serif;', css)
        self.assertIn("--motion-ease: cubic-bezier(0.2, 0, 0, 1);", css)
        self.assertIn("--shadow-sm: 0 1px 2px var(--color-gray-900);", css)

    def test_a_dark_theme_follows_the_system_unless_the_page_has_chosen(self):
        tree = self.tree()
        tree.run("build")
        css = tree.read("src/styles/tokens.css")
        self.assertIn('[data-theme="dark"] {', css)
        self.assertIn("@media (prefers-color-scheme: dark) {", css)
        self.assertIn(":root:not([data-theme]) {", css)

    def test_a_theme_block_redeclares_the_tokens_that_depend_on_an_override(self):
        """A `var()` in a custom property is worked out where it is declared and inherited as the
        result, so a dependant declared only on `:root` would keep the light value under a
        `data-theme` set below `<html>`."""
        tree = self.tree()
        tree.run("build")
        css = tree.read("src/styles/tokens.css")
        dark = css.split('[data-theme="dark"] {')[1].split("}")[0]
        media = css.split(":root:not([data-theme]) {")[1].split("}")[0]
        for theme in (dark, media):
            self.assertIn("--color-bg-default: var(--color-gray-950);", theme)
            self.assertIn("--color-text-default: var(--color-gray-0);", theme)
            self.assertNotIn("--color-gray-0:", theme)  # neither overridden nor dependent
        chained = json.loads(json.dumps(TOKENS))
        chained["color"]["border"] = {"$value": "{color.text.default}"}
        chained["shadow"]["sm"]["$value"] = "0 1px 2px {color.border}"
        tree = self.tree(chained)
        tree.run("build")
        dark = tree.read("src/styles/tokens.css").split('[data-theme="dark"] {')[1].split("}")[0]
        self.assertIn("--color-border: var(--color-text-default);", dark)
        self.assertIn("--shadow-sm: 0 1px 2px var(--color-border);", dark)

    def test_build_refuses_tokens_that_do_not_resolve(self):
        broken = json.loads(json.dumps(TOKENS))
        broken["color"]["text"]["default"]["$value"] = "{color.gray.800}"
        tree = self.tree(broken)
        code, _, err = tree.run("build")
        self.assertEqual(code, 1)
        self.assertIn("{color.gray.800} names no token", err)
        self.assertFalse(os.path.exists(os.path.join(tree.root, "src/styles/tokens.css")))


class OutputsTest(Base):
    OUTPUTS = {"css": "src/styles/tokens.css", "tailwind": "src/styles/theme.css", "ts": "src/tokens.ts"}

    def test_the_tailwind_output_needs_a_prefix(self):
        tree = self.tree(design={"outputs": self.OUTPUTS})
        code, _, err = tree.run("build")
        self.assertEqual(code, 1)
        self.assertIn("needs design.prefix", err)

    def test_tailwind_names_point_at_the_tokens_and_the_default_palette_is_gone(self):
        tree = self.tree(design={"outputs": self.OUTPUTS, "prefix": "ds"})
        code, _, err = tree.run("build")
        self.assertEqual(code, 0, err)
        theme = tree.read("src/styles/theme.css")
        self.assertIn("@theme inline {", theme)
        self.assertIn("--color-*: initial;", theme)
        self.assertIn("--color-bg-default: var(--ds-color-bg-default);", theme)
        self.assertIn("--spacing-2: var(--ds-space-2);", theme)
        self.assertIn("--radius-md: var(--ds-radius-md);", theme)
        self.assertIn("--font-sans: var(--ds-font-family-sans);", theme)
        self.assertIn("--ease-ease: var(--ds-motion-ease);", theme)
        self.assertIn("--breakpoint-md: 768px;", theme)  # a media query cannot read a property
        self.assertNotIn("motion-fast", theme)  # durations have no Tailwind namespace
        css = tree.read("src/styles/tokens.css")
        self.assertIn("--ds-color-text-default: var(--ds-color-gray-900);", css)

    def test_the_typescript_output_carries_vars_and_each_themes_literals(self):
        tree = self.tree(design={"outputs": {"ts": "src/tokens.ts"}, "prefix": "ds"})
        code, _, err = tree.run("build")
        self.assertEqual(code, 0, err)
        ts = tree.read("src/tokens.ts")
        self.assertIn('"color.text.default": "var(--ds-color-text-default)",', ts)
        self.assertIn('export type Token = keyof typeof tokens;', ts)
        default = ts.split('"default": {')[1].split("},")[0]
        dark = ts.split('"dark": {')[1].split("},")[0]
        self.assertIn('"color.text.default": "#171717",', default)
        self.assertIn('"color.text.default": "#ffffff",', dark)
        self.assertIn('"shadow.sm": "0 1px 2px #171717",', default)

    def test_every_output_is_held_to_the_tokens(self):
        tree = self.tree(design={"outputs": self.OUTPUTS, "prefix": "ds"})
        tree.run("build")
        self.assertEqual(tree.run("check")[0], 0)
        tree.write("src/tokens.ts", tree.read("src/tokens.ts").replace("#171717", "#000000"))
        code, _, err = tree.run("check")
        self.assertEqual(code, 1)
        self.assertIn("src/tokens.ts: not what the tokens compile to", err)

    def test_a_config_from_before_outputs_still_builds_its_css(self):
        tree = self.tree(design={"outputs": {}, "css": "src/legacy.css"})
        code, _, err = tree.run("build")
        self.assertEqual(code, 0, err)
        self.assertIn("--color-gray-0: #ffffff;", tree.read("src/legacy.css"))


class CheckTest(Base):
    def built(self, *args, **kwargs):
        tree = self.tree(*args, **kwargs)
        code, _, err = tree.run("build")
        self.assertEqual(code, 0, err)
        return tree

    def test_off_until_the_config_names_a_tokens_file(self):
        tree = self.tree(tokens=False, design={"tokens": "", "outputs": {}})
        code, out, _ = tree.run("check")
        self.assertEqual(code, 0)
        self.assertIn("off", out)

    def test_a_built_tree_passes(self):
        code, out, err = self.built().run("check")
        self.assertEqual(code, 0, err)
        self.assertIn("every check passes", out)

    def test_an_edit_to_the_generated_css_fails(self):
        tree = self.built()
        tree.write("src/styles/tokens.css", tree.read("src/styles/tokens.css").replace("#ffffff", "#fefefe"))
        code, _, err = tree.run("check")
        self.assertEqual(code, 1)
        self.assertIn("not what the tokens compile to", err)

    def test_a_reference_loop_is_named(self):
        looped = json.loads(json.dumps(TOKENS))
        looped["color"]["bg"]["default"]["$value"] = "{color.bg.alt}"
        looped["color"]["bg"]["alt"] = {"$value": "{color.bg.default}"}
        code, _, err = self.tree(looped).run("check")
        self.assertEqual(code, 1)
        self.assertIn("references loop", err)

    def test_a_theme_may_not_invent_a_token(self):
        extra = json.loads(json.dumps(TOKENS))
        extra["$themes"]["dark"]["color.bg.sunken"] = "{color.gray.950}"
        code, _, err = self.tree(extra).run("check")
        self.assertEqual(code, 1)
        self.assertIn("color.bg.sunken overrides a token that does not exist", err)

    def test_a_dimension_without_a_unit_fails(self):
        bad = json.loads(json.dumps(TOKENS))
        bad["space"]["3"] = {"$value": "12"}
        code, _, err = self.tree(bad).run("check")
        self.assertEqual(code, 1)
        self.assertIn("space.3: a dimension needs a unit", err)

    def test_a_contrast_pair_that_fails_only_in_the_dark_theme_names_the_theme(self):
        dim = json.loads(json.dumps(TOKENS))
        dim["$themes"]["dark"]["color.text.default"] = "{color.gray.900}"
        code, _, err = self.tree(dim).run("check")
        self.assertEqual(code, 1)
        self.assertIn("$contrast[1] dark: color.text.default on color.bg.default", err)
        self.assertNotIn("$contrast[1] default", err)

    def test_the_minimum_is_per_pair(self):
        muted = json.loads(json.dumps(TOKENS))
        muted["$themes"] = {}
        muted["$contrast"] = [{"fg": "color.text.muted", "bg": "color.bg.default", "min": 7}]
        code, _, err = self.tree(muted).run("check")
        self.assertEqual(code, 1)
        self.assertIn("below 7.0:1", err)
        muted["$contrast"][0]["min"] = 4.5
        tree = self.built(muted)
        self.assertEqual(tree.run("check")[0], 0)

    def test_a_malformed_tokens_file_is_a_finding_not_a_traceback(self):
        code, _, err = self.tree(["not", "groups"]).run("check")
        self.assertEqual(code, 1)
        self.assertIn("the top level is an object", err)
        words = json.loads(json.dumps(TOKENS))
        words["$contrast"][0]["min"] = "abc"
        code, _, err = self.tree(words).run("check")
        self.assertEqual(code, 1)
        self.assertIn("$contrast[1]: min is a number", err)
        flat = json.loads(json.dumps(TOKENS))
        flat["$themes"]["dim"] = "{color.gray.500}"
        code, _, err = self.tree(flat).run("check")
        self.assertEqual(code, 1)
        self.assertIn("$themes.dim: an object of token path", err)
        self.assertNotIn("Traceback", err)

    def test_a_translucent_pair_is_refused_rather_than_guessed(self):
        glass = json.loads(json.dumps(TOKENS))
        glass["color"]["gray"]["0"]["$value"] = "#ffffff80"
        code, _, err = self.tree(glass).run("check")
        self.assertEqual(code, 1)
        self.assertIn("translucent", err)


class SourceScanTest(Base):
    def built(self, **kwargs):
        tree = self.tree(**kwargs)
        tree.run("build")
        return tree

    def test_raw_values_in_a_component_are_findings_with_their_line(self):
        tree = self.built()
        tree.write(
            "src/Button.tsx",
            "const a = 1;\n"
            "export const B = () => <button style={{ color: '#6b6f76', padding: '13px' }} />;\n"
            "const c = 'rgb(0 0 0 / 50%)';\n",
        )
        code, _, err = tree.run("check")
        self.assertEqual(code, 1)
        self.assertIn("src/Button.tsx:2: #6b6f76 is a raw value", err)
        self.assertIn("src/Button.tsx:2: 13px is a raw value", err)
        self.assertIn("src/Button.tsx:3: rgb(0 0 0 / 50%) is a raw value", err)

    def test_tokens_allowed_values_exemptions_and_queries_pass(self):
        tree = self.built()
        tree.write(
            "src/app.css",
            ".a { color: var(--color-text-default); padding: var(--space-2); }\n"
            ".b { border: 1px solid var(--color-gray-500); margin: 0; width: 100%; }\n"
            "@media (min-width: 768px) { .c { display: grid; } }\n"
            ".d { top: 3px; } /* design-exempt: aligns the icon to the text baseline */\n"
            'a[href="#top"] { text-decoration: none; }\n',
        )
        code, _, err = tree.run("check")
        self.assertEqual(code, 0, err)

    def test_a_named_colour_where_a_colour_is_set_is_a_finding(self):
        tree = self.built()
        tree.write("src/a.css", ".a {\n  border: 1px solid white;\n  white-space: nowrap;\n}\n")
        tree.write(
            "src/B.tsx",
            "const s = { backgroundColor: 'red', color: \"navy\" };\n"
            "const t = <p>Paint it red, or white.</p>;\n",
        )
        code, _, err = tree.run("check")
        self.assertEqual(code, 1)
        self.assertIn("src/a.css:2: white is a raw value", err)
        self.assertIn("src/B.tsx:1: red is a raw value", err)
        self.assertIn("src/B.tsx:1: navy is a raw value", err)
        self.assertNotIn("src/a.css:3", err)
        self.assertNotIn("src/B.tsx:2", err)

    def test_an_id_selector_or_a_fragment_is_not_a_colour(self):
        tree = self.built()
        tree.write("src/a.css", "#fab, #cafe {\n  display: block;\n}\n#bed { color: #fab; }\n")
        tree.write("src/B.tsx", 'const l = <a href="#add">Add</a>;\nconst f = <rect fill="url(#fade)" />;\n')
        code, _, err = tree.run("check")
        self.assertEqual(code, 1)
        self.assertEqual(err.count("raw value"), 1, err)
        self.assertIn("src/a.css:4: #fab is a raw value", err)

    def test_a_hash_in_the_text_of_a_page_is_not_a_colour(self):
        tree = self.built()
        tree.write(
            "src/Notes.tsx",
            "const n = <p>Fixed in PR #123, see issue #abc</p>;\n"
            "const s = { color: \"#fff\" };\n"
            "const t = <div style={{background:'#123456'}} />;\n"
            'const u = <path fill="#fff" />;\n'
            'const v = <div className="bg-[#abcdef]" />;\n'
            "const w = { border: '1px solid #000' };\n",
        )
        code, _, err = tree.run("check")
        self.assertEqual(code, 1)
        self.assertNotIn("src/Notes.tsx:1", err)
        for number, value in ((2, "#fff"), (3, "#123456"), (4, "#fff"), (5, "#abcdef"), (6, "#000")):
            self.assertIn("src/Notes.tsx:%d: %s is a raw value" % (number, value), err)

    def test_zero_is_not_a_decision_in_any_unit(self):
        tree = self.built(design={"allow": []})
        tree.write("src/a.css", ".a { margin: 0rem 0em -0px 0.0px; }\n")
        code, _, err = tree.run("check")
        self.assertEqual(code, 0, err)

    def test_a_member_expression_a_continued_selector_and_a_one_line_query(self):
        tree = self.built()
        tree.write("src/B.tsx", "const b = <p style={{ color: theme.red, background: colors.white.muted }} />;\n")
        tree.write(
            "src/a.css",
            "#fab:hover,\n"
            "a:focus,\n"
            "#bed {\n  color: var(--color-text-default);\n}\n"
            ".s {\n  box-shadow: 0 1px #abc,\n    0 2px var(--color-gray-500);\n}\n"
            "@media (min-width: 768px) { .a { color: #fff } }\n",
        )
        code, _, err = tree.run("check")
        self.assertEqual(code, 1)
        self.assertNotIn("src/B.tsx", err)
        self.assertNotIn("#fab", err)
        self.assertIn("src/a.css:7: #abc is a raw value", err)
        self.assertIn("src/a.css:10: #fff is a raw value", err)
        self.assertNotIn("768px", err)
        self.assertEqual(err.count("raw value"), 2, err)

    def test_an_exemption_without_a_reason_exempts_nothing(self):
        tree = self.built()
        tree.write(
            "src/a.css",
            ".a { top: 3px; } /* design-exempt: */\n"
            ".b { top: 5px; } /* design-exempt:*/\n"
            ".c { top: 7px; } /* design-exempt: optical centring on the glyph */\n",
        )
        tree.write("src/B.vue", '<div style="top: 9px" /><!-- design-exempt: -->\n')
        code, _, err = tree.run("check")
        self.assertEqual(code, 1)
        self.assertIn("src/a.css:1: exemption needs a reason", err)
        self.assertIn("src/a.css:1: 3px is a raw value", err)
        self.assertIn("src/a.css:2: exemption needs a reason", err)
        self.assertIn("src/B.vue:1: exemption needs a reason", err)
        self.assertNotIn("src/a.css:3", err)

    def test_the_shipped_config_scans_what_the_defaults_scan(self):
        """The shipped `sources` replaces the defaults wholesale, so a shorter list there silently
        stops the scan reading `.vue`, `.svelte` and `.less` files."""
        with io.open(os.path.join(HERE, "ledger.config.json"), encoding="utf-8") as handle:
            shipped = json.load(handle)["design"]["sources"]
        self.assertEqual(shipped, D.DEFAULTS["sources"])

    def test_the_generated_css_and_the_tokens_are_never_scanned(self):
        tree = self.built()
        self.assertEqual(tree.run("check")[0], 0)  # tokens.css is full of literals, by design

    def test_outside_the_perimeter_nothing_is_a_finding(self):
        tree = self.built(enforce={"default": ["**"], "design_values": ["src/ui/**"]})
        tree.write("src/legacy/Old.tsx", "const c = '#123456';\n")
        self.assertEqual(tree.run("check")[0], 0)
        tree.write("src/ui/New.tsx", "const c = '#123456';\n")
        code, _, err = tree.run("check")
        self.assertEqual(code, 1)
        self.assertIn("src/ui/New.tsx:1", err)
        self.assertNotIn("legacy", err)

    def test_an_empty_perimeter_scans_nothing(self):
        tree = self.built(enforce={"default": [], "design_values": None})
        tree.write("src/Any.tsx", "const c = '#123456';\n")
        self.assertEqual(tree.run("check")[0], 0)


class ExtractTest(Base):
    def test_near_duplicates_group_under_the_most_used_spelling(self):
        tree = self.tree(tokens=False, design={"tokens": "", "outputs": {}})
        tree.write("a.css", ".a { color: #6b6f76; }\n.b { color: #6b6f76; }\n.c { color: #6c6f76; }\n")
        tree.write("b.tsx", "const x = { color: '#6B6F76', gap: '12px', pad: '0.75rem', odd: '13px' };\n")
        tree.write("c.css", ".d { color: #ff0000; }\n")
        code, out, _ = tree.run("extract", "--json")
        self.assertEqual(code, 0)
        found = json.loads(out)
        top = found["colours"][0]
        self.assertEqual(top["value"], "#6b6f76")
        self.assertEqual(top["uses"], 4)
        self.assertEqual(top["variants"], ["#6c6f76"])
        self.assertEqual(top["files"], 2)
        self.assertEqual(len(found["colours"]), 2)
        twelve = [row for row in found["lengths"] if row["px"] == 12]
        self.assertEqual({row["as_written"] for row in twelve}, {"12px", "0.75rem"})
        self.assertFalse([row for row in found["lengths"] if row["px"] == 13][0]["on_4px_grid"])

    def test_space_separated_colours_keep_their_spaces(self):
        tree = self.tree(tokens=False, design={"tokens": "", "outputs": {}})
        tree.write(
            "a.css",
            ".a { color: oklch(0.5 0.1 200); }\n"
            ".b { color: rgb(1 2 3); }\n.c { color: rgb(12 3); }\n"
            ".d { color: rgb( 1 2  3 ); }\n",
        )
        code, out, _ = tree.run("extract", "--json")
        self.assertEqual(code, 0)
        found = json.loads(out)
        spelled = {g["value"] for g in found["colours"]} | {v for g in found["colours"] for v in g["variants"]}
        self.assertIn("oklch(0.5 0.1 200)", spelled)
        self.assertIn("rgb(1 2 3)", spelled)
        self.assertEqual([g["uses"] for g in found["colours"] if g["value"] == "rgb(1 2 3)"], [2])
        self.assertEqual(found["unparsed_colours"], ["rgb(12 3)"])

    def test_the_markdown_report_renders(self):
        tree = self.tree(tokens=False, design={"tokens": "", "outputs": {}})
        tree.write("a.css", ".a { color: #111; padding: 8px; }\n")
        code, out, _ = tree.run("extract")
        self.assertEqual(code, 0)
        self.assertIn("| `#111` | 1 | 1 |", out)
        self.assertIn("| 8 | `8px` | 1 | 1 | yes |", out)


if __name__ == "__main__":
    unittest.main(verbosity=2)
