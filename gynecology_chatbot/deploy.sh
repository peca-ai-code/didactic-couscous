#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Starting GCP Deployment...${NC}"

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}❌ gcloud CLI is not installed. Please install it first.${NC}"
    exit 1
fi

# Check if user is logged in
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo -e "${YELLOW}⚠️  Please login to gcloud first${NC}"
    gcloud auth login
fi

# Set project (replace with your project ID)
read -p "Enter your Google Cloud Project ID: " PROJECT_ID
gcloud config set project $PROJECT_ID

# Enable required APIs
echo -e "${YELLOW}📦 Enabling required APIs...${NC}"
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable firestore.googleapis.com

# Deploy Backend
echo -e "${YELLOW}🔧 Deploying Backend to Cloud Run...${NC}"
cd backend

# Submit build to Cloud Build
gcloud builds submit --config cloudbuild.yaml

# Get the backend URL
BACKEND_URL=$(gcloud run services describe gynecology-backend --region=us-central1 --format="value(status.url)")
echo -e "${GREEN}✅ Backend deployed at: $BACKEND_URL${NC}"

# Deploy Frontend
echo -e "${YELLOW}🎨 Deploying Frontend to Cloud Run...${NC}"
cd ../chainlit_app

# Set environment variables for frontend
gcloud run deploy gynecology-frontend \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars="DJANGO_API_URL=$BACKEND_URL/api" \
  --set-env-vars="GEMINI_API_KEY=$GEMINI_API_KEY" \
  --set-env-vars="APPOINTMENTS_URL=$BACKEND_URL/appointments/"

# Get the frontend URL
FRONTEND_URL=$(gcloud run services describe gynecology-frontend --region=us-central1 --format="value(status.url)")
echo -e "${GREEN}✅ Frontend deployed at: $FRONTEND_URL${NC}"

# Update backend CORS settings
echo -e "${YELLOW}🔄 Updating backend CORS settings...${NC}"
cd ../backend
gcloud run services update gynecology-backend \
  --region us-central1 \
  --set-env-vars="CHAINLIT_URL=$FRONTEND_URL"

# Deploy Firebase (optional)
echo -e "${YELLOW}🔥 Setting up Firebase...${NC}"
cd ..
if command -v firebase &> /dev/null; then
    firebase deploy --only firestore:rules,firestore:indexes
    echo -e "${GREEN}✅ Firebase configured${NC}"
else
    echo -e "${YELLOW}⚠️  Firebase CLI not installed. Skipping Firebase deployment.${NC}"
fi

echo -e "${GREEN}🎉 Deployment Complete!${NC}"
echo -e "${GREEN}📱 Frontend URL: $FRONTEND_URL${NC}"
echo -e "${GREEN}🔧 Backend URL: $BACKEND_URL${NC}"
echo -e "${GREEN}🩺 Appointments: $BACKEND_URL/appointments/${NC}"
echo ""
echo -e "${YELLOW}📝 Next Steps:${NC}"
echo "1. Update your .env files with the new URLs"
echo "2. Create a guest user: python3 backend/create_guest_user.py"
echo "3. Update DJANGO_API_TOKEN in frontend environment"
echo "4. Test your deployment!"
