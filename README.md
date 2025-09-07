
### Using Python directly

1. Install the requirements:
   ```
   pip install -r requirements.txt
   ```

2. Start the application:
   ```
   uvicorn main:app --reload
   ```

3. Access the application:
   ```
   # Public endpoint (no authentication)
   http://127.0.0.1:8000/
   
   # Protected endpoint (requires API key)
   # Set the API key first:
   $env:API_KEY="your-secure-api-key"  # For PowerShell
   
   # Then access with API key header:
   curl -H "X-API-Key: your-secure-api-key" http://127.0.0.1:8000/hello
   # Or with PowerShell:
   Invoke-RestMethod -Uri "http://127.0.0.1:8000/hello" -Headers @{"X-API-Key" = "your-secure-api-key"}
   ```

### Using Docker

1. Build the Docker image:
   ```
   docker build --tag fastapi-demo .
   ```

2. Run the Docker container:
   ```
   docker run --detach --publish 8000:8000 fastapi-demo
   ```

3. Access the application:
   ```
   # Public endpoint (no authentication)
   http://localhost:8000/
   
   # Protected endpoint (requires API key)
   # Run the container with an API key:
   docker run --detach --publish 8000:8000 -e "API_KEY=your-secure-api-key" fastapi-demo
   
   # Then access with API key header:
   curl -H "X-API-Key: your-secure-api-key" http://localhost:8000/hello
   # Or with PowerShell:
   Invoke-RestMethod -Uri "http://localhost:8000/hello" -Headers @{"X-API-Key" = "your-secure-api-key"}
   ```

## Deploy to Azure Container Apps

You can deploy the application to Azure Container Apps using the Azure CLI:

### Deployment with API Key Authentication (Recommended)

For secure deployment with API key authentication from the start:

```
az containerapp up \
  --resource-group your-resource-group --name web-aca-app \
  --ingress external --target-port 8000 --source . \
  --env-vars "API_KEY=your-secure-api-key-value"
```

Replace `your-secure-api-key-value` with a strong, randomly generated key.

### Understanding Container Apps Environment

When you deploy an Azure Container App, a **Container Apps Environment** is automatically created (or an existing one is used if specified). This environment is a secure boundary around a group of container apps that:

- Provides a shared virtual network for your container apps
- Enables secure internal communications between container apps in the same environment
- Controls ingress from external sources
- Manages common settings like logging configuration
- Provides a fully managed Kubernetes-like platform without requiring Kubernetes expertise

The environment acts as a logical boundary for your container apps and provides the infrastructure needed to run them securely and efficiently.

### Finding Your Application URL

The URL for the deployed app is in the output of the `az containerapp up` command. Open the URL in your browser to see the web app running in Azure. The form of the URL will look like the following: `https://web-aca-app.<generated-text>.<location-info>.azurecontainerapps.io`, where the `<generated-text>` and `<location-info>` are unique to your deployment.

## About startup.sh

The `startup.sh` file is useful for certain Azure deployment scenarios:

- **Azure App Service**: When deploying to Azure App Service (without containers), the platform can use this script to start your application.
- **Custom startup commands**: It allows you to specify how your application should start in environments that support custom startup scripts.
- **Environment-specific configuration**: You could modify the script to include environment variables or other startup configurations.

While Docker deployments use the Dockerfile's CMD instruction instead, keeping `startup.sh` provides flexibility for non-containerized deployments.

## API Key Authentication

This application is secured with API key authentication. To access the protected endpoint `/hello`, you need to include an API key in your requests.

### Setting Up the API Key

The API key is read from an environment variable called `API_KEY`. If not set, it will use a default development key (not secure for production).

#### Setting API Key Locally
```
# Windows PowerShell
$env:API_KEY="your-secure-api-key"

# Linux/Mac
export API_KEY="your-secure-api-key"
```

#### Setting API Key in Azure Container Apps

If you've already deployed your app without an API key, update it with:
```
az containerapp update --name web-aca-app --resource-group web-fastapi-aca-rg --set-env-vars "API_KEY=your-secure-api-key"
```

For new deployments, include the API key during initial deployment as shown in the [Deployment with API Key Authentication](#deployment-with-api-key-authentication-recommended) section above.

### Making Authenticated Requests

When calling the API, include the API key in the `X-API-Key` header:

```bash
curl -H "X-API-Key: your-secure-api-key" https://your-app-url/hello
```

Or with PowerShell:
```powershell
Invoke-RestMethod -Uri "https://your-app-url/hello" -Headers @{"X-API-Key" = "your-secure-api-key"}
```

Example with your deployed app URL:
```powershell
Invoke-RestMethod -Uri "https://web-aca-app.<generated-text>.<location-info>.azurecontainerapps.io/hello" -Headers @{"X-API-Key" = "your-secure-api-key"}
```

### Testing Authentication
- The root URL `/` is public and requires no authentication
- The `/hello` endpoint requires a valid API key

## Next Steps

To learn more about FastAPI, see [FastAPI](https://fastapi.tiangolo.com/).
