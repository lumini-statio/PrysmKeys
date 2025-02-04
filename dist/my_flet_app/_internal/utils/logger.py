import logging
import os


'''The function creates a log file in a 'logs' directory and logs messages with timestamp.
    
Parameters
----------
report
    The code you provided sets up a logging system in Python that creates a log file in a 'logs'
directory within the current directory. The `log()` function is used to log reports to this file
with an INFO level.
'''
current_directory = os.path.dirname(os.path.abspath(__file__))

log_directory = os.path.join(current_directory, 'logs')

os.makedirs(log_directory, exist_ok=True)

log_file_path = os.path.join(log_directory, 'logs.log')

logging.basicConfig(
    filename=log_file_path,
    filemode='a',
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
)

def log(report):
    logging.info(report)