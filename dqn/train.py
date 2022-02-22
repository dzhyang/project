from Game import Game,Camp
from Model import Model
import tensorflow as tf
import numpy as np
import random
import threading
from collections import deque
from flask import Flask,jsonify,render_template,request
from Game import Game,Camp
import json

log=open("./state.log","w",buffering = 1)
action_mapping=[]
isdone=False
for i in range(0,4):
    for j in range(0,4):
        action_mapping.append((i,j,i,j))
        if i+1<4:
            action_mapping.append((i,j,i+1,j))
        if i-1>=0:
            action_mapping.append((i,j,i-1,j))
        if j+1<4:
            action_mapping.append((i,j,i,j+1))
        if j-1>=0:
            action_mapping.append((i,j,i,j-1))

app= Flask(__name__, static_url_path='')
play=Game(Camp.Black)
@app.route('/operate',methods=['POST'])#路由
def test_post():
    data=json.loads(request.get_data())
    x1,y1,x2,y2=data.values()
    log.write("paly:"+str((x1,y1,x2,y2))+"\n")
    result=dict()
    lock_black.acquire()
    _,_,done=play((x1,y1,x2,y2))
    isdone=done
    if isdone:
        result["state"]="done"
    else:
        result["state"]="running"
    # state=play.getState()
    # result["render"]=[]
    # if x1==x1 and y1==y2:
    #     result["render"].append([x1,y1,state[x1][y1]])
    # else:
    #     result["render"].append([x1,y1,state[x1][y1]])
    #     result["render"].append([x2,y2,state[x2][y2]])
    lock_red.release()
    
    return jsonify(result)

@app.route('/')
def index():
    return app.send_static_file('./index.html')

@app.route('/chess',methods=['GET'])  # 指定路由
def chess():
    result=dict()
    if Game._needrender:
        result["state"]="render"
        result["render"]=list(Game._render.queue)
        Game._needrender=False
        Game._render.queue.clear()
        return jsonify(result)
    result["state"]="norender"
    return jsonify(result)

def run():
    app.run(host='0.0.0.0',#任何ip都可以访问
            port=9999,#端口
            debug=True,
            use_reloader=False
            )
# Hyper Parameters
GAMMA = 0.95 # discount factor
LEARNING_RATE=0.01
 
# Hyper Parameters
ENV_NAME = 'CartPole-v0'
EPISODE = 3000 # Episode limitation
STEP = 3000 # Step limitation in an episode
TEST = 10 # The number of experiment test every 100 episode
 
def main():
    env =Game(Camp.Red)
    agent = Model()
    for episode in range(EPISODE):
        # initialize task
        # Train
        for step in range(STEP):
            lock_red.acquire()
            if not isdone:
                state = env.getState()
                action = agent.choose_action(state,episode) # e-greedy action for train
                #mapping action
                reward,effect,done = env(action_mapping[action])
                while not effect:
                    action=agent.choose_action(state,episode)
                    reward,effect,done=env(action_mapping[action])
                state = env.getState()
                log.write("agent:"+str(action_mapping[action])+"\n")
                agent.store_transition(state, action, reward)
                if done:
                    agent.learn()
                    break
                '''等待对方出棋'''
            else:
                agent.learn()
                break
            lock_black.release()

if __name__ == '__main__':
    Game.init_CheckerBoard()
    lock_red = threading.Lock()
    lock_black = threading.Lock()
    lock_black.acquire()
    web=threading.Thread(None,run)
    web.start()
    main()
    web.join()
    





# from Game import Game,Camp
# from Model import Model
# import tensorflow as tf

# num_count=3
# learning_rate = 1e-3
# r=0.7

# env=Game(Camp.Red)
# Game.init_CheckerBoard()
# model=Model()
# optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)
# replay_buffer = deque(maxlen=10000)
# '''
# 预测
# '''
# for episode_id in range(num_count):
#     reward_sum=0
#     while True:
#         state=env.getState()
#         action=model.predict(state)

#         reward,effect,done=env(action)
#         while not effect:
#             action=model.predict(state)
#             reward,effect,done=env(action)
#         reward_sum+=r*reward
#         if done:
#             break

#     y = reward_sumy + (gamma * tf.reduce_max(q_value, axis=1)) * (1 - batch_done)  # 计算 y 值

#     with tf.GradientTape() as tape:
#         loss = tf.keras.losses.mean_squared_error(
#             y_true=y,
#             y_pred=tf.reduce_sum(model(state) * tf.one_hot(batch_action, depth=2), axis=1)
#             )
#         grads = tape.gradient(loss, model.variables)
#         optimizer.apply_gradients(grads_and_vars=zip(grads, model.variables))


