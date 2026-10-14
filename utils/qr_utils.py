"""
CampusPass - QR Code Utility
Generates scannable QR ticket codes using qrcode and Pillow.
"""

import io
import qrcode
from PIL import Image

def generate_qr_image(payload: str, box_size: int = 10, border: int = 2) -> Image.Image:
    """
    Generates a PIL Image of the QR code with given payload.
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=box_size,
        border=border,
    )
    qr.add_data(payload)
    qr.make(fit=True)

    img = qr.make_image(fill_color="#0F172A", back_color="#FFFFFF")
    return img.convert("RGB")

def get_qr_image_bytes(payload: str) -> bytes:
    """
    Returns PNG bytes of the generated QR code for download or display.
    """
    img = generate_qr_image(payload)
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    return buffer.getvalue()
