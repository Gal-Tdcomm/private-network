import time
import psutil
from utils import G_LOGGER


LOGGER = G_LOGGER.G_LOGGER('components','sbc').get_logger()
CUR_STATUS = {}


def get_sbc_status():
    CUR_STATUS['CPU precentage'] = psutil.cpu_percent()
    if (CUR_STATUS['CPU precentage'] > 80):
        LOGGER.warn(f"CPU usage is dangerous {CUR_STATUS['CPU precentage']}%")
    CUR_STATUS['Virutal memomory'] = psutil.virtual_memory().percent
    if (CUR_STATUS['Virutal memomory'] > 80):
        LOGGER.warn(f"Virutal memomory usage is dangerous {CUR_STATUS['Virutal memomory']}%")
    CUR_STATUS['disk_usage'] = psutil.disk_usage('/').percent
    if (CUR_STATUS['disk_usage'] > 80):
        LOGGER.warn(f"Disk_usage usage is dangerous {CUR_STATUS['Virutal memomory']}%")
    LOGGER.info(f"Usages -  CPU:{CUR_STATUS['CPU precentage']}% , Virtual memory:{CUR_STATUS['Virutal memomory']}%, Disk:{CUR_STATUS['disk_usage']}%")
    return




if __name__ == "__main__":
    while True:
        get_sbc_status()
        time.sleep(500)
        







