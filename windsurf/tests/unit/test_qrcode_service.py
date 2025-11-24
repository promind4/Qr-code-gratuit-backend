import pytest

from src.schemas.qrcode import QRCodeFormat, QRCodeRequest
from src.services.qrcode_service import generate_qr


@pytest.mark.parametrize("format", [QRCodeFormat.png, QRCodeFormat.jpeg, QRCodeFormat.svg, QRCodeFormat.pdf])
def test_generate_all_formats(format: QRCodeFormat):
    payload = QRCodeRequest(content="https://windsurf.dev", format=format)
    request_id, payload_bytes, content_type = generate_qr(payload)

    assert request_id
    assert isinstance(payload_bytes, (bytes, bytearray))
    assert content_type.startswith("image") or format == QRCodeFormat.pdf
    assert len(payload_bytes) > 0


def test_generate_invalid_error_correction():
    with pytest.raises(ValueError):
        QRCodeRequest(content="text", error_correction="Z")
