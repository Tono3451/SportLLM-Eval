import cv2

import time
from colorama import init, Fore, Back, Style
from typing import List, Optional, Tuple

def get_frames_context(video_path: str, maxSizePixel: int, num_frames: int = 8, start_frame: int = 0, end_frame: Optional[int] = None) -> List[bytes]:

    start_time=time.perf_counter()

    # Preámbulo
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    if end_frame is None or end_frame > total_frames:
        end_frame = total_frames
        
    start_frame = max(0, min(start_frame, total_frames - 1))
    
    frames_in_segment = max(0, end_frame - start_frame)
    
    if num_frames == 0:
        frames_a_extraer = frames_in_segment
    else:
        frames_a_extraer = num_frames
        
    step = max(1, frames_in_segment // frames_a_extraer) if frames_a_extraer > 0 else 1
    
    image_sequence = []

    # Preparar frames
    for i in range(frames_a_extraer):
        # Obtener el frame
        frame_idx = start_frame + (i * step)
        
        if frame_idx >= end_frame:
            break
            
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = cap.read()
        if not ret: break
        
        # Redimensionar el frame
        h, w = frame.shape[:2]

        rh, rw = _resize_calculation(maxSizePixel, h, w)
        frame = cv2.resize(frame, (rw, rh))

        #frame = cv2.resize(frame, (437, 313))

        # Añadir frame

        _, buffer = cv2.imencode('.jpg', frame)
        image_sequence.append(buffer.tobytes())
    
    cap.release()

    end_time=time.perf_counter()
    total_time = end_time - start_time
    init(autoreset=True)
    print(Back.YELLOW + Fore.BLACK + f"Sacar los frames tardó {total_time:.4f} segundos")
    
    return image_sequence

def _resize_calculation(maxSize: int, h: int, w: int) -> Tuple[int, int]:
    #print(Back.GREEN + f"Valores reales - w: {w}, h: {h}, max size: {maxSize}")
    max_dim = maxSize
        
    if w > h:
        base_w = max_dim
        base_h = int(h * (max_dim / w))
    else:
        base_h = max_dim
        base_w = int(w * (max_dim / h))

    base_h = _round_to_multiple(base_h, 28)
    base_w = _round_to_multiple(base_w, 28)

    #init(autoreset=True)
    #print(Back.GREEN + f"Valores modificados - w: {base_w}, h: {base_h}")
    
    return base_h, base_w

def _round_to_multiple(num: float, base: int) -> int:
    return int(round(num / base) * base)
