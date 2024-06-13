import subprocess
from pathlib import Path

from eMolFrag.utilities.logging import log

data = Path(__file__).parent.parent / "data"


def test_emolfrag():
    # List of files to run emolfrag on
    files = ["seantest/unconstructed-ss.smi", "chopper/mol2-1/DB01416.mol2", "seantest/DB12924.smi", "/path/to/no/file.xyz"]

    for file in files:
        # Run emolfrag command on each file
        result = subprocess.run(["emolfrag", "-andti", data / file, "-o", "/tmp/out/output"], capture_output=True, text=True, check=False)

        print(result.stdout)
        print(result.stderr)
        log.debug(f"{result.args = }")
        log.debug(f"{result.returncode = }")

        # Check if emolfrag ran successfully
        assert result.returncode == 0
