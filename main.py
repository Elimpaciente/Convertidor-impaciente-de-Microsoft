from fastapi import FastAPI
from fastapi.responses import JSONResponse, StreamingResponse, HTMLResponse
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

@app.get("/documentacion", response_class=HTMLResponse)
@app.get("/documentacion.html", response_class=HTMLResponse)
async def documentacion():
    html_content = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Microsoft TTS API - El Impaciente</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 40px 20px;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            padding: 50px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        }
        h1 { color: #667eea; font-size: 36px; margin-bottom: 10px; }
        .subtitle { color: #666; font-size: 18px; margin-bottom: 40px; }
        .section { margin-bottom: 40px; }
        h2 {
            color: #333;
            font-size: 24px;
            margin-bottom: 15px;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }
        .info-block {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 15px;
            border-left: 4px solid #667eea;
        }
        .info-block strong { color: #667eea; display: inline-block; min-width: 120px; }
        .code-block {
            background: #2d2d2d;
            color: #f8f8f2;
            padding: 20px;
            border-radius: 8px;
            overflow-x: auto;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            margin: 10px 0;
        }
        .example-url {
            background: #e7f3ff;
            padding: 15px;
            border-radius: 8px;
            word-break: break-all;
            color: #0066cc;
            font-family: monospace;
            margin: 10px 0;
        }
        .voice-list {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 10px;
            margin-top: 15px;
        }
        .voice-item {
            background: #f8f9fa;
            padding: 10px 15px;
            border-radius: 6px;
            font-size: 14px;
            border-left: 3px solid #667eea;
        }
        .badge {
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 4px 10px;
            border-radius: 15px;
            font-size: 12px;
            margin-left: 5px;
        }
        .response-example {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            margin-top: 10px;
        }
        .footer {
            text-align: center;
            margin-top: 50px;
            padding-top: 30px;
            border-top: 2px solid #eee;
            color: #666;
        }
        .btn-test {
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px 30px;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 600;
            margin-top: 20px;
            transition: transform 0.2s;
        }
        .btn-test:hover { transform: translateY(-2px); }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎙️ Microsoft TTS API</h1>
        <p class="subtitle">Convierte texto a audio con 400+ voces neuronales de Microsoft</p>

        <div class="section">
            <h2>📋 Información General</h2>
            <div class="info-block">
                <strong>Base URL:</strong> <code>https://convertidor-impaciente-de-microsoft.vercel.app/api/tts?voice=&text=</code>
            </div>
            <div class="info-block"><strong>Método:</strong> GET</div>
            <div class="info-block"><strong>Formato:</strong> Audio MP3 (24kHz)</div>
            <div class="info-block"><strong>Precio:</strong> ✅ GRATIS</div>
            <div class="info-block"><strong>Desarrollador:</strong> El Impaciente</div>
        </div>

        <div class="section">
            <h2>🔮 Parámetros</h2>
            <div class="info-block">
                <strong>voice</strong> <span class="badge">requerido</span><br>
                Nombre de la voz neural (ej: es-MX-DaliaNeural)
            </div>
            <div class="info-block">
                <strong>text</strong> <span class="badge">requerido</span><br>
                Texto a convertir en audio
            </div>
        </div>

        <div class="section">
            <h2>💡 Ejemplo de Uso</h2>
            <div class="example-url">
                https://convertidor-impaciente-de-microsoft.vercel.app/api/tts?voice=es-MX-DaliaNeural&text=Buen día
            </div>
            <a href="/api/tts?voice=es-MX-DaliaNeural&text=Hola, esta es una prueba de la API" 
               class="btn-test" target="_blank">🎵 Probar Ahora</a>
        </div>

        <div class="section">
            <h2>📤 Respuestas</h2>
            <div class="response-example">
                <strong>✅ Éxito (200):</strong><br>
                Devuelve el archivo de audio MP3 directamente
            </div>
            <div class="response-example">
                <strong>❌ Error (400):</strong>
                <div class="code-block">{
  "status_code": 400,
  "developer": "El Impaciente",
  "message": "Se requieren los parámetros voice y text"
}</div>
            </div>
        </div>

        <div class="section">
            <h2>🎤 Voces Populares</h2>
            
            <h3 style="color: #667eea; margin-top: 20px;">🇪🇸 Español</h3>
            <div class="voice-list">
                <div class="voice-item">es-MX-DaliaNeural 👩<br><small>México</small></div>
                <div class="voice-item">es-MX-JorgeNeural 👨<br><small>México</small></div>
                <div class="voice-item">es-ES-ElviraNeural 👩<br><small>España</small></div>
                <div class="voice-item">es-ES-AlvaroNeural 👨<br><small>España</small></div>
                <div class="voice-item">es-AR-ElenaNeural 👩<br><small>Argentina</small></div>
                <div class="voice-item">es-CO-SalomeNeural 👩<br><small>Colombia</small></div>
            </div>

            <h3 style="color: #667eea; margin-top: 20px;">🇺🇸 English</h3>
            <div class="voice-list">
                <div class="voice-item">en-US-JennyNeural 👩<br><small>USA</small></div>
                <div class="voice-item">en-US-GuyNeural 👨<br><small>USA</small></div>
                <div class="voice-item">en-GB-LibbyNeural 👩<br><small>UK</small></div>
                <div class="voice-item">en-GB-RyanNeural 👨<br><small>UK</small></div>
            </div>

            <h3 style="color: #667eea; margin-top: 20px;">🌍 Otros Idiomas</h3>
            <div class="voice-list">
                <div class="voice-item">fr-FR-DeniseNeural 👩<br><small>Français</small></div>
                <div class="voice-item">de-DE-KatjaNeural 👩<br><small>Deutsch</small></div>
                <div class="voice-item">it-IT-ElsaNeural 👩<br><small>Italiano</small></div>
                <div class="voice-item">pt-BR-FranciscaNeural 👩<br><small>Português</small></div>
                <div class="voice-item">zh-CN-XiaoxiaoNeural 👩<br><small>中文</small></div>
                <div class="voice-item">ja-JP-NanamiNeural 👩<br><small>日本語</small></div>
                <div class="voice-item">ko-KR-SunHiNeural 👩<br><small>한국어</small></div>
                <div class="voice-item">ru-RU-SvetlanaNeural 👩<br><small>Русский</small></div>
            </div>

            <div class="info-block" style="margin-top: 20px;">
                <strong>Ver todas:</strong> 
                <a href="/api/voices" style="color: #667eea;">400+ voces disponibles</a>
            </div>
        </div>

        <div class="section">
            <h2>💻 Ejemplos de Código</h2>
            
            <h3 style="color: #667eea; margin-top: 20px;">JavaScript</h3>
            <div class="code-block">const url = "https://convertidor-impaciente-de-microsoft.vercel.app/api/tts";
const params = "?voice=es-MX-DaliaNeural&text=Hola mundo";

fetch(url + params)
  .then(res => res.blob())
  .then(blob => {
    const audio = new Audio(URL.createObjectURL(blob));
    audio.play();
  });</div>

            <h3 style="color: #667eea; margin-top: 20px;">Python</h3>
            <div class="code-block">import requests

url = "https://convertidor-impaciente-de-microsoft.vercel.app/api/tts"
params = {"voice": "es-MX-DaliaNeural", "text": "Hola mundo"}

response = requests.get(url, params=params)
with open("audio.mp3", "wb") as f:
    f.write(response.content)</div>

            <h3 style="color: #667eea; margin-top: 20px;">cURL</h3>
            <div class="code-block">curl "https://convertidor-impaciente-de-microsoft.vercel.app/api/tts?voice=es-MX-DaliaNeural&text=Hola" -o audio.mp3</div>

            <h3 style="color: #667eea; margin-top: 20px;">PHP</h3>
            <div class="code-block">$url = "https://convertidor-impaciente-de-microsoft.vercel.app/api/tts";
$params = "?voice=es-MX-DaliaNeural&text=Hola";

file_put_contents("audio.mp3", file_get_contents($url . $params));</div>
        </div>

        <div class="section">
            <h2>✨ Características</h2>
            <div class="voice-list">
                <div class="voice-item">✅ Totalmente gratis</div>
                <div class="voice-item">✅ Sin autenticación</div>
                <div class="voice-item">✅ 400+ voces neuronales</div>
                <div class="voice-item">✅ 30+ idiomas</div>
                <div class="voice-item">✅ Alta calidad (24kHz)</div>
                <div class="voice-item">✅ Respuesta instantánea</div>
            </div>
        </div>

        <div class="footer">
            <p><strong>👨‍💻 Desarrollador:</strong> El Impaciente</p>
            <p style="margin-top: 10px; font-size: 14px;">
                ⭐ Si te gusta esta API, compártela con otros desarrolladores
            </p>
        </div>
    </div>
</body>
</html>
    """
    return HTMLResponse(content=html_content)

@app.get("/tts")
async def text_to_speech_main(voice: str = "", text: str = ""):
    if not voice or not text or voice.strip() == "" or text.strip() == "":
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
                    "message": "No se pudo generar el audio"
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
                "message": "Error al procesar la solicitud"
            },
            status_code=400
        )

@app.get("/api/tts")
async def text_to_speech_api(voice: str = "", text: str = ""):
    if not voice or not text or voice.strip() == "" or text.strip() == "":
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
                    "message": "No se pudo generar el audio"
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
                "message": "Error al procesar la solicitud"
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
                "message": "Error al obtener las voces"
            },
            status_code=400
        )

@app.get("/api/voices")
async def list_voices_api():
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
                "message": "Error al obtener las voces"
            },
            status_code=400
        )
