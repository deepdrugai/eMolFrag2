# eMolFrag-2.0

## (Temp) Fix for Missing Path:
Navigate to folder one level above eMolFrag2 and run:
```python
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

Note: If your directory is called eMolFrag2.0, you may need to rename the eMolFrag2.0 directory to eMolFrag2 first.

## Nessary Dependencies:
Two dependencies are necessary, rdkit and networkx. 
Optionally, colorlog is used for full color logging files.

You can install them with conda, like so:

```bash
conda install -c conda-forge rdkit networkx colorlog
```

or with pip:

```bash
pip install rdkit networkx colorlog
```


