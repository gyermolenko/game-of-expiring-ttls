"""Run as a scheduler after init stage has completed.
For each player start generating new tasks following such rules:
 - each player has up to 4 tasks
 - each task is a timer between 10s and 10m
 - each of the players will start task(s) on the server with a random frequency
 - if the maximum number of tasks was reached - wait until all player's tasks are finished to start a new one
 """

# > setex XxY:t1 100000 _
# > setex 2x2:t2 100000 _
# > setex 3x2:t2 100000 _


# players = await read_players(conn)
# for each player create 1 task with ttl from 10s to 10*60s


import aioredis



def generate_tasks():
    pass