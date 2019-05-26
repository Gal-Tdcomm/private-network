from flask import Flask,request
import cell_objects
import logging
from logging.handlers import RotatingFileHandler
import json


ip ={
    '3G' : '192.168.0.95',
    '4G' : '192.168.0.87'
}

app = Flask(__name__)

@app.route('/get_params/<id>', methods=['GET'])
def get_parameters(id):
    if id == '3g':
        G_logger.info('Return %s id parameters'%(id))
        umts = cell_objects.Cell_3G(ip['3G'],G_logger)
        params = umts.get_cell_parameters()
        return json.dumps(params,sort_keys=True,indent=4)
    elif id == '4g':
        G_logger.info('Return %s id parameters'%(id))
        lte = cell_objects.Cell_4G(ip['4G'],G_logger)
        params = lte.get_cell_parameter()
        return json.dumps(params, sort_keys=True, indent=4)
    return 'Unknown id'

@app.route('/set_params',methods=['POST'])
def set_parameters():
    content = request.get_json()
    if content['rat'] == '3G':
         cur_cell = cell_objects.Cell_3G(ip['3G'],G_logger)
         plmnid = "{}{}".format(content['mcc'],content['mnc'])
         lac = content['lac']
         cellid = content['cellId']
         uarfcn = content['uarfcn']
         psc = content['psc']
         rac = content['rac']
         cur_cell.set_cell_paramters(plmnid=plmnid,lac=lac,rac=rac,cellid=cellid,uarfcn=uarfcn,psc=psc)
    elif content['rat'] == '4G':
        cur_cell = cell_objects.Cell_4G(ip['4G'],G_logger)
        plmnid = "{}{}".format(content['mcc'],content['mnc'])
        tac= content['tac']
        cid = content['l3CellId']
        earfcn = content['bw']
        bw = content['lteBandwidth']
        pci = content['pci']
        band = content['bandId']
        cur_cell.set_cell_parameters(plmnid=plmnid,tac=tac,cid=cid,bandId=band,earfcn=earfcn,pci=pci,bw=bw)
    else:
        return 'Unsupported rat'
    params = cur_cell.get_cell_parameters()
    return json.dumps(params, sort_keys=True, indent=4)

@app.route('/set_rf_state', methods=['POST'])
def rf_state():
    content = request.get_json()
    if content['rat'] == '3g':
        if content['state'] == '1':
            cur_cell = cell_objects.Cell_3G(ip['3G'],G_logger)
            cur_cell.set_admin_state('1')
        elif content['state'] == '0':
            cur_cell = cell_objects.Cell_3G(ip['3G'],G_logger)
            cur_cell.set_admin_state('0')
        else:
            G_logger.warn('Unvalid rf state param 3G recieved')
            return 'Unvalid state'
    elif content['rat'] == '4g':
        if content['state'] == '1':
            cur_cell = cell_objects.Cell_4G(ip['4G'],G_logger)
            cur_cell.set_admin_state('1')
        elif content['state'] == '0':
            cur_cell = cell_objects.Cell_4G(ip['4G'],G_logger)
            cur_cell.set_admin_state('0')
        else:
            G_logger.warn('Unvalid rf state param 4G recieved')
            return 'Unvalid state'
    else:
        G_logger.warn('Unvalid rf state rat parameter recieved')
        return 'Unvalid rat'
    return "rf state changed"



def init_logger():
    console_handler = logging.StreamHandler()
    format = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s")
    console_handler.setFormatter(format)
    
    G_logger = logging.getLogger('ip-access')
    G_logger.level = logging.DEBUG
    G_logger.addHandler(console_handler)

    return G_logger


if __name__ == '__main__':
    G_logger = init_logger()
    app.run(host='0.0.0.0', port='5000')
    # x = cell_objects.Cell_3G(ip['3G'],G_logger)
    # x.set_cell_paramters(42519,33652,20,569,10758,10)
