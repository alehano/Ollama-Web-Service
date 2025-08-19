import os
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import Response
import httpx

app = FastAPI()
OLLAMA_URL = "http://ollama:11434"
BEARER_TOKEN = os.environ.get("BEARER_TOKEN", "your_secret_token_here")

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy(request: Request, path: str):
    auth = request.headers.get("authorization")
    if not auth or auth != f"Bearer {BEARER_TOKEN}":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing token")

    async with httpx.AsyncClient(timeout=None) as client:
        url = f"{OLLAMA_URL}/{path}"
        method = request.method
        body = await request.body()
        headers = dict(request.headers)
        headers.pop("host", None)
        # Remove authorization header before proxying
        headers.pop("authorization", None)
        try:
            resp = await client.request(method, url, content=body, headers=headers, params=dict(request.query_params))
        except httpx.TimeoutException:
            raise HTTPException(status_code=504, detail="Upstream service timeout (Ollama)")
        except httpx.RequestError as exc:
            raise HTTPException(status_code=502, detail=f"Upstream service error: {exc}")
        return Response(content=resp.content, status_code=resp.status_code, headers=dict(resp.headers))
