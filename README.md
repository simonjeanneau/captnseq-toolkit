# captnseq-toolkit

Analysis tools for CAPTn-seq (transposon-insertion sequencing) data. This package holds the
scientific logic used by the [nf-core/captnseq](https://github.com/nf-core/proposals/issues/173)
pipeline, so the pipeline itself only contains Nextflow code.

## Install

```bash
pip install captnseq-toolkit        # once released on PyPI
conda install -c bioconda captnseq-toolkit   # once the Bioconda recipe is merged
```

## Usage

```bash
captnseq-toolkit --help
captnseq-toolkit sam2sites    --help   # SAM -> insertion sites (BED + bedGraph)
captnseq-toolkit sites2genes  --help   # insertion sites -> per-gene counts
captnseq-toolkit essentiality --help   # per-gene counts -> essential / ambiguous / non-essential
```

## Development

```bash
pip install -e ".[test]"
pytest
```

Releases are tagged `vX.Y.Z`. The version is set by hand in `pyproject.toml` and must match the tag: the Bioconda recipe builds from the GitHub tag and checks that `captnseq-toolkit --version` equals the recipe version.
