import httpx
import asyncio
import os

BASE_URL = "http://127.0.0.1:8000/api/v1/upload/"

async def test_upload():
    print("Testing Upload...")
    
    # Create dummy files
    with open("test.png", "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n" + b"\x00" * 100) # Valid PNG header
    
    with open("test.txt", "wb") as f:
        f.write(b"Hello World")

    with open("large.png", "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n" + b"\x00" * (2 * 1024 * 1024 + 100)) # > 2MB

    async with httpx.AsyncClient() as client:
        # 1. Valid Upload
        try:
            files = {"file": ("test.png", open("test.png", "rb"), "image/png")}
            response = await client.post(BASE_URL, files=files)
            if response.status_code == 200:
                print("Valid Upload: Success")
                print(response.json())
            else:
                print(f"Valid Upload Failed: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Valid Upload Exception: {e}")

        # 2. Invalid Type
        try:
            files = {"file": ("test.txt", open("test.txt", "rb"), "text/plain")}
            response = await client.post(BASE_URL, files=files)
            if response.status_code == 400:
                print("Invalid Type Check: Success (Rejected)")
            else:
                print(f"Invalid Type Check Failed: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Invalid Type Exception: {e}")

        # 3. Too Large
        try:
            files = {"file": ("large.png", open("large.png", "rb"), "image/png")}
            response = await client.post(BASE_URL, files=files)
            if response.status_code == 413:
                print("Size Limit Check: Success (Rejected)")
            else:
                print(f"Size Limit Check Failed: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Size Limit Exception: {e}")

    # Cleanup
    try:
        os.remove("test.png")
        os.remove("test.txt")
        os.remove("large.png")
    except:
        pass

if __name__ == "__main__":
    asyncio.run(test_upload())
