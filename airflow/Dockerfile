FROM astrocrpublic.azurecr.io/runtime:3.1-14


RUN airflow users create \
    --username admin \
    --password admin \
    --firstname admin \
    --lastname user \
    --role Admin \
    --email admin@test.com || true