# MonngorREST

RESTful API written in FastAPI for used as a backend for Monngnor online commercial platform.

## Version: 0.2.1-alpha

### /

#### GET

##### Summary:

Get Root

##### Responses

| Code | Description         |
| ---- | ------------------- |
| 200  | Successful Response |

### /users/register

#### POST

##### Summary:

Register

##### Responses

| Code | Description      |
| ---- | ---------------- |
| 201  | User Created.    |
| 400  | Bad Request.     |
| 422  | Validation Error |

### /users/signin

#### POST

##### Summary:

Signin

##### Responses

| Code | Description                                          |
| ---- | ---------------------------------------------------- |
| 200  | Return access token and token type.                  |
| 401  | Invalid access token / Invalid username or password. |
| 422  | Validation Error                                     |

### /users/query

#### GET

##### Summary:

Query User Data

##### Parameters

| Name   | Located in | Description | Required | Schema  |
| ------ | ---------- | ----------- | -------- | ------- |
| offset | query      |             | No       | integer |
| limit  | query      |             | No       | integer |
| id     | query      |             | No       | integer |

##### Responses

| Code | Description                                          |
| ---- | ---------------------------------------------------- |
| 200  | Return access token and token type.                  |
| 401  | Invalid access token / Invalid username or password. |
| 403  | Required admin token to access this route.           |
| 422  | Validation Error                                     |

##### Security

| Security Schema | Scopes |
| --------------- | ------ |
| JWTBearer       |        |

### /users

#### GET

##### Summary:

Get User Data

##### Responses

| Code | Description                                    |
| ---- | ---------------------------------------------- |
| 200  | Returned user data.                            |
| 404  | Request resourses can not found in the server. |
| 500  | Internal Server Errors                         |

##### Security

| Security Schema | Scopes |
| --------------- | ------ |
| JWTBearer       |        |

#### PUT

##### Summary:

Update Info

##### Responses

| Code | Description            |
| ---- | ---------------------- |
| 200  | Operation result.      |
| 422  | Validation Error       |
| 500  | Internal Server Errors |

##### Security

| Security Schema | Scopes |
| --------------- | ------ |
| JWTBearer       |        |

### /users/alter

#### PUT

##### Summary:

Alter User Info

##### Responses

| Code | Description            |
| ---- | ---------------------- |
| 200  | Operation result.      |
| 422  | Validation Error       |
| 500  | Internal Server Errors |

##### Security

| Security Schema | Scopes |
| --------------- | ------ |
| JWTBearer       |        |

### /users/{user_id}

#### DELETE

##### Summary:

Delete User

##### Parameters

| Name    | Located in | Description | Required | Schema  |
| ------- | ---------- | ----------- | -------- | ------- |
| user_id | path       |             | Yes      | integer |

##### Responses

| Code | Description            |
| ---- | ---------------------- |
| 200  | Operation result.      |
| 422  | Validation Error       |
| 500  | Internal Server Errors |

##### Security

| Security Schema | Scopes |
| --------------- | ------ |
| JWTBearer       |        |

### /products

#### GET

##### Summary:

Query Product Data

##### Parameters

| Name         | Located in | Description | Required | Schema  |
| ------------ | ---------- | ----------- | -------- | ------- |
| offset       | query      |             | No       | integer |
| limit        | query      |             | No       | integer |
| id           | query      |             | No       | integer |
| prod_cate_id | query      |             | No       | integer |

##### Responses

| Code | Description                  |
| ---- | ---------------------------- |
| 200  | Returned query product data. |
| 400  | Bad Request.                 |
| 422  | Validation Error             |
| 500  | Internal Server Errors       |

#### POST

##### Summary:

Create Product

##### Responses

| Code | Description            |
| ---- | ---------------------- |
| 201  | Product Created.       |
| 400  | Bad Request.           |
| 422  | Validation Error       |
| 500  | Internal Server Errors |

##### Security

| Security Schema | Scopes |
| --------------- | ------ |
| JWTBearer       |        |

### /products/categories

#### POST

##### Summary:

Create Product Category

##### Responses

| Code | Description               |
| ---- | ------------------------- |
| 201  | Product Category Created. |
| 422  | Validation Error          |
| 500  | Internal Server Errors    |

##### Security

| Security Schema | Scopes |
| --------------- | ------ |
| JWTBearer       |        |

### /products/images

#### POST

##### Summary:

Create Product Images

##### Parameters

| Name       | Located in | Description | Required | Schema  |
| ---------- | ---------- | ----------- | -------- | ------- |
| product_id | query      |             | Yes      | integer |

##### Responses

| Code | Description                     |
| ---- | ------------------------------- |
| 201  | Product image created.          |
| 413  | Request entity too small/large. |
| 415  | Unsupported media types         |
| 422  | Validation Error                |

##### Security

| Security Schema | Scopes |
| --------------- | ------ |
| JWTBearer       |        |

### Models

#### Body_create_product_images_products_images_post

| Name   | Type       | Description | Required |
| ------ | ---------- | ----------- | -------- |
| images | [ binary ] |             | Yes      |

#### HTTPExceptionRes

| Name   | Type   | Description | Required |
| ------ | ------ | ----------- | -------- |
| detail | string |             | Yes      |

#### HTTPValidationError

| Name   | Type                                    | Description | Required |
| ------ | --------------------------------------- | ----------- | -------- |
| detail | [ [ValidationError](#validationerror) ] |             | No       |

#### Product

| Name               | Type        | Description | Required |
| ------------------ | ----------- | ----------- | -------- |
| pcate_id           | integer     |             | Yes      |
| name               | string      |             | Yes      |
| description        | string      |             | No       |
| price              | number      |             | Yes      |
| discount           | number      |             | Yes      |
| quantity           | integer     |             | Yes      |
| is_extension       | boolean     |             | Yes      |
| duplicate_able     | boolean     |             | Yes      |
| extension_position | [ integer ] |             | No       |
| create_dt          | dateTime    |             | No       |
| modified_dt        | dateTime    |             | No       |
| product_id         | integer     |             | Yes      |

#### ProductCategoryInfo

| Name | Type   | Description | Required |
| ---- | ------ | ----------- | -------- |
| name | string |             | Yes      |

#### ProductInfo

| Name               | Type        | Description | Required |
| ------------------ | ----------- | ----------- | -------- |
| pcate_id           | integer     |             | Yes      |
| name               | string      |             | Yes      |
| description        | string      |             | No       |
| price              | number      |             | Yes      |
| discount           | number      |             | Yes      |
| quantity           | integer     |             | Yes      |
| is_extension       | boolean     |             | Yes      |
| duplicate_able     | boolean     |             | Yes      |
| extension_position | [ integer ] |             | No       |
| create_dt          | dateTime    |             | No       |
| modified_dt        | dateTime    |             | No       |

#### UserInfo

| Name       | Type    | Description                                         | Required |
| ---------- | ------- | --------------------------------------------------- | -------- |
| user_id    | integer |                                                     | No       |
| email      | string  | User email.                                         | No       |
| first_name | string  |                                                     | No       |
| last_name  | string  |                                                     | No       |
| role       | boolean | If not defined role will be user(false) by default. | No       |

#### UserInfoPwd

| Name       | Type    | Description                                         | Required |
| ---------- | ------- | --------------------------------------------------- | -------- |
| user_id    | integer |                                                     | No       |
| email      | string  | User email.                                         | No       |
| first_name | string  |                                                     | No       |
| last_name  | string  |                                                     | No       |
| role       | boolean | If not defined role will be user(false) by default. | No       |
| password   | string  | User password.                                      | No       |

#### UserRegis

| Name       | Type    | Description                                         | Required |
| ---------- | ------- | --------------------------------------------------- | -------- |
| email      | string  | User email.                                         | Yes      |
| password   | string  | User password.                                      | Yes      |
| first_name | string  |                                                     | Yes      |
| last_name  | string  |                                                     | Yes      |
| role       | boolean | If not defined role will be user(false) by default. | No       |

#### UserSignin

| Name     | Type   | Description    | Required |
| -------- | ------ | -------------- | -------- |
| email    | string | User email.    | Yes      |
| password | string | User password. | Yes      |

#### ValidationError

| Name | Type       | Description | Required |
| ---- | ---------- | ----------- | -------- |
| loc  | [ string ] |             | Yes      |
| msg  | string     |             | Yes      |
| type | string     |             | Yes      |

