import os
import uuid
from flask import request
from werkzeug.utils import secure_filename
from PIL import Image

# Configuración de carpetas y extensiones permitidas
UPLOAD_FOLDER = "app/public/assets/imagestemp"
THUMBNAIL_FOLDER = os.path.join("app", "public","assets", "thumbnails")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
THUMBNAIL_SIZE = (150, 150)  # Tamaño del thumbnail

# Asegurar que las carpetas existen
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(THUMBNAIL_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Verifica si el archivo tiene una extensión permitida."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_file():
    """Guarda la imagen subida y genera un thumbnail."""
    if 'file' not in request.files:
        return None, "No se encontró el archivo en la solicitud."
    
    file = request.files['file']
    
    if file.filename == '':
        return None, "El nombre del archivo está vacío."
    
    if not allowed_file(file.filename):
        return None, "Extensión de archivo no permitida."
    
    file.seek(0, os.SEEK_END)
    file_length = file.tell()
    file.seek(0)
    
    if file_length > MAX_FILE_SIZE:
        return None, "El archivo excede el tamaño máximo permitido de 5MB."
    
    file_extension = file.filename.rsplit('.', 1)[1].lower()
    unique_filename = secure_filename(f"{uuid.uuid4()}.{file_extension}")
    filepath = os.path.join(UPLOAD_FOLDER, unique_filename)
    
    try:
        # Guardar imagen original
        file.save(filepath)

        # Crear y guardar thumbnail
        thumbnail_success = create_thumbnail(filepath, unique_filename)
        if not thumbnail_success:
            os.remove(filepath)  
            return None, "Error al crear el thumbnail."
        
        return unique_filename, None
    except Exception as e:
        print(f"Error al guardar la imagen: {e}")
        return None, "Error al guardar la imagen."

def create_thumbnail(image_path, filename):
    """Crea un thumbnail de la imagen subida."""
    try:
        img = Image.open(image_path)
        img = img.convert("RGB")  
        img.thumbnail(THUMBNAIL_SIZE)

        thumbnail_filename = f"{filename.rsplit('.', 1)[0]}.jpg" 
        thumbnail_path = os.path.join(THUMBNAIL_FOLDER, secure_filename(thumbnail_filename))

        img.save(thumbnail_path, "JPEG")  

        print(f"Thumbnail creado correctamente en: {thumbnail_path}")
        return True
    except Exception as e:
        print(f"Error al crear el thumbnail para {image_path}: {e}")
        return False

def delete_file(filename):
    """Elimina la imagen y su thumbnail asociado."""
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    thumbnail_filename = f"{filename.rsplit('.', 1)[0]}.jpg"  
    thumbnail_path = os.path.join(THUMBNAIL_FOLDER, thumbnail_filename)
    
    for path in [file_path, thumbnail_path]:
        if os.path.exists(path):
            os.remove(path)

    return True

def delete_thumbnail(filename):
    """Elimina el thumbnail asociado con la imagen."""
    thumbnail_filename = f"{filename.rsplit('.', 1)[0]}.jpg"  
    thumbnail_path = os.path.join(THUMBNAIL_FOLDER, secure_filename(thumbnail_filename))

    if os.path.exists(thumbnail_path):
        os.remove(thumbnail_path)
        print(f"Thumbnail {thumbnail_filename} eliminado correctamente.")
    else:
        print(f"No se encontró el thumbnail {thumbnail_filename}.")





