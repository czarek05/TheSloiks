# TheSloiks

Manage budget with TheSloiks.

## Install the app with Docker on Linux (tested on Ubuntu 18.04)
sudo is required. cd to the directory containing script `provision_first.sh`. Run script `provision_first.sh`. When the script is finished and the app is running, open new terminal, cd to the directory containing script `provision_second.sh` and run script `provision_second.sh`. Check if tests passed. The app should be available at http://0.0.0.0:8000/thesloiks/


If the app was already installed and is turned off, it can be started with:

sudo docker-compose up

## API

### GET /thesloiks/jar

Get list of all jars.

### GET /thesloiks/jar/1

Get jar with id 1.

### POST /thesloiks/jar/

Post new jar. It is required to send JSON body with exactly one field: currency. Possible values: PLN, USD, EUR.

### GET /thesloiks/transaction

Get all transactions.

### GET /thesloiks/transaction/?sortBy=value&sortOrder=asc&jarsIds=11,77

Get all transactions where the source jar is equal 11 or 77, or the target jar is equal 11 or 77 sorted by value ascending. Proper values for sortBy: date_created, value, type, title, currency. Proper values for sortOrder: asc, desc. Proper values for jarsIds - comma separated numbers.

### POST /thesloiks/transaction/

Post new transaction. It is required to send JSON body. The request must contain fields: value (non-zero, positive number, two decimal places, less than all money in the world in PLN) and currency (PLN, USD, EUR). The request must contain at least one from fields: targetJar, sourceJar (integers, ids of jars). The request also may contain field title (text, up to 250 chars). The request must not contain other fields. If sourceJar and targetJar are provided, it means that it is a transfer. If only sourceJar is provided, it means that it is a withdraw. If only targetJar is provided, it means that it is deposit.

## More examples

### POST /thesloiks/transaction/

JSON: {"targetJar": 1, "value": 100, "currency": "PLN"}

Deposit 100 PLN in jar with id 1 (the jar must exists and has currency equal to request currency).

### POST /thesloiks/transaction/

JSON: {"sourceJar": 1, "value": 100, "currency": "PLN"}

Withdraw 100 PLN from jar with id 1 (the jar must exists, has currency equal to request currency, has balance not less than 100).

### POST /thesloiks/transaction/

JSON: {"sourceJar": 2, "targetJar": 1, "value": 100, "currency": "PLN"}

Transfer 100 PLN from jar with id 2 to jar with id 1 (boths jars must exist, have currency equal to request currency, the source jar must have balance not less than 100).

### GET /thesloiks/transaction/?jarsIds=1

Check transactions history for jar (with id = 1).
