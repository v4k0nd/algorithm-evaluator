#!/bin/sh

pip install fastapi jinja2 "uvicorn[standard]"
cd backend
uvicorn main:app --reload --host 0.0.0.0
