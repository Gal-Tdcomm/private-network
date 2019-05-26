# IP.access API
## Requirements for running server
* docker-engine
* docker-compose
* port **5000** on host.

## 3G API - Reference
1. get parameters configured in femto-cell:\

**Request**\
URI: `http://<api-ip>:5000/get_params/3g` \
Method: `GET`

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

2. set parameters:

**Request:**\
URI: `http://<api-ip>::5000/set_params`\
Method: `Post`\
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

**Response**\
Check the current configured parameters and return them like response in section 1 of get `http://<api-ip>:5000/get_params/3g`

3. RF state:

**Request**\
URI: `http://<api-ip>::5000/set_rf_state`\
Method: `POST`\
Body:
```json
{
	"rat" : "3g",
	"state" : "<0/1>"
}
```
* 0 - tx off , 1 - tx on\
Example:
```json
{
	"rat" : "3g",
	"state" : "1"
}
```


## 4G API - Reference
1. get parameters configured in femto-cell:\

**Request**\
URI: `http://<api-ip>:5000/get_params/4g` \
Method: `GET`

**Response**
```json
{
    "Admin-state": {
        "column": "AdminState",
        "parameter": "0",
        "table": "FAPServiceFAPControlLTE"
    },
    "Band": {
        "column": "FreqBandIndicator",
        "parameter": "3",
        "table": "FAPServiceCellConfigLTERANRF"
    },
    "Cell-ID": {
        "column": "CellIdentity",
        "parameter": "88888",
        "table": "FAPServiceCellConfigLTERANCommon"
    },
    "Dl-BW": {
        "column": "DLBandwidth",
        "parameter": "15",
        "table": "FAPServiceCellConfigLTERANRF"
    },
    "Dl-EARFCN": {
        "column": "EARFCNDL",
        "parameter": "1325",
        "table": "FAPServiceCellConfigLTERANRF"
    },
    "PCI": {
        "column": "PhyCellID",
        "parameter": "999",
        "table": "FAPServiceCellConfigLTERANRF"
    },
    "PLMNID": {
        "column": "PLMNID",
        "parameter": "42519",
        "table": "FAPServiceCellConfigLTEEPCPLMNList"
    },
    "RFTxStatus": {
        "column": "RFTxStatus",
        "parameter": "0",
        "table": "FAPServiceFAPControlLTE"
    },
    "TAC": {
        "column": "TAC",
        "parameter": "677",
        "table": "FAPServiceCellConfigLTEEPC"
    },
    "Ul-BW": {
        "column": "ULBandwidth",
        "parameter": "15",
        "table": "FAPServiceCellConfigLTERANRF"
    },
    "Ul-EARFCN": {
        "column": "EARFCNUL",
        "parameter": "19325",
        "table": "FAPServiceCellConfigLTERANRF"
    }
}
```

2. set parameters:

**Request:**\
URI: `http://<api-ip>::5000/set_params`\
Method: `Post`\
Body:
```json
{
	"bandId": "<band_num>",
	"earfcn": "<dl_earfcn>",
	"pci": "<pci>",
	"lteBandwidth": "<bw>",
	"mcc": "<mcc>",
	"mnc": "<mnc>",
	"rat": "4G",
	"tac": "<tac>",
	"l3CellId": "<cid>"
}
```
Example: 
```json
{
	"bandId": "3",
	"earfcn": "1325",
	"pci": "999",
	"lteBandwidth": "3",
	"mcc": "425",
	"mnc": "19",
	"rat": "4G",
	"tac": "677",
	"l3CellId": "88888"
}
```

**Response**\
Check the current configured parameters and return them like response in section 1 of get `http://<api-ip>:5000/get_params/3g`

3. RF state:

**Request**\
URI: `http://<api-ip>::5000/set_rf_state`\
Method: `POST`\
Body:
```json
{
	"rat" : "4g",
	"state" : "<0/1>"
}
```
* 0 - tx off , 1 - tx on\
Example:
```json
{
	"rat" : "3g",
	"state" : "1"
}
```



