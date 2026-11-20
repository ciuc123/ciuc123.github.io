"""Console, JSON and Markdown output."""
import json

from . import model as m

MAX_LISTED = 25


def summary(results):
    return {
        "score": results.score(),
        "checks": len(results.active()),
        "passed": len(results.passes),
        "errors": len(results.errors),
        "warnings": len(results.warnings),
    }


def to_json(results, meta):
    return json.dumps({"meta": meta, "summary": summary(results), "rules": results.by_rule()}, indent=2)


def _sorted_rules(results):
    order = {m.ERROR: 0, m.WARNING: 1}
    return sorted(results.by_rule().items(), key=lambda kv: (kv[1]["failed"] == 0, order.get(kv[1]["severity"], 2), kv[0]))


def to_console(results, meta):
    s = summary(results)
    lines = ["SEO audit: %s %s" % (meta.get("mode"), meta.get("target")),
             "Score %(score)d/100 · %(checks)d checks · %(passed)d passed · %(errors)d errors · %(warnings)d warnings" % s, ""]
    for rule_id, r in _sorted_rules(results):
        if not r["failed"]:
            continue
        lines.append("%-7s %-24s %d failed / %d passed  %s" % (r["severity"].upper(), rule_id, r["failed"], r["passed"], m.RULES[rule_id].description))
        for f in r["failures"][:5]:
            lines.append("          %s: %s" % (f["target"], f["message"]))
        if r["failed"] > 5:
            lines.append("          … %d more" % (r["failed"] - 5))
    passing = [rid for rid, r in _sorted_rules(results) if not r["failed"]]
    if passing:
        lines += ["", "Passing: " + ", ".join(passing)]
    return "\n".join(lines)


def to_markdown(results, meta):
    s = summary(results)
    out = ["# SEO audit report", "",
           "- **Mode:** `%s`  **Target:** `%s`" % (meta.get("mode"), meta.get("target")),
           "- **Date:** %s  **Tool:** seo_audit %s" % (meta.get("date"), meta.get("version")), "",
           "**Score: %(score)d/100** · %(checks)d checks · %(passed)d passed · %(errors)d errors · %(warnings)d warnings" % s, "",
           "| Rule | Severity | Failed | Passed | What it checks |", "|---|---|---:|---:|---|"]
    for rule_id, r in _sorted_rules(results):
        mark = "✅" if not r["failed"] else ("❌" if r["severity"] == m.ERROR else "⚠️")
        out.append("| %s `%s` | %s | %d | %d | %s |" % (mark, rule_id, r["severity"], r["failed"], r["passed"], m.RULES[rule_id].description))
    failing = [(rid, r) for rid, r in _sorted_rules(results) if r["failed"]]
    if failing:
        out += ["", "## Failures"]
        for rule_id, r in failing:
            out += ["", "### `%s` (%s, %d)" % (rule_id, r["severity"], r["failed"])]
            for f in r["failures"][:MAX_LISTED]:
                out.append("- `%s`: %s" % (f["target"], f["message"].replace("|", "\\|")))
            if r["failed"] > MAX_LISTED:
                out.append("- … %d more (see the JSON report)" % (r["failed"] - MAX_LISTED))
    return "\n".join(out) + "\n"
