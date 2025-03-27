db.createUser({
    user: "dbuser",
    pwd: "dbpasswd",
    roles: [{
        role: "readWrite",
        db: "group8_db"
    }]
});