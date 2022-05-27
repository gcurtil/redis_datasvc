import logging
import os, os.path
import time

import numpy as np
import pandas as pd
import redis

from util import Timer, TableTimer

#https://stackoverflow.com/questions/13479295/python-using-basicconfig-method-to-log-to-console-and-file
# format='%(asctime)s %(levelname)s %(module)s %(funcName)s %(message)s',
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(module)s %(message)s',
                    handlers=[logging.StreamHandler()])



def covid_data():
    #"enhanced_sur_covid_19_eng.csv"
    rootdir = 'test_data'
    with Timer("os.listdir for <%s>", rootdir, verbose=True) as t1:
        fnames = [ p for p in os.listdir(rootdir) if p.endswith('.csv') ]
    logging.info("after listdir, timer value is %f", t1.elapsed())

    logging.info("rootdir: %s, fnames: %s", rootdir, fnames)
    for p in [ os.path.join(rootdir, fname) for fname in fnames ]:
        for _ in range(3):
            with Timer("pd.read_csv(%s)", p, verbose=True):
                df = pd.read_csv(p)
            logging.info("p: %s, df: %s", p, df.shape)
            logging.info("")


def test_get_set():
    tt = TableTimer()    
    with tt.timer(f"initial"):
        pass
    with tt.timer(f"redis_connect"):
        r = redis.Redis(host='localhost', port=6379, db=0)
    logging.info("r: %s", r)

    for i in range(4):
        with tt.timer(f"step_{i}"):
            k, v = 'foo', f"val_{i}"
            logging.info("setting %s to %s", k, v)
            r.set(k, v)
            x = r.get(k)
        logging.info("x: %s", x)
        
    print(tt.table())

def main():
    #covid_data()
    test_get_set()

if __name__ == '__main__':
    main()
