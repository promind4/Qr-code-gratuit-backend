import httpx
import json
import asyncio

BASE_URL = "http://127.0.0.1:8000/api/v1/qrcode/generate"

async def test_svg():
    print("Testing SVG generation...")
    payload = {
        "content": "https://example.com",
        "color": "#000000",
        "background": "#ffffff",
        "size": 500,
        "margin": 1,
        "format": "svg",
        "error_correction": "M"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(BASE_URL, json=payload)
            if response.status_code == 200:
                print("SVG Success")
                with open("test.svg", "wb") as f:
                    f.write(response.content)
                print("Saved test.svg")
                # Check content
                content = response.content.decode('utf-8')
                if 'width="500px"' in content:
                    print("SVG Width correct")
                else:
                    print("SVG Width INCORRECT")
            else:
                print(f"SVG Failed: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"SVG Exception: {e}")

async def test_pdf():
    print("\nTesting PDF generation...")
    payload = {
        "content": "https://example.com",
        "color": "#000000",
        "background": "#ffffff",
        "size": 500,
        "margin": 1,
        "format": "pdf",
        "error_correction": "M"
    }
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(BASE_URL, json=payload)
            if response.status_code == 200:
                print("PDF Success")
                with open("test.pdf", "wb") as f:
                    f.write(response.content)
                print(f"Saved test.pdf (Size: {len(response.content)} bytes)")
            else:
                print(f"PDF Failed: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"PDF Exception: {repr(e)}")

if __name__ == "__main__":
    asyncio.run(test_svg())
    asyncio.run(test_pdf())
