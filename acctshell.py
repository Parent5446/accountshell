#!/bin/python

import app.bootstrap
config = app.models.Config()
database = app.models.Database(config)
request = app.models.Request(config, database)
controller = app.controllers.AccountShell(config, database, request)
