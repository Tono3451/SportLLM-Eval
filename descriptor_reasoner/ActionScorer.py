import sys
import time
import threading
import itertools
from descriptor_reasoner.descriptor.Descriptor import Descriptor
from descriptor_reasoner.descriptor.DescriptorModels import DescriptorModels


class ActionScorer():
    process = False

    def __init__(self, videoUrl, descriptorModel, reasonerModel, secondsDescription=0, fps=8):
        self.videoUrl = videoUrl
        self.descriptorModel = descriptorModel
        self.reasonerModel = reasonerModel
        self.secondsDescription = secondsDescription
        self.fps = fps

    def scoreAction(self, showDescription=True):
        pass

    def describeVideo(self, prompt, batchSeconds=0):
        #ActionScorer.process = True 

        #hilo_spinner = threading.Thread(target=self.showSpinner)
        #hilo_spinner.start()

        return Descriptor.procesar(
                model=self.descriptorModel, 
                prompt=prompt, 
                videoUrl=self.videoUrl
            )

        """try:
            return Descriptor.procesar(
                model=self.descriptorModel, 
                prompt=prompt, 
                videoUrl=self.videoUrl
            )
        finally:
            # 3. Importante: nos aseguramos de detener el spinner pase lo que pase (incluso si hay error)
            self.process = False
            hilo_spinner.join()"""

        

    def reasonDescription(self):
        pass

    @classmethod
    def showSpinner(cls): # 4. Se añade 'cls' por ser un @classmethod
        """Muestra un indicador giratorio en la consola mientras 'process' sea True."""
        spinner = itertools.cycle(['-', '/', '|', '\\'])
        
        # 5. Se accede a la variable a través de 'cls'
        while cls.process: 
            sys.stdout.write(f'\rProcesando el video, por favor espera... {next(spinner)}')
            sys.stdout.flush()
            time.sleep(0.1)
        
        # Limpia la línea una vez que ha terminado
        sys.stdout.write('\r' + ' ' * 50 + '\r') 
        sys.stdout.flush()
