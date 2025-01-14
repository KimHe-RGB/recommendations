

# NYU DevOps: Recommendation

[![Build Status](https://github.com/CSCI-GA-2820-FA23-001/recommendations/actions/workflows/tdd-tests.yml/badge.svg)](https://github.com/CSCI-GA-2820-FA23-001/recommendations/actions)
[![Build Status](https://github.com/CSCI-GA-2820-FA23-001/recommendations/actions/workflows/bdd-tests.yml/badge.svg)](https://github.com/CSCI-GA-2820-FA23-001/recommendations/actions)
[![codecov](https://codecov.io/gh/CSCI-GA-2820-FA23-001/recommendations/branch/master/graph/badge.svg?token=X2VCL7ZZGQ)](https://codecov.io/gh/CSCI-GA-2820-FA23-001/recommendations)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://python.org/)

Database, API and scripts for product recommendation

## Overview

This project facilitates the recommendation function of an online shopping website.

Goals to implement:

* Get a list recommended products related a requested product by customers.
* Get recommendations based on user preference
* Regularly update recommendation, based on product validity, sponsorship from seller, price changes, etc.
* Create / Delete recommendation
  
foo

## Contents

### Tables

#### Recommendation

| Key | Type | Description |
| -------- | -------- | -------- |
| id | Key | Primary |
| source_item_id | Key | Foreign from Items |
| target_item_id | Key | Foreign from Items |
| recommendation_type | ENUM("up-sell", "cross-sell", "accessory") | type of recommendation |
| recommendation_weight | DECIMAL(0, 1) | priority of the rec to be shown |
| status | ENUM ("valid", "out of stock", "deprecated") | whether the rec is valid |
| created_at | TIMESTAMP | Create time |
| updated_at | TIMESTAMP | Update time |

<!-- #### Items

| Key | Type | Description |
| -------- | -------- | -------- |
| id | Key | Primary |
| category_id | Key | Foreign from Categories |
| name | VARCHAR | Name of the item |
| price | FLOAT | Price of the item |
| in_stock | BOOLEAN | Whether in stock |
| created_at | TIMESTAMP | Create time |
| updated_at | TIMESTAMP | Update time | -->

<!-- #### Categories

| Key | Type | Description |
| -------- | -------- | -------- |
| id | Key | Primary |
| name | VARCHAR | Name of the category | -->

### API List

| URL | HTTP Method | Description
| -------- | -------- | -------- |
| [/](#get-/) | GET | API version information |
| [/recommendations?](#get-/recommendations?) | GET | List recommendation by page |
| [/recommendations/{int:id}](#get-/recommendations/{id}) | GET | Read recommendation by id |
| [/recommendations/source_product?](#get-/recommendations/source_product?) | GET | Read recommendation by source_product_id |
| [/recommendations](#post-/recommendations) | POST | Create recommendation |
| [/recommendations/{int:id}](#put-/recommendations/{id}) | PUT | Update recommendation |
| [/recommendations/{int:id}](#delete-/recommendations/{id}) | DELETE | Delete recommendation |


### File Structure

```text
.gitignore          - this will ignore vagrant and other metadata files
.flaskenv           - Environment variables to configure Flask
.gitattributes      - File to gix Windows CRLF issues
.devcontainers/     - Folder with support for VSCode Remote Containers
dot-env-example     - copy to .env to use environment variables
requirements.txt    - list if Python libraries required by your code
config.py           - configuration parameters

service/                   - service python package
├── __init__.py            - package initializer
├── models.py              - module with business models
├── routes.py              - module with service routes
└── common                 - common code package
    ├── error_handlers.py  - HTTP error handling code
    ├── log_handlers.py    - logging setup code
    └── status.py          - HTTP status constants

tests/              - test cases package
├── __init__.py     - package initializer
├── test_models.py  - test suite for business models
└── test_routes.py  - test suite for service routes
```

### API Documentation

#### GET /

Retrieve API information

#### GET /recommendations?

List all recommendations with pagination, optional filter by recommendation_type

```http
GET /recommendations?page-index=1&page-size=10&type=UP_SELL
```

Status Code | Note
--- | ---
200 | OK

#### GET /recommendations/{id}

Read recommendation by id

```http
GET /recommendations/123
```

Status Code | Note
--- | ---
200 | OK
404 | Not found

#### GET /recommendations/source_product?

Read recommendation by source_product_id/status

```http
GET /recommendations/source_product?source_product_id=123
GET /recommendations/source_product?status=valid
```

Status Code | Note
--- | ---
200 | OK
404 | Not found

#### POST /recommendations

Create a new recommendation:

```http
POST /recommendations
Content-Type: application/json

{
  "source_item_id" : 123,
  "target_item_id" : 456,
  "recommendation_type" : "UNKNOWN",
  "recommendation_weight" : 0.8,
  "status" : "UNKNOWN"
}
```

Response:

```http
{
  "created_at": "2023-10-17T02:59:59.536538",
  "id": 625,
  "recommendation_type": "UNKNOWN",
  "recommendation_weight": 0.8,
  "source_item_id": 123,
  "status": "UNKNOWN",
  "target_item_id": 456,
  "updated_at": "2023-10-17T02:59:59.536542"
}
```

Status Code | Note
--- | ---
201 | Created
415 | content_type must be application/json

#### PUT /recommendations/{id}

Update a new recommendation

```http
PUT /recommendations/625
Content-Type: application/json

{
  "source_item_id": 88888
  "recommendation_weight" : 0.9,
  "status" : "VALID"
}
```

Response:

```http
{
  "created_at": "2023-10-17T02:59:59.536538",
  "id": 625,
  "recommendation_type": "UNKNOWN",
  "recommendation_weight": 0.9,
  "source_item_id": 88888,
  "status": "VALID",
  "target_item_id": 456,
  "updated_at": "2023-10-17T03:00:32.831226"
}
```

Status Code | Note
--- | ---
200 | OK
415 | content_type must be application/json
404 | Not found

#### DELETE /recommendations/{id}

Delete recommendation by id

```http
DELETE /recommendations/123
```

Status Code | Note
--- | ---
204 | Success
404 | Not found

bla

## License

Copyright (c) John Rofrano. All rights reserved.

Licensed under the Apache License. See [LICENSE](LICENSE)

This repository is part of the NYU masters class: **CSCI-GA.2820-001 DevOps and Agile Methodologies** created and taught by *John Rofrano*, Adjunct Instructor, NYU Courant Institute, Graduate Division, Computer Science, and NYU Stern School of Business.
