FROM python:3.10

WORKDIR /model

COPY . /model

RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
RUN pip3 install -r requirements.txt
RUN pip install --no-cache-dir fastapi uvicorn
RUN pip install pathlib 
RUN pip install python-multipart

EXPOSE 8000

CMD ["uvicorn", "diff_detection:app", "--host", "0.0.0.0", "--port", "8000"]