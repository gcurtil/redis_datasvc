# datasvc

Will need:

- a redis server
- pip install the packages for Arrow in a conda env
- Docker-compose file to start the python service / redis etc.
- could also use supervisor and do a multi-service container

## git setup

```
cd ~/devel
git clone git@gitlab.com:gcurtil/datasvc.git
```

## setup

### Python

```
(base) gui@monolith:~/devel/datasvc$ conda create -n datasvc python=3.8 
Collecting package metadata (current_repodata.json): done

```

New environment for ```datasvc```.
```
(base) gui@monolith:~/devel/datasvc$ conda activate datasvc
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


#### Redis command

```bash
docker run --name myredis -p 6379:6379 -v /home/gui/devel/datasvc/redisdata:/data --rm -d redis redis-server --save 60 1 --loglevel warning
```

### Test data

#### gov hk covid data

```
http://www.chp.gov.hk/files/misc/enhanced_sur_covid_19_eng.csv
```

```
https://api.data.gov.hk/v1/historical-archive/get-file?url=http%3A%2F%2Fwww.chp.gov.hk%2Ffiles%2Fmisc%2Fenhanced_sur_covid_19_eng.csv&amp;time=20211029-0921

https://api.data.gov.hk/v1/historical-archive/get-file?url=http%3A%2F%2Fwww.chp.gov.hk%2Ffiles%2Fmisc%2Flatest_situation_of_reported_cases_covid_19_chi.csv&amp;time=20211029-0922

https://api.data.gov.hk/v1/historical-archive/get-file?url=http%3A%2F%2Fwww.chp.gov.hk%2Ffiles%2Fmisc%2Fbuilding_list_eng.csv&amp;time=20211029-0921

https://api.data.gov.hk/v1/historical-archive/get-file?url=http%3A%2F%2Fwww.chp.gov.hk%2Ffiles%2Fmisc%2Fbuilding_list_chi.csv&amp;time=20211029-0921

https://api.data.gov.hk/v1/historical-archive/get-file?url=http%3A%2F%2Fwww.chp.gov.hk%2Ffiles%2Fmisc%2Flatest_situation_of_reported_cases_covid_19_eng.csv&amp;time=20211029-0922

https://api.data.gov.hk/v1/historical-archive/get-file?url=http%3A%2F%2Fwww.chp.gov.hk%2Ffiles%2Fmisc%2Fenhanced_sur_covid_19_chi.csv&amp;time=20211029-0921

https://api.data.gov.hk/v1/historical-archive/get-file?url=http%3A%2F%2Fwww.chp.gov.hk%2Ffiles%2Fmisc%2Fflights_trains_list_chi.csv&amp;time=20211029-0921

https://api.data.gov.hk/v1/historical-archive/get-file?url=http%3A%2F%2Fwww.chp.gov.hk%2Ffiles%2Fmisc%2Fflights_trains_list_eng.csv&amp;time=20211029-0921

https://api.data.gov.hk/v1/historical-archive/get-file?url=http%3A%2F%2Fwww.chp.gov.hk%2Ffiles%2Fmisc%2Fbuilding_list_home_confinees_eng.csv&amp;time=20211029-0921

https://api.data.gov.hk/v1/historical-archive/get-file?url=http%3A%2F%2Fwww.chp.gov.hk%2Ffiles%2Fmisc%2Flist_of_collection_points_eng.csv&amp;time=20211029-0922

https://api.data.gov.hk/v1/historical-archive/get-file?url=http%3A%2F%2Fwww.chp.gov.hk%2Ffiles%2Fmisc%2Flist_of_collection_points_chi.csv&amp;time=20211029-0922

https://api.data.gov.hk/v1/historical-archive/get-file?url=http%3A%2F%2Fwww.chp.gov.hk%2Ffiles%2Fmisc%2Fbuilding_list_home_confinees_chi.csv&amp;time=20211029-0921

https://api.data.gov.hk/v1/historical-archive/get-file?url=http%3A%2F%2Fwww.chp.gov.hk%2Ffiles%2Fmisc%2Fhome_confinees_tier2_building_list.csv&amp;time=20211029-0922

https://api.data.gov.hk/v1/historical-archive/get-file?url=http%3A%2F%2Fwww.chp.gov.hk%2Ffiles%2Fmisc%2Fnewly_issued_quarantine_orders_cap599c.csv&amp;time=20211029-0922

https://api.data.gov.hk/v1/historical-archive/get-file?url=http%3A%2F%2Fwww.chp.gov.hk%2Ffiles%2Fmisc%2Factive_quarantine_orders_cap599c.csv&amp;time=20211029-0920

https://api.data.gov.hk/v1/historical-archive/get-file?url=http%3A%2F%2Fwww.chp.gov.hk%2Ffiles%2Fmisc%2Flatest_situation_of_reported_cases_mainland_china_chi.csv&amp;time=20211029-0922

https://api.data.gov.hk/v1/historical-archive/get-file?url=http%3A%2F%2Fwww.chp.gov.hk%2Ffiles%2Fmisc%2Flatest_situation_of_reported_cases_mainland_china_eng.csv&amp;time=20211029-0922

https://api.data.gov.hk/v1/historical-archive/get-file?url=http%3A%2F%2Fwww.chp.gov.hk%2Ffiles%2Fmisc%2Fareas_in_mainland_china_have_reported_cases_eng.csv&amp;time=20211029-0921

https://api.data.gov.hk/v1/historical-archive/get-file?url=http%3A%2F%2Fwww.chp.gov.hk%2Ffiles%2Fmisc%2Fdistribution_of_reported_cases_in_guangdong_province_eng.csv&amp;time=20211029-0921

https://api.data.gov.hk/v1/historical-archive/get-file?url=http%3A%2F%2Fwww.chp.gov.hk%2Ffiles%2Fmisc%2Fareas_in_mainland_china_have_reported_cases_chi.csv&amp;time=20211029-0921

https://api.data.gov.hk/v1/historical-archive/get-file?url=http%3A%2F%2Fwww.chp.gov.hk%2Ffiles%2Fmisc%2Fcountries_areas_outside_mainland_china_have_reported_cases_eng.csv&amp;time=20211029-0921

https://api.data.gov.hk/v1/historical-archive/get-file?url=http%3A%2F%2Fwww.chp.gov.hk%2Ffiles%2Fmisc%2Fdistribution_of_reported_cases_in_guangdong_province_chi.csv&amp;time=20211029-0921

https://api.data.gov.hk/v1/historical-archive/get-file?url=http%3A%2F%2Fwww.chp.gov.hk%2Ffiles%2Fmisc%2Fcountries_areas_outside_mainland_china_have_reported_cases_chi.csv&amp;time=20211029-0921

https://api.data.gov.hk/v1/historical-archive/get-file?url=http%3A%2F%2Fwww.chp.gov.hk%2Ffiles%2Fmisc%2Fcountries_areas_have_reported_cases_eng.csv&amp;time=20211029-0921

https://api.data.gov.hk/v1/historical-archive/get-file?url=http%3A%2F%2Fwww.chp.gov.hk%2Ffiles%2Fmisc%2Fcountries_areas_have_reported_cases_chi.csv&amp;time=20211029-0921

https://api.data.gov.hk/v1/historical-archive/get-file?url=http%3A%2F%2Fwww.chp.gov.hk%2Ffiles%2Fmisc%2Fdistribution_of_reported_cases_in_korea_eng.csv&amp;time=20211029-0921

https://api.data.gov.hk/v1/historical-archive/get-file?url=http%3A%2F%2Fwww.chp.gov.hk%2Ffiles%2Fmisc%2Fdistribution_of_reported_cases_in_korea_chi.csv&amp;time=20211029-0921

https://api.data.gov.hk/v1/historical-archive/get-file?url=http%3A%2F%2Fwww.chp.gov.hk%2Ffiles%2Fmisc%2Fstatistics_on_covid_19_testing_cumulative.csv&amp;time=20211029-0922

https://api.data.gov.hk/v1/historical-archive/get-file?url=http%3A%2F%2Fwww.chp.gov.hk%2Ffiles%2Fmisc%2Fcountries_areas_visited_by_cases_with_travel_history_eng.csv&amp;time=20211029-0921

https://api.data.gov.hk/v1/historical-archive/get-file?url=http%3A%2F%2Fwww.chp.gov.hk%2Ffiles%2Fmisc%2Fcountries_areas_visited_by_cases_with_travel_history_chi.csv&amp;time=20211029-0921

https://api.data.gov.hk/v1/historical-archive/get-file?url=http%3A%2F%2Fwww.chp.gov.hk%2Ffiles%2Fmisc%2Fstatistics_on_covid_19_testing_daily.csv&amp;time=20211029-0922

https://api.data.gov.hk/v1/historical-archive/get-file?url=http%3A%2F%2Fwww.chp.gov.hk%2Ffiles%2Fmisc%2Fmode_of_detection_eng.csv&amp;time=20211029-0922

https://api.data.gov.hk/v1/historical-archive/get-file?url=http%3A%2F%2Fwww.chp.gov.hk%2Ffiles%2Fmisc%2Fmode_of_detection_chi.csv&amp;time=20211029-0922

https://api.data.gov.hk/v1/historical-archive/get-file?url=http%3A%2F%2Fwww.chp.gov.hk%2Ffiles%2Fmisc%2Foccupancy_of_quarantine_centres_eng.csv&amp;time=20211029-0922

https://api.data.gov.hk/v1/historical-archive/get-file?url=http%3A%2F%2Fwww.chp.gov.hk%2Ffiles%2Fmisc%2Foccupancy_of_quarantine_centres_chi.csv&amp;time=20211029-0922

https://api.data.gov.hk/v1/historical-archive/get-file?url=http%3A%2F%2Fwww.chp.gov.hk%2Ffiles%2Fmisc%2Fno_of_confines_by_types_in_quarantine_centres_eng.csv&amp;time=20211029-0922

https://api.data.gov.hk/v1/historical-archive/get-file?url=http%3A%2F%2Fwww.chp.gov.hk%2Ffiles%2Fmisc%2Fno_of_confines_by_types_in_quarantine_centres_chi.csv&amp;time=20211029-0922

https://api.data.gov.hk/v1/historical-archive/get-file?url=http%3A%2F%2Fwww.chp.gov.hk%2Ffiles%2Fmisc%2Fquarantine_hotel_eng.csv&amp;time=20211029-0922

https://api.data.gov.hk/v1/historical-archive/get-file?url=http%3A%2F%2Fwww.chp.gov.hk%2Ffiles%2Fmisc%2Fquarantine_hotel_chi.csv&amp;time=20211029-0922

https://api.data.gov.hk/v1/historical-archive/get-file?url=http%3A%2F%2Fwww.chp.gov.hk%2Ffiles%2Fmisc%2Flarge_clusters_chi.csv&amp;time=20211029-0922

https://api.data.gov.hk/v1/historical-archive/get-file?url=http%3A%2F%2Fwww.chp.gov.hk%2Ffiles%2Fmisc%2Flarge_clusters_eng.csv&amp;time=20211029-0922

```

### Results

```
2022-05-27 15:06:57,810 INFO dclient timings: 
    Step                   Cmd        Name  clt_sz_MB  dsk_sz_MB  dt_client  dt_server   dt00   dt01   dt02   dt03   Speed
0      0           json_direct  d-data.csv    112.384     33.323      4.038      1.418  459.4  958.4    0.0    0.0   8.253
1      0         json_indirect  d-data.csv    112.384     33.323      1.999      1.712  523.4  990.1    0.0  198.6  16.667
2      0    json_zlib_indirect  d-data.csv     27.649     33.323      2.484      2.358  434.3  963.9  920.1   39.2  13.413
3      0     json_lz4_indirect  d-data.csv     42.429     33.323      1.882      1.735  476.2  929.7  248.9   80.1  17.706
4      0   to_parquet_indirect  d-data.csv      8.023     33.323      0.737      0.709  441.4  255.8    0.0   11.4  45.214
5      0      pqarrow_indirect  d-data.csv      8.023     33.323      0.752      0.727  462.3  249.7    0.0   15.4  44.305
6      0      ftarrow_indirect  d-data.csv     10.922     33.323      0.596      0.567  492.9   55.3    0.0   18.5  55.867
7      0      rbarrow_indirect  d-data.csv     65.959     33.323      0.820      0.639  423.9  113.1    0.0  102.5  40.623
8      0  rbarrow_lz4_indirect  d-data.csv     10.870     33.323      0.699      0.653  477.8  113.6   47.7   13.8  47.678
9      0           json_direct  19_eng.csv      2.214      1.114      0.135      0.033   16.0   17.1    0.0    0.0   8.269
10     0         json_indirect  19_eng.csv      2.214      1.114      0.047      0.038   16.0   15.8    0.0    6.0  23.823
11     0    json_zlib_indirect  19_eng.csv      0.391      1.114      0.052      0.045   14.3   16.0   13.0    1.5  21.337
12     0     json_lz4_indirect  19_eng.csv      0.642      1.114      0.044      0.036   14.1   17.2    3.0    1.9  25.264
13     0   to_parquet_indirect  19_eng.csv      0.114      1.114      0.033      0.026   14.2   11.1    0.0    1.0  33.784
14     0      pqarrow_indirect  19_eng.csv      0.114      1.114      0.044      0.036   14.8   19.7    0.0    1.7  25.493
15     0      ftarrow_indirect  19_eng.csv      0.485      1.114      0.032      0.023   14.6    6.5    0.0    2.3  34.581
16     0      rbarrow_indirect  19_eng.csv      1.539      1.114      0.039      0.027   15.2    7.8    0.0    3.6  28.792
17     0  rbarrow_lz4_indirect  19_eng.csv      0.481      1.114      0.062      0.052   15.3   34.1    1.0    1.6  18.028
```

Reusing the Redis connection on server:
```
2022-05-27 15:09:11,359 INFO dclient timings: 
    Step                   Cmd        Name  clt_sz_MB  dsk_sz_MB  dt_client  dt_server   dt00   dt01   dt02   dt03   Speed
0      0           json_direct  d-data.csv    112.384     33.323      4.106      1.452  493.9  957.7    0.0    0.0   8.116
1      0         json_indirect  d-data.csv    112.384     33.323      1.902      1.641  476.2  981.9    0.0  182.8  17.521
2      0    json_zlib_indirect  d-data.csv     27.649     33.323      2.417      2.308  423.9  928.0  923.5   32.7  13.789
3      0     json_lz4_indirect  d-data.csv     42.429     33.323      1.941      1.842  532.8  947.7  282.9   78.3  17.166
4      0   to_parquet_indirect  d-data.csv      8.023     33.323      0.798      0.769  461.2  293.6    0.0   14.3  41.784
5      0      pqarrow_indirect  d-data.csv      8.023     33.323      0.694      0.674  420.2  245.3    0.0    8.9  48.010
6      0      ftarrow_indirect  d-data.csv     10.922     33.323      0.554      0.530  444.7   71.8    0.0   13.4  60.180
7      0      rbarrow_indirect  d-data.csv     65.959     33.323      0.749      0.597  420.9   99.4    0.0   76.8  44.486
8      0  rbarrow_lz4_indirect  d-data.csv     10.870     33.323      0.687      0.651  478.1  112.5   46.7   13.6  48.539
9      0           json_direct  19_eng.csv      2.214      1.114      0.115      0.054   33.1   20.6    0.0    0.0   9.687
10     0         json_indirect  19_eng.csv      2.214      1.114      0.047      0.037   16.4   16.8    0.0    4.0  23.615
11     0    json_zlib_indirect  19_eng.csv      0.391      1.114      0.054      0.047   14.3   17.3   14.3    0.9  20.824
12     0     json_lz4_indirect  19_eng.csv      0.642      1.114      0.041      0.034   14.4   15.4    2.8    1.0  27.084
13     0   to_parquet_indirect  19_eng.csv      0.114      1.114      0.036      0.027   14.0   12.6    0.0    0.6  30.955
14     0      pqarrow_indirect  19_eng.csv      0.114      1.114      0.034      0.027   13.7   13.2    0.0    0.4  32.999
15     0      ftarrow_indirect  19_eng.csv      0.485      1.114      0.029      0.022   14.2    6.9    0.0    1.0  38.878
16     0      rbarrow_indirect  19_eng.csv      1.539      1.114      0.031      0.022   13.9    6.2    0.0    2.2  35.460
17     0  rbarrow_lz4_indirect  19_eng.csv      0.481      1.114      0.028      0.021   12.3    6.4    0.9    1.0  40.257
```

Reusing the Redis connection on server and client:
```
2022-05-27 15:13:51,720 INFO dclient timings: 
    Step                   Cmd        Name  clt_sz_MB  dsk_sz_MB  dt_client  dt_server   dt00   dt01   dt02   dt03   Speed
0      0           json_direct  d-data.csv    112.384     33.323      4.045      1.413  476.4  936.9    0.0    0.0   8.239
1      0         json_indirect  d-data.csv    112.384     33.323      1.974      1.704  559.1  944.3    0.0  200.8  16.882
2      0    json_zlib_indirect  d-data.csv     27.649     33.323      2.440      2.312  445.9  890.7  934.2   41.5  13.656
3      0     json_lz4_indirect  d-data.csv     42.429     33.323      1.835      1.729  458.2  950.0  240.0   80.9  18.163
4      0   to_parquet_indirect  d-data.csv      8.023     33.323      0.729      0.695  445.8  235.2    0.0   13.6  45.703
5      0      pqarrow_indirect  d-data.csv      8.023     33.323      0.736      0.701  439.1  251.9    0.0    9.8  45.281
6      0      ftarrow_indirect  d-data.csv     10.922     33.323      0.585      0.554  488.9   51.5    0.0   13.5  56.923
7      0      rbarrow_indirect  d-data.csv     65.959     33.323      0.848      0.675  450.0  112.9    0.0  112.3  39.293
8      0  rbarrow_lz4_indirect  d-data.csv     10.870     33.323      0.638      0.591  453.9   72.0   49.4   16.2  52.228
9      0           json_direct  19_eng.csv      2.214      1.114      0.135      0.032   15.1   16.5    0.0    0.0   8.250
10     0         json_indirect  19_eng.csv      2.214      1.114      0.048      0.037   16.1   16.5    0.0    4.4  22.977
11     0    json_zlib_indirect  19_eng.csv      0.391      1.114      0.056      0.046   14.0   16.6   14.1    0.9  19.872
12     0     json_lz4_indirect  19_eng.csv      0.642      1.114      0.044      0.034   13.6   16.4    3.1    1.2  25.178
13     0   to_parquet_indirect  19_eng.csv      0.114      1.114      0.043      0.033   13.8   18.3    0.0    0.7  26.111
14     0      pqarrow_indirect  19_eng.csv      0.114      1.114      0.044      0.033   12.5   20.0    0.0    0.6  25.225
15     0      ftarrow_indirect  19_eng.csv      0.485      1.114      0.054      0.044   35.4    7.9    0.0    1.0  20.613
16     0      rbarrow_indirect  19_eng.csv      1.539      1.114      0.034      0.025   14.4    7.3    0.0    3.2  33.009
17     0  rbarrow_lz4_indirect  19_eng.csv      0.481      1.114      0.031      0.023   14.7    6.3    0.9    1.1  36.454
```

With waitress:
```
2022-05-27 15:22:42,674 INFO dclient timings: 
    Step                   Cmd        Name  clt_sz_MB  dsk_sz_MB  dt_client  dt_server   dt00   dt01   dt02   dt03   Speed
0      0           json_direct  d-data.csv    112.384     33.323      4.250      1.371  435.4  936.0    0.0    0.0   7.841
1      0         json_indirect  d-data.csv    112.384     33.323      1.838      1.600  419.3  978.8    0.0  202.3  18.133
2      0    json_zlib_indirect  d-data.csv     27.649     33.323      2.363      2.287  418.5  925.8  894.1   48.4  14.099
3      0     json_lz4_indirect  d-data.csv     42.429     33.323      1.800      1.703  479.6  930.6  242.9   49.7  18.513
4      0   to_parquet_indirect  d-data.csv      8.023     33.323      0.759      0.731  478.0  243.3    0.0    9.9  43.887
5      0      pqarrow_indirect  d-data.csv      8.023     33.323      0.747      0.721  457.7  250.2    0.0   12.7  44.635
6      0      ftarrow_indirect  d-data.csv     10.922     33.323      0.535      0.506  429.4   64.5    0.0   12.0  62.279
7      0      rbarrow_indirect  d-data.csv     65.959     33.323      0.866      0.690  444.5  137.2    0.0  108.6  38.494
8      0  rbarrow_lz4_indirect  d-data.csv     10.870     33.323      0.704      0.671  492.4  115.0   46.0   17.4  47.314
9      0           json_direct  19_eng.csv      2.214      1.114      0.180      0.080   34.3   46.0    0.0    0.0   6.202
10     0         json_indirect  19_eng.csv      2.214      1.114      0.038      0.031   12.6   15.4    0.0    3.4  29.143
11     0    json_zlib_indirect  19_eng.csv      0.391      1.114      0.048      0.042   13.0   15.4   12.7    1.0  23.042
12     0     json_lz4_indirect  19_eng.csv      0.642      1.114      0.048      0.040   17.6   17.5    3.0    1.4  23.027
13     0   to_parquet_indirect  19_eng.csv      0.114      1.114      0.063      0.054   35.6   17.4    0.0    0.8  17.603
14     0      pqarrow_indirect  19_eng.csv      0.114      1.114      0.058      0.051   30.0   20.4    0.0    0.6  19.283
15     0      ftarrow_indirect  19_eng.csv      0.485      1.114      0.030      0.024   14.5    8.6    0.0    0.9  37.512
16     0      rbarrow_indirect  19_eng.csv      1.539      1.114      0.031      0.024   14.4    7.3    0.0    2.5  35.503
17     0  rbarrow_lz4_indirect  19_eng.csv      0.481      1.114      0.042      0.036   24.7    9.1    1.2    1.0  26.499
```
