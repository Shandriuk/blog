FROM python:3.8
ENV PYTHONUNBUFFERED 1
ENV WEB=/blog

RUN mkdir -p $WEB


WORKDIR $WEB/
COPY requirements.txt $WEB
RUN pip3 install --upgrade pip && pip install -r requirements.txt
ADD . $WEB
