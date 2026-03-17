#!/bin/bash

sleep 10

mongosh <<EOF
rs.initiate({
  _id: "dbrs",
  members: [
    { _id: 0, host: "mongodb-primary:27017", priority: 3 },
    { _id: 1, host: "mongodb-secondary:27017", priority: 2 },
    { _id: 2, host: "mongodb-arbiter:27017", arbiterOnly: true }
  ]
})

rs.status()
EOF