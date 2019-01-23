Two independant services:
 - `webserver` responds to http requests with the list of running tasks
 - `scheduler` periodically creates tasks for each player
 
Start
=====
```
$ python -m game.webserver.main
```

```
$ python game/scheduler/daemon.py
```


Redis
=====

**Players**

`players:by_x` - zset with scores by X coord and player_id members (`<X>x<Y>`)

`players:by_y` - scores by Y

**Tasks**

`<player_id>:t[1-4]`

E.g. "396x22:t1",  "160x169:t3"

