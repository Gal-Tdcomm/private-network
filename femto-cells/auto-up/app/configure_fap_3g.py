import paramiko
import time

IP = '192.168.0.87'
dmi_location = '/opt/ipaccess/DMI/ipa-dmi'

## Femoto cell credentials
USER = 'root'
PASSWORD = 'D9!*3n4Fw7Ka'

def startup():
    time.sleep(120)
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(IP,username=USER,password=PASSWORD)
    client.exec_command(dmi_location + "-c \"set system.Device.Services.FAPService.1.REM.X_000295_RFParamsCandidateList = \"10788-10\"​\"")
    client.exec_command(dmi_location + "-c \"set system.Device.Services.FAPService.1.FAPControl.UMTS.AdminState = 1\"")


if __name__ == "__main__":
    startup()