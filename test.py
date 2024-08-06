import asyncio
from modules.collector.servo import ServoController

async def main():
    servo = ServoController(25)
    print("Starting servo test")

    try:
        await servo.set_angle(100)
        await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("Program stopped")
    except AngleOutOfRangeError as e:
        print(e)
    finally:
        await servo.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
