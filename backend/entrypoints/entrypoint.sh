#!/bin/sh

alembic upgrade head

uvicorn proshield.main:app --reload --workers 1 --host 0.0.0.0 --port 8000