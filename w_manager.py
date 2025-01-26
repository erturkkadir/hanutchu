# section 1: Communication between listen.js to web_server
#   The web server is located at syshuman.com
#   The sound from microphone is sent to the web server over port 7860
#   The web server will send the sound to the listen.js over port 7861

# section 2: Communication between webserver to ai/sound servers
#   The web server will send the sound to the sound server (https://sound.syshuman.com) over port 8861 (kokoro/F5 TTS)
#   The web server will send the sound to the ai server (https://ai.syshuman.com) over port 8862 with cURL (ollama)

# THIS CODE WILL RUN ON THE WEB SERVER (www.syshuman.com/doktor)

import asyncio
import websockets
import json
import ssl
import aiohttp
from typing import Optional, Dict, Any

class WServer:
    def __init__(self):
        # SSL Configuration needs syshuman.com cert.pem and priv.key
        self.ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        self.ssl_context.load_cert_chain('cert.pem', 'priv.key')
        
        # Server endpoints
        self.sound_server_url = "https://sound.syshuman.com:8861"
        self.ai_server_url = "https://ai.syshuman.com:8862"
        
        # HTTP session for API calls
        self.session: Optional[aiohttp.ClientSession] = None
        
        # WebSocket server ports
        self.listen_port = 7860
        self.send_port = 7861

    async def initialize(self):
        """Initialize HTTP session"""
        self.session = aiohttp.ClientSession()

    async def cleanup(self):
        """Cleanup resources"""
        if self.session:
            await self.session.close()

    async def forward_to_sound_server(self, audio_data: bytes) -> Optional[bytes]:
        """Forward audio data to sound server"""
        try:
            async with self.session.post(
                self.sound_server_url,
                data=audio_data,
                headers={'Content-Type': 'audio/wav'}
            ) as response:
                if response.status == 200:
                    return await response.read()
                print(f"Sound server error: {response.status}")
                return None
        except Exception as e:
            print(f"Error sending to sound server: {e}")
            return None

    async def forward_to_ai_server(self, text: str) -> Optional[Dict[str, Any]]:
        """Forward text to AI server"""
        try:
            async with self.session.post(
                self.ai_server_url,
                json={'prompt': text},
                headers={'Content-Type': 'application/json'}
            ) as response:
                if response.status == 200:
                    return await response.json()
                print(f"AI server error: {response.status}")
                return None
        except Exception as e:
            print(f"Error sending to AI server: {e}")
            return None

    async def handle_client(self, websocket, path):
        """Handle WebSocket client connection"""
        try:
            async for message in websocket:
                # Read 5-byte header
                header = await websocket.recv(5)
                data_length = int.from_bytes(header[:4], byteorder='big')
                message_type = header[4]

                # Read payload
                data = await websocket.recv(data_length)

                # Process based on message type
                if message_type == 0:  # Text
                    # Forward text to AI server
                    if ai_response := await self.forward_to_ai_server(data.decode('utf-8')):
                        # Get TTS audio from sound server
                        if audio_response := await self.forward_to_sound_server(
                            json.dumps({'text': ai_response['response']}).encode()
                        ):
                            # Send audio back to client
                            header = bytearray(5)                            
                            header[:4] = len(audio_response).to_bytes(4, byteorder='big')
                            header[4] = 1  # Audio type
                            await websocket.send(header)
                            await websocket.send(audio_response)

                elif message_type == 1:  # Audio
                    # Forward to sound server for STT
                    if text_response := await self.forward_to_sound_server(data):
                        # Forward text to AI server
                        if ai_response := await self.forward_to_ai_server(
                            text_response.decode('utf-8')
                        ):
                            # Get TTS from sound server
                            if audio_response := await self.forward_to_sound_server(
                                json.dumps({'text': ai_response['response']}).encode()
                            ):
                                # Send audio back to client
                                header = bytearray(5)
                                header[:4] = len(audio_response).to_bytes(4, byteorder='big')
                                header[4] = 1  # Audio type
                                await websocket.send(header)
                                await websocket.send(audio_response)

        except websockets.exceptions.ConnectionClosed:
            print("Client disconnected")
        except Exception as e:
            print(f"Error handling client: {e}")

    async def start(self):
        """Start the WebSocket server"""
        await self.initialize()
        
        async with websockets.serve(
            self.handle_client,
            '0.0.0.0',
            self.listen_port,
            ssl=self.ssl_context
        ):
            print(f"Server listening on wss://0.0.0.0:{self.listen_port}")
            await asyncio.Future()  # run forever

    def run(self):
        """Run the server"""
        try:
            asyncio.run(self.start())
        except KeyboardInterrupt:
            print("\nShutting down server...")
            asyncio.run(self.cleanup())
        except Exception as e:
            print(f"Server error: {e}")
            asyncio.run(self.cleanup())

if __name__ == "__main__":
    server = WServer()
    server.run()