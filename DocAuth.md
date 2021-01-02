#  Endpoint Documentation and User Model

* Base route: `/auth`

| URL                                                                 | Method  | Authentication | Descriiption                                                                         |
| :------------------------------------------------------------------ | :-----: | :------------: | :----------------------------------------------------------------------------------: |
| [`/login`](#markdown-header-post-login)                        | `POST`  |     No         | Makes login and gives a token to an user |
| [`/register`](#markdown-header-post-register)                    | `POST`  |     No         | Create a new user.|

User Fields

#### id
- Description: the identifier of user
- Type: int
- Required

#### username
- Description: The user username
- Type: String
- Max Length: 150
- Unique
- Required

#### fisrt_name
- Description: The user first name
- Type: String
- Max Length: 150
- Required

#### last_name
- Description: The user last name
- Type: String
- Max Length: 150
- Required.

#### password
- Description: The user password
- Type: String
- Required

#### email
- Description: The user email
- Type: String in email format
- Required
---
## POST /login
### Description
Makes login and gives a token to an user. To use the returned token, put in request headers the key `Authorization` and value `JWT your_token`

### Params
#### body
username, password

### Response
| statusCode |  Fields                               | Desciption                                                      |
| :--------- | :-----------------------------------: | --------------------------------------------------------------- |
| `400`      |     `detail`                          | User not found to sent values.                                  |
| `200`      |      `token`                          | User logged                                                     |
| `500`      |     `detail`                          | Server error  .                                                 |

### Example
#### Request - POST /login/
```
{
	"username": "cdac",
	"password": "teste"
}
```

#### Response - 201

```
{
  "token": "token here"
}

```



## POST /register
### Description
Create a new user.

### Params
#### body
username, password

### Response
| statusCode |  Fields                                                                    | Desciption                                                      |
| :--------- | :------------------------------------------------------------------------: | --------------------------------------------------------------- |
| `400`      |     `detail`                                                               | One or more fields are invalids                                 |
| `200`      |  `id`,`username`,`first_name`, `last_name`, `email`                        | User logged                                                     |
| `500`      |     `detail`                                                               | Server error  .                                                 |

### Example
#### Request - POST /register/
```
{
	"first_name": "Carlos",
	"last_name": "Daniel",
	"username": "cdac",
	"password": "teste",
	"email": "carlsosd.1199@gmail.com"
}
```

#### Response - 201

```
{
  "id": 6,
  "username": "cdac",
  "first_name": "Carlos",
  "last_name": "Daniel",
  "email": "carlosd.1199@gmail.com"
}

```
