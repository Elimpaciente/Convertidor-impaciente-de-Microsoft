from fastapi import FastAPI
from fastapi.responses import JSONResponse, StreamingResponse
import edge_tts
from io import BytesIO

app = FastAPI()

@app.get("/")
async def root():
    return {
        "status": "online",
        "message": "API de Edge-TTS funcionando",
        "developer": "El Impaciente",
        "endpoints": {
            "tts": "/tts?voice=VOICE_NAME&text=YOUR_TEXT",
            "voices": "/voices"
        },
        "ejemplo": "/tts?voice=es-MX-DaliaNeural&text=Hola mundo"
    }

@app.get("/tts")
async def text_to_speech(voice: str = None, text: str = None):
    # Validar que ambos parámetros estén presentes
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
        # Crear comunicador de Edge-TTS
        communicate = edge_tts.Communicate(text, voice)
        
        # Buffer para almacenar el audio
        audio_buffer = BytesIO()
        
        # Generar el audio
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_buffer.write(chunk["data"])
        
        # Verificar que se generó audio
        if audio_buffer.tell() == 0:
            return JSONResponse(
                content={
                    "status_code": 400,
                    "developer": "El Impaciente",
                    "message": "No se pudo generar audio. Verifica que la voz sea válida."
                },
                status_code=400
            )
        
        # Resetear el puntero del buffer al inicio
        audio_buffer.seek(0)
        
        # Devolver el audio como respuesta
        return StreamingResponse(
            audio_buffer,
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": "inline; filename=audio.mp3",
                "X-Developer": "El Impaciente",
                "X-Status-Code": "200"
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
    """Lista todas las voces disponibles"""
    try:
        voices = await edge_tts.list_voices()
        
        # Formatear voces para una respuesta más limpia
        formatted_voices = [
            {
                "name": voice["ShortName"],
                "gender": voice["Gender"],
                "locale": voice["Locale"],
                "language": voice["Locale"].split("-")[0]
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

@app.get("/voices/spanish")
async def spanish_voices():
    """Devuelve voces populares en español"""
    return JSONResponse(
        content={
            "status_code": 200,
            "developer": "El Impaciente",
            "message": "Voces en español disponibles",
            "voices": [
                "es-MX-DaliaNeural",
                "es-MX-JorgeNeural",
                "es-ES-ElviraNeural",
                "es-ES-AlvaroNeural",
                "es-AR-ElenaNeural",
                "es-AR-TomasNeural",
                "es-CO-SalomeNeural",
                "es-CO-GonzaloNeural",
                "es-CL-CatalinaNeural",
                "es-PE-CamilaNeural"
            ]
        },
        status_code=200
    )