import argparse
import sys

from eMolFrag2.src.utilities.logging import log
from eMolFrag2.src.input import ConfigReader

#
# Arg     Explanation
# ---     ---------------------------------------
# -i      input folder path
# -o      output folder path
# -u      output only TC-unique fragments
# -indiv  output all fragments in indivudal files
# -c      parameters specified in a configuration file 
#

INPUT_ARG = 'i'
OUTPUT_ARG = 'o'
CONFIGURATION_FILE_ARG = 'c'
ALL_FRAGMENTS_ARG = 'all'
INDIVIDUAL_FILE_ARG = 'indiv'

class Options:
    def __init__(self):
        self.INPUT_PATH = None
        self.OUTPUT_PATH = None
        self.CONFIGURATION_FILE = None
        
        self.INDIVIDUAL = False
        self.ALL_FRAGMENTS = False
        
        arg_env = self._parseCommandLineArgs()
        if arg_env is None:
          return
        
        self._interpretArgs(arg_env)

    def isRunnable(self):
        """
            After parsing the input command-line or configuration file,
            do we have the minimum requirements to execute?
            
            Requirements:
              (1) input directory
              (2) output directory
        """
        return self.INPUT_PATH is not None or self.OUTPUT_PATH is not None

    def _parseCommandLineArgs(self):
        """
            Analyze the command-line arguments.
            If a configuration file is specified, parse it.
            
            @output: argument environment created by argparse
        """

        # Add full help message on incorrect parameters
        class MyParser(argparse.ArgumentParser):
            def error(self, message):
                sys.stderr.write('error: %s\n' % message)
                self.print_help()
                sys.exit(2)

        parser = MyParser(description="eMolFrag2")

        #
        # eMolFrag arguments
        #
        parser.add_argument('-' + INPUT_ARG,
                            type = str,
                            help = 'Input path to molecules to fragment', 
                            required=True)
  
        parser.add_argument('-' + OUTPUT_ARG,
                            type = str,
                            help = 'Output path for fragments (existing files will be overwritten.)', 
                            required=True)

        parser.add_argument('-' + CONFIGURATION_FILE_ARG,
                            type = str,
                            help = 'Configuration file: .emf extension required.)')

        parser.add_argument('-' + ALL_FRAGMENTS_ARG,
                            action = 'store_true',
                            default = self.INDIVIDUAL,
                            help = 'Output all fragments (all non-unique molecules)')
  
        parser.add_argument('-' + INDIVIDUAL_FILE_ARG,
                            action = 'store_true',
                            default = self.ALL_FRAGMENTS,
                            help = 'Fragment will be output in their own individual files')

        args = parser.parse_args()        

        # Configuration file used for execution
        if args.c is not None:

            # Did the user state more than "eMolFrag2 -c *.emf"?
            if len(sys.argv) > 3:
                log.warning(f'Configuration file specified. All other command-line arguments ignored.')
   
            # TODO: Read config file
            args = ConfigReader.readConfig(args.c, parser)
 
        return args

    def _interpretArgs(self, arg_env):
        """
            Set the user-defined options
        """
        for arg in vars(arg_env):

            if (arg == INPUT_ARG):
                self.INPUT_PATH = getattr(arg_env, arg)

            elif (arg == OUTPUT_ARG):
                self.OUTPUT_PATH = getattr(arg_env, arg)

            elif (arg == CONFIGURATION_FILE_ARG):
                self.CONFIGURATION_FILE = getattr(arg_env, arg)
            
            elif (arg == ALL_FRAGMENTS_ARG):
                self.ALL_FRAGMENTS = getattr(arg_env, arg)

            elif (arg == INDIVIDUAL_FILE_ARG):
                self.INDIVIDUAL = getattr(arg_env, arg)
        
    def __str__(self):
        """
            Report the current preferences for each option available
        """
        return f'Input Path: {self.INPUT_PATH}\nOutput Path: {self.OUTPUT_PATH}\nIndividual output files: {self.INDIVIDUAL}\nAll Fragments: {self.ALL_FRAGMENTS}'