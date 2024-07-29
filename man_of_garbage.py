import streamlit as st
import random
import time
import math

# Initialize game state
if 'game_state' not in st.session_state:
    st.session_state.game_state = {
        'points': 0,
        'time_left': 120,
        'garbage_positions': [],
        'game_over': False,
        'last_spawn_time': time.time()
    }

def distance(pos1, pos2):
    return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

def spawn_garbage():
    if len(st.session_state.game_state['garbage_positions']) < 5:  # Limit to 5 pieces of garbage
        max_attempts = 100
        for _ in range(max_attempts):
            x = random.randint(50, 750)  # X coordinate
            y = random.randint(50, 550)  # Y coordinate
            new_position = (x, y)
            
            # Check for overlaps
            if not any(distance(new_position, pos) < 60 for pos in st.session_state.game_state['garbage_positions']):
                st.session_state.game_state['garbage_positions'].append(new_position)
                break

def collect_garbage(x, y):
    if (x, y) in st.session_state.game_state['garbage_positions']:
        st.session_state.game_state['garbage_positions'].remove((x, y))
        st.session_state.game_state['points'] += 1
        spawn_garbage()  # Spawn a new piece of garbage immediately

def reset_game():
    st.session_state.game_state = {
        'points': 0,
        'time_left': 120,
        'garbage_positions': [],
        'game_over': False,
        'last_spawn_time': time.time()
    }

def main():
    random.seed()  # Initialize random seed
    st.title("Man of Garbage")

    # Create placeholders for dynamic content
    timer_placeholder = st.empty()
    points_placeholder = st.empty()
    game_area = st.empty()
    result_placeholder = st.empty()

    # Main game loop
    if not st.session_state.game_state['game_over']:
        # Update timer
        st.session_state.game_state['time_left'] -= 1
        
        # Spawn garbage every 3 seconds
        current_time = time.time()
        if current_time - st.session_state.game_state['last_spawn_time'] >= 3:
            spawn_garbage()
            st.session_state.game_state['last_spawn_time'] = current_time

        # Display game elements
        with game_area.container():
            cols = st.columns(5)  # Create 5 columns for garbage placement
            for idx, (x, y) in enumerate(st.session_state.game_state['garbage_positions']):
                col = cols[idx % 5]
                if col.button("🗑️", key=f"garbage_{x}_{y}"):
                    collect_garbage(x, y)

        # Check game over conditions
        if st.session_state.game_state['points'] >= 10:
            st.session_state.game_state['game_over'] = True
            result_placeholder.success("Winner winner chicken dinner!")
        elif st.session_state.game_state['time_left'] <= 0:
            st.session_state.game_state['game_over'] = True
            result_placeholder.error("Sorry not sorry, you lose!")

    else:
        # Game over state
        if st.button("Play Again"):
            reset_game()
            st.rerun()

    # Update displays
    timer_placeholder.text(f"Time left: {st.session_state.game_state['time_left']} seconds")
    points_placeholder.text(f"Points: {st.session_state.game_state['points']}")

    # Rerun the app
    if not st.session_state.game_state['game_over']:
        time.sleep(1)
        st.rerun()

if __name__ == "__main__":
    main()
