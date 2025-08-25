# FROM python:3.11-slim
FROM pytorch/pytorch:2.2.0-cuda12.1-cudnn8-runtime

# Set working directory
WORKDIR /app

# Copy files
COPY ./app /app
COPY setup.txt /app/

# Cài đặt dependencies
RUN pip install --upgrade pip
# RUN pip install -r setup.txt
RUN pip install --no-cache-dir -r setup.txt

# Expose port FastAPI dùng
EXPOSE 8000

# CMD khởi chạy Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
