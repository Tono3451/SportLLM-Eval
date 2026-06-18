import cv2
import ollama
import time
from colorama import init, Fore, Back, Style

from descriptor_reasoner.utilities.ImageProcessor import get_frames_context

def description(prompt, video_path, maxSizePixel, num_frames=8, start_frame=0, end_frame=None):
    init(autoreset=True)
    frames = get_frames_context(video_path, maxSizePixel, num_frames, start_frame, end_frame)

    print(Fore.BLUE + f"Generando respuesta: numero de frames {num_frames} (Esto puede tardar varios segundos ...)")
    start_time=time.perf_counter()
    response = ollama.chat(
    model='qwen2.5vl:3b',
    messages=[
        {
            'role': 'system',
            'content': prompt.getSystemPrompt()
        },
        {
            'role': 'user',
            'content': prompt.getUserPrompt(),
            'images': frames
        }
    ],
    options={
        'temperature': 0.7,
        'top_p': 0.9,

        'repeat_penalty': 1.2,
        'repeat_last_n': 256,

        'num_predict': 250
    }
)

    end_time=time.perf_counter()

    tiempo_total = end_time - start_time

    print(Back.YELLOW + Fore.BLACK + f"La respuesta del modelo tardó {tiempo_total:.4f} segundos")

    return response['message']['content']