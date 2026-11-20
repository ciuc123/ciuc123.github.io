"""Command line: lint-content, audit-site, audit-url."""
import argparse
import datetime as dt
import json
import os
import sys

from . import __version__
from . import model as m
from . import report
from .content_rules import lint_content
from .site_rules import audit_site
from .url_audit import audit_url

DEFAULT_CONFIG = ".seo-audit.json"


def load_config(path):
    if path is None:
        path = DEFAULT_CONFIG if os.path.exists(DEFAULT_CONFIG) else None
    if path is None:
        return {}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def build_parser():
    p = argparse.ArgumentParser(prog="seo_audit", description="Dependency-free SEO / AEO / GEO audit.")
    p.add_argument("--version", action="version", version=__version__)
    sub = p.add_subparsers(dest="mode", required=True)

    def common(sp):
        sp.add_argument("--config", help="JSON config with severity overrides (default: ./.seo-audit.json if present)")
        sp.add_argument("--json", metavar="FILE", help="write the JSON report here")
        sp.add_argument("--markdown", metavar="FILE", help="write the Markdown report here")
        sp.add_argument("--today", help="YYYY-MM-DD, for the future-date rule (default: today)")
        sp.add_argument("--quiet", action="store_true", help="no console report")

    sp = sub.add_parser("lint-content", help="check post front matter and bodies")
    sp.add_argument("posts_dir")
    common(sp)

    sp = sub.add_parser("audit-site", help="check a built site directory (e.g. _site)")
    sp.add_argument("site_dir")
    sp.add_argument("--posts", metavar="DIR", help="also lint this posts directory into the same report")
    sp.add_argument("--base-url", help="the site's public URL (default: base_url from config)")
    common(sp)

    sp = sub.add_parser("audit-url", help="check a live site through its sitemap (client mode)")
    sp.add_argument("url")
    sp.add_argument("--max-pages", type=int, default=50)
    sp.add_argument("--max-links", type=int, default=300, help="max internal links to request")
    common(sp)
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        config = load_config(args.config)
    except (OSError, ValueError) as e:
        print("config error: %s" % e, file=sys.stderr)
        return 2
    today = dt.date.fromisoformat(args.today) if args.today else dt.date.today()
    overrides = config.get("severity", {}) if args.mode != "audit-url" else config.get("url_severity", {})
    try:
        results = m.Results(overrides)
    except ValueError as e:
        print("config error: %s" % e, file=sys.stderr)
        return 2

    if args.mode == "lint-content":
        target = args.posts_dir
        lint_content(args.posts_dir, results, config, today)
    elif args.mode == "audit-site":
        target = args.site_dir
        if args.base_url:
            config = dict(config, base_url=args.base_url)
        if args.posts:
            lint_content(args.posts, results, config, today)
        audit_site(args.site_dir, results, config)
    else:
        target = args.url
        audit_url(args.url, results, config, args.max_pages, args.max_links)

    meta = {"mode": args.mode, "target": target, "date": today.isoformat(), "version": __version__}
    if not args.quiet:
        print(report.to_console(results, meta))
    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            f.write(report.to_json(results, meta))
    if args.markdown:
        with open(args.markdown, "w", encoding="utf-8") as f:
            f.write(report.to_markdown(results, meta))
    return 1 if results.errors else 0
