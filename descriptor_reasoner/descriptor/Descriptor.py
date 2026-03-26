import importlib
from descriptor_reasoner.descriptor.DescriptorModels import DescriptorModels

class Descriptor:
    @staticmethod
    def procesar(model: DescriptorModels, prompt: str, videoUrl: str, batchSeconds=0):
        model_filename = model.value 
        
        try:
            modulo = importlib.import_module(f"descriptor_reasoner.descriptor.models.{model_filename}")
            
            if hasattr(modulo, "description"):
                return modulo.description(prompt, videoUrl)
            else:
                raise NotImplementedError(f"El modelo '{model_filename}' no implementa 'description'.")
                
        except ImportError as e:
            raise ValueError(f"No se encontró el modelo '{model_filename}' en 'models/'. Error: {e}")