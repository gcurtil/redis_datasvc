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