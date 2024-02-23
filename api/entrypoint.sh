
#!/bin/bash

set -e # Exit on error

if [ "$ENVIRONMENT" = "production" ]; then
  # Run your production entrypoint
  uvicorn app.main:app --proxy-headers --host 0.0.0.0 --port 8080 --workers 2
elif [ "$ENVIRONMENT" = "test" ]; then
  # Run your tests
  pytest -vvv
else
  # Default case or error handling
  uvicorn app.main:app --proxy-headers --host 0.0.0.0 --port 8080 --reload
fi