# IP.access API
## Requirements
* docker-engine
* docker-compose
* port **5000** on host.

## 3G API
1. get parameters configured in femto-cell:\
   **Request**\
   URI: http://<api-ip>:5000/get_params/\<id\> (id=3g/4g)\
   Method: GET\

   **Response**
```
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

