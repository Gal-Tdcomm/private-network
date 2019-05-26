# IP.access API
## Requirements
* docker-engine
* docker-compose
* port **5000** on host.

## 3G API
1. get parameters configured in femto-cell:\
   **Request**\
   URI: `http://<api-ip>:5000/get_params/3g` \
   Method: `GET`\

   **Response**
```json
        {
            "Admin-state": {
                "Location": "system.Device.Services.FAPService.1.FAPControl.UMTS.AdminState",
                "parameter": "TRUE"
            },
            "Cell-ID": {
                "Location": "system.Device.Services.FAPService.1.CellConfig.UMTS.RAN.CellID",
                "parameter": "580"
            },
            "LAC:RAC": {
                "Location": "system.Device.Services.FAPService.1.CellConfig.UMTS.CN.LACRAC",
                "parameter": "\"33500:15\""
            },
            "PLMNID": {
                "Location": "system.Device.Services.FAPService.1.CellConfig.UMTS.CN.PLMNID",
                "parameter": "\"46019\""
            },
            "RFTxStatus": {
                "Location": "system.Device.Services.FAPService.1.FAPControl.UMTS.RFTxStatus",
                "parameter": "TRUE"
            },
            "UARFCN-PSC": {
                "Location": "system.Device.Services.FAPService.1.REM.X_000295_RFParamsCandidateList",
                "parameter": "\"10786-10\""
            }
        }
```

2. set parameters:\
**Request:**
URI: `192.168.0.12:5000/set_params`\
Method: `Post`\
Example: 
```json
        {
            "rat" : "3G",
            "mcc" : "460",
            "mnc" : "19",
            "rac" : "15",
            "lac" : "33500",
            "cellId" : "580",
            "uarfcn" : "10786",
            "psc" : "10"
        }
```
Body:
```json
        {
            "rat" : "3g",
            "mcc" : "<mcc>",
            "mnc" : "<mnc>",
            "rac" : "<rac>",
            "lac" : "<lac>",
            "cellId" : "<cid>",
            "uarfcn" : "<uarfcn>",
            "psc" : "<psc>"
        }
```



