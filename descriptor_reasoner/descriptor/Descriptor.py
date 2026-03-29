import importlib
import cv2
from descriptor_reasoner.descriptor.DescriptorModels import DescriptorModels

class Descriptor:
    @staticmethod
    def process(model: DescriptorModels, prompt: str, videoUrl: str , maxSizePixel: int, num_frames=8, batchSeconds=0):
        model_filename = model.value 
        
        try:
            modulo = importlib.import_module(f"descriptor_reasoner.descriptor.models.{model_filename}")
            
            # Procesamiento de todo el video
            if batchSeconds <= 0:
                return modulo.description(prompt, videoUrl, maxSizePixel, num_frames)
            
            return Descriptor.process_video_segments(modulo, videoUrl,  prompt, maxSizePixel, num_frames, batchSeconds)
                
        except ImportError as e:
            raise ValueError(f"No se encontró el modelo '{model_filename}' en 'models/'. Error: {e}")

    @staticmethod    
    def process_video_segments(modulo, videoUrl, prompt, maxSizePixel, num_frames, batchSeconds):
        # Procesamiento del video por segmentos
        cap = cv2.VideoCapture(videoUrl)
        if not cap.isOpened():
            raise ValueError(f"Could not open video at: {videoUrl}")
            
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        cap.release()
        
        if fps <= 0:
            fps = 30
            
        frames_per_batch = int(fps * batchSeconds)
        all_descriptions = []
        segment_number = 1
        
        for start_frame in range(0, total_frames, frames_per_batch):
            end_frame = min(start_frame + frames_per_batch, total_frames)
            
            segment_desc = modulo.description(
                prompt, 
                videoUrl, 
                maxSizePixel,
                num_frames,
                start_frame=start_frame, 
                end_frame=end_frame,
            )

            if prompt.enableHistory and hasattr(prompt, 'addDescription'):
                prompt.addDescription(segment_desc)
            
            start_time = start_frame / fps
            end_time = end_frame / fps
            
            all_descriptions.append(
                f"--- Segment {segment_number} ({start_time:.1f}s to {end_time:.1f}s) ---\n{segment_desc}"
            )
            
            segment_number += 1
        
        unified_description = "\n\n".join(all_descriptions)
        return unified_description