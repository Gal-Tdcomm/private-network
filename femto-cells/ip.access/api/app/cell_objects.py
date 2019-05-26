import paramiko
import logging
import time
import  copy
from pprint import pprint

## Femoto cell credentials
USER = 'root'
PASSWORD = 'D9!*3n4Fw7Ka'

PARAMS_3G = {
            'PLMNID':
                {'Location': "system.Device.Services.FAPService.1.CellConfig.UMTS.CN.PLMNID",
                 'parameter': 0},
            'LAC:RAC' :
                {'Location' : "system.Device.Services.FAPService.1.CellConfig.UMTS.CN.LACRAC",
                 'parameter' : 0},
            'Cell-ID':
                {'Location': "system.Device.Services.FAPService.1.CellConfig.UMTS.RAN.CellID",
                 'parameter': 0},
            'UARFCN-PSC':
                {'Location': "system.Device.Services.FAPService.1.REM.X_000295_RFParamsCandidateList",
                 'parameter': 0},
            'Admin-state':
                {'Location': "system.Device.Services.FAPService.1.FAPControl.UMTS.AdminState",
                 'parameter': 0},
            'RFTxStatus':
                {'Location': "system.Device.Services.FAPService.1.FAPControl.UMTS.RFTxStatus",
                 'parameter': 0},
        }


class Cell_3G:
    def __init__(self,ip,logger):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ip = ip
        self.dmi_location = '/opt/ipaccess/DMI/ipa-dmi'
        self.logger = logger
        
    def get_cell_parameters(self):
        """Getting S60 parameters by ssh, using embeded dmi interface of
        ip.access.

        @return: parameters list
        """
        ### open ssh client
        try:
            self.logger.info('Try to ssh %s 3G cell - Getting params'%(self.ip))
            self.client.connect(self.ip, username=USER, password=PASSWORD)
            self.logger.info('Successfully ssh %s 3G cell - Getting params'%(self.ip))

            # Building query
            PARAMS = copy.deepcopy(PARAMS_3G)
            query = self.dmi_location + " -c \""
            for i, j in PARAMS.items():
                debug_query = 'get ' + j['Location'] + "\n"
                self.logger.debug("3G ip %s cell get dmi configuration line : %s"%(self.ip,debug_query))
                query += debug_query
            query += "\""

            # Qurying and response analyzing
            stdin, stdout, stderr = self.client.exec_command(query)
            warnings = stderr.readlines()
            if len(warnings) > 1:
                for i in warnings:
                    self.logger.error("3G ip %s cell stderr after querying : %s"%(self.ip,i))
            response = stdout.readlines()
            for i in response:
                if ' is ' in i:
                    if 'RFParamsCandidateList' in i:
                        PARAMS['UARFCN-PSC']['parameter'] = i.split('is ')[1].split('\n')[0]
                        self.logger.info("Cell 3G ip %s conf param %s is %s"%(self.ip,'uarfcn-psc',PARAMS['UARFCN-PSC']['parameter']))
                    if 'AdminState' in i:
                        PARAMS['Admin-state']['parameter'] = i.split('is ')[1].split('\n')[0]
                        self.logger.info("Cell 3G ip %s conf param %s is %s"%(self.ip,'Admin-state',PARAMS['Admin-state']['parameter']))
                if ' = ' in i:
                    if 'RFParamsCandidateList' in i:
                        PARAMS['UARFCN-PSC']['parameter'] = i.split(' = ')[1].split('\n')[0]
                        self.logger.info("Cell 3G ip %s conf param %s is %s"%(self.ip,'uarfcn-psc',PARAMS['UARFCN-PSC']['parameter']))
                    if '.PLMNID' in i:
                        PARAMS['PLMNID']['parameter'] = i.split(' = ')[1].split('\n')[0]
                        self.logger.info("Cell 3G ip %s conf param %s is %s"%(self.ip,'plmnid',PARAMS['PLMNID']['parameter']))
                    if 'LACRAC' in i:
                        PARAMS['LAC:RAC']['parameter'] = i.split(' = ')[1].split('\n')[0]
                        self.logger.info("Cell 3G ip %s conf param %s is %s"%(self.ip,'lac:rac',PARAMS['LAC:RAC']['parameter']))
                    if '.CellID' in i:
                        PARAMS['Cell-ID']['parameter'] = i.split(' = ')[1].split('\n')[0]
                        self.logger.info("Cell 3G ip %s conf param %s is %s"%(self.ip,'Cell-ID',PARAMS['Cell-ID']['parameter']))
                    if '.RFTxStatus' in i:
                        PARAMS['RFTxStatus']['parameter'] = i.split(' = ')[1].split('\n')[0]
                        self.logger.info("Cell 3G ip %s conf param %s is %s"%(self.ip,'RFTxStatus',PARAMS['RFTxStatus']['parameter']))
                    if 'AdminState' in i:
                        PARAMS['Admin-state']['parameter'] = i.split(' = ')[1].split('\n')[0]
                        self.logger.info("Cell 3G ip %s conf param %s is %s"%(self.ip,'Admin-state',PARAMS['Admin-state']['parameter']))
            self.client.close()
            return PARAMS
        except Exception:
            self.logger.critical('Unable %s 3G to get params'%(self.ip))


    def set_admin_state(self, adminState):
        try:
            self.logger.info('Try to ssh %s 3G cell - Admin-state change'%(self.ip))
            self.client.connect(self.ip, username=USER, password=PASSWORD)
            self.logger.info('Successfully ssh %s 3G cell- Admin-state change'%(self.ip))

            # Building query
            setter = self.dmi_location + " -c \"set " + PARAMS_3G['Admin-state']['Location'] + ' = ' + adminState + '\"'
            self.logger.debug("3G ip %s cell set dmi configuration admin-state : %s"%(self.ip,setter))
            stdin, stdout, stderr = self.client.exec_command(setter)
            
            #Analying if error occured
            warnings = stderr.readlines()
            if len(warnings) > 1:
                for i in warnings:
                    self.logger.error("3G ip %s cell stderr set admin-state : %s"%(self.ip,i))
            self.logger.info('3G cell ip-%s admin-state changed to %s'%(self.ip,adminState))
            time.sleep(2)
            self.client.close()
        except Exception:
            self.logger.critical('Unable to set admin-state in 3G %s'%(self.ip),exec_info=True)


    def set_cell_paramters(self, plmnid,lac,rac,cellid,uarfcn, psc):
        self.logger.info('Received request changing 3G ip %s conf to : plmn=%s,lac=%s,rac=%s,cellid=%s,uarfcn=%s,psc=%s'%(self.ip,plmnid,lac,rac,cellid,uarfcn,psc))
        self.logger.info('Setting 3G %s admin state to 0 before conf change'%(self.ip))
        self.set_admin_state('0')
        try:
            self.logger.info('Try to ssh %s 3G cell - params change'%(self.ip))
            self.client.connect(self.ip, username=USER, password=PASSWORD)
            self.logger.info('Successfully ssh %s 3G cell- params change'%(self.ip))

            PARAMS = copy.deepcopy(PARAMS_3G)
            PARAMS['PLMNID']['parameter'] = "{}".format(plmnid)
            PARAMS['LAC:RAC']['parameter'] = "{}:{}".format(lac,rac)
            PARAMS['Cell-ID']['parameter'] = "{}".format(cellid)
            PARAMS['UARFCN-PSC']['parameter'] = "{}-{}".format(uarfcn,psc)


            # Building setter
            setter = self.dmi_location + " -c \""
            for i, j in PARAMS.items():
                if i == 'RFTxStatus' or i == 'Admin-state':
                    continue
                setter += "set {}=\\\"{}\\\"\n".format(j['Location'],j['parameter']) 
                self.logger.debug("3G ip %s cell set dmi : %s"%(self.ip,setter))
            setter += "\""

            # Setting parameters
            stdin, stdout, stderr = self.client.exec_command(setter)
            
            #Analyzing errors
            warnings = stderr.readlines()
            if len(warnings) > 1:
                for i in warnings:
                    self.logger.error("3G ip %s cell stderr set admin-state : %s"%(self.ip,i))
            time.sleep(2)
            self.client.close()
            self.logger.info('Cell params 3G ip %s changed'%(self.ip))
        except Exception:
            self.logger.critical('Unable to set params in 3G %s'%(self.ip))



PARAMS_4G = {
            'PLMNID':
                {'table': "FAPServiceCellConfigLTEEPCPLMNList",
                 'column' : "PLMNID",
                 'parameter': 0},
            'TAC' :
                {'table': "FAPServiceCellConfigLTEEPC",
                 'column': "TAC",
                 'parameter' : 0},
            'Cell-ID':
                {'table': "FAPServiceCellConfigLTERANCommon",
                 'column': "CellIdentity",
                 'parameter': 0},
            'Band':
                {'table': "FAPServiceCellConfigLTERANRF",
                 'column': "FreqBandIndicator",
                 'parameter': 0},
            'Dl-EARFCN':
                {'table': "FAPServiceCellConfigLTERANRF",
                 'column': "EARFCNDL",
                 'parameter': 0},
            'Ul-EARFCN':
                {'table': "FAPServiceCellConfigLTERANRF",
                 'column': "EARFCNUL",
                 'parameter': 0},
            'Dl-BW':
                {'table': "FAPServiceCellConfigLTERANRF",
                 'column': "DLBandwidth",
                 'parameter': 0},
            'Ul-BW':
                {'table': "FAPServiceCellConfigLTERANRF",
                 'column': "ULBandwidth",
                 'parameter': 0},
            'PCI':
                {'table': "FAPServiceCellConfigLTERANRF",
                 'column': "PhyCellID",
                 'parameter': 0},
            'Admin-state':
                {'table': "FAPServiceFAPControlLTE",
                 'column': "AdminState",
                 'parameter': 0},
            'RFTxStatus':
                {'table': "FAPServiceFAPControlLTE",
                 'column': "RFTxStatus",
                 'parameter': 0},
            }

class Cell_4G:
    def __init__(self,ip,logger):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ip = ip
        self.db_cmd = 'sqlite3 /config/femto.db'
        self.logger = logger


    def get_cell_parameters(self):
        try:
            self.logger.info('Try to ssh %s 4G cell - get params'%(self.ip))
            self.client.connect(self.ip, username=USER, password=PASSWORD)
            self.logger.info('Successfully ssh %s 4G cell- get params'%(self.ip))
            PARAMS = copy.deepcopy(PARAMS_4G)
            for i in PARAMS.keys():
                #query building
                query = "{} \"SELECT {} FROM {}\"".format(self.db_cmd,PARAMS[i]['column'],PARAMS[i]['table'])
                self.logger.debug("4G ip %s cell query db configuration line : %s"%(self.ip,query))
                
                #Querying 
                stdin, stdout, stderr = self.client.exec_command(query)
                
                #Warning capture
                warnings = stderr.readlines()
                if len(warnings) != 0:
                    for i in warnings:
                        self.logger.error("4G ip %s cell stderr get-params : %s"%(self.ip,i))
                
                #Response analyzing
                response = stdout.readlines()[0].split('\n')[0]
                self.logger.debug("Cell 4G ip %s conf param %s is %s"%(self.ip,i,response))
                PARAMS[i]['parameter'] = response
            self.client.close()
            return PARAMS
        except Exception:
            self.logger.critical('Unable %s 4G get params'%(self.ip))

    def set_admin_state(self, adminState):
        try:
            self.logger.info('Try to ssh %s 4G cell - Admin-state'%(self.ip))
            self.client.connect(self.ip, username=USER, password=PASSWORD)
            self.logger.info('Successfully ssh %s 4G cell- Admin-state'%(self.ip))

            # Building query
            setter = "{} \"update {} set {}='{}'\"".format(self.db_cmd,PARAMS_4G['Admin-state']['table'],PARAMS_4G['Admin-state']['column'],adminState)
            self.logger.debug("4G ip %s cell set db configuration admin-state : %s"%(self.ip,setter))
            stdin, stdout, stderr = self.client.exec_command(setter)

             #Analying if error occured
            warnings = stderr.readlines()
            if len(warnings) != 0:
                for i in warnings:
                    self.logger.error("4G ip %s cell stderr set admin-state : %s"%(self.ip,i))
            self.logger.info('4G cell ip-%s admin-state changed to %s'%(self.ip,adminState))

            # Waiting parameter to adapt
            time.sleep(2)
            self.client.close()
        except Exception:
            self.logger.critical('Unable to set admin-state in 4G %s'%(self.ip))



    def set_cell_parameters(self,plmnid, tac, cid, bandId, earfcn, pci, bw):
        try:
            self.logger.info('Received request changing 4G ip %s conf to : plmn=%s,tac=%s,cid=%s,band=%s,earfcn=%s,pci=%s,bw=%s'%(self.ip,plmnid,tac,cid,bandId,earfcn,pci,bw))

            # Turning off rf before rf configuration change
            self.logger.info('Setting 4G %s admin state to 0 before conf change'%(self.ip))
            self.set_admin_state('0')

            self.logger.info('Try to ssh %s 4G cell - params change'%(self.ip))
            self.client.connect(self.ip, username=USER, password=PASSWORD)
            self.logger.info('Successfully ssh %s 4G cell- params change'%(self.ip))

            rs_mhz = {
                '1.4' : '6',
                '3' : '15',
                '5' : '25',
                '10' : '50',
                '15' : '75',
                '20' : '100'
            }

            # Setting parameters in dictionary
            PARAMS = copy.deepcopy(PARAMS_4G)
            PARAMS['PLMNID']['parameter'] = plmnid
            PARAMS['TAC']['parameter'] = tac
            PARAMS['Cell-ID']['parameter'] = cid
            PARAMS['Dl-EARFCN']['parameter'] = earfcn
            PARAMS['Ul-EARFCN']['parameter'] = int(earfcn) + 18000
            PARAMS['Dl-BW']['parameter'] = rs_mhz[bw]
            PARAMS['Ul-BW']['parameter'] = rs_mhz[bw]
            PARAMS['PCI']['parameter'] = pci
            PARAMS['Band']['parameter'] = bandId

            # Building query & excuting
            notSettindDb = ['Dl-BW','Ul-BW','Ul-EARFCN','Dl-EARFCN','Band']
            notSetter = ['Admin-state','RFTxStatus']
            # Setting parameters in DB
            for i in PARAMS.keys():
                if i not  in notSettindDb and i not in notSetter:
                    setter = "{} \"update {} set {}='{}';\"\n".format(self.db_cmd, PARAMS[i]['table'],
                                                                   PARAMS[i]['column'], PARAMS[i]['parameter'])
                    self.logger.debug("4G ip %s cell set db conf : %s"%(self.ip,setter))
                    stdin, stdout, stderr = self.client.exec_command(setter)
                    
                    #Analying if error occured
                    warnings = stderr.readlines()
                    if len(warnings) != 0:
                        for i in warnings:
                            self.logger.error("4G ip %s cell stderr set conf-1 : %s"%(self.ip,i))
            
            # Setting RF parameters
            for i in PARAMS.keys():
                if i in notSettindDb and i not in notSetter:
                    setter = '{} "update {} set {}={};"\n'.format(self.db_cmd, PARAMS[i]['table'],
                                                                   PARAMS[i]['column'], PARAMS[i]['parameter'])
                    self.logger.debug("4G ip %s cell set db conf : %s"%(self.ip,setter))
                    stdin, stdout, stderr = self.client.exec_command(setter)

                    #Analying if error occured
                    warnings = stderr.readlines()
                    if len(warnings) != 0:
                        for i in warnings:
                            self.logger.error("4G ip %s cell stderr set conf: %s"%(self.ip,i))

            # Waiting parameter to adapt
            time.sleep(2)
            self.client.close()
            self.logger.info('Cell params 4G ip %s changed'%(self.ip))
        except Exception:
            self.logger.warn('Unable to set params in 4G %s'%(self.ip))





    






