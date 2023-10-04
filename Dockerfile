FROM python:3.9-alpine as linux-build
WORKDIR /app
COPY . .
RUN apk add patchelf build-base zstd-dev libffi-dev python3-dev
RUN pip install --upgrade pip setuptools
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir --force-reinstall -Iv cffi==1.15.1 
RUN pip install --no-cache-dir --force-reinstall -Iv grpcio==1.36.1 
RUN pip install --no-cache-dir zstandard nuitka
ENTRYPOINT python -m nuitka --standalone /app/glogger/main.py --follow-imports --output-dir='./dist/linux' --output-file='glogger' 

FROM python:3.9-alpine as windows-build
WORKDIR /app
COPY . .
RUN apk add patchelf build-base zstd-dev libffi-dev python3-dev
RUN pip install --upgrade pip setuptools
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir --force-reinstall -Iv cffi==1.15.1 
RUN pip install --no-cache-dir --force-reinstall -Iv grpcio==1.36.1 
RUN pip install --no-cache-dir zstandard nuitka
ENTRYPOINT python -m nuitka --mingw64 --standalone  /app/glogger/main.py --follow-imports --output-dir='./dist/windows' --output-file='glogger'
