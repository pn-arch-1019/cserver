# Sử dụng một base image có Python
FROM python:3.10-slim

# Cập nhật và cài đặt tesseract-ocr
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    && rm -rf /var/lib/apt/lists/* 

RUN apt update \
    && apt-get install ffmpeg libsm6 libxext6 -y
RUN pip3 install pytesseract
RUN pip3 install opencv-python
RUN pip3 install pillow 

# Thiết lập thư mục làm việc cho ứng dụng
WORKDIR /app

# Sao chép tệp requirements.txt vào container và cài đặt các thư viện Python cần thiết
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép mã nguồn vào container
COPY . .

# Thiết lập biến môi trường cho Django (nếu bạn sử dụng Django)
ENV DJANGO_SETTINGS_MODULE=coinserver.settings

# Chạy lệnh để khởi động server, thay đổi lệnh này tùy thuộc vào framework của bạn (Django, Flask, etc.)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]
