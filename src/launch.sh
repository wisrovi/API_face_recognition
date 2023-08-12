uvicorn api:app --host 0.0.0.0 --port 1722 --reload


#gunicorn -w 4 -k uvicorn.workers.UvicornWorker api:app 
gunicorn -b 0.0.0.0:1722 -w 4 -k uvicorn.workers.UvicornWorker api:app
gunicorn -b 0.0.0.0:1722 -w 4 -t 120 -k uvicorn.workers.UvicornWorker --access-logfile access.log --log-level info api:app
