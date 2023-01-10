import logging
import os


logging.basicConfig(
    filename=os.path.join(os.getcwd(), 'info.log'),
    format='[%(asctime)s] %(levelname)s : %(message)s',
    # handlers=[logging.FileHandler(filename=os.path.join(os.getcwd(), 'info.log'))],
    level=logging.INFO,
    datefmt='%Y/%m/%d %H:%M:%S'
)

# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)
# handler = logging.FileHandler(filename=os.path.join(os.getcwd(), 'info.log'))
# logger.addHandler(handler)

# logging.info('test')
# print('name', __name__)
# print(os.getcwd())
