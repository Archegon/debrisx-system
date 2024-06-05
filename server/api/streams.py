from . import api_router
from fastapi import BackgroundTasks
from fastapi.responses import StreamingResponse
from server.modules import camera_stream, PiCameraStream

def stop_stream(stream: PiCameraStream):
    stream.stop()

@api_router.get('/stream.mjpg')
async def video_feed(background_tasks: BackgroundTasks):
    camera_stream.start()
    background_tasks.add_task(stop_stream, camera_stream)
    return StreamingResponse(camera_stream.generate_frames(), media_type='multipart/x-mixed-replace; boundary=FRAME')