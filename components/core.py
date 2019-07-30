# Standard python libaries
import re
import time

# Third party libaries
import asyncssh
import asyncio

# Local libaries 
from utils.G_LOGGER import G_LOGGER

# VM credentials
IP = '192.168.0.5'
USER = 'root'
PASS = 'tddcom1234'

# Logger
LOGGER = None
r
# STATIC STATUS
NOT_RUNNING = 'Raemis is not running\n'
RUNNING = 'Raemis is running\n'
OLD_STATUS = None

async def check_status_core():
    global OLD_STATUS
    try:
        async with asyncssh.connect(IP,username=USER,password=PASS,known_hosts=None) as conn:
            result = await conn.run('service raemis status')
            status = result.stdout
            if  status in RUNNING and status != OLD_STATUS:
                LOGGER.info('RAEMIS core is running')
                OLD_STATUS = result.stdout
            if status == NOT_RUNNING and status != OLD_STATUS:
                LOGGER.info('RAEMIS core is not running!!!!!')
                OLD_STATUS = result.stdout
    except Exception as ex:
        LOGGER.exception(ex)
        LOGGER.error('Unable to get raemis core status')

if __name__ == "__main__":
    LOGGER = G_LOGGER(part='components', sub_part='core').get_logger()
    loop = asyncio.get_event_loop()
    while True:
        loop.run_until_complete(check_status_core())
        time.sleep(20)
    
