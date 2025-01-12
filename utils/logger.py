import logging

logging.basicConfig(
    filename='logs/logs.log',
    filemode='a',
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
)

def log(report):
    logging.info(report)