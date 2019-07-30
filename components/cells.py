# Standard libary imports
import time
import path
from pprint import pprint as pp

# Related third party imports
import asyncio, asyncssh
import re

# Local libary imports
from utils import G_LOGGER

# Modem details:
IP_MODEM = '192.168.0.1'
USER_MODEM = 'tdcomm'
PASS_MODEM = 'tddcom1234'

# Femto details
USER_IPACCESS = 'root'
PASS_IPACCESS = 'D9!*3n4Fw7Ka'

# LOGGER
LOGGER = None

#STATIC CELLS
CELLS = {}

async def get_cell_fault(mac_addr: str,ip: str, type: str) -> int:
    try:
        if type == '3g':
            async with asyncssh.connect(ip,username=USER_IPACCESS,password=PASS_IPACCESS,known_hosts=None) as conn:
                # get cell number of faults
                result = await conn.run('/opt/ipaccess/DMI/ipa-dmi -c "get system.Device.FaultMgmt.CurrentAlarmNumberOfEntries"')
                numberOfFaults = int(re.search(pattern=r'.* = (\d+)\n',string=result.stdout).group(1))
                # get fault details
                if numberOfFaults:
                    detailsFaults = str(await conn.run('/opt/ipaccess/DMI/ipa-dmi -c "get system.Device.FaultMgmt.CurrentAlarm"'))
                    cur_faults = set(re.findall(pattern='.* \(root.system.Device.FaultMgmt.CurrentAlarm.\d.SpecificProblem\) = "(.*?)"\n',string=detailsFaults))
                    cur_faults = cur_faults.symmetric_difference(CELLS[mac_addr]['old_faults'])
                    for warn_fault in cur_faults:
                        LOGGER.critical(f'cell {ip} type {type} fault message {warn_fault}')
                    CELLS[mac_addr]['old_faults'] = CELLS[mac_addr]['old_faults'].union(cur_faults)
                return numberOfFaults
        else:
            async with asyncssh.connect(ip,username=USER_IPACCESS,password=PASS_IPACCESS,known_hosts=None) as conn:
                result = await conn.run('sqlite3 /opt/ipaccess/femto.db "select CurrentAlarmNumberOfEntries from DeviceFaultMgmt"')
                numberOfFaults = int(re.search(pattern='\d+',string=result.stdout).group())
                return numberOfFaults
    except Exception as ex:   
        LOGGER.warning(f"unable to get cell faults from {ip}")
    

async def get_cell_type(ip: str):
    """Analyze femto cell and determine if 3G or 4G
    
    Arguments:                  
        ip {str} -- ip of cell to get cell type
    """
    try:
        async with asyncssh.connect(ip,username=USER_IPACCESS,password=PASS_IPACCESS,known_hosts=None) as conn:
            result = await conn.run('ls /opt/ipaccess')
            if 'DMI' in result.stdout:
                return '3g'
            else:
                return '4g'
    except:
        LOGGER.warning(f"unable to get cell type from {ip}")


async def get_cells_connected():
    """Get currently connected cells
    
    Checks connected cell by checking lan status.

    Returns:
        bool -- true if modem connneced else false 
        dict -- dictionary of cells connected
    """
    global CELLS
    # Perfrom modem lan query
    try:
        async with asyncssh.connect(IP_MODEM,username=USER_MODEM,password=PASS_MODEM,known_hosts=None) as conn:
            result = await conn.run('status lan')
            connected_devices = re.findall(pattern = r'connected_device {.*?}', string = result.stdout, flags=re.DOTALL)
        for mac in connected_devices:
            mac_addr = re.search(pattern=r'mac = (00:02:95:03:.*?)\n',string=mac)
            if mac_addr:
                mac_addr = mac_addr.group(1)
                if mac_addr not in CELLS:
                    ip = re.search(pattern='ip = (192.168.0.\d+)\n', string=mac).group(1)
                    type = await get_cell_type(ip)
                    CELLS[mac_addr] = {
                        'ip' : ip,
                        'type' : type,
                        'fault': None,
                        'old_faults' : set()
                    }
                    LOGGER.info(f"Femto-cell S60Z {type} with IP {ip} is connected")
                fault = await get_cell_fault(mac_addr,CELLS[mac_addr]['ip'],CELLS[mac_addr]['type'])
                if fault != CELLS[mac_addr]['fault']:
                    CELLS[mac_addr]['fault'] = fault
                    if CELLS[mac_addr]['fault'] == 0:
                        LOGGER.info(f"Number of alarms in femto {CELLS[mac_addr]['ip']} {CELLS[mac_addr]['type']} is {CELLS[mac_addr]['fault']}")
                    else:
                        LOGGER.warning(f"Number of alarms in femto {CELLS[mac_addr]['ip']} {CELLS[mac_addr]['type']} changed to {CELLS[mac_addr]['fault']}") 
    except:
        LOGGER.warning('unable to get lan status from modem')

   
if __name__ == "__main__":
    LOGGER = G_LOGGER.G_LOGGER(part='components',sub_part='femto cells').get_logger()

    # Init loop for event loop
    loop = asyncio.get_event_loop()
    while True:
        loop.run_until_complete(get_cells_connected())
        time.sleep(30)
    

    

    