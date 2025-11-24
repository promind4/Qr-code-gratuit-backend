
import qrcode
from qrcode.image.svg import SvgImage

def test_svg_generation():
    qr = qrcode.QRCode(box_size=10, border=4)
    qr.add_data("https://example.com")
    qr.make(fit=True)

    # Test with hex colors as used in the service
    fill_color = "#000000"
    back_color = "#ffffff"

    try:
        img = qr.make_image(
            image_factory=SvgImage,
            fill_color=fill_color,
            back_color=back_color
        )
        svg_content = img.to_string()
        if isinstance(svg_content, bytes):
            svg_content = svg_content.decode("utf-8")
        
        print("--- Generated SVG Content ---")
        print(svg_content[:500]) # Print first 500 chars
        print("...")
        print("--- End Content ---")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_svg_generation()
