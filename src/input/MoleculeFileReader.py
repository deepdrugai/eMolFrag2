from pathlib import Path

from SuperSecretProject.src.input import Options
from SuperSecretProject.src.utilities import constants
from SuperSecretProject.src.utilities import logging

def getFiles(options):
    """
        From the input directory specified, acquire all applicable molecule files
    """
    folderPath = Path(options.INPUT_PATH)
      
    # Non-existing directory means no files to process
    if not folderPath.exists():
        logging.logger.error(f'Input path {options.INPUT_PATH} does not exist.')
        return []

    # Path is not a directory
    if not folderPath.is_dir():
        logging.logger.error(f'Input path {options.INPUT_PATH} is not a directory. Did you mean: {folderPath.parent} ?')
        return []
     
    files = []
    bad_files = []

    # grab each file with acceptable molecule extension
    for current_file in folderPath.iterdir():
      
        #if the file extension is not a supportedd format, add the file to the bad file list, otherwise add it to the file list
        extension = current_file.suffix
        if extension in constants.ACCEPTED_FORMATS:
            files.append(folderPath / current_file.name)
        else:
            bad_files.append(current_file)

    # Report unacceptable files
    if bad_files:
        logging.logger.warning(f'emolFrag2 only accepts the following formats {", ".join(constants.ACCEPTED_FORMATS)}')
        logging.logger.warning(f'The following files will be ignored: {", ".join([bf.name for bf in bad_files])}')
      
    return files

#
# Given a configuration file, return the file path
#
def acquireConfigurationFile(usr_file):
    filePath = Path(usr_file)

    #if the folder path doesnt exist, exit processing
    if not filePath.exists():

        #print(f'Input path {usr_file} does not exist.')
        logging.logger.error(f"Input path {usr_file} does not exist.")
        return None
    
    return filePath