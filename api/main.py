import os
import random
import time
from _md5 import md5
from datetime import datetime

from flask import Flask, request, render_template, session, flash, redirect, \
    url_for, jsonify

from celery import Celery

from elasticsearch import Elasticsearch

app = Flask('SPARK_API')
app.config['SECRET_KEY'] = 'top-secret!'

# Celery Configuration
app.config['CELERY_BROKER_URL'] = 'redis://redis:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

# Initialize Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# ElasticSearch Configuration
ES_HOST = {
    "host": "elastic",
    "port": 9200
}
ES_SPARK_JOBS_INDEX = 'spark-jobs'
ES_SPARK_JOB_DOC_TYPE = 'job'

es = Elasticsearch(hosts=[ES_HOST])


##########
# ROUTES #
##########


# Main Route
@app.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        return jsonify({}), 200, {'Ping': 'pong'}


@app.route('/submit', methods=['POST'])
def sparktask():
    if not es.indices.exists(ES_SPARK_JOBS_INDEX):
        print("Creating {0} index on ES...".format(ES_SPARK_JOBS_INDEX))
        res = es.indices.create(index=ES_SPARK_JOBS_INDEX, body={
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 0
            }
        })
        print(res)
    task_id = '{0}-{1}-{2}-{3}'.format(random.getrandbits(28), random.getrandbits(28), random.getrandbits(28)
                                       , random.getrandbits(28))
    task = {
        'current': 0,
        'total': 100,
        'status': 'Spark job pending..',
        'start_time': datetime.utcnow()
    }
    es.index(index=ES_SPARK_JOBS_INDEX, doc_type=ES_SPARK_JOB_DOC_TYPE, id=task_id, body=task)
    task['id'] = '{0}'.format(task_id)
    return jsonify(task), 202


##########
# MAIN #
##########

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='6060')
