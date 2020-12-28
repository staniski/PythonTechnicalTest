# Origin Markets Backend Test

### Spec:

We would like you to implement an api to: ingest some data representing bonds, query an external api for some additional data, store the result, and make the resulting data queryable via api.
- Fork this hello world repo leveraging Django & Django Rest Framework. (If you wish to use something else like flask that's fine too.)
- Please pick and use a form of authentication, so that each user will only see their own data. ([DRF Auth Options](https://www.django-rest-framework.org/api-guide/authentication/#api-reference))
- We are missing some data! Each bond will have a `lei` field (Legal Entity Identifier). Please use the [GLEIF API](https://www.gleif.org/en/lei-data/gleif-lei-look-up-api/access-the-api) to find the corresponding `Legal Name` of the entity which issued the bond.
- If you are using a database, SQLite is sufficient.
- Please test any additional logic you add.

#### Project Quickstart

Inside a virtual environment running Python 3:
- `pip install -r requirement.txt`
- `./manage.py runserver` to run server.
- `./manage.py test` to run tests.

#### API

We should be able to send a request to:

`POST /bonds/`

to create a "bond" with data that looks like:
~~~
{
    "isin": "FR0000131104",
    "size": 100000000,
    "currency": "EUR",
    "maturity": "2025-02-28",
    "lei": "R0MUWSFPU8MPRO8K5P83"
}
~~~
---
We should be able to send a request to:

`GET /bonds/`

to see something like:
~~~
[
    {
        "isin": "FR0000131104",
        "size": 100000000,
        "currency": "EUR",
        "maturity": "2025-02-28",
        "lei": "R0MUWSFPU8MPRO8K5P83",
        "legal_name": "BNPPARIBAS"
    },
    ...
]
~~~
We would also like to be able to add a filter such as:
`GET /bonds/?legal_name=BNPPARIBAS`

to reduce down the results.


#### Implementation

Creation and get methods for users and bonds are written using generic clas-based views.
Token Authentication is enabled. Each user gets a token after creation of a user instance.
-To register send request to:
    `POST /register/`
with username and password as data.

-To filter throw individual legal_name do a GET request to /bonds/?legal_name=<quary>
-To add a bond:
    `POST /bonds/`

with data like this:
~~~
{
    "isin": "FR0000131104",
    "size": 100000000,
    "currency": "EUR",
    "maturity": "2025-02-28",
    "lei": "R0MUWSFPU8MPRO8K5P83",
    "legal_name: "anything"

}
~~~
"legal_name" will be fetched with GLEIF API and replaced if provided lei is correct, otherwise it will return legal_name:"Unknown".

-To connect:
`curl --header "Content-Type: application/json" --request POST --data '{"username": "user", "password": "password"}' http://127.0.0.1:8000/api-token-auth/`
`>>>{"token":"<>USER TOKEN"}`
`curl --header "Authorization: Token <USER TOKEN>" --request GET http://127.0.0.1:8000/bonds/`
`>>>[]`
~~~
curl --header "Authorization: Token <USER TOKEN>" -H  "Content-Type: application/json" --request POST --data '{"isin": "FR0000131104","size": 1000000,"currency": "USD",
"maturity": "2025-09-25","lei": "R0MUWSFPU8MPRO8K5P83","legal_name": "X"}' http://127.0.0.1:8000/bonds/
~~~
`>>>{"isin":"FR0000131104","size":1000000,"currency":"USD","maturity":"2025-09-25","lei":"R0MUWSFPU8MPRO8K5P83","legal_name":"BNPPARIBAS","owner":"user"}`



