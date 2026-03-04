from flask import Flask, request, jsonify, send_file
import copy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    # 直接从当前目录提供HTML文件
    html_file = os.path.join(os.path.dirname(__file__), '5114056002index.html')
    return send_file(html_file)

def value_iteration(n, start_state, end_state, obstacles, actions, action_symbols, gamma=0.9, theta=1e-4):
    """
    Perform value iteration to find optimal policy and value function.
    Returns optimal policy and value function.
    """
    V = { (r, c): 0.0 for r in range(n) for c in range(n) }
    policy = {}
    
    iteration = 0
    while True:
        delta = 0
        
        # Policy Evaluation
        for r in range(n):
            for c in range(n):
                s = (r, c)
                state_list = [r, c]
                
                if state_list == end_state or state_list in obstacles:
                    continue
                
                old_v = V[s]
                
                # Find best action
                action_values = []
                for a_idx in range(len(actions)):
                    dr, dc = actions[a_idx]
                    next_r, next_c = r + dr, c + dc
                    next_state_list = [next_r, next_c]
                    
                    reward = -1.0
                    
                    if 0 <= next_r < n and 0 <= next_c < n and next_state_list not in obstacles:
                        next_s = (next_r, next_c)
                        if next_state_list == end_state:
                            q_value = reward + gamma * 0.0
                        else:
                            q_value = reward + gamma * V[next_s]
                    else:
                        next_s = s
                        q_value = reward + gamma * V[next_s]
                    
                    action_values.append(q_value)
                
                # Select best action
                best_action = action_values.index(max(action_values))
                V[s] = max(action_values)
                policy[s] = best_action
                
                delta = max(delta, abs(old_v - V[s]))
        
        if delta < theta:
            break
        iteration += 1
        if iteration > 1000:
            break
    
    return policy, V

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

    # Actions: 0: Up, 1: Down, 2: Left, 3: Right
    actions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    action_symbols = ['↑', '↓', '←', '→']
    
    gamma = 0.9
    theta = 1e-4

    # HW1-3: Value Iteration Algorithm
    policy, V = value_iteration(n, start_state, end_state, obstacles, actions, action_symbols, gamma, theta)

    # Calculate optimal path from start to end
    optimal_path = []
    if start_state and end_state:
        current = tuple(start_state)
        optimal_path.append(list(current))
        visited = set()
        max_steps = n * n  # Prevent infinite loops
        
        while list(current) != end_state and len(optimal_path) < max_steps:
            if current in visited:
                break
            visited.add(current)
            
            if current in policy:
                action_idx = policy[current]
                dr, dc = actions[action_idx]
                next_r, next_c = current[0] + dr, current[1] + dc
                
                # Check if next state is valid
                if 0 <= next_r < n and 0 <= next_c < n and [next_r, next_c] not in obstacles:
                    current = (next_r, next_c)
                    optimal_path.append(list(current))
                else:
                    break
            else:
                break

    # Build policy matrix
    policy_matrix = [['' for _ in range(n)] for _ in range(n)]
    for r in range(n):
        for c in range(n):
            state = [r, c]
            if state in obstacles:
                policy_matrix[r][c] = 'X' 
            elif state == end_state:
                policy_matrix[r][c] = 'G'
            else:
                if (r, c) in policy:
                    act_idx = policy[(r, c)]
                    policy_matrix[r][c] = action_symbols[act_idx]

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
                value_matrix[r][c] = round(V.get((r, c), 0.0), 2)
                
    return jsonify({
        'value_matrix': value_matrix,
        'policy_matrix': policy_matrix,
        'optimal_path': optimal_path
    })

if __name__ == '__main__':
    # Force single thread for easier dev debugging
    app.run(debug=True, port=5000, host="0.0.0.0", threaded=False)
