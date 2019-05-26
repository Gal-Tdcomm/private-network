FROM python
COPY app /app
WORKDIR /app
EXPOSE 5000
RUN ["pip","install","-r","requirements"]
CMD [ "python3", "app.py"]
