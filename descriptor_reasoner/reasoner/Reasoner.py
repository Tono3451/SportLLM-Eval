import importlib
from descriptor_reasoner.reasoner.ReasonerModels import ReasonerModels

class Reasoner:
    @staticmethod
    def process(model: ReasonerModels, prompt: str, description: str):
        model_filename = model.value 
        
        try:
            modulo = importlib.import_module(f"descriptor_reasoner.reasoner.models.{model_filename}")
            
            return modulo.reasoner(prompt, description)
                
        except ImportError as e:
            raise ValueError(f"No se encontró el modelo '{model_filename}' en 'models/'. Error: {e}")