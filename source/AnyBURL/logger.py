import logging
class Logger(object):

  def __init__(self):
    pass

  def get_logger(class_name):
    logging.basicConfig(filename='log_debug/log.txt', filemode='a', format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                      datefmt='%H:%M:%S', level=logging.INFO)
    return logging.getLogger(class_name)

  def get_log_cate(cate, class_name):
    logging.basicConfig(filename='log_debug/{}'.format(cate), filemode='a', format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                      datefmt='%H:%M:%S', level=logging.INFO)
    return logging.getLogger(class_name)