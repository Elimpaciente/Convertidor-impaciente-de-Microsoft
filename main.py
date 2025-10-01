from fastapi import FastAPI
from fastapi.responses import JSONResponse, StreamingResponse
import edge_tts
from io import BytesIO

app = FastAPI()

@app.get("/")
async def root():
    return JSONResponse(
        content={
            "status_code": 200,
            "developer": "El Impaciente"
        },
        status_code=200
    )

@app.get("/tts")
async def text_to_speech(voice: str = None, text: str = None):
    if not voice or not text:
        return JSONResponse(
            content={
                "status_code": 400,
                "developer": "El Impaciente",
                "message": "Se requieren los parámetros voice y text"
            },
            status_code=400
        )
    
    try:
        communicate = edge_tts.Communicate(text, voice)
        audio_buffer = BytesIO()
        
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_buffer.write(chunk["data"])
        
        if audio_buffer.tell() == 0:
            return JSONResponse(
                content={
                    "status_code": 400,
                    "developer": "El Impaciente",
                    "message": "No se pudo generar audio"
                },
                status_code=400
            )
        
        audio_buffer.seek(0)
        
        return StreamingResponse(
            audio_buffer,
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": "inline; filename=audio.mp3"
            }
        )
        
    except Exception as e:
        return JSONResponse(
            content={
                "status_code": 400,
                "developer": "El Impaciente",
                "message": f"Error: {str(e)}"
            },
            status_code=400
        )

@app.get("/voices")
async def list_voices():
    try:
        voices = await edge_tts.list_voices()
        formatted_voices = [
            {
                "name": voice["ShortName"],
                "gender": voice["Gender"],
                "locale": voice["Locale"]
            }
            for voice in voices
        ]
        
        return JSONResponse(
            content={
                "status_code": 200,
                "developer": "El Impaciente",
                "total": len(formatted_voices),
                "voices": formatted_voices
            },
            status_code=200
        )
        
    except Exception as e:
        return JSONResponse(
            content={
                "status_code": 400,
                "developer": "El Impaciente",
                "message": f"Error: {str(e)}"
            },
            status_code=400
        )
