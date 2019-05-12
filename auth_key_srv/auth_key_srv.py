import logging
import logging.handlers
#import requests
from aiohttp_requests import requests
from optparse import OptionParser
import configparser
import json
import urllib
import time

from aiohttp import web

AUTH_KEY_SRV_VERSION = "1.0"
G_LOGGER = None



async def sendAuthVectorsRequest(aucRequest):

    url = "https://geo.m2i-api.com/newAuthKeys/%s" % (aucRequest['imsi'])
    headers = {'Content-Type': 'application/json', 'Authorization': 'Token rqGEJPwKCFsySiWDGAQyFTmyeGMxAUc4'}
    
#    url = "https://geo.m2i-api.com/getAccount"
#    headers = {'Content-Type': 'application/json', 'Authorization': 'tdcomm yhshEUO@3XhXnT'}
    
    try:
        resp =  await requests.get(url,headers=headers)
        #time.sleep(1)        
        auc_response = {
            'user_reference' : aucRequest['user_reference'],
#            'response_type'  : message.authVectorsResponse.responseType,
#            'result'         : message.authVectorsResponse.result,
            'imsi'           : aucRequest['imsi'],
            'responding_node': aucRequest['node_type'],
        }
        
        #resp_content = json.loads(resp.content)
        resp_content = await resp.json()
        G_LOGGER.debug("sendAuthVectorsRequest got response: " + str(resp_content))
        
        if "data" in resp_content:
        
            if 'authType' in resp_content['data']:
                if resp_content['data']['authType'] == 'GSM':
                    auc_response['auth_type'] = 0
                elif resp_content['data']['authType'] == 'UTRAN':
                    auc_response['auth_type'] = 1
            
            if 'rand' in resp_content['data']:
                auc_response['rand'] = resp_content['data']['rand']

            if 'xres' in resp_content['data']:
                auc_response['xres'] = resp_content['data']['xres']

            if 'ck' in resp_content['data']:
                auc_response['ck'] = resp_content['data']['ck']

            if 'ik' in resp_content['data']:
                auc_response['ik'] = resp_content['data']['ik']

            if 'autn' in resp_content['data']:
                auc_response['autn'] = resp_content['data']['autn']

            if 'sres' in resp_content['data']:
                auc_response['sres'] = resp_content['data']['sres']

            if 'kc' in resp_content['data']:
                auc_response['kc'] = resp_content['data']['kc']
                
        elif "error" in resp_content:
            G_LOGGER.error("sendAuthVectorsRequest got error in response: ",resp_content["error"])
            
        return auc_response
    
    except Exception as error:
        G_LOGGER.error("sendAuthVectorsRequest got exception: ",error)
        return None


async def handle(request):
    #name = request.match_info.get('name', "Anonymous")
    #text = "Hello, " + name
    if request.body_exists:
        body = await request.read()
        auc_req = urllib.parse.unquote(str(body, 'utf-8'))
        G_LOGGER.debug("auth request received: " + auc_req)
        #auc_req = {"user_reference": 60, "imsi": "425030004594090", "node_type": 0}
        resp = await sendAuthVectorsRequest(json.loads(auc_req))
        G_LOGGER.debug("resp = " + str(resp))

    return web.json_response(resp)


def setupLogger(config):

    global G_LOGGER
    G_LOGGER = logging.getLogger('auth_key_srv')

    logging_ini = config._sections['Logger']

    log_file   = logging_ini['log_file']
    log_format = logging_ini['log_format']
    log_level  = logging_ini['log_level']

    if log_file:
        file_handler = logging.handlers.RotatingFileHandler(log_file,
                                                            maxBytes = 1048576,
                                                            backupCount = 5)
        file_handler.setFormatter(logging.Formatter(log_format))
        G_LOGGER.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(log_format))

    G_LOGGER.addHandler(console_handler)

    G_LOGGER.setLevel(log_level)


def main():

    # Parse command line options
    parser = OptionParser()

    parser.add_option("-c", default = "/usr/share/tdcomm/auth_key_srv.ini", dest = 'config_file', help = "Configuration file")

    (options, args) = parser.parse_args()

    # Parse config file
    config = configparser.SafeConfigParser()
    config.read(options.config_file)

    # Setup logger
    setupLogger(config)

    G_LOGGER.info("********** STARTING AUTH KEY SERVER (VERSION: %s) **********", AUTH_KEY_SRV_VERSION)

    
    # Ext Proc HTTP server parameters
    server_ini = config._sections['Ext_Proc_Server']

    G_LOGGER.info("Created HTTP server listening on port %s:%s. Waiting for Auth Vector requests to /%s from Ext Proc ...",
                server_ini['ip'], server_ini['port'], server_ini['auc_url'])

    # Create HTTP server to handle requests from Ext Proc
    app = web.Application()
    app.add_routes([web.post('/'+ server_ini['auc_url'], handle)])

    web.run_app(app, host = server_ini['ip'], port = server_ini['port'])


if __name__ == "__main__":
    main()


