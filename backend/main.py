from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.config import ConfigManager
from core.model import get_llm_adapter
from core.memory import ShortTermMemory

app = FastAPI(title="AI女友")

config = ConfigManager()
short_term_memory = ShortTermMemory(max_size=config.get("memory.short_term_max", 20))

frontend_path = Path(__file__).parent.parent / "frontend"
app.mount("/static", StaticFiles(directory=str(frontend_path)), name="static")


@app.get("/")
async def read_root():
    return FileResponse(str(frontend_path / "index.html"))


@app.get("/api/config")
async def get_config():
    return config.config


@app.post("/api/config")
async def save_config(new_config: dict):
    config.config = new_config
    config.save_config()
    return {"success": True}


@app.get("/api/models")
async def get_models():
    return {
        "llm": list(config.get("llm_models", {}).keys()),
        "tts": list(config.get("tts_models", {}).keys())
    }


@app.get("/api/chat/history")
async def get_chat_history():
    return {"messages": short_term_memory.get_history()}


@app.post("/api/chat/clear")
async def clear_chat_history():
    short_term_memory.clear()
    return {"success": True}


@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            user_message = message.get("message", "")
            
            if not user_message:
                continue
            
            short_term_memory.add_message("user", user_message)
            
            active_llm = config.get("active_llm", "deepseek")
            llm_config = config.get(f"llm_models.{active_llm}", {})
            
            if not llm_config.get("api_key"):
                await websocket.send_json({
                    "type": "error",
                    "message": "请先在设置中配置API密钥"
                })
                continue
            
            try:
                adapter = get_llm_adapter(active_llm, llm_config)
                
                messages = short_term_memory.get_history()
                
                await websocket.send_json({
                    "type": "start"
                })
                
                full_response = ""
                if hasattr(adapter, 'chat'):
                    result = await adapter.chat(messages, stream=True)
                    if hasattr(result, '__aiter__'):
                        async for chunk in result:
                            full_response += chunk
                            await websocket.send_json({
                                "type": "chunk",
                                "content": chunk
                            })
                    else:
                        full_response = result
                        await websocket.send_json({
                            "type": "chunk",
                            "content": full_response
                        })
                
                short_term_memory.add_message("assistant", full_response)
                
                await websocket.send_json({
                    "type": "done"
                })
                
            except Exception as e:
                await websocket.send_json({
                    "type": "error",
                    "message": f"发生错误: {str(e)}"
                })
                
    except WebSocketDisconnect:
        pass
    except Exception as e:
        print(f"WebSocket错误: {e}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
