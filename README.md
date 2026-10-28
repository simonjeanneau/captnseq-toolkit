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

## Origins and references

The analysis steps build on earlier work, which should be credited and cited:

- `sam2sites` and `sites2genes` are based on `sam2sites.py` and `sites2genes.py` from [HDTM_tools](https://github.com/fredericQC/HDTM_tools) (Frederic Grenier, MIT licence). Its README credits Audrey Bioteau for cleaning up `sam2sites.py`.
- `essentiality` is based on the essentiality analysis `tradis_essentiality.R` of [Bio-Tradis](https://github.com/sanger-pathogens/Bio-Tradis) (Wellcome Trust Sanger Institute, GPLv3).

If you use this toolkit, please also cite the TraDIS toolkit:

> Barquist L, Mayho M, Cummins C, Cain AK, Boinett CJ, Page AJ, Langridge G, Quail MA, Keane JA, Parkhill J. The TraDIS toolkit: sequencing and analysis for dense transposon mutant libraries. *Bioinformatics*. 2016;32(7):1109-1111. doi: [10.1093/bioinformatics/btw022](https://doi.org/10.1093/bioinformatics/btw022)

Copyright and licence notices of these projects are in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

## Licence

Most of the toolkit is released under the MIT licence ([LICENSE](LICENSE)). The `essentiality` module is based on GPLv3 code and is licensed under the GNU General Public License v3 ([LICENSE-GPL-3.0](LICENSE-GPL-3.0)). Distributed together as the `captnseq-toolkit` program, the GPL terms apply to the whole.

## Development

```bash
pip install -e ".[test]"
pytest
```

Releases are tagged `vX.Y.Z`. The version is set by hand in `pyproject.toml` and must match the tag: the Bioconda recipe builds from the GitHub tag and checks that `captnseq-toolkit --version` equals the recipe version.
