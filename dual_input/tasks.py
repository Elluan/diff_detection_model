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

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

model = load_model_for_interactive()
logger.info(f"Model loaded: {model}")


minio_client = Minio(
    "minio:9000",
    access_key="1GuTxVoX2I5R9qwxC8Aq",
    secret_key="00eXWYBYKkmdkYQ4UnwnSyMZlzTDFvScCvtlSQ8Z",
    secure=False
)

def get_audio_files(bucket_name, case_name, folder):
    objects = minio_client.list_objects(bucket_name, prefix=f"{case_name}/{folder}/", recursive=True)
    files = []
    for obj in objects:
        if obj.object_name.endswith(".mp3"):
            # Načti soubor přímo do paměti
            response = minio_client.get_object(bucket_name, obj.object_name)
            file_bytes = io.BytesIO(response.read())
            files.append((obj.object_name, file_bytes))
    return files

@shared_task()
def get_dual_input_prediction(bucket_name, case_name):
    try:
        logger.info("Starting dual input prediction")
        questioned_files = get_audio_files(bucket_name, case_name, "questioned")
        ref_files = get_audio_files(bucket_name, case_name, "ref")

        _, questioned_bytes = questioned_files[0]
        _, ref_bytes = ref_files[0]

        wf1, sr1 = load(questioned_bytes)
        wf2, sr2 = load(ref_bytes)

        logger.info(f"Audio files loaded successfully {questioned_files[0]} and {ref_files[0]}")

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

        logger.info(f"Score is {result}")

        minio_client.put_object(
            bucket_name,
            f"{case_name}/result.json",
            data=io.BytesIO(data_bytes),
            length=len(data_bytes),
            content_type="application/json"
        )
        logger.info(f"Score sent to minio")
    except Exception as e:
        logger.error(f"Exception in /diff-model/: {e}")

