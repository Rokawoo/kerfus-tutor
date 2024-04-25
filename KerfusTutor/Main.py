import asyncio
import random
import time
from threading import Thread, Event

from collections import deque
from GUI import create_gui, random_expression_from_set, async_random_expression_from_set, reset, update_image, IDLE_FUNCS, COMPLETION_FUNCS, KerfusTalkOpen_IMAGE_PATH
from TTSSTT.audioProcessing import active_listening, convert_audio_to_text, play_and_delete_sound_files, get_audio_duration_soundfile
from TTSSTT.tiktockTts import tts
from ChatAI.gptChat import process_message_and_generate_response, get_current_date

IN_PROGRESS = False
EXIT_EVENT = Event()

def random_expression_trigger(root, image_label, screen_width, screen_height):
    while True:
        delay = random.uniform(5, 10)
        time.sleep(delay)
        if not IN_PROGRESS:
            random_expression_from_set(
                root,
                image_label,
                screen_width,
                screen_height,
                IDLE_FUNCS
            )
            if not IN_PROGRESS:
                reset(root, image_label, screen_width, screen_height)
            else:
                update_image(image_label, KerfusTalkOpen_IMAGE_PATH, screen_width, screen_height)


async def main(root, image_label, screen_width, screen_height):
    global IN_PROGRESS

    today = get_current_date()

    message_history = deque(maxlen=7)
    response_history = deque(maxlen=7)

    while not EXIT_EVENT.is_set():
        audio = await active_listening()
        if audio:
            text = await convert_audio_to_text(audio)
            
            if text:
                if text.lower() == "exit":
                    EXIT_EVENT.set()

                IN_PROGRESS = True
                print(text)

                response, success = await process_message_and_generate_response(today, text, message_history, response_history)
                print(response)

                if success:
                    message_history.append(response)
                    response_history.append(response)

                await tts(response, "en_us_002", "output0.mp3")

                tts_time = get_audio_duration_soundfile("output0.mp3") or 7

                play_task = asyncio.create_task(play_and_delete_sound_files())
                expression_task = asyncio.create_task(
                    async_random_expression_from_set(
                        root, image_label, screen_width, screen_height, COMPLETION_FUNCS, max(tts_time - 1.5, 0),
                    )
                )

                await asyncio.gather(play_task, expression_task)

                reset(root, image_label, screen_width, screen_height)

        IN_PROGRESS = False


if __name__ == "__main__":
    root, image_label, screen_width, screen_height = create_gui()
    expression_thread = Thread(
        target=random_expression_trigger,
        args=(root, image_label, screen_width, screen_height),
    )
    expression_thread.daemon = True
    expression_thread.start()

    loop = asyncio.new_event_loop()
    asyncio_thread = Thread(
        target=loop.run_until_complete,
        args=(main(root, image_label, screen_width, screen_height),),
    )
    asyncio_thread.daemon = True
    asyncio_thread.start()

    try:
        root.mainloop()
    finally:
        join_timeout = 5
        if root:
            root.destroy()
        

        if expression_thread.is_alive():
            expression_thread.join(join_timeout)
        

        if loop and not loop.is_closed():
            loop.stop()
            loop.run_until_complete(loop.shutdown_asyncgens())
            loop.close()
        

        if asyncio_thread.is_alive():
            asyncio_thread.join(join_timeout)
        
        print("Application has exited gracefully.")
