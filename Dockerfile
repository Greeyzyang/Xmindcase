FROM python:3.7
MAINTAINER Greey
WORKDIR /Xmind_Tapd
COPY . .
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
CMD ["gunicorn", "flask_web:app", "-c", "./gunicorn.conf.py"]
