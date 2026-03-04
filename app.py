from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import random

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    # 直接從當前目錄提供 HTML 檔案
    html_file = os.path.join(os.path.dirname(__file__), '5114056002index.html')
    return send_file(html_file)

def next_state_of(r, c, action_idx, n, actions, obstacle_set):
    dr, dc = actions[action_idx]
    next_r, next_c = r + dr, c + dc
    if 0 <= next_r < n and 0 <= next_c < n and (next_r, next_c) not in obstacle_set:
        return next_r, next_c
    return r, c


def random_policy(n, end_state, obstacle_set, actions_count):
    policy = {}
    for r in range(n):
        for c in range(n):
            if [r, c] == end_state or (r, c) in obstacle_set:
                continue
            policy[(r, c)] = random.randint(0, actions_count - 1)
    return policy


def policy_evaluation(n, policy, end_state, obstacle_set, actions, gamma=0.9, theta=1e-4):
    v = {(r, c): 0.0 for r in range(n) for c in range(n)}

    while True:
        delta = 0.0
        for r in range(n):
            for c in range(n):
                if [r, c] == end_state or (r, c) in obstacle_set:
                    continue

                old_v = v[(r, c)]
                act_idx = policy.get((r, c), 0)
                ns_r, ns_c = next_state_of(r, c, act_idx, n, actions, obstacle_set)

                reward = -1.0
                if [ns_r, ns_c] == end_state:
                    new_v = reward
                else:
                    new_v = reward + gamma * v[(ns_r, ns_c)]

                v[(r, c)] = new_v
                delta = max(delta, abs(old_v - new_v))

        if delta < theta:
            break

    return v


def value_iteration(n, end_state, obstacle_set, actions, gamma=0.9, theta=1e-4):
    """
    使用 Value Iteration 求最佳策略與價值函數
    """
    v = {(r, c): 0.0 for r in range(n) for c in range(n)}
    policy = {}

    while True:
        delta = 0.0

        for r in range(n):
            for c in range(n):
                if [r, c] == end_state or (r, c) in obstacle_set:
                    continue

                old_v = v[(r, c)]
                action_values = []
                for act_idx in range(len(actions)):
                    next_r, next_c = next_state_of(r, c, act_idx, n, actions, obstacle_set)
                    reward = -1.0

                    if [next_r, next_c] == end_state:
                        q_value = reward
                    else:
                        q_value = reward + gamma * v[(next_r, next_c)]

                    action_values.append(q_value)

                best_action = max(range(len(action_values)), key=lambda i: action_values[i])
                v[(r, c)] = action_values[best_action]
                policy[(r, c)] = best_action
                delta = max(delta, abs(old_v - v[(r, c)]))

        if delta < theta:
            break

    return policy, v


def build_policy_matrix(n, policy, end_state, obstacle_set, action_symbols):
    matrix = [['' for _ in range(n)] for _ in range(n)]
    for r in range(n):
        for c in range(n):
            if (r, c) in obstacle_set:
                matrix[r][c] = 'X'
            elif [r, c] == end_state:
                matrix[r][c] = 'G'
            elif (r, c) in policy:
                matrix[r][c] = action_symbols[policy[(r, c)]]
    return matrix


def build_value_matrix(n, values, end_state, obstacle_set):
    matrix = [[0.0 for _ in range(n)] for _ in range(n)]
    for r in range(n):
        for c in range(n):
            if (r, c) in obstacle_set:
                matrix[r][c] = 'X'
            elif [r, c] == end_state:
                matrix[r][c] = 0.0
            else:
                matrix[r][c] = round(values.get((r, c), 0.0), 2)
    return matrix


def calculate_optimal_path(n, start_state, end_state, obstacle_set, actions, policy):
    optimal_path = []
    if not start_state or not end_state:
        return optimal_path

    current = tuple(start_state)
    optimal_path.append(list(current))
    visited = set()
    max_steps = n * n

    while list(current) != end_state and len(optimal_path) < max_steps:
        if current in visited:
            break
        visited.add(current)

        if current not in policy:
            break

        action_idx = policy[current]
        next_r, next_c = next_state_of(current[0], current[1], action_idx, n, actions, obstacle_set)
        if (next_r, next_c) == current:
            break

        current = (next_r, next_c)
        optimal_path.append(list(current))

    return optimal_path

@app.route('/api/evaluate', methods=['POST'])
def evaluate():
    data = request.json or {}
    n = int(data.get('n', 5))
    start_state = data.get('start')
    end_state = data.get('end')
    obstacles = data.get('obstacles', [])

    if start_state:
        start_state = [int(start_state[0]), int(start_state[1])]
    if end_state:
        end_state = [int(end_state[0]), int(end_state[1])]
    obstacles = [[int(o[0]), int(o[1])] for o in obstacles]

    if n < 5 or n > 9:
        return jsonify({'error': 'Grid size n must be between 5 and 9.'}), 400

    if not start_state or not end_state:
        return jsonify({'error': 'Start and end states are required.'}), 400

    if start_state == end_state:
        return jsonify({'error': 'Start and end cannot be the same cell.'}), 400

    if len(obstacles) != (n - 2):
        return jsonify({'error': f'Obstacle count must be exactly n-2 ({n - 2}).'}), 400

    obstacle_set = {(o[0], o[1]) for o in obstacles}
    if tuple(start_state) in obstacle_set or tuple(end_state) in obstacle_set:
        return jsonify({'error': 'Start/end cannot be set as obstacles.'}), 400

    # Actions: 0: Up, 1: Down, 2: Left, 3: Right
    actions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    action_symbols = ['↑', '↓', '←', '→']

    gamma = 0.9
    theta = 1e-4

    # HW1-2: 隨機策略 + 策略評估
    rnd_policy = random_policy(n, end_state, obstacle_set, len(actions))
    rnd_values = policy_evaluation(n, rnd_policy, end_state, obstacle_set, actions, gamma, theta)

    # HW1-3: Value Iteration 最佳策略
    optimal_policy, optimal_values = value_iteration(n, end_state, obstacle_set, actions, gamma, theta)
    optimal_path = calculate_optimal_path(n, start_state, end_state, obstacle_set, actions, optimal_policy)

    random_policy_matrix = build_policy_matrix(n, rnd_policy, end_state, obstacle_set, action_symbols)
    random_value_matrix = build_value_matrix(n, rnd_values, end_state, obstacle_set)
    optimal_policy_matrix = build_policy_matrix(n, optimal_policy, end_state, obstacle_set, action_symbols)
    optimal_value_matrix = build_value_matrix(n, optimal_values, end_state, obstacle_set)

    return jsonify({
        'random_policy_matrix': random_policy_matrix,
        'random_value_matrix': random_value_matrix,
        'optimal_policy_matrix': optimal_policy_matrix,
        'optimal_value_matrix': optimal_value_matrix,
        'optimal_path': optimal_path
    })

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(debug=debug, port=port, host="0.0.0.0")
