<h1 align="center"> SportLLM-Eval </h1>

SportLLM-Eval es un sistema de evaluación automática de la
calidad de acciones deportivas basado en la integración de LLMs generales para comprobar su capacidad _"off-the-self"_.

## Instalación y Ejecución

Sigue estos pasos para configurar y ejecutar el proyecto.

1. **Clonar repositorio:**

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

   Iniciar el proyecto mediante su archivo inicial con las opciones preferidas:

   ```bash
   python main.py
   ```

## Opciones de configuración

Las opciones principales se encuentran y cambian directamente en `main.py`:

| Opción | Funcionamiento |
|---|---|
| `SPORT_KEY` | Deporte a evaluar. |
| `PROCESS_MODE` | Modo de entrada: `single`, `all`, `subset` o `range`. |
| `VIDEO_PATH` | Video único a procesar cuando `PROCESS_MODE` es `single`. |
| `VIDEO_DIRECTORY` | Carpeta base de videos para los modos `all`, `subset` y `range`. |
| `SUBSET_INDICES` | Lista de índices de video para el modo `subset` (Empieza en 1). |
| `START_INDEX` y `END_INDEX` | Rango de videos para el modo `range` (Ambos incluidos). |
| `OUTPUT_FILE` | Archivo `.jsonl` donde se guardan los resultados. |
| `MAT_FILE_PATH` | Archivo `.mat` con la nota real para comparar (Tiene que ser un vector). |
| `MAT_SCORE_INDEX` | Índice fijo de la nota real, si no se quiere usar el nombre del video. |
| `DESCRIPTOR_MODEL` | Modelo que genera la descripción visual. |
| `REASONER_MODEL` | Modelo que calcula la puntuación final. |
| `DESCRIPTION_SECONDS` | Duración de cada segmento visual. |
| `FRAMES_PER_SEGMENT` | Cantidad de frames por segmento. |
| `MAX_PIXEL_SIZE` | Tamaño máximo de los frames antes de redimensionar. |
| `ACTIVATE_MEMORY` | Activa historial entre segmentos. |
| `ACTIVATE_ONLY_SCORE` | Si es `True`, el razonador devuelve solo la nota final. |

## Modos de uso

- `single`: procesa un solo video definido en `VIDEO_PATH`.
- `all`: procesa todos los videos de `VIDEO_DIRECTORY`.
- `subset`: procesa solo los videos cuyos índices estén en `SUBSET_INDICES`.
- `range`: procesa los videos entre `START_INDEX` y `END_INDEX`.
