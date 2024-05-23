# eMolFrag-2.0

[![eMolFrag Tests (PyPI)](https://github.com/deepdrugai/eMolFrag2/actions/workflows/emolfrag-pip.yml/badge.svg)](https://github.com/deepdrugai/eMolFrag2/actions/workflows/emolfrag-pip.yml)

## (Temp) Fix for Missing Path
Navigate to folder one level above eMolFrag2 and run:
```shell
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

Note: If your directory is called eMolFrag2.0, you may need to rename the eMolFrag2.0 directory to eMolFrag2 first.

Our team will eventually shift to an installable eMolFrag package, but for now, you can put  
`export PYTHONPATH="${PYTHONPATH}:<PATH TO eMolFrag2 PARENT DIRECTORY>"` into your .bash_profile or .bashrc file (after replacing the path betwen <> with your own path) so that the environmental variable loads on start.

## Necessary Dependencies
Two dependencies are required for eMolFrag: rdkit and networkx. Optionally, colorlog is used for full color logging files.

You can install them with conda, like so:

```shell
conda install -c conda-forge rdkit networkx colorlog
```

or with pip:

```shell
pip install rdkit networkx colorlog
```


