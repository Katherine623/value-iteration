from flask import Flask, render_template, request, jsonify
import random
import copy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('5114056002index.html')

@app.route('/api/evaluate', methods=['POST'])
def evaluate():
    data = request.json
    n = int(data.get('n', 5))
    start_state = data.get('start')
    end_state = data.get('end')
    obstacles = data.get('obstacles', [])

    if start_state: start_state = [int(start_state[0]), int(start_state[1])]
    if end_state: end_state = [int(end_state[0]), int(end_state[1])]
    obstacles = [[int(o[0]), int(o[1])] for o in obstacles]

    # Directions matching standard RL grid logic.
    # Note: the y-axis in the HW image seems reversed (bottom is 0, top is n-1)
    # But usually grids are represented top-to-bottom. We will keep standard top-to-bottom r,c and handle drawing on frontend.
    # r increases downwards, c increases left-to-right
    # 0: Up (row-1), 1: Down (row+1), 2: Left (col-1), 3: Right (col+1)
    actions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    # Unicode: Up, Down, Left, Right
    action_symbols = ['↑', '↓', '←', '→']

    policy = {}
    policy_matrix = [['' for _ in range(n)] for _ in range(n)]
    
    # 1. Random Policy Generation
    for r in range(n):
        for c in range(n):
            state = [r, c]
            if state in obstacles:
                policy_matrix[r][c] = 'X' 
            elif state == end_state:
                policy_matrix[r][c] = 'G'
            else:
                act_idx = random.choice([0, 1, 2, 3])
                policy[(r, c)] = act_idx
                policy_matrix[r][c] = action_symbols[act_idx]

    # 2. Iterative Policy Evaluation
    gamma = 0.9 # Discount factor default (standard value)
    theta = 1e-4
    
    V = { (r, c): 0.0 for r in range(n) for c in range(n) }
    
    iteration = 0
    while True:
        delta = 0
        new_V = copy.deepcopy(V)
        
        for r in range(n):
            for c in range(n):
                s = (r, c)
                state_list = [r, c]
                
                if state_list == end_state or state_list in obstacles:
                    continue
                
                a_idx = policy[s]
                dr, dc = actions[a_idx]
                next_r, next_c = r + dr, c + dc
                next_state_list = [next_r, next_c]
                
                # Standard Gridworld reward structure matching general textbook examples (like Sutton & Barto):
                # -1 per step. Goal provides no penalty (or positive reward).
                # But let's use -1 per step, 0 to goal.
                reward = -1.0
                
                # Check boundaries and obstacles
                if 0 <= next_r < n and 0 <= next_c < n and next_state_list not in obstacles:
                    next_s = (next_r, next_c)
                    if next_state_list == end_state:
                        # Reaching goal
                        v_expected = reward + gamma * 0.0 # Goal state value is 0
                    else:
                        v_expected = reward + gamma * V[next_s]
                else:
                    # Bump into wall/obstacle: state doesn't change
                    next_s = s 
                    v_expected = reward + gamma * V[next_s]
                
                new_V[s] = v_expected
                delta = max(delta, abs(v_expected - V[s]))
                
        V = new_V
        if delta < theta:
            break
        iteration += 1
        if iteration > 1000:
            break

    # Prepare return Value Matrix
    value_matrix = [[0.0 for _ in range(n)] for _ in range(n)]
    for r in range(n):
        for c in range(n):
            state_list = [r, c]
            if state_list in obstacles:
                value_matrix[r][c] = 'X'
            elif state_list == end_state:
                value_matrix[r][c] = 0.0
            else:
                value_matrix[r][c] = round(V[(r, c)], 2)
                
    return jsonify({
        'value_matrix': value_matrix,
        'policy_matrix': policy_matrix
    })

if __name__ == '__main__':
    # Force single thread for easier dev debugging
    app.run(debug=True, port=5000, host="0.0.0.0", threaded=False)
