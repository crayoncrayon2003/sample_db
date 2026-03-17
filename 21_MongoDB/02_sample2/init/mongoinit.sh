#!/bin/bash

mongo <<EOF
var config = {
    "_id": "dbrs",
    "version": 1,
    "members": [
        {
            "_id": 1,
            "host": "mongodb-primary:27017",
            "priority": 3
        },
        {
            "_id": 2,
            "host": "mongodb-secondary:27018",
            "priority": 2
        },
        {
            "_id": 3,
            "host": "mongodb-arbiter:27019",
            "arbiterOnly": true
        }
    ]
};
rs.initiate(config);
rs.status();
EOF