# datasvc

Will need:

- a redis server
- pip install the packages for Arrow in a conda env
- Docker-compose file to start the python service / redis etc.
- could also use supervisor and do a multi-service container

### Python

```
conda create -n datasvc python=3.8 
Collecting package metadata (current_repodata.json): done

```

New environment for ```datasvc```.
```
conda activate datasvc
(datasvc) gui@monolith:~/devel/datasvc$ 
```

### Redis

We can do a few differents ways:

- the official docker image for sth simple.
  - <https://hub.docker.com/_/redis>
  - for persistence,
    ```docker run --name myredis -d redis redis-server --save 60 1 --loglevel warning```
- or build a Docker image from centos 7.9 and add redis in there
  - either via yum package
  - or bundle the tar.gz source and compile, as recommended by antirez.
- or install the package on local box 
  - advantage is you also get the redis-cli and redis can access the local filesystem
  - easy to develop from local vscode and test perf in a 'standard' host, not from docker
  - also for plasma-store, not sure how the shared memory would work via docker.

### Commands 

We need to start redis, the server and then start the client to run the benchmark.


#### Redis command

For example run redis on port 6380:

```bash
docker run --name myredis -p 6380:6379 -v /home/gui/devel/datasvc/redisdata:/data --rm -d redis redis-server --save 60 1 --loglevel warning
```

#### Server

```bash
python dserver.py --redis-port=6380
```

#### Client

```bash
python  dclient.py --redis-port=6380 --num-runs=1
```



### Test data


#### gov hk covid data

```
http://www.chp.gov.hk/files/misc/enhanced_sur_covid_19_eng.csv
```
