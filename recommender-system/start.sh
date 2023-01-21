#!/bin/bash
mlflow ui &
uvicorn main:app --host 0.0.0.0 --port 8080 &

# Wait for any process to exit
wait -n
  
# Exit with status of process that exited first
exit $?