import paramiko
import time

IP_3G = '192.168.0.87'
IP_4G = '192.168.0.95'
dmi_location_3g = '/opt/ipaccess/DMI/ipa-dmi'
db_cmd_4g = 'sqlite3 /config/femto.db'


## Femoto cell credentials
USER = 'root'
PASSWORD = 'D9!*3n4Fw7Ka'

def startup_3g():
    min_cpich()
    client_3g.exec_command(dmi_location_3g + "-c \"set system.Device.Services.FAPService.1.REM.X_000295_RFParamsCandidateList = \"10788-10\"​\"")
    client_3g.exec_command(dmi_location_3g + "-c \"set system.Device.Services.FAPService.1.FAPControl.UMTS.AdminState = 1\"")

def min_cpich():
    client_3g.exec_command(dmi_location_3g + "-c \"set system.Device.Services.FAPService.1.CellConfig.UMTS.RAN.RF.PCPICHPower = \"-10..-10\"\"")


def min_reference():
    #resource blocks
    rs_mhz = {
        '1.4' : '6',
        '3' : '15',
        '5' : '25',
        '10' : '50',
        '15' : '75',
        '20' : '100'
    }
    stdin, stdout, stderr = client_4g.exec_command(db_cmd_4g + "\"SELECT X_000295_MinTxPower FROM FAPServiceCapabilitiesLTE\"")
    response = stdout.readlines()[0].split('\n')[0]
    rs = rs_mhz[response]

    # min tx power
    stdin, stdout, stderr = client_4g.exec_command(db_cmd_4g + "\"SELECT DLBandwidth FROM FAPServiceCellConfigLTERANRF\"")
    min_tx_pow = stdout.readlines()[0].split('\n')[0]
    
    from math import log10
    min_reference = int(min_tx_pow) - 10 * log10(int(rs)*12)
    client_4g.exec_command(db_cmd_4g + "\"update FAPServiceFAPControlLTE set AdminState='0'\"")
    client_4g.exec_command(db_cmd_4g + "\"UPDATE FAPServiceCellConfigLTERANRF set ReferenceSignalPower=\'{}\'\"".format(min_reference))
    time.sleep(15)
    client_4g.exec_command(db_cmd_4g + "\"update FAPServiceFAPControlLTE set AdminState='1'\"")

if __name__ == "__main__":
    time.sleep(120)
    client_3g = paramiko.SSHClient()
    client_3g.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client_3g.connect(IP_3G,username=USER,password=PASSWORD)
    startup_3g()

    client_4g = paramiko.SSHClient()
    client_4g.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client_4g.connect(IP_4G,username=USER,password=PASSWORD)
    min_reference()