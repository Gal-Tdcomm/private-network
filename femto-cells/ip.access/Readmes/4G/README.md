## S60z - LTE 
### NTP 
1. change default ntp in :\
`vi /var/ipaccess/hw_description.dat`
```
DEFAULT_NTP_SERVER_ADDRESS​
String​
1​
192.168.0.1
```
2. Add the following configuration to:\
`vi /var/ipaccess/hw_description.dat`
```
NTP_SERVER_NOWAIT​
string​
1​
TRUE​
NET_PRIVATE_NETWORK​
string​
1​
TRUE​
```

### eNodeB GW
| Parameter | Information |example |
| --- | --- | --- |
| S1 end-point | Set the S1 End Point Type - 0 (MME) / 1 (HeNBGW) |`sqlite3 $SQLITE_FEMTO_DB_PATH "update FAPServiceFAPControlLTEGateway set X_000295_RemoteS1EndPointType=0"` |
| S1 end point ip | set ip of MME/HeNBGW | `sqlite3 $SQLITE_FEMTO_DB_PATH "update FAPServiceFAPControlLTEGateway set S1SigLinkServerList='192.168.0.5'"​`|
|

### RF state
**1-transmiting, 0- not transmiting**
| Parameter | Information |example |
| --- | --- | --- |
| Admin State of the AP | connection on to MME/HeNBGW (1-on, 0-off) | `sqlite3 $SQLITE_FEMTO_DB_PATH "update FAPServiceFAPControlLTE set AdminState='1'" `|
| set auto start | set auto start for connection to MME/HeNBGW | `set_auto_start 1` |

### Radio Parameters
**run the command in terminal**
| Parameter | Information |example |
| --- | --- | --- |
| set radio parameters | `set_radio_params <UL_EARFCN> <DL_EARFCN> <LTE_BAND> <BANDWIDTH_MHz>` | `set_radio_params 21100 3100 7 10` |

### Cell identifiers
| Parameter | Information |example |
| --- | --- | --- |
| Cell ID (PCI) | Physical cell id | `sqlite3 $SQLITE_FEMTO_DB_PATH "update FAPServiceCellConfigLTERANRF set PhyCellID='270'"​`|
| TAC | Tracking area code | `sqlite3 $SQLITE_FEMTO_DB_PATH "update FAPServiceCellConfigLTEEPC set TAC='9'"​`|
| Cell identity HeNB | cell unique identity in HeNB | `sqlite3 $SQLITE_FEMTO_DB_PATH "update FAPServiceCellConfigLTERANCommon set CellIdentity='2155'"` |
| PLMN | Public land mobile network | `sqlite3 $SQLITE_FEMTO_DB_PATH "update FAPServiceCellConfigLTEEPCPLMNList set PLMNID='00101'"​` |


### TR69
1. disable default tr69 in (0-disable,1-enable):\
`vi /var/ipaccess/hw_description.dat`
```
REDIRECTOR_URL​
string​
0​
http://192.168.0.30/acs
```
2. change parameter in DB:
| Parameter | Information |
| ---- | ---- | ---- |
| TR69 state | 0-diable, 1- enable |

**Summary**
```
sqlite3 $SQLITE_FEMTO_DB_PATH "update FAPServiceFAPControlLTEGateway set X_000295_RemoteS1EndPointType=0"
sqlite3 $SQLITE_FEMTO_DB_PATH "update FAPServiceFAPControlLTEGateway set S1SigLinkServerList='192.168.0.5'"
sqlite3 $SQLITE_FEMTO_DB_PATH "update FAPServiceFAPControlLTE set AdminState='1'"
set_auto_start 1
set_radio_params 21100 3100 7 10
sqlite3 $SQLITE_FEMTO_DB_PATH "update FAPServiceCellConfigLTERANRF set PhyCellID='270'"​
sqlite3 $SQLITE_FEMTO_DB_PATH "update FAPServiceCellConfigLTEEPC set TAC='9'"​
sqlite3 $SQLITE_FEMTO_DB_PATH "update FAPServiceCellConfigLTERANCommon set CellIdentity='2155'"
sqlite3 $SQLITE_FEMTO_DB_PATH "update FAPServiceCellConfigLTEEPCPLMNList set PLMNID='00102'"​
sqlite3 /sysconfig/commonstate.db "update SysConfigInfo set Tr069Enabled='0'"

sqlite3 $SQLITE_FEMTO_DB_PATH "UPDATE FAPServiceCellConfigLTERANRF set ReferenceSignalPower='-2'"
sqlite3 $SQLITE_FEMTO_DB_PATH "UPDATE FAPServiceFAPControlLTE set AdminState='0'"
sqlite3 $SQLITE_FEMTO_DB_PATH "SELECT RFTxStatus FROM FAPServiceFAPControlLTE"
sqlite3 $SQLITE_FEMTO_DB_PATH "SELECT AdminState FROM FAPServiceFAPControlLTE"
sqlite3 $SQLITE_FEMTO_DB_PATH "SELECT * FROM DeviceFaultMgmtCurrentAlarm"
sqlite3 $SQLITE_FEMTO_DB_PATH "SELECT * FROM DeviceFaultMgmtHistoryEvent"
```

### FEM 
- **Max tx power of PA without FEM is 5 dBm, MAX_TX_POWER = (5 + PA gain)dBm**
- **Min tx power is -50 dBm in all states**
- **MAX RSP = max tx power of LTE AP - 10 * log(RS DL BW * 12)**\

| Parameter | Information |example |
| --- | --- | --- |
| RSP | Reference signal power between max to min (Example gain 44 dBm) | `sqlite3 $SQLITE_FEMTO_DB_PATH "update FAPServiceCellConfigLTERANRF set ReferenceSignalPower=21"​`|
| Gain | change the max tx power of the S60 (gain in dB * 10) | `sqlite3 $SQLITE_FEMTO_DB_PATH "update FAPServiceCellConfigLTERANRF set X_000295_ExternalPAGain=440;"` |
| ZCZC | Defining the range of operating (8=5km) | `sqlite3 $SQLITE_FEMTO_DB_PATH "updat FAPServiceCellConfigLTERANPHYPRACH set ZeroCorrelationZoneConfig=8"` |​ 

**Summary**
```
sqlite3 $SQLITE_FEMTO_DB_PATH "UPDATE FAPServiceFAPControlLTE set AdminState='0'"
sqlite3 $SQLITE_FEMTO_DB_PATH "update FAPServiceCellConfigLTERANRF set ReferenceSignalPower=21"
sqlite3 $SQLITE_FEMTO_DB_PATH "update FAPServiceCellConfigLTERANRF set X_000295_ExternalPAGain=440"
sqlite3 $SQLITE_FEMTO_DB_PATH "update FAPServiceCellConfigLTERANPHYPRACH set ZeroCorrelationZoneConfig=8"
```

### NWL
**Fast scan**
1. disbale-
```
    ipaDbi -c internalDbUpdate "update featureActivation set NwlFastScanEnable =0;"
```

2. enable-
```
    ipaDbi -c internalDbUpdate "update featureActivation set NwlFastScanEnable =1;"
    /bin/sh /opt/ipaccess/bin/fastNmmConf 1 0 (without LNA)
    /bin/sh /opt/ipaccess/bin/fastNmmConf 1 1 (with LNA)
```

reboot between changing 

**scan configuration**
1. LTE -
```
ipaDbi -c setParameterValues Device.Services.FAPService.1.REM.LTE.REMBandList 3,7
ipaDbi -c setParameterValues Device.Services.FAPService.1.REM.LTE.EUTRACarrierARFCNDLList "1283,1300"
```
2. UMTS -
``` 
ipaDbi -c setParameterValues Device.Services.FAPService.1.REM.UMTS.WCDMA.REMBandList "I"
ipaDbi -c setParameterValues Device.Services.FAPService.1.REM.UMTS.WCDMA.UARFCNDLList "10788,10763"
```

3. Others -
```
ipaDbi -c setParameterValues Device.Services.FAPService.1.REM.LTE.ScanPeriodically 0
ipaDbi -c setParameterValues Device.Services.FAPService.1.REM.LTE.ScanOnBoot 0
```

4. Operations -\
    a. start - `
ipaDbi -c setParameterValues Device.Services.FAPService.1.REM.LTE.X_000295_NWLCommand 'Start NWL'`\
    b. stop - `ipaDbi -c setParameterValues Device.Services.FAPService.1.REM.LTE.X_000295_NWLCommand 'Stop NWL'`
