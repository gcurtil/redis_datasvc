import argparse
from contextlib import closing 
import io
import logging
import os, os.path
from sre_compile import isstring
import time
import uuid
import zlib

import lz4.frame
import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.feather as ft
import pyarrow.parquet as pq

from flask import Flask, request, jsonify
import redis
import waitress

from util import Timer, TableTimer


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(module)s %(message)s',
                    handlers=[logging.StreamHandler()])


app = Flask(__name__)

REDIS_HOST = ""
REDIS_PORT = 0
TABLE_DATA_DIR = 'test_data'
REDIS_R_OBJ: redis.Redis = None

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/list_tables")
def list_tables():
    with Timer("os.listdir", verbose=True) as t:
        fnames = os.listdir(TABLE_DATA_DIR)
        sizes = [ os.path.getsize(os.path.join(TABLE_DATA_DIR, p)) for p in fnames ]
    
    data = {
        'names'  : fnames,
        'sizes_at_rest' : sizes,
        'dt'    : t.elapsed(),
    }
    return jsonify(data)

@app.route("/load_table_1")
def load_table_1():
    p = os.path.join(TABLE_DATA_DIR, 'enhanced_sur_covid_19_eng.csv')
    with Timer("pd.read_csv(%s)", p, verbose=True) as t:
        df = pd.read_csv(p)
    data = {
        'path'  : p,
        'shape' : df.shape,
        'dt'    : t.elapsed(),
    }
    return jsonify(data)

def push_timer_stats(data, timers):
    total = 0.0
    for i, t in enumerate(timers):
        dt = t.elapsed()
        data[f"dt{i:02d}"] = dt
        total += dt
    data["dt"] = total

@app.route("/load_table_json_direct")
def load_table_json_direct():
    name = request.args.get('name')
    timers = []
    p = os.path.join(TABLE_DATA_DIR, name)
    with Timer("pd.read_csv(%s)", p, verbose=True) as t:
        df = pd.read_csv(p)    
    timers.append(t)
    with Timer("df.to_json()", verbose=True) as t:
        table_data = df.to_json(date_format='iso')
    timers.append(t)
    
    data = {
        'name'  : name,
        'table_data' : table_data,        
    }
    push_timer_stats(data, timers)

    return jsonify(data)


@app.route("/load_table_json_indirect")
def load_table_json_indirect():
    return load_table_json_compr_indirect(compression="none")

@app.route("/load_table_json_zlib_indirect")
def load_table_json_zlib_indirect():    
    return load_table_json_compr_indirect(compression="zlib")

@app.route("/load_table_json_lz4_indirect")
def load_table_json_lz4_indirect():    
    return load_table_json_compr_indirect(compression="lz4")

@app.route("/load_table_to_parquet_indirect")
def load_table_to_parquet_indirect():
    return load_table_json_compr_indirect(binfmt="to_parquet", compression="none")

@app.route("/load_table_pqarrow_indirect")
def load_table_pqarrow_indirect():
    return load_table_json_compr_indirect(binfmt="pqarrow", compression="none")

@app.route("/load_table_ftarrow_indirect")
def load_table_ftarrow_indirect():
    return load_table_json_compr_indirect(binfmt="ftarrow", compression="none")

@app.route("/load_table_rbarrow_indirect")
def load_table_rbarrow_indirect():
    return load_table_json_compr_indirect(binfmt="rbarrow", compression="none")

@app.route("/load_table_rbarrow_lz4_indirect")
def load_table_rbarrow_lz4_indirect():
    return load_table_json_compr_indirect(binfmt="rbarrow", compression="lz4")

def load_table_json_compr_indirect(binfmt=None, compression=None):
    name = request.args.get('name')
    p = os.path.join(TABLE_DATA_DIR, name)
    timers = []    

    def to_bin(data):
        return data.encode("utf-8") if isinstance(data, str) else data

    with Timer("pd.read_csv(%s)", p, verbose=True) as t:
        df = pd.read_csv(p)
    timers.append(t)

    binfmt = "to_json" if binfmt is None else binfmt
    with Timer(f"df_to_bin_{binfmt}", verbose=True) as t:
        if binfmt == "to_json":
            table_data = df.to_json(date_format='iso')
        elif binfmt == "to_parquet":
            buffer = io.BytesIO()
            df.to_parquet(buffer, engine='auto')
            table_data = buffer.getvalue()
        elif binfmt == "rbarrow":
            rb = pa.RecordBatch.from_pandas(df)
            sink = pa.BufferOutputStream()
            with closing(pa.RecordBatchStreamWriter(sink, rb.schema)) as writer:
                writer.write_batch(rb)
            table_data = sink.getvalue().to_pybytes()            
        elif binfmt == "ftarrow":
            buf = pa.BufferOutputStream()
            #table = pa.Table.from_pandas(df)            
            #ft.write_feather(table, buf)
            ft.write_feather(df, buf)
            table_data = buf.getvalue().to_pybytes()
        elif binfmt == "pqarrow":
            table = pa.Table.from_pandas(df)
            buf = pa.BufferOutputStream()
            pq.write_table(table, buf)
            table_data = buf.getvalue().to_pybytes()
        else:
            raise Exception(f"unknown binfmt {binfmt}")
    timers.append(t)    
    
    with Timer(f"compress_{compression}", verbose=True) as t:
        if compression == "zlib":
            table_data = zlib.compress(to_bin(table_data), level=1)
        elif compression == "lz4":
            table_data = lz4.frame.compress(to_bin(table_data))
        elif compression == "none":
            pass
    timers.append(t)

    # now insert into redis
    with Timer("store", verbose=True) as t:
        uk =  uuid.uuid4().hex
        key = f"tmpdoc:{uk}"
        #with Timer(f"redis_connect", verbose=True):
        #    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
        r = REDIS_R_OBJ
        with Timer(f"r.set", verbose=True):
            r.set(key, table_data, ex=30) # 30s expiry 
    timers.append(t)

    data = {
        'name'  : name,
        'key'   : key,        
    }
    push_timer_stats(data, timers)
    return jsonify(data)



def main():
    #from waitress import serve
    #serve(app, host='0.0.0.0', port=8090)
    parser = argparse.ArgumentParser(description='Redis perf test server')
    parser.add_argument('--redis-host', default="127.0.0.1", help='redis host')
    parser.add_argument('--redis-port', type=int, default=6379, help='redis port')
    args = parser.parse_args()
    global REDIS_HOST, REDIS_PORT, REDIS_R_OBJ
    REDIS_HOST = args.redis_host
    REDIS_PORT = args.redis_port
    

    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
    logging.info("Redis connection: %s", r)
    REDIS_R_OBJ = r

    #app.run(host='0.0.0.0', port=8090, debug=True)    
    waitress.serve(app, host='0.0.0.0', port=8090)


if __name__=='__main__':
    main()
