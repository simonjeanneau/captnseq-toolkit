import pandas as pd
import pytest

from captnseq_toolkit.aggregate import compute_aggregates
from captnseq_toolkit.cli import main


def _write_sample(folder, name, counts, essential):
    """counts: {gene: (ins_count, read_count)}; essential: genes listed in .essen.csv."""
    rows = "".join(f"{g},{ic},{rc}\n" for g, (ic, rc) in counts.items())
    (folder / f"{name}-genes_insertions.all.csv").write_text("gene_name,ins_count,read_count\n" + rows)
    ess = "".join(f"{g}\n" for g in essential)
    (folder / f"{name}-genes_insertions.essen.csv").write_text("gene_name\n" + ess)
    # ambiguous calls are written by the pipeline too, but must not be read
    (folder / f"{name}-genes_insertions.ambig.csv").write_text("gene_name\ngeneC\n")


@pytest.fixture
def folder(tmp_path):
    _write_sample(tmp_path, "s2", {"geneA": (5, 50), "geneB": (0, 0), "geneC": (3, 30)}, ["geneB"])
    _write_sample(tmp_path, "s1", {"geneA": (7, 70), "geneB": (1, 10), "geneC": (0, 0)}, ["geneC"])
    return tmp_path


def _read(path):
    return pd.read_csv(path, sep="\t", index_col="gene")


def test_ic_rc_bt_values(folder, tmp_path):
    out = tmp_path / "out"
    out.mkdir()
    compute_aggregates(folder, out / "ic.tsv", out / "rc.tsv", out / "bt.tsv")
    ic, rc, bt = _read(out / "ic.tsv"), _read(out / "rc.tsv"), _read(out / "bt.tsv")

    assert list(ic.columns) == ["s1", "s2"]  # sorted by sample name, whatever the file order
    assert ic.index.name == rc.index.name == bt.index.name == "gene"
    assert ic.loc["geneA"].tolist() == [7, 5]
    assert rc.loc["geneA"].tolist() == [70, 50]
    # BT: 1 only for genes in .essen.csv; the .ambig.csv gene (geneC in s2) stays 0
    assert bt["s1"].to_dict() == {"geneA": 0, "geneB": 0, "geneC": 1}
    assert bt["s2"].to_dict() == {"geneA": 0, "geneB": 1, "geneC": 0}


def test_missing_files_raise(tmp_path):
    with pytest.raises(FileNotFoundError, match="genes_insertions.all.csv"):
        compute_aggregates(tmp_path, tmp_path / "a", tmp_path / "b", tmp_path / "c")


def test_aggregate_runs_through_top_level_cli(folder, tmp_path):
    out = tmp_path / "out"
    out.mkdir()
    rc = main([
        "aggregate",
        "--input-dir", str(folder),
        "--output-ic", str(out / "ic.tsv"),
        "--output-rc", str(out / "rc.tsv"),
        "--output-bt", str(out / "bt.tsv"),
    ])
    assert rc == 0
    assert _read(out / "bt.tsv").shape == (3, 2)
