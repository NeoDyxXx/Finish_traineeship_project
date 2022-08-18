from elasticsearch import Elasticsearch
import json
from elasticsearch.helpers import scan
import pandas as pd
from time import sleep
from datetime import datetime

es = Elasticsearch("http://localhost:9200")