import os
from PIL import Image

IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.bmp', '.webp')

def _log(msg, logger):
    if logger:
        logger(msg)

def _convert_folder_images_to_pdf(folder_path, logger=None):
    files = os.listdir(folder_path)

    image_files = [
        f for f in files
        if f.lower().endswith(IMAGE_EXTENSIONS)
        and os.path.isfile(os.path.join(folder_path, f))
    ]

    if not image_files:
        return

    image_files.sort()

    images = []
    for name in image_files:
        path = os.path.join(folder_path, name)
        try:
            img = Image.open(path).convert("RGB")
            images.append(img)
        except Exception as e:
            _log(f"❌ Failed to open {path}: {e}", logger)
            return

    pdf_name = os.path.basename(folder_path) + ".pdf"
    pdf_path = os.path.join(folder_path, pdf_name)

    try:
        images[0].save(
            pdf_path,
            save_all=True,
            append_images=images[1:]
        )
        _log(f"✔ PDF created: {pdf_path}", logger)
    except Exception as e:
        _log(f"❌ PDF save failed in {folder_path}: {e}", logger)

def scan_and_convert(root_folder, logger=None):
    root_folder = os.path.normpath(root_folder)

    if not os.path.isdir(root_folder):
        _log(f"Invalid root folder: {root_folder}", logger)
        return

    for current_root, dirs, files in os.walk(root_folder):
        _convert_folder_images_to_pdf(current_root, logger)
