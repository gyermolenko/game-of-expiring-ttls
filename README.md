Two independant services:
 - `webserver` responds to http requests with the list of running tasks
 - `scheduler` periodically creates tasks for each player
 
Start
=====
```
$ python -m game.webserver.main
```

```
$ python game/scheduler/main.py
```


Redis
=====

**Players**

`players:by_x` - zset with scores by X coord and player_id members (`<X>x<Y>`)

`players:by_y` - scores by Y

**Tasks**

`<player_id>:t[1-4]`

E.g. "396x22:t1",  "160x169:t3"


Results
=======
20k, 0x32

iscan count=10_000
```
INFO:root:creating view: view:0-32:0-32
INFO:root:tasks qty: 0
INFO:root:--TIME-- response: 0.004085063934326172
INFO:root:--------------------------------------------------------------------------------
INFO:root:creating view: view:0-32:0-32
INFO:root:tasks qty: 74
INFO:root:--TIME-- response: 1.6496071815490723
INFO:root:--------------------------------------------------------------------------------
INFO:root:tasks qty: 88
INFO:root:--TIME-- response: 1.8168559074401855
INFO:root:--------------------------------------------------------------------------------
INFO:root:tasks qty: 148
INFO:root:--TIME-- response: 2.7153828144073486
INFO:root:--------------------------------------------------------------------------------
INFO:root:tasks qty: 221
INFO:root:--TIME-- response: 3.733328104019165

```

iscan count=5_000
```
INFO:root:creating view: view:0-32:0-32
INFO:root:tasks qty: 0
INFO:root:--TIME-- response: 0.032588958740234375
INFO:root:--------------------------------------------------------------------------------
INFO:root:creating view: view:0-32:0-32
INFO:root:tasks qty: 81
INFO:root:--TIME-- response: 1.9561562538146973
INFO:root:--------------------------------------------------------------------------------
INFO:root:tasks qty: 128
INFO:root:--TIME-- response: 2.361870050430298
INFO:root:--------------------------------------------------------------------------------
INFO:root:tasks qty: 162
INFO:root:--TIME-- response: 2.74166202545166
INFO:root:--------------------------------------------------------------------------------
INFO:root:tasks qty: 243
INFO:root:--TIME-- response: 3.9544858932495117

```

iscan count=1_000
```
INFO:root:creating view: view:0-32:0-32
INFO:root:tasks qty: 103
INFO:root:--TIME-- response: 2.7517199516296387
INFO:root:--------------------------------------------------------------------------------
INFO:root:tasks qty: 166
INFO:root:--TIME-- response: 3.6034722328186035
INFO:root:--------------------------------------------------------------------------------
INFO:root:tasks qty: 251
INFO:root:--TIME-- response: 5.307642698287964
INFO:root:--------------------------------------------------------------------------------
INFO:root:tasks qty: 303
INFO:root:--TIME-- response: 6.1502227783203125
INFO:root:--------------------------------------------------------------------------------
INFO:root:tasks qty: 298
INFO:root:--TIME-- response: 6.010218858718872


```
