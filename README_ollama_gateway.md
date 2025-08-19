# Ollama Gateway with Bearer Token Authentication

This setup adds a FastAPI-based gateway in front of the Ollama service, requiring a Bearer token for all requests.

## Usage

1. **Build and Start Services**

From the `gemma3` directory, run:

```bash
docker compose up --build
```

2. **Access the Secured Endpoint**

Send requests to the gateway at `http://localhost:8080` instead of directly to Ollama.

All requests must include an `Authorization` header:

```
Authorization: Bearer your_secret_token_here
```

Replace `your_secret_token_here` with the value set in `docker-compose.yml` under `BEARER_TOKEN`.

3. **Example cURL Request**

```bash
curl -H "Authorization: Bearer your_secret_token_here" \
     -X POST http://localhost:8080/v1/chat/completions \
     -d '{
    "model": "gemma3:270m",
    "messages": [
      {
        "role": "user",
        "content": [
          {"type": "text", "text": "Hello, how are you?"}
        ]
      }
    ]
}'
```

4. **Change the Bearer Token**

Edit the `BEARER_TOKEN` value in `docker-compose.yml` under the `ollama-gateway` service. Restart the services for changes to take effect.

---

**Note:**

- The Ollama backend is only accessible via the gateway, not directly from outside the Docker network.
- The gateway proxies all HTTP methods and paths to the Ollama backend, enforcing authentication on every request.
