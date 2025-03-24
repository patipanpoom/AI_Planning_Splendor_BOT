# Splendor AI Agent - COMP90054 AI Planning for Autonomy

This project was completed as part of **COMP90054: AI Planning for Autonomy** at The University of Melbourne (Semester 1, 2024). The objective was to design an autonomous agent to play the strategic board game **Splendor** intelligently in a competitive environment.

## Overview

Splendor is a resource management and strategy game. In this project, I developed an AI agent capable of making optimal decisions based on the game state, opponent behavior, and available actions.

My custom agent implementation is located in:

agents/t_039/myTeam.py

You can run the agent using:

The second agent can be replaced with any other agent for testing purposes.

python general_game_runner.py -g Splendor -a agents.t_039.myTeam,agents.t_039.minimax
---

## AI Techniques Used

The agent combines the following three AI techniques:

### 1. Q-Learning (Model-Free Reinforcement Learning)

- Implemented to enable the agent to learn optimal policies through exploration and exploitation.
- The agent updates its action-value function based on game state transitions and rewards.
- This approach produced the **best overall performance** among the techniques used.

### 2. Monte Carlo Tree Search (MCTS)

- Utilized to probabilistically explore possible future game states.
- Balances exploration and exploitation to optimize decision-making under uncertainty.

### 3. Minimax Algorithm

- Applied to model adversarial scenarios by assuming rational opponent behavior.
- Useful for evaluating safe moves in deterministic parts of the game.

---

## Key Features

- **Reinforcement Learning-Based Strategy**: Q-Learning agent continuously refines its policy through experience.
- **Dynamic Opponent Modeling**: Adapts based on observed opponent actions.
- **Robustness**: Avoids hard-coded rules, ensuring generalization across various game situations.
- **Efficient Decision-Making**: Designed to perform reliably within time constraints during competitions.

---

## How to Run

1. Clone the repository:

    ```bash
    git clone <your-repo-link>
    cd <repo-directory>
    ```

2. Run the agent:

    ```bash
    python general_game_runner.py -g Splendor -a agents.t_039.myTeam,agents.t_039.minimax
    ```

3. Replace `agents.t_039.minimax` with other agents for testing if desired.

---

## Technologies Used

- **Python 3**
- AI Techniques: Q-Learning, Monte Carlo Tree Search (MCTS), Minimax
- Provided Splendor game simulator and engine.

---

## My Role

- Designed and implemented the AI agent logic in `agents/t_039/myTeam.py`.
- Integrated Q-Learning to balance short-term and long-term strategies.
- Conducted testing and fine-tuning to ensure robust performance in competitive scenarios.
