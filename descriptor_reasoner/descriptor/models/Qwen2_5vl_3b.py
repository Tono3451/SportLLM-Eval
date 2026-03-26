import cv2
import ollama

def preparar_secuencia_video(video_path, num_frames=8, start_frame=0, end_frame=None):
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    if end_frame is None or end_frame > total_frames:
        end_frame = total_frames
        
    start_frame = max(0, min(start_frame, total_frames - 1))
    
    frames_en_segmento = max(0, end_frame - start_frame)
    paso = frames_en_segmento // num_frames if frames_en_segmento > 0 else 1
    
    secuencia_imagenes = []
    
    for i in range(num_frames):
        frame_idx = start_frame + (i * paso)
        
        if frame_idx >= end_frame:
            break
            
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = cap.read()
        if not ret: break
        
        frame = cv2.resize(frame, (640, 480))
        _, buffer = cv2.imencode('.jpg', frame)
        secuencia_imagenes.append(buffer.tobytes())
    
    cap.release()
    return secuencia_imagenes

def description(prompt, video_path, num_frames=8, start_frame=0, end_frame=None):
    frames = preparar_secuencia_video(video_path, num_frames, start_frame, end_frame)

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

    return response['message']['content']