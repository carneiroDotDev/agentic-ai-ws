# Part 9: Deploying Agents to Cloud Run ☁️

Learn how to deploy your ADK agents to Google Cloud Run for production-ready, scalable AI applications.

## Prerequisites

- Google Cloud account with billing enabled
- [Google Cloud SDK (gcloud CLI)](https://cloud.google.com/sdk/docs/install) installed
- Docker (for local testing before deployment)
- A Google API Key for Gemini

## Why Cloud Run?

**Cloud Run** is perfect for deploying ADK agents because:
- ✅ **Serverless** - Pay only for what you use
- ✅ **Auto-scaling** - Handles traffic spikes automatically
- ✅ **Container-based** - Use the Dockerfiles already in this repo
- ✅ **Fully managed** - No infrastructure to maintain
- ✅ **Global** - Deploy to regions worldwide

## Dockerfiles Provided

All workshop parts (P1-P8) include production-ready Dockerfiles:
- `P1-ToolCalling/Dockerfile`
- `P2-CustomTools/Dockerfile`
- `P3-AgentTeams/Dockerfile`
- `P4-Memory/Dockerfile`
- `P5-RouterAgent/Dockerfile`
- `P6-SequentialAgents/Dockerfile`
- `P7-LoopAgents/Dockerfile`
- `P8-ParallelAgents/Dockerfile`

Each Dockerfile:
- Uses Python 3.13 slim base
- Installs dependencies via `uv`
- Exposes port 8000 for ADK web interface
- Runs `adk web --port 8000 --host 0.0.0.0`

## Official Tutorials

Follow these comprehensive Google tutorials for step-by-step deployment:

### Tutorial 1: Deploy to Cloud Run (Basic)
**Link:** [goo.gle/aaiwcr-1](https://goo.gle/aaiwcr-1)

Covers:
- Setting up Cloud Run
- Building and pushing container images
- Deploying your first agent
- Setting environment variables

### Tutorial 2: Deploy to Cloud Run (Advanced)
**Link:** [goo.gle/aaiwcr-2](https://goo.gle/aaiwcr-2)

Covers:
- CI/CD integration
- Custom domains
- Authentication
- Monitoring and logging

## Quick Start: Deploy Any Workshop Part

Here's a general workflow to deploy any part from this workshop:

### 1. Set Up Google Cloud Project

```bash
# Set your project ID
export PROJECT_ID="your-project-id"
gcloud config set project $PROJECT_ID

# Enable required APIs
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

### 2. Choose Your Agent

Navigate to the part you want to deploy:

```bash
cd P1-ToolCalling  # Or any other part (P2, P3, P4, etc.)
```

### 3. Build and Push Container

```bash
# Set your image name
export IMAGE_NAME="gcr.io/$PROJECT_ID/day-trip-agent"

# Build and push to Google Container Registry
gcloud builds submit --tag $IMAGE_NAME
```

### 4. Deploy to Cloud Run

```bash
# Deploy with your API key as environment variable
gcloud run deploy day-trip-agent \
  --image $IMAGE_NAME \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_API_KEY="your-gemini-api-key"
```

### 5. Access Your Deployed Agent

After deployment, Cloud Run will provide a URL like:
```
https://day-trip-agent-xxxxx-uc.a.run.app
```

Visit this URL to access the ADK web interface for your agent!

## Deployment Tips

### Security Best Practices

**Don't hardcode API keys!** Use Secret Manager:

```bash
# Store API key in Secret Manager
echo -n "your-api-key" | gcloud secrets create GOOGLE_API_KEY --data-file=-

# Deploy with secret
gcloud run deploy your-agent \
  --image $IMAGE_NAME \
  --region us-central1 \
  --set-secrets GOOGLE_API_KEY=GOOGLE_API_KEY:latest
```

### Cost Optimization

Configure Cloud Run resources based on your needs:

```bash
gcloud run deploy your-agent \
  --image $IMAGE_NAME \
  --region us-central1 \
  --memory 512Mi \
  --cpu 1 \
  --min-instances 0 \
  --max-instances 10 \
  --concurrency 80
```

- `--min-instances 0`: Scale to zero when not in use (save costs)
- `--max-instances 10`: Limit concurrent instances
- `--concurrency 80`: Requests per container

### Custom Domains

Map your own domain:

```bash
gcloud run domain-mappings create \
  --service your-agent \
  --domain agent.yourdomain.com \
  --region us-central1
```

### Monitoring

View logs:

```bash
gcloud run services logs read your-agent --region us-central1
```

Monitor in Cloud Console:
- Navigate to Cloud Run → Your Service
- Click "Logs" tab
- View metrics, errors, and request traces

## Example: Deploy Router Agent (P5)

Complete example for the Router Agent:

```bash
# Navigate to P5
cd P5-RouterAgent

# Set variables
export PROJECT_ID="my-agentic-ai-project"
export IMAGE_NAME="gcr.io/$PROJECT_ID/router-agent"
export GOOGLE_API_KEY="your-api-key"

# Build
gcloud builds submit --tag $IMAGE_NAME

# Deploy
gcloud run deploy router-agent \
  --image $IMAGE_NAME \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_API_KEY=$GOOGLE_API_KEY \
  --memory 1Gi \
  --cpu 2

# Get URL
gcloud run services describe router-agent \
  --region us-central1 \
  --format 'value(status.url)'
```

## Which Part Should You Deploy?

Choose based on your use case:

- **P1 (Tool Calling)**: Simple day-trip planner with web search
- **P2 (Custom Tools)**: Weather-aware planner with external API
- **P3 (Agent Teams)**: Multi-agent delegation system
- **P4 (Memory)**: Conversational agent with session memory
- **P5 (Router)**: Intelligent request router with specialists
- **P6 (Sequential)**: Multi-step workflow agent
- **P7 (Loop)**: Iterative planning with refinement
- **P8 (Parallel)**: High-speed concurrent execution

## CI/CD Integration

For production deployments, set up automated deployments:

### GitHub Actions Example

```yaml
name: Deploy to Cloud Run

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - uses: google-github-actions/setup-gcloud@v0
        with:
          service_account_key: ${{ secrets.GCP_SA_KEY }}
          
      - name: Build and Push
        run: |
          gcloud builds submit --tag gcr.io/$PROJECT_ID/agent
          
      - name: Deploy
        run: |
          gcloud run deploy agent \
            --image gcr.io/$PROJECT_ID/agent \
            --region us-central1
```

## Troubleshooting

### Common Issues

**Port Mismatch:**
- Ensure Dockerfile exposes port 8000
- ADK web runs on `--port 8000 --host 0.0.0.0`

**API Key Not Working:**
```bash
# Check environment variable is set
gcloud run services describe your-agent --format export
```

**Container Fails to Start:**
```bash
# View detailed logs
gcloud run services logs read your-agent --limit 50
```

**Memory Issues:**
```bash
# Increase memory allocation
gcloud run services update your-agent --memory 2Gi
```

## Next Steps

1. **Follow Official Tutorials**: [goo.gle/aaiwcr-1](https://goo.gle/aaiwcr-1) and [goo.gle/aaiwcr-2](https://goo.gle/aaiwcr-2)
2. **Test Locally First**: Run Docker container before deploying
3. **Start Simple**: Deploy P1 first, then advance to complex agents
4. **Monitor Costs**: Use Cloud Run pricing calculator
5. **Secure Production**: Use Secret Manager for API keys

## Resources

- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [ADK Documentation](https://google.github.io/adk-docs/)
- [Cloud Run Pricing](https://cloud.google.com/run/pricing)
- [Best Practices for Cloud Run](https://cloud.google.com/run/docs/best-practices)

## Workshop Complete! 🎉

You've learned to build, test, and deploy production-ready AI agents:
- ✅ Basic agents with tools (P1)
- ✅ Custom tools and APIs (P2)
- ✅ Multi-agent systems (P3)
- ✅ Memory and sessions (P4)
- ✅ Router patterns (P5)
- ✅ Sequential workflows (P6)
- ✅ Iterative refinement (P7)
- ✅ Parallel execution (P8)
- ✅ Cloud deployment (P9)

**Now go build amazing AI agents!** 🚀

