from torchaudio import load
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from pathlib import Path
import shutil
import logging
from celery import shared_task
from minio import Minio
import json
import io
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from load_model_for_interactive import load_model_for_interactive

# Use Uvicorn's logger
logger = logging.getLogger("uvicorn.error")

model = load_model_for_interactive()
logger.info(f"Model loaded: {model}")


minio_client = Minio(
    "minio:9000",
    access_key="1GuTxVoX2I5R9qwxC8Aq",
    secret_key="00eXWYBYKkmdkYQ4UnwnSyMZlzTDFvScCvtlSQ8Z",
    secure=False
)

@shared_task()
def get_dual_input_prediction(self, bucket_name, folder,real: UploadFile = File(...), fake: UploadFile = File(...)):
    try:
        base_path = Path("audio")  # changed to relative path for Docker safety
        base_path.mkdir(parents=True, exist_ok=True)

        pathReal = base_path / real.filename
        pathFake = base_path / fake.filename

        with open(pathReal, "wb") as f:
            shutil.copyfileobj(real.file, f)
        with open(pathFake, "wb") as f:
            shutil.copyfileobj(fake.file, f)

        logger.info(f"Saved files to {pathReal} and {pathFake}")

        wf1, sr1 = load(pathReal)
        wf2, sr2 = load(pathFake)

        logger.info("Audio files loaded successfully")

        try:
            logger.info(f"Attempting model inference with inputs: wf1={wf1.shape}, wf2={wf2.shape}")
            logger.info(f"Model loaded: {model}")
            result = model(wf1, wf2)[1].flatten()[0].item()
        except Exception as model_error:
            logger.error(f"Model inference failed with error: {model_error}")
            result = None

        result = {
            "score" : result
        }

        result_json = json.dumps(result)
        data_bytes = result_json.encode('utf-8')

        minio_client.put_object(
            bucket_name,
            f"{folder}/diff_input_result.json",
            data=io.BytesIO(data_bytes),
            length=len(data_bytes),
            content_type="application/json"
        )
            
        # result = 0.5
        logger.info(f"Model inference result: {result}")

        return JSONResponse(content={"response": result})
    except Exception as e:
        logger.error(f"Exception in /diff-model/: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})
