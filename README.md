# Containment Protocol


# Week 1 — Conway's Game of Life

## Overview

The goal of Week 1 is to understand how extremely simple local rules can generate surprisingly complex global behavior through **Conway's Game of Life**.

## Learning Objectives

- Understand Cellular Automata
- Learn neighborhood-based state updates
- Observe emergent behavior
- Experiment with modified rules

## Resources

- Numberphile — Game of Life
- Conway's Game of Life explanation videos

## Tasks

- Implement Conway's Game of Life using NumPy
- Visualize the simulation
- Modify one rule and observe its effect
- Record a 30-second demonstration

## Concepts Covered

- Cellular Automata
- Moore Neighborhood
- Emergence
- Oscillators
- Still Lifes
- Gliders

## Deliverables

- Source code
- Simulation video
- Brief explanation of the modified rule

---

# Week 2 — Neural Cellular Automata

## Overview

Traditional Cellular Automata use hand-crafted update rules. Neural Cellular Automata instead **learn local update rules using neural networks**, enabling growth, regeneration, and self-organization from a simple seed.

## Learning Objectives

- Understand Neural Cellular Automata
- Learn how local neural updates create global structures
- Explore growth and self-repair

## Resources

- Distill — Growing Neural Cellular Automata
- Neural Cellular Automata videos
- Weights & Biases implementation guide

## Tasks

### Task 1 — Reproduce the Baseline

Implement the baseline Neural Cellular Automata model.

### Task 2 — Analyze the Model

Study:

- Input to the update network
- Output of the update network
- State tensor dimensions
- Hidden channels
- Training objective

### Task 3 — Growth Visualization

Visualize:

- Initial seed
- Intermediate growth
- Final image

### Task 4 — Damage and Recovery

- Introduce damage after growth
- Observe and visualize recovery

## Concepts Covered

- Learned local rules
- Self-organization
- Regeneration
- Neural update networks
- Differentiable simulation

## Deliverables

- Model implementation
- Growth visualization
- Recovery experiment

---

# Week 3 — Multi-Agent Systems and Emergent Behavior

## Overview

Week 3 explores how intelligent global behavior emerges from interactions among many independent agents without any centralized controller. Using the **Boids** model, this week demonstrates how simple local rules lead to flocking, coordination, and other emergent behaviors. 0

## Learning Objectives

- Understand agents and multi-agent systems
- Learn how local interactions create global behavior
- Explore flocking and swarm intelligence
- Understand information propagation in decentralized systems 1

## Resources

- Sebastian Lague — Boids
- Craig Reynolds — *Flocks, Herds, and Schools*
- Kurzgesagt — Emergence
- Introduction to Agent-Based Modeling
- Network Effects and Spreading Dynamics 2

## Tasks

### Task 1 — Boids Simulation

Implement a Boids simulation featuring:

- Separation
- Alignment
- Cohesion

### Task 2 — Parameter Exploration

Experiment with:

- Neighbor radius
- Alignment strength
- Separation strength

Observe changes in flocking behavior.

### Task 3 — Obstacles

Introduce environmental obstacles and observe how agents adapt.

### Task 4 — Predator and Prey

Add:

- Predator agents
- Prey agents

Study chasing and escape dynamics.

### Task 5 — Information Propagation

Mark one agent as informed and visualize how information spreads through the population.

### Mini Project — Zombie Evacuation Simulator

Build a simulation where:

- Civilians avoid zombies
- Zombies chase civilians
- Civilians share danger information

The objective is to study emergent behavior using only local interaction rules. 3

## Concepts Covered

- Multi-Agent Systems
- Emergence
- Swarm Intelligence
- Agent-Based Modeling
- Information Propagation
- Decentralized Coordination

## Deliverables

- Boids simulation
- Parameter experiments
- Obstacle simulation
- Predator-prey simulation
- Information propagation simulation

---

## Technologies

- Python
- NumPy
- Matplotlib / Pygame (Visualization)
- PyTorch (Week 2)

---

## Learning Outcome

By the end of this series, I gained practical experience in how **simple local interactions can collectively produce complex, intelligent global behavior**, forming the foundation of Cellular Automata, Neural Cellular Automata, Multi-Agent Systems, and Swarm Intelligence.
