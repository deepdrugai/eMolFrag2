import argparse
import sys

from eMolFrag.input import ConfigReader
from eMolFrag.utilities.constants import *
from eMolFrag.utilities.logging import log

# ruff: noqa: F403, F405

#
# Arg     Explanation
# ---     ---------------------------------------
# -i      input folder path
# -o      output folder path
# -u      output only TC-unique fragments
# -n      output all fragments in indivdual files
# -c      parameters specified in a configuration file
#

# Values in constants.py:
# ------------------------
# INPUT_ARG = "input"
# OUTPUT_ARG = "output"
# LOGGING_ARG = "log"
# CONFIGURATION_FILE_ARG = "config"
# ALL_FRAGMENTS_ARG = "all"
# INDIVIDUAL_FILE_ARG = "indiv"
# TRACE_ARG = "trace"
# DEFAULT_LOG_LEVEL = "INFO"


class Options:
    def __init__(self):
        self.INPUT_PATH = None
        self.OUTPUT_PATH = None
        self.CONFIGURATION_FILE = None

        self.INDIVIDUAL = False
        self.ALL_FRAGMENTS = False

        self.TRACE = False

        arg_env = self._parseCommandLineArgs()
        if arg_env is None:
            return

        self._interpretArgs(arg_env)

    # def isRunnable(self):
    #     """
    #         After parsing the input command-line or configuration file,
    #         do we have the minimum requirements to execute?

    #         Requirements:
    #           (1) input directory
    #           (2) output directory
    #     """
    #     return self.INPUT_PATH is not None or self.OUTPUT_PATH is not None

    def _parseCommandLineArgs(self):
        """
        Analyze the command-line arguments.
        If a configuration file is specified, parse it.

        @output: argument environment created by argparse
        """

        # Add full help message on incorrect parameters
        class MyParser(argparse.ArgumentParser):
            def error(self, message):
                sys.stderr.write("error: %s\n" % message)
                self.print_help()
                sys.exit(2)

        parser = MyParser(
            prog="eMolFrag2",
            description=f"eMolFrag 2.0 is a molecular fragmentation tool based on BRICS algorithm written in Python. \nThe options for this program are as follows:",
            add_help=False,
            # epilog=f"Example: eMolFrag2 -i /path/to/input -o /path/to/output -u -n -c /path/to/config.emf\n\n",
            epilog="Examples:\n"
            "  $ python emfragment.py -i data/test_data/ -o results/\n"
            "  $ python emfragment.py -i data/test_data/ -o results/ -a -nt\n"
            "  $ python emfragment.py -i data/test_data.smi -o results/\n"
            "  $ python emfragment.py -i data/test_data.sdf -o results/ -c config.emf\n"
            "  $ python emfragment.py -i data/test_data.mol2 -o results/ -an\n\n"
            "Note: The default configuration assumes that your input contains RDKit Mol objects serialized as SMILES or MOL2 format.\n"
            f"You can customize the behavior by providing a {EMF_FORMAT_EXT} configuration file (-c option).",
            # formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )

        # eMolFrag arguments
        #
        parser.add_argument(
            "-" + INPUT_ARG[0],
            "--" + INPUT_ARG,
            type=str,
            help="Path containing source molecules for fragmentation. Single file or directory.",
            required=True,
        )

        parser.add_argument(
            "-" + OUTPUT_ARG[0],
            "--" + OUTPUT_ARG,
            type=str,
            help="Path for output fragments. If the directory does not exist, it will be created.",
            required=True,
        )

        parser.add_argument(
            "-" + LOGGING_ARG[0],
            "--" + LOGGING_ARG,
            dest="logLevel",
            choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
            default=DEFAULT_LOG_LEVEL,
            type=str.upper,
            help=f"Set the logging level to print to console. Default is {DEFAULT_LOG_LEVEL}.",
        )

        parser.add_argument(
            "-" + CONFIGURATION_FILE_ARG[0],
            "--" + CONFIGURATION_FILE_ARG,
            type=str,
            help="Configuration file: .emf extension required.)",
        )

        parser.add_argument(
            "-" + ALL_FRAGMENTS_ARG[0],
            "--" + ALL_FRAGMENTS_ARG,
            action="store_true",
            default=self.INDIVIDUAL,
            help="Output all non-unique fragments. Default is to output only TC-unique fragments.",
        )

        parser.add_argument(
            "-" + INDIVIDUAL_FILE_ARG[1],
            "--" + INDIVIDUAL_FILE_ARG,
            action="store_true",
            default=self.ALL_FRAGMENTS,
            help="Each fragment will be saved individually in separate files. Default is to save in one unified file each for bricks, linkers, and freeatoms.",
        )

        parser.add_argument(
            "-" + TRACE_ARG[0],
            "--" + TRACE_ARG,
            action="store_true",
            default=self.TRACE,
            help="Print trace file for reconstructing original molecules.",
        )

        parser.add_argument("-d", "--debug", dest="debug", action="store_true", help="Quick flag to set logging level to debug.")

        parser.add_argument("-h", "--help", action="help", default=argparse.SUPPRESS, help="Show this help message and exit.")

        args = parser.parse_args()

        if not args.debug:
            log.setLevel(args.logLevel)
        else:
            log.setLevel("DEBUG")

        # Configuration file used for execution
        config = getattr(args, CONFIGURATION_FILE_ARG)
        if config is not None:
            # Did the user state more than "eMolFrag2 -c *.emf"?
            if len(sys.argv) > 3:
                log.warning(f"Configuration file specified. All other command-line arguments ignored.")

            # TODO: Read config file
            args = ConfigReader.readConfig(config, parser)

        return args

    def _interpretArgs(self, arg_env):
        """
        Set the user-defined options
        """
        for arg in vars(arg_env):
            log.debug(f"{(arg + ':').upper():<11}{vars(arg_env)[arg]}")

            if arg == INPUT_ARG:
                self.INPUT_PATH = getattr(arg_env, arg)

            elif arg == OUTPUT_ARG:
                self.OUTPUT_PATH = getattr(arg_env, arg)

            elif arg == CONFIGURATION_FILE_ARG:
                self.CONFIGURATION_FILE = getattr(arg_env, arg)

            elif arg == ALL_FRAGMENTS_ARG:
                self.ALL_FRAGMENTS = getattr(arg_env, arg)

            elif arg == INDIVIDUAL_FILE_ARG:
                self.INDIVIDUAL = getattr(arg_env, arg)

            elif arg == TRACE_ARG:
                self.TRACE = getattr(arg_env, arg)

    def __str__(self):
        """
        Report the current preferences for each option available
        """
        return f"Input Path: {self.INPUT_PATH}\nOutput Path: {self.OUTPUT_PATH}\nIndividual output files: {self.INDIVIDUAL}\nAll Fragments: {self.ALL_FRAGMENTS}"
