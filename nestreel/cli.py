import argparse
def main(argv=None):
    p=argparse.ArgumentParser(prog="nestreel")
    sub=p.add_subparsers(dest="cmd", required=True)
    e=sub.add_parser("extract")
    e.add_argument("--mbox", required=True)
    e.add_argument("--tickets", required=True)
    e.add_argument("--out", required=True)
    e.add_argument("--checkpoint", required=True)
    v=sub.add_parser("verify")
    v.add_argument("--out", required=True)
    v.add_argument("--expect", required=True)
    args=p.parse_args(argv)
    if args.cmd=="extract":
        from nestreel.extract import run_extract
        return run_extract(args)
    if args.cmd=="verify":
        from nestreel.verify import run_verify
        return run_verify(args)
    return 2
if __name__=="__main__":
    raise SystemExit(main())
