# eMolFrag 2

| **CI/CD** | [![Tests & Coverage](https://github.com/deepdrugai/eMolFrag2/actions/workflows/emolfrag-hatch.yml/badge.svg)](https://github.com/deepdrugai/eMolFrag2/actions/workflows/emolfrag-hatch.yml) |
| ---: | :--- |
| **Package** | [![Python 3.8](https://img.shields.io/badge/python-≥3.8-blue.svg)](https://www.python.org/downloads/) |
| **Meta** | [![Hatch Project](https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg)](https://github.com/pypa/hatch) [![Code Style - Black](https://img.shields.io/badge/code_style-Black-000000.svg)](https://github.com/psf/black) [![types - Pyright](https://img.shields.io/badge/types-%F0%9F%AA%A8_Pyright-7a7953.svg)](https://github.com/microsoft/pyright) |
| **License** | [![License - MIT](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/license/mit/) |
-----

<!-- [![eMolFrag Tests (PyPI)](https://github.com/deepdrugai/eMolFrag2/actions/workflows/emolfrag-hatch.yml/badge.svg)](https://github.com/deepdrugai/eMolFrag2/actions/workflows/emolfrag-hatch.yml)
[![Tests & Coverage (eMolFrag2-packaging)](https://github.com/deepdrugai/eMolFrag2/actions/workflows/emolfrag-hatch.yml/badge.svg?branch=eMolFrag2-packaging)](https://github.com/deepdrugai/eMolFrag2/actions/workflows/emolfrag-hatch.yml) 

----- -->

## Table of Contents

- [Quick Start](#quick-start)
- [Installation](#installation)
- [Necessary Dependencies](#necessary-dependencies)
- [License](#license)

## Quick Start
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/deepdrugai/eMolFrag2/blob/main/eMolFrag2_Notebook.ipynb)

## Installation
Install eMolFrag2 with:
```shell
pip install "git+https://github.com/deepdrugai/eMolFrag2.git"
```

## eMolFrag Usage Help Text

```shell
emolfrag
```
<!-- options for codeblock syntax language:
(https://github.com/jincheng9/markdown_supported_languages)
ahk
 (all white)
blitzmax
cl 
-->
```blitzmax
$ emolfrag

usage: emolfrag -i INPUT [-o OUTPUT] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                [-c CONFIG] [-a] [-n] [-t] [-d] [-h]

eMolFrag2 is a molecular fragmentation tool based on the BRICS algorithm written in Python.
Brought to you by LSU's DeepDrug.ai team.

options:
  -i, --input INPUT     Path containing source molecules for fragmentation.
                        Single file or directory.
  -o, --output OUTPUT   Path for output fragments. If the directory does not
                        exist, it will be created. Default output directory is
                        'out/output/'.
  -l, --log {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        Set the logging level to print to console. Default is
                        INFO.
  -c, --config CONFIG   Configuration file: .emf extension required.)
  -a, --all             Output all fragments. Default is to output only TC-
                        unique fragments.
  -n, --indiv           Each fragment will be saved individually in separate
                        files. Default is to save in one unified file each for
                        bricks, linkers, and freeatoms.
  -t, --trace           Print trace file for reconstructing original
                        molecules.
  -d, --debug           Quick flag to set logging level to debug.
  -h, --help            Show this help message and exit.

Examples:
  $ emolfrag -i data/test_data/ -o results/
  $ emolfrag -i data/test_data/ -o results/ -a -nt
  $ emolfrag -i data/test_data.smi -o results/
  $ emolfrag -i data/test_data.sdf -o results/ -c config.emf
  $ emolfrag -i data/test_data.mol2 -o results/ -an

Note: The default configuration assumes that your input contains RDKit Mol objects serialized as SMILES or MOL2 format.
You can customize the behavior by providing a .emf configuration file (-c option).
```

## Necessary Dependencies
Three dependencies are required for eMolFrag: rdkit, networkx and matplotlib. Optionally, colorlog is used for full color logging files.

## License
This repository is licensed under the MIT License. See [LICENSE](LICENSE).
Some included third-party-derived files remain under their original BSD-style
licenses; see [THIRD_PARTY_LICENSES](THIRD_PARTY_LICENSES).
