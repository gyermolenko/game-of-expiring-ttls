
Prerequisites
=============
- Redis server
- Python 3.7
- `$ pip install -r requirements.txt`

Description
===========
Solution contains two independant services:
 - `webserver` responds to http requests with the list of running tasks
 - `scheduler` creates players and then periodically creates tasks for each
 
Start
=====
```
$ python -m game.webserver.main
```

```
$ python -m game.scheduler.main
```

Results
=======
Params: 20k players, 32x32 view, ~80k tasks total, ~350 tasks running

Request-Response time: ~0.04s

Possible improvements 
---------------------

- multi dimensional indexes: https://redis.io/topics/indexes#multi-dimensional-indexes



Redis structures
================
Could be configured from `settings.py`

**Players**

`players:by_x` - zset with scores by X coord and player_id members (`<X>x<Y>`)

`players:by_y` - scores by Y

**Views**

`view:<xstart>-<xend>:<ystart>-<yend>` - lists of players in x-y diapason


**Individual tasks**

`<player_id>:t[1-4]` (e.g. "396x22:t1",  "160x169:t3") - key with ttl, per task

**Task lists**

`tasks:<player_id>`

