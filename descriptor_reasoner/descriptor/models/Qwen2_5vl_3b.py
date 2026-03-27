import cv2
import ollama

import time
from colorama import init, Fore, Back, Style


def prepare_video_sequence(video_path, num_frames=8, start_frame=0, end_frame=None):
    start_time=time.perf_counter()

    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    if end_frame is None or end_frame > total_frames:
        end_frame = total_frames
        
    start_frame = max(0, min(start_frame, total_frames - 1))
    
    frames_in_segment = max(0, end_frame - start_frame)
    step = max(1, frames_in_segment // num_frames)
    
    image_sequence = []
    
    for i in range(num_frames):
        frame_idx = start_frame + (i * step)
        
        if frame_idx >= end_frame:
            break
            
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = cap.read()
        if not ret: break
        
        frame = cv2.resize(frame, (640, 480))
        _, buffer = cv2.imencode('.jpg', frame)
        image_sequence.append(buffer.tobytes())
    
    cap.release()

    end_time=time.perf_counter()

    tiempo_total = end_time - start_time

    print(Back.YELLOW + Fore.BLACK + f"Sacar los frames tardó {tiempo_total:.4f} segundos")
    return image_sequence

def description(prompt, video_path, num_frames=8, start_frame=0, end_frame=None):
    init(autoreset=True)
    frames = prepare_video_sequence(video_path, num_frames, start_frame, end_frame)

    print(Fore.BLUE + f"Cargando modelo de respuesta (Esto puede tardar varios segundos ...)")
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
        ]
    )

    end_time=time.perf_counter()

    tiempo_total = end_time - start_time

    print(Back.YELLOW + Fore.BLACK + f"La respuesta del modelo tardó {tiempo_total:.4f} segundos")

    return response['message']['content']