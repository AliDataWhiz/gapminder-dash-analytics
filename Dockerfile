# 1) Base image
FROM python:3.11-slim

# 2) System deps (fast, small)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

# 3) App folder
WORKDIR /app

# 4) Install Python deps first (better caching)
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


# 5) Copy your code
COPY . .

# 6) Expose the default Dash port
EXPOSE 8050

# 7) Run the app
# Your app reads PORT from env with default 8050 and binds 0.0.0.0. :contentReference[oaicite:2]{index=2}
ENV PORT=8050
CMD ["python", "app.py"]
