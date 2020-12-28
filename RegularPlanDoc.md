#  Endpoint Documentation and Regular Plan Model

* Base route: `/regularplan`

| URL                                                                 | Method  | Authentication | Descriiption                                                                         |
| :------------------------------------------------------------------ | :-----: | :------------: | :----------------------------------------------------------------------------------: |
| [`/regularplan`](#markdown-header-get-regularplan)                  | `GET`   |     Yes        | List the Regular Plans that has publish = true or that belongs to user authenticated |
| [`/regularplan`](#markdown-header-post-regularplan)                 | `POST`  |     Yes        | Create a new Regular Plan with the user authenticated as owner.                      |
| [`/regularplan/:pk`](#markdown-header-post-regularplan)             | `PATCH` |     Yes        | Update a Regular Plan with the user authenticated as owner.                      |

RegularPlan Fields

#### id
- Description: the identifier of the plan
- Type: int
- Required

#### name
- Description: the name of the plan
- Type: String
- Max Length: 100
- Required

#### tar_included
- Description: 
- Type: Boolean
- Required

#### subscription
- Description: it’s the monthly subscription for the user
- Type: Float
- Requried
- Value valid: bigger than zero.

#### cycle
- Description: The Regular plan tariff cycle
- Type: IntegerField
- choices: 1 - daily ; 2 - weekly
- Required

#### type
- Description: The Regular plan tariff type
- Type: IntegerField
- choices: 1 - bi-time ; 2 - tri-time; 3 - simple
- Required


#### offer_iva
- Description: boolean true or false
- Type: Boolean
- Required

#### off_peak_price
- Description: The Regular Plan price off peak 
- Type: float
- Value valid: bigger than zero.
- Required

#### peak_price
- Description: The Regular Plan price peak 
- Type: float
- Value valid: bigger than zero.
- Required

#### unit
- Description: The Regular Plan unit charge measure
- Type: IntegerField
- choices: 1 - kwh ; 2 - min
- Required

#### valid
- Description: 
- Type: Boolean
- Required

#### publish
- Description: Indicates if a Regular Plan is published
- Type: Boolean
- Required

#### vat
- Description: 
- Type: IntegerField
- Max Value: 100
- Min Value: 1
- Required

#### owner
- Description: The Regular Plan's owner. Can be null if publish is true or false
- Type: User
- No required
---
## GET /regularplan
### Description
List the Regular Plans that has publish = true or that belongs to user authenticated

### Params
#### query
| Field      |               Description                                                 |       Type        | Required |
| :----:     | :-----------------------------------------------------------------------: | :---------------: | :------: |
| `publish`  | indicates if the user want list the Regular Plans that has publish = true | boolean           |   No     |

### Response
| statusCode |  Fields                               | Desciption                                    |
| :--------- | :-----------------------------------: | --------------------------------------------- |
| `401`      |     `detail`                          | Invalid token or token not sent in headers.   |
| `200`      |  `count, next,previous,results`       | List of Regular Plan                          |
| `500`      |     `detail`                          | Server error  .                               |
  
### Example
#### Request - GET /regularplan/?publish=True

#### Response - 200
```python
{
  "count": 6,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 2,
      "owner": {
        "id": 2,
        "username": "cdac",
        "first_name": "Carlos",
        "last_name": "Daniel",
        "email": "carlosd.1199@gmail.com"
      },
      "name": "dfd",
      "tar_included": true,
      "subscription": 1.0,
      "cycle": 1,
      "type": 2,
      "offer_iva": false,
      "off_peak_price": 0.05,
      "peak_price": 2.23,
      "unit": 1,
      "valid": false,
      "publish": true,
      "vat": 1
    },
    {
      "id": 3,
      "owner": {
        "id": 2,
        "username": "cdac",
        "first_name": "Carlos",
        "last_name": "Daniel",
        "email": "carlosd.1199@gmail.com"
      },
      "name": "dfd",
      "tar_included": true,
      "subscription": 1.0,
      "cycle": 1,
      "type": 2,
      "offer_iva": false,
      "off_peak_price": 0.05,
      "peak_price": 2.23,
      "unit": 1,
      "valid": false,
      "publish": true,
      "vat": 1
    },
    {
      "id": 4,
      "owner": {
        "id": 1,
        "username": "cdac",
        "first_name": "Carlos",
        "last_name": "Daniel",
        "email": "carlosd.1199@gmail.com"
      },
      "name": "dfd",
      "tar_included": true,
      "subscription": 1.0,
      "cycle": 1,
      "type": 2,
      "offer_iva": false,
      "off_peak_price": 0.05,
      "peak_price": 2.23,
      "unit": 1,
      "valid": false,
      "publish": true,
      "vat": 1
    },
    {
      "id": 5,
      "owner": {
        "id": 1,
        "username": "cdac",
        "first_name": "Carlos",
        "last_name": "Daniel",
        "email": "carlosd.1199@gmail.com"
      },
      "name": "dfd",
      "tar_included": true,
      "subscription": 1.0,
      "cycle": 1,
      "type": 2,
      "offer_iva": false,
      "off_peak_price": 0.05,
      "peak_price": 2.23,
      "unit": 1,
      "valid": false,
      "publish": true,
      "vat": 1
    },
    {
      "id": 6,
      "owner": {
        "id": 1,
        "username": "cdac",
        "first_name": "Carlos",
        "last_name": "Daniel",
        "email": "carlosd.1199@gmail.com"
      },
      "name": "dfd",
      "tar_included": true,
      "subscription": 1.0,
      "cycle": 1,
      "type": 2,
      "offer_iva": false,
      "off_peak_price": 0.05,
      "peak_price": 2.23,
      "unit": 1,
      "valid": false,
      "publish": true,
      "vat": 1
    },
    {
      "id": 7,
      "owner": {
        "id": 1,
        "username": "cdac",
        "first_name": "Carlos",
        "last_name": "Daniel",
        "email": "carlosd.1199@gmail.com"
      },
      "name": "dfd",
      "tar_included": true,
      "subscription": 1.0,
      "cycle": 1,
      "type": 2,
      "offer_iva": false,
      "off_peak_price": 0.05,
      "peak_price": 2.23,
      "unit": 1,
      "valid": false,
      "publish": true,
      "vat": 1
    },
```


