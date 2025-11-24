from io import BytesIO
from uuid import uuid4
import httpx
from PIL import Image

import qrcode
from qrcode.constants import (
    ERROR_CORRECT_L,
    ERROR_CORRECT_M,
    ERROR_CORRECT_Q,
    ERROR_CORRECT_H,
)
from qrcode.image.pil import PilImage
from qrcode.image.svg import SvgImage
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import (
    SquareModuleDrawer,
    GappedSquareModuleDrawer,
    CircleModuleDrawer,
    RoundedModuleDrawer,
    VerticalBarsDrawer,
    HorizontalBarsDrawer,
)
from qrcode.image.styles.colormasks import SolidFillColorMask

from src.schemas.qrcode import QRCodeFormat, QRCodeRequest

ERROR_CORRECTION_MAP = {
    "L": ERROR_CORRECT_L,
    "M": ERROR_CORRECT_M,
    "Q": ERROR_CORRECT_Q,
    "H": ERROR_CORRECT_H,
}

CONTENT_TYPES = {
    QRCodeFormat.png: "image/png",
    QRCodeFormat.jpeg: "image/jpeg",
    QRCodeFormat.svg: "image/svg+xml",
    QRCodeFormat.pdf: "application/pdf",
}

MODULE_DRAWERS = {
    "square": SquareModuleDrawer(),
    "gapped": GappedSquareModuleDrawer(),
    "circle": CircleModuleDrawer(),
    "rounded": RoundedModuleDrawer(),
    "vertical": VerticalBarsDrawer(),
    "horizontal": HorizontalBarsDrawer(),
}

EYE_DRAWERS = {
    "square": SquareModuleDrawer(),
    "circle": CircleModuleDrawer(),
    "rounded": RoundedModuleDrawer(),
}


def _build_qr(payload: QRCodeRequest) -> qrcode.QRCode:
    return qrcode.QRCode(
        version=None,
        error_correction=ERROR_CORRECTION_MAP[payload.error_correction],
        box_size=10,
        border=payload.margin,
    )


def _hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


from pathlib import Path

def _get_logo_image(url: str) -> Image.Image | None:
    try:
        # Check if it's a local upload (simple check based on URL structure)
        # Assumes running from project root where 'uploads' dir exists
        if "/uploads/" in url:
            filename = url.split("/uploads/")[-1]
            local_path = Path("uploads") / filename
            if local_path.exists():
                return Image.open(local_path)
        
        # Fallback to HTTP fetch for external URLs with retry
        retries = 2
        for attempt in range(retries + 1):
            try:
                response = httpx.get(url, timeout=10.0) # Increased timeout
                response.raise_for_status()
                return Image.open(BytesIO(response.content))
            except (httpx.RequestError, httpx.HTTPStatusError):
                if attempt == retries:
                    raise
                import time
                time.sleep(0.5 * (attempt + 1)) # Backoff
                
    except Exception as e:
        print(f"Failed to load logo: {e}")
        return None


def _render_pil(payload: QRCodeRequest) -> Image.Image:
    qr = _build_qr(payload)
    qr.add_data(payload.content)
    qr.make(fit=True)

    # If default styles and no logo, use standard generation for speed
    if (
        payload.body_style == "square"
        and payload.eye_style == "square"
        and not payload.logo_url
    ):
        pil_img = qr.make_image(
            image_factory=PilImage,
            fill_color=payload.color,
            back_color=payload.background,
        ).get_image()
        return pil_img.resize((payload.size, payload.size), Image.LANCZOS)

    # Advanced styling
    module_drawer = MODULE_DRAWERS.get(payload.body_style, SquareModuleDrawer())
    eye_drawer = EYE_DRAWERS.get(payload.eye_style, SquareModuleDrawer())
    
    rgb_front = _hex_to_rgb(payload.color)
    rgb_back = _hex_to_rgb(payload.background)
    
    color_mask = SolidFillColorMask(
        back_color=rgb_back,
        front_color=rgb_front,
    )

    img = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=module_drawer,
        eye_drawer=eye_drawer,
        color_mask=color_mask,
    )
    
    pil_img = img.get_image() if hasattr(img, "get_image") else img

    # Handle Logo
    if payload.logo_url:
        logo = _get_logo_image(payload.logo_url)
        if logo:
            # Resize logo to 20% of QR code size
            qr_width, qr_height = pil_img.size
            logo_size = int(qr_width * 0.2)
            logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
            
            # Calculate position
            pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
            
            # Paste with mask if RGBA
            mask = logo if logo.mode == "RGBA" else None
            pil_img.paste(logo, pos, mask=mask)

    return pil_img.resize((payload.size, payload.size), Image.LANCZOS)


def _composite_with_sticker(qr_img: Image.Image, sticker_type: str) -> Image.Image:
    """Composite QR code with a ScanMe sticker frame - QR overlays on sticker"""
    try:
        from pathlib import Path
        from cairosvg import svg2png
        
        # Path to sticker SVG
        # Backend runs in 'windsurf' dir, so we need to go up one level to reach 'frontend'
        sticker_path = Path("../frontend/public/stickers") / f"{sticker_type}.svg"
        if not sticker_path.exists():
            return qr_img  # Return original if sticker not found
        
        # Read SVG
        svg_data = sticker_path.read_text(encoding="utf-8")
        
        # Sticker dimensions based on QR size
        # Sticker should be larger to frame the QR code
        sticker_scale = 1.4  # 40% larger than QR
        sticker_width = int(qr_img.width * sticker_scale)
        sticker_height = int(qr_img.width * sticker_scale * 1.15)  # Slightly taller for frames
        
        # Convert SVG to PNG
        png_bytes = svg2png(
            bytestring=svg_data.encode('utf-8'),
            output_width=sticker_width,
            output_height=sticker_height
        )
        
        sticker_img = Image.open(BytesIO(png_bytes)).convert("RGBA")
        
        # Create canvas with sticker size
        canvas = Image.new("RGB", (sticker_width, sticker_height), (255, 255, 255))
        
        # Paste sticker as background
        canvas.paste(sticker_img, (0, 0), sticker_img if sticker_img.mode == "RGBA" else None)
        
        # Calculate position to center QR code on sticker
        # Position depends on sticker type - adjust for each frame design
        qr_positions = {
            "grid": (int(sticker_width * 0.08), int(sticker_height * 0.17)),  # Below top banner
            "bubble": (int(sticker_width * 0.08), int(sticker_height * 0.17)),  # Below bubble top
            "film": (int(sticker_width * 0.08), int(sticker_height * 0.20)),  # Below clapperboard
            "book": (int(sticker_width * 0.55), int(sticker_height * 0.17)),  # Right page
            "beer": (int(sticker_width * 0.33), int(sticker_height * 0.44)),  # Center of cup
        }
        
        qr_pos = qr_positions.get(sticker_type, (int((sticker_width - qr_img.width) / 2), int((sticker_height - qr_img.height) / 2)))
        
        # Paste QR code on top of sticker
        if qr_img.mode == "RGBA":
            canvas.paste(qr_img, qr_pos, qr_img)
        else:
            # Convert to RGBA if needed
            qr_rgba = qr_img.convert("RGBA")
            canvas.paste(qr_rgba, qr_pos, qr_rgba)
        
        return canvas
        
    except Exception as e:
        print(f"Error compositing sticker: {e}")
        import traceback
        traceback.print_exc()
        return qr_img  # Return original on error



def generate_qr(payload: QRCodeRequest) -> tuple[str, bytes, str]:
    request_id = str(uuid4())
    
    # SVG Handling
    if payload.format == QRCodeFormat.svg:
        from qrcode.image.svg import SvgPathImage
        
        qr = _build_qr(payload)
        qr.add_data(payload.content)
        qr.make(fit=True)
        
        # SvgPathImage creates a single path for the QR code
        # It handles colors via fill_color and back_color arguments
        svg_img = qr.make_image(
            image_factory=SvgPathImage,
            fill_color=payload.color,
            back_color=payload.background,
        )
        
        svg_content = svg_img.to_string()
        if isinstance(svg_content, bytes):
            svg_content = svg_content.decode("utf-8")
            
        # Inject width and height to enforce requested size
        # SvgPathImage usually produces <svg ... width="Xmm" height="Ymm" ...>
        # We want to force pixels for web display consistency
        import re
        
        # Replace existing width/height with requested pixel size
        # Note: We use regex to safely replace existing attributes
        if 'width="' in svg_content:
            svg_content = re.sub(r'width="[^"]*"', f'width="{payload.size}px"', svg_content)
        else:
            svg_content = svg_content.replace('<svg', f'<svg width="{payload.size}px"', 1)
            
        if 'height="' in svg_content:
            svg_content = re.sub(r'height="[^"]*"', f'height="{payload.size}px"', svg_content)
        else:
            svg_content = svg_content.replace('<svg', f'<svg height="{payload.size}px"', 1)
            
        # Ensure viewBox is preserved (it usually is)
        
        svg_bytes = svg_content.encode("utf-8")
            
        return request_id, svg_bytes, CONTENT_TYPES[payload.format]

    # PIL Generation (PNG, JPEG, PDF)
    pil_image = _render_pil(payload)
    
    # Add sticker if requested
    if payload.sticker_type:
        pil_image = _composite_with_sticker(pil_image, payload.sticker_type)
    
    buffer = BytesIO()
    
    if payload.format == QRCodeFormat.pdf:
        # For PDF, we prefer vector if possible, but since we are using PIL for composition/styling
        # (especially with stickers), we will save the high-res image as PDF.
        # To ensure high quality, we might want to upscale if it's small, but _render_pil 
        # already respects 'size' payload.
        
        # If no sticker and simple style, we COULD use vector PDF via cairosvg on the SVG output,
        # but for consistency and sticker support, we'll use PIL's PDF save.
        # It embeds the raster image in PDF.
        if pil_image.mode == "RGBA":
            # PDF doesn't support RGBA, convert to RGB with white background
            bg = Image.new("RGB", pil_image.size, (255, 255, 255))
            bg.paste(pil_image, mask=pil_image.split()[3])
            bg.save(buffer, format="PDF", resolution=300)
        else:
            pil_image.convert("RGB").save(buffer, format="PDF", resolution=300)
            
        return request_id, buffer.getvalue(), CONTENT_TYPES[payload.format]
        
    else:
        # PNG / JPEG
        output_format = payload.format.value.upper()
        if output_format == "JPEG":
             pil_image.convert("RGB").save(buffer, format=output_format, quality=95)
        else:
             pil_image.save(buffer, format=output_format)
             
    return request_id, buffer.getvalue(), CONTENT_TYPES[payload.format]
