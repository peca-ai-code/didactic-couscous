#!/bin/bash

# Start the Django backend
echo "Starting Django backend on port 9000..."
cd backend
source venv/bin/activate
python manage.py runserver 9000 &
BACKEND_PID=$!
deactivate
cd ..

# Wait a moment for the backend to start
sleep 3

# Start the Chainlit frontend
echo "Starting Chainlit frontend on port 8000..."
cd chainlit_app
source venv/bin/activate
chainlit run app.py --port 8001 &
FRONTEND_PID=$!
deactivate
cd ..

# Handle SIGINT (Ctrl+C) to gracefully shut down both servers
trap 'echo "Shutting down servers..."; kill $BACKEND_PID; kill $FRONTEND_PID; exit' SIGINT

echo "Both servers are running:"
echo "- Backend: http://localhost:9000/admin"
echo "- Frontend: http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop."
wait
