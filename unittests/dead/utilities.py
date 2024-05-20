# #
# # Unit Testing Utility functionality
# #

# from rdkit import Chem
# from pathlib import Path
# # import argparse
# # from eMolFrag.utilities import constants
# # from eMolFrag.input import Options


# def fileToString(file):
#     """ Takes the contents of a file and puts it in a string for processing """
#     contents = ""
#     with open(file) as f:
#         contents = f.read()

#     return contents

# def convertToRDkit(contents, extension):
#     """ Converts the contents of a file to a molecule """
#     #kekulize = False       # TODO: Should we move this to args?
#     #Chem.doKekule = False  # TODO: This one too?

#     if (extension == ".fasta"):
#         return Chem.MolFromFASTA(contents)

#     if (extension == ".yaml"):
#         return Chem.MolFromHELM(contents)

#     if (extension == ".mol2"):
#       try:
#         # default parameters: (str)contents
#         #                     sanitize=True
#         #                     removeHs=True
#         #                     cleanupSubstructures=True
#         return Chem.MolFromMol2Block(contents)
#       except:
#         return Chem.MolFromMol2Block(contents, sanitize = False)

#     if (extension == ".mol"):
#         return Chem.MolFromMolBlock(contents)

#     if (extension == ".pdb"):
#         return Chem.MolFromPDBBlock(contents)

#     if (extension == ".sma"):
#         return Chem.MolFromSmarts(contents)

#     if (extension == ".smi"):
#         return Chem.MolFromSmiles(contents)

#     if (extension == ".tpl"):
#         return Chem.MolFromTPLBlock(contents)

#     return None

# def getRDKitMolecule(path, extension=None):
#     """
#         Given a path object, return the corresponding RDKit molecule object
#         This simplified functionality is for testing only
#     """
#     if extension is None:
#        extension = Path(path).suffix
#     content = fileToString(path)
#     return convertToRDkit(content, extension)

# # def createParser():
# #   parser = argparse.ArgumentParser(description = 'eMolFrag2')
# #   #
# #   # eMolFrag arguments
# #   #
# #   parser.add_argument('-' + Options.INPUT_ARG,
# #                       type = str,
# #                       help = 'Input path to molecules to fragment')
# #   parser.add_argument('-' + Options.OUTPUT_ARG,
# #                       type = str,
# #                       help = 'Output path for fragments (existing files will be overwritten.)')

# #   parser.add_argument('-' + Options.CONFIGURATION_FILE_ARG,
# #                       type = str,
# #                       help = 'Configuration file: .emf extension required.)')

# #   parser.add_argument('-' + Options.ALL_FRAGMENTS_ARG,
# #                       action = 'store_true',
# #                       default = False,
# #                       help = 'Output all fragments (all non-unique molecules)')

# #   parser.add_argument('-' + Options.INDIVIDUAL_FILE_ARG,
# #                       action = 'store_true',
# #                       default = False,
# #                       help = 'Fragment will be output in their own individual files')

# #   return parser

# #
# #
# # Printing to console ; can modify later to dump stream to other locations
# #
# #
# # def emit(level, s):
# #     print("  " * level + s)

# # def emitError(level, s):
# #     print("  " * level + "Error:", s)

# # def emitWarning(level, s):
# #     print("  " * level + "Warning:", s)
