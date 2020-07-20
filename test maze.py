import time

from ma_maze_env import MeetEnv

env=MeetEnv()
for j in range(3):
    env.reset()

    env.render()
    time.sleep(3)

    actions=[[4,3],[2,1],[4,3],[2,1]]
    for i in range(len(actions)):
        ne_obs, re, done, info = env.step(actions[i])
        print(ne_obs)
        print(re)
        print(done)
        env.render()
        time.sleep(1)

env.windows.mainloop()