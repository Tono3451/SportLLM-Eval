import cv2
import ollama
import time
from colorama import init, Fore, Back, Style

def reasoner(prompt, description):
    init(autoreset=True)

    print(Fore.GREEN + f"Generando puntuación (Esto puede tardar varios segundos ...)")
    start_time=time.perf_counter()
    response = ollama.chat(
        model='deepseek-r1:14b',
        messages=[
            {'role': 'system', 'content': prompt.getSystemPrompt()},
            {'role': 'user', 'content': prompt.getUserPrompt(description)}
        ],
        options={
            'num_ctx': 8192
        }
    )

    end_time=time.perf_counter()

    tiempo_total = end_time - start_time

    print(Back.BLUE + Fore.BLACK + f"La respuesta del modelo tardó {tiempo_total:.4f} segundos")

    return response['message']['content']