## S60z - UMTS
The UMTS version uses diffrent version of SW on the sdr, after installing apply all the follow command in the dmi interface:\
`/opt/ipaccess/DMI/ipa-dmi`

### IPSEC
| Parameter | Information |example |
| --- | --- | --- |
| IPsec | Enable / disable Ipsec | `set system.Device.IPsec.Enable = 0`|

### NTP
| Parameter | Information |example |
| --- | --- | --- |
| NTP server | NTP server ip | `set system.Device.Time.NTPServer1 = "192.168.0.1"` |

### HnB GW
| Parameter | Information |example |
| --- | --- | --- |
| HnB GW  | HnB GW IP | `set system.Device.Services.FAPService.1.FAPControl.UMTS.Gateway.FAPGWServer1 = "192.168.0.5"`|

### UE access mode
| Parameter | Information |example |
| --- | --- | --- |
| Access class alow | alow access class imsi | `set system.Device.Services.FAPService.1.AccessMgmt.UMTS.AccessMode = "Open Access"`|
| CSG | Closed subscribers group method | `set system.Device.Services.FAPService.1.AccessMgmt.UMTS.NonCSGUEAccessDecision = "Query FAPGW"` |
| Access decision mode | defined in tr196 | `set system.Device.Services.FAPService.1.AccessMgmt.UMTS.X_000295_AccessDecisionMode = "Legacy Mode"` |

### Reject method
| Parameter | Information |example |
| --- | --- | --- |
| Reject method | defined by ip access |`set system.Device.Services.FAPService.1.AccessMgmt.UMTS.X_000295_DefaultUERejectMethod = "AUTO"` |

### Cell identifiers
| Parameter | Information |example |
| --- | --- | --- |
| LAC / RAC | location identifiers (lac:rac) | `set system.Device.Services.FAPService.1.CellConfig.UMTS.CN.LACRAC = "33961:10"` |
| PLMNID | PLMN id to broadcast | `set system.Device.Services.FAPService.1.CellConfig.UMTS.CN.PLMNID = "00102"` |
| Cell id | cell id to broadcast | `set system.Device.Services.FAPService.1.CellConfig.UMTS.RAN.CellID = 561` |
| RNC ID | Radio network controler to broadcast | `set system.Device.Services.FAPService.1.CellConfig.UMTS.RAN.RNCID = 71` |

### RF parameters
| Parameter | Information |example |
| --- | --- | --- |
| Pcpich | Pcpich power range in dBm | `set system.Device.Services.FAPService.1.CellConfig.UMTS.RAN.RF.PCPICHPower = "-10..5"` |
| UARFCN-PSC | Frequency channel configuration | `set system.Device.Services.FAPService.1.REM.X_000295_RFParamsCandidateList = "10788-3"` |

### RF  state
| Parameter | Information |example |
| --- | --- | --- |
| Admin state | Set RF on/off | `set system.Device.Services.FAPService.1.FAPControl.UMTS.AdminState = 1` |

### NWL
| Parameter | Information |example |
| --- | --- | --- |
| Scan periodicaly | on/off | `set system.Device.Services.FAPService.1.REM.UMTS.WCDMA.ScanPeriodically= 0` |
| Scan on boot | on/off | `set system.Device.Services.FAPService.1.REM.UMTS.WCDMA.ScanOnBoot = 0` |

### Configuration method
| Parameter | Information |example |
| --- | --- | --- |
| Configure method | configure cell by scan auto or manulaly | `set system.Device.Services.FAPService.1.REM.X_000295_CellParameterSelectionMethod="CONFIGURED"` |


**Summary**
```
set system.Device.IPsec.Enable = 0
set system.Device.Services.FAPService.1.AccessMgmt.UMTS.AccessMode = "Open Access"​
set system.Device.Services.FAPService.1.AccessMgmt.UMTS.NonCSGUEAccessDecision = "Query FAPGW"​
set system.Device.Services.FAPService.1.AccessMgmt.UMTS.X_000295_AccessDecisionMode = "Legacy Mode"​
set system.Device.Services.FAPService.1.AccessMgmt.UMTS.X_000295_DefaultUERejectMethod = "AUTO"​
set system.Device.Services.FAPService.1.CellConfig.UMTS.CN.LACRAC = "33961:10"​
set system.Device.Services.FAPService.1.CellConfig.UMTS.CN.PLMNID = "00102"​
set system.Device.Services.FAPService.1.CellConfig.UMTS.RAN.CellID = 130539
set system.Device.Services.FAPService.1.CellConfig.UMTS.RAN.RNCID = 1
set system.Device.Services.FAPService.1.CellConfig.UMTS.RAN.RF.PCPICHPower = "3..3"​
set system.Device.Services.FAPService.1.FAPControl.UMTS.Gateway.FAPGWServer1 = "192.168.0.5"​
set system.Device.Services.FAPService.1.REM.X_000295_RFParamsCandidateList = "10788-10"​
set system.Device.Time.NTPServer1 = "192.168.0.1"​
set system.Device.Services.FAPService.1.REM.UMTS.WCDMA.ScanOnBoot = 0
set system.Device.Services.FAPService.1.REM.UMTS.WCDMA.ScanPeriodically= 0
set system.Device.Services.FAPService.1.REM.X_000295_CellParameterSelectionMethod="CONFIGURED"​
set system.Device.Services.FAPService.1.FAPControl.UMTS.AdminState = 1
```


### FEM
| Parameter | Information |example |
| --- | --- | --- |
| Pcipich | pcpich power range should be extended | `set system.Device.Services.FAPService.1.CellConfig.UMTS.RAN.RF.PCPICHPower = "-10.0..29.9"`
| Gain | Gain of FEM (mulitpy the gain by 10) | `set system.Device.Services.FAPService.1.REM.X_000295_ExternalPaGain = 440` |

**Summary**
```
set system.Device.Services.FAPService.1.CellConfig.UMTS.RAN.RF.PCPICHPower = "-10.0..29.9"
set system.Device.Services.FAPService.1.REM.X_000295_ExternalPaGain = 440
```















