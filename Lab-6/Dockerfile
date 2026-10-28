FROM python:3.11-slim

# no __pycache__ written into the mounted folder, print output shows immediately
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
COPY product.py inventory.py inventory_manager.py ./

CMD ["python", "inventory_manager.py"]
