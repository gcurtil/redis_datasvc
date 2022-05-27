import argparse
import logging
import os, os.path
import re
import time
import zlib

import numpy as np
import pandas as pd
import redis
import requests

from util import Timer, TableTimer

#https://stackoverflow.com/questions/13479295/python-using-basicconfig-method-to-log-to-console-and-file
# format='%(asctime)s %(levelname)s %(module)s %(funcName)s %(message)s',
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(module)s %(message)s',
                    handlers=[logging.StreamHandler()])


def get_url(p):
    return f"http://127.0.0.1:8090/{p}"


def do_benchmark(redis_host: str, redis_port: int, num_runs: int):
    # create redis connection
    r = redis.Redis(host=redis_host, port=redis_port, db=0)

    cmd = "list_tables"
    with Timer("req %s", cmd, verbose=True):
        resp = requests.get(get_url(cmd), {})
    logging.info("resp for <%s>: %s", cmd, resp)
    x = resp.json()
    logging.info("resp for <%s>: x: %s", cmd, type(x))
    names = x['names']
    sizes_at_rest = x['sizes_at_rest']

    num_dt_details = 4
    def dt_details(x):
        return tuple([ x.get(f"dt{i:02d}", 0.0) for i in range(num_dt_details) ])

    data = []
    for i in range(num_runs):
        for name, sz_at_rest in zip(names, sizes_at_rest):
            logging.info("calling for name: <%s>", name)
            cmd = "load_table_json_direct"
            with Timer("req %s for %s", cmd, name, verbose=True) as t1:
                resp = requests.get(get_url(cmd), { 'name' : name})
                x = resp.json()
                nb = len(x['table_data'])
                logging.info("data recv for name: <%s>: len: %d, dt: %s", 
                    name, nb, x['dt'])            
            data.append((i, cmd, name, nb, sz_at_rest, t1.elapsed(), x['dt']) + dt_details(x))
            
            for cmd in [
                "load_table_json_indirect", 
                "load_table_json_zlib_indirect",
                "load_table_json_lz4_indirect",
                "load_table_to_parquet_indirect",
                "load_table_pqarrow_indirect",
                "load_table_ftarrow_indirect",
                "load_table_rbarrow_indirect",
                "load_table_rbarrow_lz4_indirect",
            ]:
                with Timer("req %s for %s", cmd, name, verbose=True) as t:
                    resp = requests.get(get_url(cmd), { 'name' : name})
                    x = resp.json()

                    #with Timer(f"redis_connect", verbose=True):
                    #    r = redis.Redis(host=redis_host, port=redis_port, db=0)
                    with Timer(f"r.get", verbose=True):
                        table_data = r.get(x['key'])
                    with Timer(f"r.delete", verbose=True):
                        r.delete(x['key'])
                    # compression = ...

                    nb = len(table_data)
                    logging.info("data recv for name: <%s>: len: %d, dt: %s", 
                        name, nb, x['dt'])
                data.append((i, cmd, name, nb, sz_at_rest, t.elapsed(), x['dt']) + dt_details(x))


    columns=["Step", "Cmd", "Name", "clt_sz_MB", "dsk_sz_MB", 
                            "dt_client", "dt_server"] + [ f"dt{i:02d}" for i in range(num_dt_details) ]
    df = pd.DataFrame(data, columns=columns)    
    
    df["Cmd"] = df["Cmd"].str.replace("load_table_", "", regex=False)
    df["Name"] = df["Name"].str.slice(-10)
    df["clt_sz_MB"] /= 2**20
    df["dsk_sz_MB"] /= 2**20
    for c in [c for c in df.columns if re.match(r"dt[0-9]+", c)]:
        df[c] *= 1000.0
        df[c] = df[c].round(1)
    df["Speed"] = df["dsk_sz_MB"] / df["dt_client"] # MB/s
    
    return df
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Redis perf test client')
    parser.add_argument('--redis-host', default="localhost", help='redis host')
    parser.add_argument('--redis-port', type=int, default=6379, help='redis port')
    parser.add_argument('--num-runs', type=int, default=1, help='number of times to fetch data')
    args = parser.parse_args()

    df = do_benchmark(args.redis_host, args.redis_port, args.num_runs)
    
    #with pd.option_context('display.float_format', '{:0.3f}'.format):
    with pd.option_context('display.precision', 3):
        logging.info("timings: \n%s", df)
