<h1 align="center"> SportLLM-Eval </h1>

SportLLM-Eval es un sistema de evaluación automática de la
calidad de acciones deportivas basado en la integración de LLMs generales para comprobar su capacidad _"off-the-self"_.

## Instalación y Ejecución

Sigue estos pasos para configurar y ejecutar el proyecto.

1. **Clonar el repositorio:**

   ```bash
   git clone https://github.com/Tono3451/SportLLM-Eval
   ```

2. **Crear y activar el entorno de Anaconda:**

   Instala Anaconda o Miniconda para la creación y mantenimiento de entornos y ejecuta los siguientes comandos:

    ```bash
    conda create -n sportllm_env python=3.10 -y

    conda activate sportllm_env
    ```

3. **Instalación de dependencias:**

   - Instala OpenCV para el procesamiento de los videos e imágenes:

        ```bash
        pip install opencv-python
        ```

   - Descarga e instala [Ollama](https://ollama.com/) para descargar y utilizar los modelos soportados.

4. **Ejecutar el proyecto:**

   Asegúrate de iniciar el servicio de Ollama antes de la ejecución para que los modelos puedan ser consultados:

   ```bash
   ollama serve
   ```

   Luego, corre el archivo principal del proyecto:

   ```bash
   python main.py
   ```
