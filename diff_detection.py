from load_model_for_interactive import load_model_for_interactive
from torchaudio import load
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from pathlib import Path
import shutil

model = load_model_for_interactive()

app = FastAPI()

@app.post("/diff-model/")
async def diff_model(real: UploadFile = File(...), fake: UploadFile = File(...)):

    base_path = Path("/model/audio")
    base_path.mkdir(parents=True, exist_ok=True)

    pathReal = base_path / real.filename
    pathFake = base_path / fake.filename

    with open(pathReal, "wb") as f:
        shutil.copyfileobj(real.file, f)
    with open(pathFake, "wb") as f:
        shutil.copyfileobj(fake.file, f)
    
    wf1, sr1 = load(pathReal)
    wf2, sr2 = load(pathFake)

    return JSONResponse(content={"response" : model(wf1, wf2)[1].flatten()[0].item()})
    

