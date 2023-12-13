# 
FROM python:3.11

# 
# WORKDIR /backend

# 
COPY ./requirements.txt ./requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

# 
COPY . .

#
EXPOSE 8005

# 
CMD ["python", "main.py"]