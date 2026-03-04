import streamlit as st
import numpy as np
import pandas as pd
from copy import deepcopy

st.set_page_config(page_title="Grid World Value Iteration", layout="wide")

def value_iteration(n, start_state, end_state, obstacles, actions, action_symbols, gamma=0.9, theta=1e-4):
    """
    Perform value iteration to find optimal policy and value function.
    """
    V = {(r, c): 0.0 for r in range(n) for c in range(n)}
    policy = {}
    
    iteration = 0
    while True:
        delta = 0
        
        for r in range(n):
            for c in range(n):
                s = (r, c)
                state_list = [r, c]
                
                if state_list == end_state or state_list in obstacles:
                    continue
                
                old_v = V[s]
                
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

def get_optimal_path(n, start_state, end_state, obstacles, actions, policy):
    """Calculate optimal path from start to end following the policy"""
    optimal_path = []
    if start_state and end_state:
        current = tuple(start_state)
        optimal_path.append(list(current))
        visited = set()
        max_steps = n * n
        
        while list(current) != end_state and len(optimal_path) < max_steps:
            if current in visited:
                break
            visited.add(current)
            
            if current in policy:
                action_idx = policy[current]
                dr, dc = actions[action_idx]
                next_r, next_c = current[0] + dr, current[1] + dc
                
                if 0 <= next_r < n and 0 <= next_c < n and [next_r, next_c] not in obstacles:
                    current = (next_r, next_c)
                    optimal_path.append(list(current))
                else:
                    break
            else:
                break
    
    return optimal_path

# Initialize session state
if 'grid_size' not in st.session_state:
    st.session_state.grid_size = 5
if 'start_pos' not in st.session_state:
    st.session_state.start_pos = None
if 'end_pos' not in st.session_state:
    st.session_state.end_pos = None
if 'obstacles' not in st.session_state:
    st.session_state.obstacles = []
if 'show_results' not in st.session_state:
    st.session_state.show_results = False

st.title("🌐 Grid World Value Iteration")
st.subheader("HW1-3: 使用價值迭代演算法實現網格世界最優策略求解")

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ 設置")
    
    st.session_state.grid_size = st.slider("網格大小", 3, 10, st.session_state.grid_size)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 重置網格"):
            st.session_state.start_pos = None
            st.session_state.end_pos = None
            st.session_state.obstacles = []
            st.session_state.show_results = False
            st.rerun()

# Main grid interaction
st.subheader("📍 設置網格")

col_left, col_right = st.columns([2, 1])

with col_left:
    st.write("**點擊下方選擇位置：**")
    
    # Create interactive grid using buttons
    n = st.session_state.grid_size
    grid = st.columns(n)
    
    mode = st.radio("選擇模式:", ["設置起始點", "設置終點", "設置障礙物"], horizontal=True)
    
    st.write("")  # spacing
    
    grid_rows = []
    for r in range(n):
        row_cols = st.columns(n)
        row_buttons = []
        
        for c in range(n):
            with row_cols[c]:
                # Determine button appearance
                button_color = "gray"
                button_text = f"{r},{c}"
                
                if st.session_state.start_pos == [r, c]:
                    button_color = "green"
                    button_text = f"{r},{c}\n🟢"
                elif st.session_state.end_pos == [r, c]:
                    button_color = "red"
                    button_text = f"{r},{c}\n🔴"
                elif [r, c] in st.session_state.obstacles:
                    button_color = "gray"
                    button_text = f"{r},{c}\n■"
                
                if st.button(button_text, key=f"btn_{r}_{c}", use_container_width=True):
                    if mode == "設置起始點":
                        st.session_state.start_pos = [r, c]
                    elif mode == "設置終點":
                        st.session_state.end_pos = [r, c]
                    elif mode == "設置障礙物":
                        if [r, c] in st.session_state.obstacles:
                            st.session_state.obstacles.remove([r, c])
                        else:
                            st.session_state.obstacles.append([r, c])
                    st.rerun()

with col_right:
    st.write("**目前設置：**")
    if st.session_state.start_pos:
        st.success(f"起始點: {st.session_state.start_pos}")
    else:
        st.info("起始點: 未設置")
    
    if st.session_state.end_pos:
        st.error(f"終點: {st.session_state.end_pos}")
    else:
        st.info("終點: 未設置")
    
    st.warning(f"障礙物: {len(st.session_state.obstacles)} 個")
    if st.session_state.obstacles:
        st.write(st.session_state.obstacles)

# Calculate button
st.divider()

if st.button("🚀 計算最優策略與價值函數", use_container_width=True, type="primary"):
    if not st.session_state.start_pos:
        st.error("❌ 請先設置起始點")
    elif not st.session_state.end_pos:
        st.error("❌ 請先設置終點")
    else:
        st.session_state.show_results = True
        st.rerun()

# Display results
if st.session_state.show_results:
    st.divider()
    st.subheader("📊 計算結果")
    
    # Run value iteration
    n = st.session_state.grid_size
    actions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    action_symbols = ['↑', '↓', '←', '→']
    
    with st.spinner("⏳ 正在計算中..."):
        policy, V = value_iteration(
            n,
            st.session_state.start_pos,
            st.session_state.end_pos,
            st.session_state.obstacles,
            actions,
            action_symbols,
            gamma=0.9,
            theta=1e-4
        )
        
        optimal_path = get_optimal_path(
            n,
            st.session_state.start_pos,
            st.session_state.end_pos,
            st.session_state.obstacles,
            actions,
            policy
        )
    
    # Build policy matrix
    policy_matrix = [['' for _ in range(n)] for _ in range(n)]
    for r in range(n):
        for c in range(n):
            state = [r, c]
            if state in st.session_state.obstacles:
                policy_matrix[r][c] = '■'
            elif state == st.session_state.end_pos:
                policy_matrix[r][c] = 'G'
            else:
                if (r, c) in policy:
                    act_idx = policy[(r, c)]
                    policy_matrix[r][c] = action_symbols[act_idx]
    
    # Build value matrix
    value_matrix = [[0.0 for _ in range(n)] for _ in range(n)]
    for r in range(n):
        for c in range(n):
            state_list = [r, c]
            if state_list in st.session_state.obstacles:
                value_matrix[r][c] = 'X'
            elif state_list == st.session_state.end_pos:
                value_matrix[r][c] = 0.0
            else:
                value_matrix[r][c] = round(V.get((r, c), 0.0), 2)
    
    # Display matrices
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Policy Matrix (最優策略)：**")
        st.dataframe(
            pd.DataFrame(policy_matrix),
            use_container_width=True,
            hide_index=False
        )
    
    with col2:
        st.write("**Value Function (狀態價值)：**")
        st.dataframe(
            pd.DataFrame(value_matrix),
            use_container_width=True,
            hide_index=False
        )
    
    # Display optimal path
    st.divider()
    st.write("**最優路徑：**")
    if optimal_path:
        path_str = " → ".join([f"({p[0]},{p[1]})" for p in optimal_path])
        st.info(f"路徑: {path_str}")
        st.success(f"路徑長度: {len(optimal_path) - 1} 步")
    else:
        st.warning("無法到達終點")
    
    # Visualize path on grid
    st.write("**路徑可視化：**")
    grid_visual = [['.' for _ in range(n)] for _ in range(n)]
    
    # Mark obstacles
    for obs in st.session_state.obstacles:
        grid_visual[obs[0]][obs[1]] = '■'
    
    # Mark optimal path
    for pos in optimal_path:
        if pos != st.session_state.start_pos and pos != st.session_state.end_pos:
            grid_visual[pos[0]][pos[1]] = '*'
    
    # Mark start and end
    if st.session_state.start_pos:
        grid_visual[st.session_state.start_pos[0]][st.session_state.start_pos[1]] = 'S'
    if st.session_state.end_pos:
        grid_visual[st.session_state.end_pos[0]][st.session_state.end_pos[1]] = 'G'
    
    grid_visual_str = "\n".join(["  ".join(row) for row in grid_visual])
    st.code(grid_visual_str, language="text")
    
    st.caption("S=起始點, G=終點, *=最優路徑, ■=障礙物, .=其他格子")
