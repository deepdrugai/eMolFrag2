from pathlib import Path

# from eMolFrag2.src.input import Options
from eMolFrag2.src.utilities import constants
from eMolFrag2.src.utilities.logging import log

def getFiles(options):
    """
        From the input directory specified, acquire all applicable molecule files
    """
    folderPath = Path(options.INPUT_PATH)
      
    # Non-existing directory means no files to process
    if not folderPath.exists():
        log.error(f'Input path {options.INPUT_PATH} does not exist.')
        return []

    # Path is not a directory
    if not folderPath.is_dir():
        log.error(f'Input path {options.INPUT_PATH} is not a directory. Did you mean: {folderPath.parent} ?')
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
        log.warning(f'emolFrag2 only accepts the following formats {", ".join(constants.ACCEPTED_FORMATS)}')
        log.warning(f'The following files will be ignored: {", ".join([bf.name for bf in bad_files])}')
      
    return files

#
# Given a configuration file, return the file path
#
def acquireConfigurationFile(usr_file):
    filePath = Path(usr_file)

    #if the folder path doesnt exist, exit processing
    if not filePath.exists():

        #print(f'Input path {usr_file} does not exist.')
        log.error(f"Input path {usr_file} does not exist.")
        return None
    
    return filePath