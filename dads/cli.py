"""D.A.D.S. Standalone CLI & Terminal Dashboard."""

import argparse
import sys
import http.server
import socketserver
import webbrowser
from pathlib import Path

from dads import (
    __version__,
    PORTAL_DIR,
    load_benchmark_data,
    load_turns
)
from dads.verify import print_verification_report, verify_benchmark_integrity
from dads.benchmark import run_state_microbenchmarks


def cmd_verify(args):
    """Verify cryptographic hashes and statistical integrity."""
    print_verification_report()


def cmd_models(args):
    """Display model performance comparison matrix."""
    data = load_benchmark_data()
    models = data.get("models", [])

    print("\n" + "=" * 76)
    print(f"  D.A.D.S. STANDARD TRIAL: MODEL COMPARISON MATRIX (N=11,000 TURNS)")
    print("=" * 76)
    print(f"  {'Model Name':<22} | {'Maker':<10} | {'Type':<14} | {'Unrailed':<10} | {'Railed (DADS)'}")
    print("  " + "-" * 72)
    for m in models:
        u = f"{m['unrailed_overall']:.1f}%"
        r = f"{m['railed_overall']:.1f}%"
        delta = f"(+{m['railed_overall'] - m['unrailed_overall']:.1f}%)"
        print(f"  {m['name']:<22} | {m['maker']:<10} | {m['type']:<14} | {u:<10} | {r:<6} {delta}")
    print("=" * 76 + "\n")


def cmd_turns(args):
    """List or inspect pre-registered benchmark turns."""
    turns = load_turns()

    if args.turn:
        # Inspect single turn
        matched = [t for t in turns if str(t.get("number")) == str(args.turn).zfill(2) or t.get("id") == args.turn]
        if not matched:
            print(f"[!] Turn '{args.turn}' not found. Valid options: 01 to 11.")
            sys.exit(1)
        t = matched[0]
        print("\n" + "=" * 76)
        print(f"  TURN {t.get('number')}: {t.get('title').upper()}")
        print("=" * 76)
        print(f"  Capability Domain:  {t.get('capability')}")
        print(f"  Pass Criteria:      {t.get('criteria')}")
        print(f"  Primary Failure:    {t.get('failure_mode')}")
        print(f"\n  [PROMPT]:\n  \"{t.get('prompt')}\"")
        print("\n  " + "-" * 72)
        print(f"  UNRAILED FAILURE SAMPLE (Pass Rate: {t.get('unrailed_pass_pct')}%):")
        print("  " + "\n  ".join(t.get("unrailed_sample", "").splitlines()))
        print(f"\n  Forensic Analysis: {t.get('unrailed_analysis')}")
        print("\n  " + "-" * 72)
        print(f"  D.A.D.S. RAILED PASS SAMPLE (Pass Rate: {t.get('railed_pass_pct')}% | McNemar: {t.get('mcnemar_p')}):")
        print("  " + "\n  ".join(t.get("railed_sample", "").splitlines()))
        print(f"\n  Forensic Analysis: {t.get('railed_analysis')}")
        print("=" * 76 + "\n")
    else:
        # List all turns
        print("\n" + "=" * 76)
        print("  D.A.D.S. 11 PRE-REGISTERED WORKDAY STRESS TURNS")
        print("=" * 76)
        print(f"  {'#':<4} | {'Capability Domain':<32} | {'Unrailed':<10} | {'Railed':<8} | {'p-value'}")
        print("  " + "-" * 72)
        for t in turns:
            num = str(t.get("number")).zfill(2)
            cap = t.get("capability")[:32]
            u = f"{t.get('unrailed_pass_pct', 0):.1f}%"
            r = f"{t.get('railed_pass_pct', 0):.1f}%"
            p = t.get("mcnemar_p", "N/A")
            print(f"  {num:<4} | {cap:<32} | {u:<10} | {r:<8} | {p}")
        print("=" * 76)
        print("  Tip: Inspect individual turn details with: dads turns --turn 02\n")


def cmd_benchmark(args):
    """Run decoupled memory hardware microbenchmarks."""
    run_state_microbenchmarks(iterations=args.iterations)


def cmd_serve(args):
    """Start local web server for the interactive visualizer dashboard."""
    port = args.port
    directory = str(PORTAL_DIR)

    class CustomHandler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *handler_args, **handler_kwargs):
            super().__init__(*handler_args, directory=directory, **handler_kwargs)

    print("\n" + "=" * 68)
    print(f"  Serving D.A.D.S. Interactive Evidence Dashboard")
    print(f"  URL: http://localhost:{port}")
    print(f"  Path: {directory}")
    print("  Press Ctrl+C to stop.")
    print("=" * 68 + "\n")

    if not args.no_browser:
        webbrowser.open(f"http://localhost:{port}")

    with socketserver.TCPServer(("", port), CustomHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")


def main():
    parser = argparse.ArgumentParser(
        prog="dads",
        description="Deterministic Autonomous Decoupled State (D.A.D.S.) Benchmark Suite CLI"
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # verify
    sub_verify = subparsers.add_parser("verify", help="Verify cryptographic hashes & trial integrity")
    sub_verify.set_defaults(func=cmd_verify)

    # models
    sub_models = subparsers.add_parser("models", help="Display model performance matrix")
    sub_models.set_defaults(func=cmd_models)

    # turns
    sub_turns = subparsers.add_parser("turns", help="List or inspect benchmark evaluation turns")
    sub_turns.add_argument("--turn", type=str, help="Turn number (01 to 11) or turn ID to inspect")
    sub_turns.set_defaults(func=cmd_turns)

    # benchmark
    sub_bench = subparsers.add_parser("benchmark", help="Execute decoupled state microbenchmarks")
    sub_bench.add_argument("--iterations", type=int, default=10000, help="Iteration count (default: 10,000)")
    sub_bench.set_defaults(func=cmd_benchmark)

    # serve
    sub_serve = subparsers.add_parser("serve", help="Serve interactive web evidence dashboard")
    sub_serve.add_argument("--port", type=int, default=8090, help="HTTP port (default: 8090)")
    sub_serve.add_argument("--no-browser", action="store_true", help="Do not auto-open browser")
    sub_serve.set_defaults(func=cmd_serve)

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

