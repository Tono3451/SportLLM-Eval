# Guía para ejecutar

## Configurar el entorno (Anaconda)

### 1. Crear el entorno

```bash
conda create -n sport-analysis python=3.10 -y
```

### 2. Activar el entorno

```bash
conda activate sport-analysis
```

### 3. Instalar librerías

Necesitamos la librería de Ollama, OpenCV y Pillow. Ya no usaremos PyTorch ni Transformers directamente.

```bash
pip install ollama opencv-python pillow
```

## Ejecución

```bash
python main.py
```
