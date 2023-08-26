#!/bin/sh
exec uvicorn timekeeper_server.main:app --reload