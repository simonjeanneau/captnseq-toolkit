"""Compile per-sample gene tables into run-level gene x sample matrices.

Reads every ``<sample>-genes_insertions.all.csv`` and ``<sample>-genes_insertions.essen.csv`` in a
folder (the ``essentiality`` outputs) and writes three tab-separated tables:

  IC  insertion count (``ins_count``) per gene and sample
  RC  read count (``read_count``) per gene and sample
  BT  binary essentiality: 1 if the gene is in the sample's .essen.csv, 0 otherwise (ambiguous = 0)

Usage: captnseq-toolkit aggregate --input-dir 07_statisticalreport --output-ic IC.tsv
       --output-rc RC.tsv --output-bt BT.tsv

Ported from the CAPTn-seq Snakemake pipeline (BTaggregator_v2.BTAggregate, rule wrapper_BTA);
only the IC / RC / BT outputs used by the pipeline are kept.
"""

import argparse
from pathlib import Path

import pandas as pd

ALL_SUFFIX = "-genes_insertions.all.csv"
ESSEN_SUFFIX = "-genes_insertions.essen.csv"


def _find_files(input_dir, suffix):
    files = sorted(Path(input_dir).glob(f"*{suffix}"), key=lambda p: p.name)
    if not files:
        raise FileNotFoundError(f"No files found with extension {suffix} in {input_dir}")
    return files


def _sample_name(path, suffix):
    return path.name[: -len(suffix)]


def compute_aggregates(input_dir, output_ic, output_rc, output_bt):
    all_files = _find_files(input_dir, ALL_SUFFIX)
    essen_files = _find_files(input_dir, ESSEN_SUFFIX)

    ic, rc = {}, {}
    for path in all_files:
        df = pd.read_csv(path, usecols=["gene_name", "ins_count", "read_count"], index_col="gene_name")
        name = _sample_name(path, ALL_SUFFIX)
        ic[name] = df["ins_count"]
        rc[name] = df["read_count"]

    samples = sorted(ic)
    ic_df = pd.concat({name: ic[name] for name in samples}, axis=1)
    rc_df = pd.concat({name: rc[name] for name in samples}, axis=1)
    ic_df.index.name = rc_df.index.name = "gene"

    # Gene order of BT follows the first .all.csv
    genes = pd.read_csv(all_files[0], usecols=["gene_name"])["gene_name"].tolist()
    essential = {
        _sample_name(path, ESSEN_SUFFIX): set(pd.read_csv(path, usecols=["gene_name"])["gene_name"])
        for path in essen_files
    }
    bt_df = pd.DataFrame(
        {name: [1 if gene in essential[name] else 0 for gene in genes] for name in sorted(essential)},
        index=genes,
    )
    bt_df.index.name = "gene"

    ic_df.to_csv(output_ic, sep="\t")
    rc_df.to_csv(output_rc, sep="\t")
    bt_df.to_csv(output_bt, sep="\t")


def add_arguments(parser):
    """Register this subcommand's options on *parser*."""
    parser.add_argument("--input-dir", default=".", help="folder with the *-genes_insertions.{all,essen}.csv files")
    parser.add_argument("--output-ic", required=True)
    parser.add_argument("--output-rc", required=True)
    parser.add_argument("--output-bt", required=True)


def run_args(args):
    """Run the subcommand from an ``argparse.Namespace``."""
    compute_aggregates(
        input_dir=args.input_dir,
        output_ic=args.output_ic,
        output_rc=args.output_rc,
        output_bt=args.output_bt,
    )


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="captnseq-toolkit aggregate",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    add_arguments(parser)
    run_args(parser.parse_args(argv))


if __name__ == "__main__":
    main()
