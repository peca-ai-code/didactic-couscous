#!/bin/bash

PROJECT_ID="linen-hook-461007-c8"
REGION="us-central1"

echo "🚀 Deploying Backend with Landing Page..."
cd backend

# Deploy backend directly from source
gcloud run deploy gynecology-backend \
  --source . \
  --region $REGION \
  --allow-unauthenticated \
  --set-env-vars="DJANGO_SETTINGS_MODULE=gynecology_chatbot_project.settings_production" \
  --set-env-vars="DJANGO_API_TOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ5MDkzMzgyLCJpYXQiOjE3NDkwMDY5ODIsImp0aSI6ImI5NTY0MmI0MWUzZTQ3ZDFhYjA1ODAwZjMxYzA2NDQ1IiwidXNlcl9pZCI6MX0.AN5CDf-AfUnNRC6gYJ6907kv8tcDtksemwHwl4FWWXg" \
  --set-env-vars="GEMINI_API_KEY=AIzaSyC4z2Quwghmoutzr0KEp5SHFfRo4lVG-sP" \
  --set-env-vars="FRONTEND_URL=https://gynecology-frontend-ffyownlhbq-uc.a.run.app,CHAINLIT_URL=https://gynecology-frontend-ffyownlhbq-uc.a.run.app" \
  --timeout=3600 \
  --memory=2Gi \
  --cpu=2

# Get backend URL
BACKEND_URL=$(gcloud run services describe gynecology-backend --region=$REGION --format="value(status.url)")
echo "✅ Backend deployed at: $BACKEND_URL"

cd ..

echo "🚀 Deploying Frontend..."
cd chainlit_app

# Deploy frontend directly from source
gcloud run deploy gynecology-frontend \
  --source . \
  --region $REGION \
  --allow-unauthenticated \
  --set-env-vars="DJANGO_API_URL=https://gynecology-backend-ffyownlhbq-uc.a.run.app/api" \
  --set-env-vars="APPOINTMENTS_URL=https://gynecology-backend-ffyownlhbq-uc.a.run.app/appointments/" \
  --set-env-vars="GEMINI_API_KEY=AIzaSyC4z2Quwghmoutzr0KEp5SHFfRo4lVG-sP" \
  --set-env-vars="DJANGO_API_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ5MDg3NTc2LCJpYXQiOjE3NDkwMDExNzYsImp0aSI6IjI3MzYwNzI2Zjg1YTRkNGZhMTk4OWJjZjI1ZGVjYjk1IiwidXNlcl9pZCI6MX0.WiGHMKG3C6EkJ5yoeLgnswXn3lyQSHVIW3dhI3ot5SI" \
  --timeout=3600 \
  --memory=2Gi \
  --cpu=2

# Get frontend URL
FRONTEND_URL=$(gcloud run services describe gynecology-frontend --region=$REGION --format="value(status.url)")
echo "✅ Frontend deployed at: $FRONTEND_URL"

echo "🎉 Deployment Complete!"
echo "🏠 Landing Page: $BACKEND_URL"
echo "📱 Chatbot: $FRONTEND_URL"
echo "🩺 Appointments: $BACKEND_URL/appointments/"

cd ..
