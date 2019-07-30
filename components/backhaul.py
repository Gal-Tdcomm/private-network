from utils import G_LOGGER
import json
import speedtest
from urllib.request import urlopen
import time

LOGGER = G_LOGGER.G_LOGGER(part='components',sub_part='backhaul').get_logger()
OLD_STATUS = None
START = None

# define if to measure speed test or not
speed_test = True


def check_wan(speed_test):
    if (speed_test):
        try:
            servers = []
            # If you want to test against a specific server
            # servers = [1234]

            threads = None
            # If you want to use a single threaded test
            # threads = 1

            s = speedtest.Speedtest()
            s.get_servers(servers)
            s.get_best_server()
            s.download(threads=threads)
            s.upload(threads=threads)
            s.results.share()

            results_dict = s.results.dict()
            LOGGER.info(f"Speed test - DL: {results_dict['download']} Bytes, UP: {results_dict['upload']} Bytes")
        except:
            LOGGER.critical("failed to perform speed test check")
    else:
        try:
            urlopen('https://www.google.com/', timeout=4)
            return True
        except:
            if OLD_STATUS or OLD_STATUS is None : 
                LOGGER.critical('Backhaul failure!!!!!!!!!')
            return False

if __name__ == "__main__":
    START = 1
    if speed_test:
        counter_speed_test = 0
    while True:
        # check if wan access
        CUR_STATUS = check_wan(False)
        if CUR_STATUS != OLD_STATUS:
            OLD_STATUS = CUR_STATUS
            if OLD_STATUS:
                LOGGER.info('Backhaul ok')
        if speed_test and OLD_STATUS:
            if counter_speed_test == 20 or (counter_speed_test == 0 and START == 1):
                counter = 0
                START = 0
                check_wan(True)   
            counter_speed_test += 1
        time.sleep(20)
        

        
                

        
            



