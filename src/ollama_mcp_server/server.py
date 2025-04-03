from mcp.server.fastmcp import FastMCP, Context
import httpx
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
import json
import sys
import traceback
import asyncio
from pathlib import Path
import os

# Initialize FastMCP server
mcp = FastMCP("ollama")

# Default Ollama API endpoint
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434")

class OllamaClient:
    def __init__(self, api_url: str = OLLAMA_API_URL):
        self.api_url = api_url.rstrip('/')
        
    async def _make_request(self, method: str, endpoint: str, json_data: Optional[Dict] = None) -> Dict:
        url = f"{self.api_url}/{endpoint}"
        async with httpx.AsyncClient() as client:
            response = await client.request(method, url, json=json_data, timeout=None)
            response.raise_for_status()
            return response.json()

    async def create_model(self, modelfile: str, name: str, ctx: Context) -> str:
        """Create a model from a Modelfile"""
        try:
            await ctx.info(f"Creating model {name} from Modelfile")
            response = await self._make_request("POST", "create", {
                "name": name,
                "modelfile": modelfile
            })
            return f"Model {name} created successfully"
        except Exception as e:
            await ctx.error(f"Error creating model: {str(e)}")
            return f"Error: {str(e)}"

    async def show_model(self, name: str, ctx: Context) -> str:
        """Show information for a model"""
        try:
            await ctx.info(f"Fetching information for model {name}")
            response = await self._make_request("GET", f"show?name={name}")
            return json.dumps(response, indent=2)
        except Exception as e:
            await ctx.error(f"Error showing model info: {str(e)}")
            return f"Error: {str(e)}"

    async def run_model(self, name: str, prompt: str, ctx: Context, **params) -> str:
        """Run a model"""
        try:
            await ctx.info(f"Running model {name}")
            data = {
                "model": name,
                "prompt": prompt,
                **params
            }
            response = await self._make_request("POST", "generate", data)
            return response.get("response", "No response generated")
        except Exception as e:
            await ctx.error(f"Error running model: {str(e)}")
            return f"Error: {str(e)}"

    async def stop_model(self, name: str, ctx: Context) -> str:
        """Stop a running model"""
        try:
            await ctx.info(f"Stopping model {name}")
            response = await self._make_request("POST", f"stop?name={name}")
            return f"Model {name} stopped successfully"
        except Exception as e:
            await ctx.error(f"Error stopping model: {str(e)}")
            return f"Error: {str(e)}"

    async def pull_model(self, name: str, ctx: Context) -> str:
        """Pull a model from a registry"""
        try:
            await ctx.info(f"Pulling model {name}")
            response = await self._make_request("POST", "pull", {"name": name})
            return f"Model {name} pulled successfully"
        except Exception as e:
            await ctx.error(f"Error pulling model: {str(e)}")
            return f"Error: {str(e)}"

    async def push_model(self, name: str, ctx: Context) -> str:
        """Push a model to a registry"""
        try:
            await ctx.info(f"Pushing model {name}")
            response = await self._make_request("POST", "push", {"name": name})
            return f"Model {name} pushed successfully"
        except Exception as e:
            await ctx.error(f"Error pushing model: {str(e)}")
            return f"Error: {str(e)}"

    async def list_models(self, ctx: Context) -> str:
        """List all models"""
        try:
            await ctx.info("Listing models")
            response = await self._make_request("GET", "tags")
            models = response.get("models", [])
            return json.dumps(models, indent=2)
        except Exception as e:
            await ctx.error(f"Error listing models: {str(e)}")
            return f"Error: {str(e)}"

    async def list_running(self, ctx: Context) -> str:
        """List running models"""
        try:
            await ctx.info("Listing running models")
            # Note: This endpoint might need to be adjusted based on Ollama's actual API
            response = await self._make_request("GET", "running")
            return json.dumps(response, indent=2)
        except Exception as e:
            await ctx.error(f"Error listing running models: {str(e)}")
            return f"Error: {str(e)}"

    async def copy_model(self, source: str, destination: str, ctx: Context) -> str:
        """Copy a model"""
        try:
            await ctx.info(f"Copying model from {source} to {destination}")
            response = await self._make_request("POST", "copy", {
                "source": source,
                "destination": destination
            })
            return f"Model copied from {source} to {destination} successfully"
        except Exception as e:
            await ctx.error(f"Error copying model: {str(e)}")
            return f"Error: {str(e)}"

    async def remove_model(self, name: str, ctx: Context) -> str:
        """Remove a model"""
        try:
            await ctx.info(f"Removing model {name}")
            response = await self._make_request("DELETE", f"delete?name={name}")
            return f"Model {name} removed successfully"
        except Exception as e:
            await ctx.error(f"Error removing model: {str(e)}")
            return f"Error: {str(e)}"

# Initialize Ollama client
ollama = OllamaClient()

@mcp.tool()
async def create(modelfile: str, name: str, ctx: Context) -> str:
    """Create a model from a Modelfile"""
    return await ollama.create_model(modelfile, name, ctx)

@mcp.tool()
async def show(name: str, ctx: Context) -> str:
    """Show information for a model"""
    return await ollama.show_model(name, ctx)

@mcp.tool()
async def run(name: str, prompt: str, ctx: Context, **params) -> str:
    """Run a model with optional parameters"""
    return await ollama.run_model(name, prompt, ctx, **params)

@mcp.tool()
async def stop(name: str, ctx: Context) -> str:
    """Stop a running model"""
    return await ollama.stop_model(name, ctx)

@mcp.tool()
async def pull(name: str, ctx: Context) -> str:
    """Pull a model from a registry"""
    return await ollama.pull_model(name, ctx)

@mcp.tool()
async def push(name: str, ctx: Context) -> str:
    """Push a model to a registry"""
    return await ollama.push_model(name, ctx)

@mcp.tool()
async def list_models(ctx: Context) -> str:
    """List all available models"""
    return await ollama.list_models(ctx)

@mcp.tool()
async def ps(ctx: Context) -> str:
    """List running models"""
    return await ollama.list_running(ctx)

@mcp.tool()
async def cp(source: str, destination: str, ctx: Context) -> str:
    """Copy a model"""
    return await ollama.copy_model(source, destination, ctx)

@mcp.tool()
async def rm(name: str, ctx: Context) -> str:
    """Remove a model"""
    return await ollama.remove_model(name, ctx)

def main():
    mcp.run()

if __name__ == "__main__":
    main() 