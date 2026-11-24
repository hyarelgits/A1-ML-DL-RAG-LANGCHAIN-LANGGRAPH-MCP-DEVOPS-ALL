FROM python:3.10
# # FROM python:3.10 = Take base image Python 3.10 - Like base Tiffin
WORKDIR /app
# # WORKDIR /app = Work inside /app folder in container
COPY requirements.txt .
# # COPY requirements.txt . = Copy requirements file to /app
RUN pip install -r requirements.txt
# # RUN = Run command in container - Install packages
COPY . .
# # COPY . . = Copy all backend files to /app
EXPOSE 8000
# # EXPOSE 8000 = Open port 8000 in container
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
# # CMD = Command to run when container starts - Start FastAPI
