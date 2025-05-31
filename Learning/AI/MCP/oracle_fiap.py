from contextlib import asynccontextmanager
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, Any, Optional
import httpx

OPENAPI_URL = "https://g12bbd4aea16cc4-orcl1.adb.ca-toronto-1.oraclecloudapps.com/ords/fiap/metadata-catalog/"

async def fetch_openapi_spec():
    async with httpx.AsyncClient() as client:
        response = await client.get(OPENAPI_URL)
        response.raise_for_status()
        return response.json()

def generate_tools_from_openapi(openapi: dict[str, any]):
    paths = openapi.get("paths", {})
    for path, methods in paths.items():
        if not isinstance(methods, dict):
            continue
        for method, details in methods.items():
            if not isinstance(details, dict):
                continue
            operation_id = details.get("operationId")
            if not operation_id:
                continue
            operation_id = f"{method}"