from utils import G_LOGGER
import logging, logging.handlers
import asyncio, asyncssh, sys
import time


STATUS = 1
LAST_STATUS= {
    'first' : {
        'type' : '',
        'status' : ''
    },
    'second' : {
        'type' : '',
        'status' : ''
    }
}

USER = 'tdcomm'
PASSWORD = 'tddcom1234'
IP = '192.168.0.1'
LOGGER = None

async def get_link_status():
    try:
        async with asyncssh.connect(IP,username=USER,password=PASSWORD,known_hosts=None) as conn:
            result = await conn.run('status link_manager')
            return result.stdout
    except:
        return False

async def check_status():
    global LOGGER
    global LAST_STATUS
    global STATUS

    link_status = await get_link_status()
    if not link_status:
        if STATUS == 1:
            LOGGER.critical('ROBUSTEL R2000 is not connected to the system')
            STATUS = 0
        return
    
    STATUS = 1
    
    # link status check
    link_status = link_status.split('link_status')[1:]
    
    
    CUR_STATUS = {
        'first' : {
            'type' : '',
            'status' : ''
        },
        'second' : {
            'type' : '',
            'status' : ''
        }
    }

    first_link = link_status[0].split()
    CUR_STATUS['first']['type'] = first_link[first_link.index('link') + 2]
    CUR_STATUS['first']['status'] = first_link[first_link.index('status') + 2]
    
    if (CUR_STATUS['first']['type'] != LAST_STATUS['first']['type']):
        if (LAST_STATUS['first']['type'] == ''):
            LOGGER.info(f"first interface is {CUR_STATUS['first']['type']}")
        else:
            LOGGER.info(f"first interface change from {LAST_STATUS['first']['type']} to {CUR_STATUS['first']['type']}")
    
    if (CUR_STATUS['first']['status'] != LAST_STATUS['first']['status']):
        if (LAST_STATUS['first']['status'] == ''):
            LOGGER.info(f"interface {CUR_STATUS['first']['type']} is {CUR_STATUS['first']['status']}")
        else:
            LOGGER.info(f"interface {CUR_STATUS['first']['type']} status changed from {LAST_STATUS['first']['status']} to {CUR_STATUS['first']['status']}")
    

    second_link = link_status[1].split()
    CUR_STATUS['second']['type'] = second_link[second_link.index('link') + 2]
    CUR_STATUS['second']['status'] = second_link[second_link.index('status') + 2]
    
    if (CUR_STATUS['second']['type'] != LAST_STATUS['second']['type']):
        if (LAST_STATUS['second']['type'] == ''):
            LOGGER.info(f"second interface is {CUR_STATUS['second']['type']}")
        else:
            LOGGER.info(f"second interface change from {LAST_STATUS['second']['type']} to {CUR_STATUS['second']['type']}")
    
    if (CUR_STATUS['second']['status'] != LAST_STATUS['second']['status']):
        if (LAST_STATUS['second']['status'] == ''):
            LOGGER.info(f"interface {LAST_STATUS['second']['type']} is {CUR_STATUS['second']['status']}")
        else:
            LOGGER.info(f"interface {LAST_STATUS['second']['type']} status changed from {LAST_STATUS['second']['status']} to {CUR_STATUS['second']['status']}")

    if (CUR_STATUS['second']['status'] != 'Connected' and CUR_STATUS['first']['status'] != 'Connected'):
        LOGGER.critical('NO INTERFACE CONNECTION!!!!!!!!!!!!!!!!!!!!!!')
    
    LAST_STATUS = CUR_STATUS
    


if __name__ == "__main__":
    LOGGER = G_LOGGER.G_LOGGER('components','modem').get_logger()
    loop = asyncio.get_event_loop()
    while True:
        loop.run_until_complete(check_status())
        time.sleep(10)

    
        
        

