from . import api_router
from fastapi.responses import StreamingResponse
from server.modules import camera_stream

@api_router.get('/stream.mjpg')
async def video_feed():
    camera_stream.start()
    return StreamingResponse(camera_stream.generate_frames(), media_type='multipart/x-mixed-replace; boundary=FRAME')