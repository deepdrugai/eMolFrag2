from pathlib import Path

from eMolFrag.utilities.constants import EMF_FORMAT_EXT, INPUT_ARG, OUTPUT_ARG
from eMolFrag.utilities.logging import log


def cleanCommandList(cmdList):
    """
    Trims whitespace and other discrepancies

    @output: a list of flags and arguments
    """
    bad_tokens = ["", " ", "\n"]
    return [token for token in cmdList if token not in bad_tokens]


def grabCommands(config_file):
    """
    Takes the string contents of a configuration file
    and grabs its command line arguments.
    If there are comments, ignore anything to the right of it

    @output: a list of flags and arguments
    """
    retString = ""
    position = 0

    with open(config_file) as f:
        contents = f.readlines()

    # Read line by line, ignore comments, concatenate the remaining tokens into one string
    for line in contents:
        position = line.find("#")
        if position >= 0:
            retString += line[:position]
        else:
            retString += line

    if len(retString) <= 0:
        log.error(f"Configuration File is empty")
        return None

    return cleanCommandList(retString.split(" "))


def readConfig(config_file, parser):
    """
    Reads a config file and parses arguments
    If the file is empty, throw an error

    @output: parsed arguments from argparser
    """
    if not Path(config_file).exists():
        log.error(f"{Path(config_file)} does not exist")
        return None

    if Path(config_file).suffix != EMF_FORMAT_EXT:
        log.error(f"Configuration files must have the {EMF_FORMAT_EXT} extension")
        return None

    # Grab the commands and then parse them
    cmdList = grabCommands(config_file)

    args = parser.parse_args(cmdList)
    input_args = getattr(args, INPUT_ARG)
    output = getattr(args, OUTPUT_ARG)
    if input_args is None or output is None:
        log.error(f"Command-line arguments failed to parse; execution of eMolFrag will stop.")
        return None

    return args
