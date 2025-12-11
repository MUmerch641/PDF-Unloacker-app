from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from starlette.background import BackgroundTask
import pikepdf
import os
import shutil
import uuid
import subprocess
from fastapi.middleware.cors import CORSMiddleware
import itertools

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
PROCESSED_DIR = "processed"
ROCKYOU_PATH = "rockyou.txt"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

QUICK_PASSWORDS = [
    "", " ", "password", "Password", "PASSWORD", "123456", "12345678", "1234",
    "qwerty", "admin", "letmein", "welcome", "123", "1234567890", "000000",
]

def try_unlock_with_password(input_path: str, output_path: str, password: str) -> bool:
    try:
        pdf = pikepdf.open(input_path, password=password)
        pdf.save(output_path)
        pdf.close()
        return True
    except pikepdf.PasswordError:
        return False
    except Exception:
        return False

def try_unlock_with_qpdf(input_path: str, output_path: str, password: str) -> bool:
    try:
        result = subprocess.run(
            ["qpdf", "--password=" + password, "--decrypt", input_path, output_path],
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.returncode == 0 and os.path.exists(output_path)
    except Exception:
        return False

def try_rockyou_wordlist(input_path: str, output_path: str, max_attempts: int = 100000) -> bool:
    if not os.path.exists(ROCKYOU_PATH):
        return False
    
    count = 0
    try:
        with open(ROCKYOU_PATH, 'r', encoding='latin-1', errors='ignore') as f:
            for line in f:
                if count >= max_attempts:
                    break
                
                password = line.strip()
                if not password:
                    continue
                    
                count += 1
                
                if try_unlock_with_password(input_path, output_path, password):
                    return True
                    
    except Exception:
        pass
    
    return False

def try_numeric_bruteforce(input_path: str, output_path: str, max_digits: int = 6) -> bool:
    for length in range(1, max_digits + 1):
        for p in itertools.product("0123456789", repeat=length):
            password = "".join(p)
            if try_unlock_with_password(input_path, output_path, password):
                return True
    return False

@app.post("/unlock-pdf")
async def unlock_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDFs are allowed.")

    file_id = str(uuid.uuid4())
    input_path = os.path.join(UPLOAD_DIR, f"{file_id}.pdf")
    output_path = os.path.join(PROCESSED_DIR, f"{file_id}_unlocked.pdf")

    try:
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        unlocked = False
        
        try:
            pdf = pikepdf.open(input_path)
            pdf.save(output_path)
            pdf.close()
            unlocked = True
        except pikepdf.PasswordError:
            pass
        except Exception as e:
            if os.path.exists(input_path):
                os.remove(input_path)
            raise HTTPException(status_code=500, detail=str(e))
        
        if not unlocked:
            for password in QUICK_PASSWORDS:
                if try_unlock_with_password(input_path, output_path, password):
                    unlocked = True
                    break
        
        if not unlocked:
            unlocked = try_rockyou_wordlist(input_path, output_path, max_attempts=30000)

        if not unlocked:
            unlocked = try_numeric_bruteforce(input_path, output_path, max_digits=4)
        
        if not unlocked:
            if os.path.exists(input_path):
                os.remove(input_path)
            raise HTTPException(
                status_code=400, 
                detail="Could not unlock PDF. Password is likely complex."
            )
            
        def cleanup():
            if os.path.exists(input_path):
                os.remove(input_path)
            if os.path.exists(output_path):
                os.remove(output_path)

        return FileResponse(output_path, media_type="application/pdf", filename=f"unlocked_{file.filename}", background=BackgroundTask(cleanup))

    except HTTPException:
        raise
    except Exception as e:
        if os.path.exists(input_path):
            os.remove(input_path)
        raise HTTPException(status_code=500, detail=str(e))
