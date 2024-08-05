FROM python:3.12


RUN apt-get update && \
    apt-get install -y openjdk-17-jdk && \
    apt-get clean;


ENV JAVA_HOME /usr/lib/jvm/java-17-openjdk-amd64
ENV PATH $JAVA_HOME/bin:$PATH

WORKDIR /app


ADD app/ .

# Installer les dépendances Python
RUN pip install -r requirements.txt

# Exposer le port de l'application
EXPOSE 5000

# Lancer l'application
CMD ["flask", "run", "--host=0.0.0.0" ,"--port=5000"]
