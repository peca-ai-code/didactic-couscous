#!/bin/bash

PROJECT_ID="linen-hook-461007-c8"
REGION="us-central1"

echo "🚀 Deploying Backend..."
cd backend

# Deploy backend directly from source
gcloud run deploy gynecology-backend \
  --source . \
  --region $REGION \
  --allow-unauthenticated \
  --set-env-vars="DJANGO_SETTINGS_MODULE=gynecology_chatbot_project.settings_production" \
  --timeout=3600 \
  --memory=2Gi \
  --cpu=2

# Get backend URL
BACKEND_URL=$(gcloud run services describe gynecology-backend --region=$REGION --format="value(status.url)")
echo "✅ Backend deployed at: $BACKEND_URL"

echo "🚀 Deploying Frontend..."
cd ../chainlit_app

# Deploy frontend directly from source
gcloud run deploy gynecology-frontend \
  --source . \
  --region $REGION \
  --allow-unauthenticated \
  --set-env-vars="DJANGO_API_URL=$BACKEND_URL/api" \
  --set-env-vars="APPOINTMENTS_URL=$BACKEND_URL/appointments/" \
  --timeout=3600 \
  --memory=2Gi \
  --cpu=2

# Get frontend URL
FRONTEND_URL=$(gcloud run services describe gynecology-frontend --region=$REGION --format="value(status.url)")
echo "✅ Frontend deployed at: $FRONTEND_URL"

# Update backend CORS settings
echo "🔄 Updating backend CORS settings..."
cd ../backend
gcloud run services update gynecology-backend \
  --region $REGION \
  --set-env-vars="CHAINLIT_URL=$FRONTEND_URL"

echo "🎉 Deployment Complete!"
echo "📱 Frontend URL: $FRONTEND_URL"
echo "🔧 Backend URL: $BACKEND_URL"
echo "🩺 Appointments: $BACKEND_URL/appointments/"

cd ..
