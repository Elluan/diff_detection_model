FROM python:3.10

WORKDIR /app

COPY . /app

RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
RUN pip3 install -r requirements.txt
RUN pip install --no-cache-dir fastapi uvicorn
RUN pip install pathlib 
RUN pip install python-multipart

EXPOSE 8000

CMD [ "celery", "-A", "dual_input", "worker", "--loglevel=debug", "-n", "worker_dual", "-Q", "dual_input"]