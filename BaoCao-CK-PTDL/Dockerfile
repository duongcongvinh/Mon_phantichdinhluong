FROM python:3-slim

# Prevent Python from generating .pyc files in containers
ENV PYTHONDONTWRITEBYTECODE=1

# Disable caching to easily log from containers
ENV PYTHONUNBUFFERED=1

# Copy and install Python dependencies
COPY requirements.txt ./BaoCao
RUN python -m pip install -r requirements.txt

# Set working directory
WORKDIR /usr/src/app

# Copy and install Python dependencies
COPY requirements.txt ./BaoCao
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Define the default command
CMD ["sh", "-c", "sleep 60 && python -m scrapy runspider myAmazon/myAmazon/spiders/amazon.py"]