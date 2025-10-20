"""
FastAPI Backend Server for Axonyx GUI
Exposes Windows Agent functionality via REST API
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uvicorn
import os
from dotenv import load_dotenv

from agent import WindowsAgent

load_dotenv()

app = FastAPI(title="Axonyx Revolt API", version="1.0.0")

# Enable CORS for Flutter app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global agent instance
agent: Optional[WindowsAgent] = None
current_model: str = os.getenv("CLAUDE_MODEL", "claude-3-5-haiku-20241022")


class ExecuteRequest(BaseModel):
    task: str
    model: Optional[str] = None


class SetModelRequest(BaseModel):
    model: str


class ToolCallResponse(BaseModel):
    name: str
    input: Dict[str, Any]
    result: Dict[str, Any]
    success: bool


class AgentResponse(BaseModel):
    final_response: str
    success: bool
    tool_calls: List[ToolCallResponse]
    iterations: int


def get_agent() -> WindowsAgent:
    """Get or create agent instance"""
    global agent, current_model
    
    if agent is None or agent.model != current_model:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="ANTHROPIC_API_KEY not set")
        agent = WindowsAgent(api_key=api_key, model=current_model)
        # Disable confirmation for GUI mode
        agent.require_confirmation = False
    
    return agent


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "model": current_model,
        "api_key_set": bool(os.getenv("ANTHROPIC_API_KEY"))
    }


@app.post("/execute", response_model=AgentResponse)
async def execute_task(request: ExecuteRequest):
    """
    Execute a task using the Windows Agent
    """
    try:
        # Update model if specified
        if request.model:
            global current_model
            current_model = request.model
            
        agent = get_agent()
        result = agent.execute_task(request.task)
        
        # Extract tool calls information
        tool_calls = []
        if "tool_results" in result:
            for tool_result in result["tool_results"]:
                tool_calls.append(ToolCallResponse(
                    name=tool_result.get("tool_name", "unknown"),
                    input=tool_result.get("input", {}),
                    result=tool_result.get("result", {}),
                    success=tool_result.get("result", {}).get("success", False)
                ))
        
        return AgentResponse(
            final_response=result.get("final_response", "Task completed"),
            success=result.get("success", False),
            tool_calls=tool_calls,
            iterations=result.get("iterations", 0)
        )
        
    except Exception as e:
        import traceback
        error_details = {
            "error": str(e),
            "type": type(e).__name__,
            "traceback": traceback.format_exc()
        }
        print(f"❌ Error executing task: {error_details}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/set-model")
async def set_model(request: SetModelRequest):
    """
    Change the Claude model
    """
    global current_model, agent
    current_model = request.model
    agent = None  # Force recreation with new model
    
    # Update .env file
    try:
        from pathlib import Path
        env_path = Path(__file__).parent / ".env"
        
        if env_path.exists():
            with open(env_path, 'r') as f:
                lines = f.readlines()
            
            with open(env_path, 'w') as f:
                for line in lines:
                    if line.startswith('CLAUDE_MODEL='):
                        f.write(f'CLAUDE_MODEL={request.model}\n')
                    else:
                        f.write(line)
    except Exception as e:
        print(f"Warning: Could not update .env file: {e}")
    
    return {
        "success": True,
        "model": current_model,
        "message": f"Model changed to {request.model}"
    }


@app.get("/models")
async def get_available_models():
    """
    Get list of available Claude models
    """
    return {
        "models": [
            {
                "id": "claude-3-5-haiku-20241022",
                "name": "Haiku 3.5",
                "description": "Fast & Cheap ⚡"
            },
            {
                "id": "claude-3-5-sonnet-20241022",
                "name": "Sonnet 3.5",
                "description": "Balanced 🎯"
            },
            {
                "id": "claude-sonnet-4-20250514",
                "name": "Sonnet 4",
                "description": "Most Powerful 🚀"
            }
        ],
        "current": current_model
    }


@app.get("/tools")
async def get_available_tools():
    """
    Get list of all available tools
    """
    try:
        agent = get_agent()
        return {
            "tools": [
                {
                    "name": tool["name"],
                    "description": tool["description"]
                }
                for tool in agent.tools
            ],
            "count": len(agent.tools)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    print("🚀 Starting Axonyx Revolt API Server...")
    print(f"📡 Backend URL: http://localhost:8000")
    print(f"🤖 Model: {current_model}")
    print(f"📚 API Docs: http://localhost:8000/docs")
    print("\n✨ GUI: Run Flutter app to connect\n")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
