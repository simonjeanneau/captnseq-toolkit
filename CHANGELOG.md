# Changelog

## Unreleased

- New `aggregate` subcommand (from the pipeline's `wrapper_BTA` / `BTAggregate`): compiles the per-sample `essentiality` outputs into run-level insertion-count (IC), read-count (RC) and binary essentiality (BT) gene x sample tables.
- Initial import of `sam2sites`, `sites2genes` and `essentiality` from the nf-core/captnseq pipeline `bin/` (logic unchanged).
- The `captnseq-toolkit` command is now a standard argparse CLI with subparsers. `--help`, `--version` and error handling come from argparse, so running with no subcommand or an unknown one exits with status 2 and argparse's usage message. Each tool's options are unchanged.
