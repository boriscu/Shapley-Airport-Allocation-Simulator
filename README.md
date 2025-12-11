# Airport Runway Cost-Sharing Problem with Shapley Values

## Overview

This project implements a simulation of the **Airport Runway Cost-Sharing Problem**, a classic problem in cooperative game theory. The application demonstrates how to fairly distribute the cost of shared infrastructure among multiple stakeholders with different requirements.

### The Real-World Problem

Multiple airlines operate at an airport and need runways of different lengths:
- **Small aircraft** (regional jets): Need ~1,500m runway
- **Medium aircraft** (narrow-body): Need ~2,500m runway  
- **Large aircraft** (wide-body): Need ~3,500m runway.

Instead of each airline building their own runway, they can **share one runway** that's long enough for the largest aircraft. Building a runway costs approximately **$1,000 per meter**.

**The Question**: How should the airlines fairly split the construction cost?

The system uses **Shapley Values** from cooperative game theory to determine a fair cost allocation that considers each airline's runway requirement and their marginal contribution to the shared infrastructure.

### Example Scenario: The Airport (Runway) Problem

Three airlines require different runway lengths:

- **Airline A**: 1,500 m
- **Airline B**: 2,500 m
- **Airline C**: 3,500 m

If each airline built separately, the total cost would be:

- 1,500 m → $1.5M
- 2,500 m → $2.5M
- 3,500 m → $3.5M
- **Total if built alone**: $7.5M

If they cooperate, only one runway must be built, at the longest required length:

- **Joint cost** = $3.5M

This creates substantial savings. The question is: **How should the $3.5M be split fairly among the airlines?**

This is the classic **Airport Problem** in cooperative game theory, solved by the Shapley value.

## Why Not Split Cost Proportionally to Runway Length?

A proportional split based on runway requirements seems intuitive, but **it is not valid for this problem**.

The reason is simple: **runway length is a non-additive, nested public good.**

- The cost is determined by the **maximum requirement**, not by summing individual requirements.
- Proportional allocation incorrectly assumes that each airline contributes proportionally to the total cost, but in reality:
  - Airlines contribute **only by increasing the maximum runway length**.
  - Additional runway length beyond an airline's requirement provides it **no additional value**.
  - Smaller airlines do not cause extensions beyond the larger airlines' requirements.

Therefore, **proportional splitting does not reflect how cost is actually generated**.

## Shapley Value: The Fair Solution

In the Airport Problem, the Shapley value distributes cost based on **which coalition of airlines causes each segment of the runway to be necessary**.

**Break the 3,500 m runway into cost segments** based on requirement thresholds:

| Runway Segment | Length | Cost | Required by |
|----------------|--------|------|-------------|
| 0–1,500 m | 1,500 m | $1.5M | A, B, C |
| 1,500–2,500 m | 1,000 m | $1.0M | B, C |
| 2,500–3,500 m | 1,000 m | $1.0M | C |

**Each segment is split equally among the airlines that need it.**

### Segment 1 (0–1,500 m)
- **Cost**: $1.5M
- **Users**: A, B, C
- **Share**: $0.5M each

### Segment 2 (1,500–2,500 m)
- **Cost**: $1.0M
- **Users**: B, C
- **Share**: $0.5M each

### Segment 3 (2,500–3,500 m)
- **Cost**: $1.0M
- **Users**: C
- **Share**: $1.0M

### Final Shapley Value Cost Allocation

| Airline | Segment 1 | Segment 2 | Segment 3 | Total |
|---------|-----------|-----------|-----------|-------|
| A | $0.5M | — | — | **$0.5M** |
| B | $0.5M | $0.5M | — | **$1.0M** |
| C | $0.5M | $0.5M | $1.0M | **$2.0M** |

**Total**: $0.5M + $1.0M + $2.0M = $3.5M

### Key Advantages

This allocation satisfies the key Shapley axioms:

✅ **Efficiency** (the full cost is allocated)  
✅ **Symmetry** (equal treatment of equal contributors)  
✅ **Dummy player** (those who add no extension pay nothing for it)  
✅ **Additivity** (consistent across cost structures)

### Mathematical Guarantee

For the Airport Problem, the Shapley value is known to be the **unique allocation rule** satisfying these fairness properties.

## Features

- **Web Interface**: Modern Gradio-based web UI accessible from any browser
- **Real-World Context**: Generates realistic runway requirements (1,000-4,000 meters)
- **Accurate Costing**: Uses industry-standard construction costs ($1,000/meter)
- **Modular Architecture**: Clean separation of concerns using Domain-Driven Design (DDD) principles
- **Shapley Value Calculation**:
  - **Exact Algorithm**: Computes exact Shapley values by evaluating all permutations (O(N!)). Suitable for small groups (2-10 airlines)
  - **Approximate Algorithm**: Uses Monte Carlo sampling to estimate Shapley values. Suitable for larger groups
- **Interactive Visualization**: Bar charts showing cost allocation with dollar amounts
- **Shareable Links**: Create public sharing links to demonstrate the simulation
- **Extensible Design**: Built with inheritance, polymorphism, and design patterns (Factory, Singleton)

## Installation

### Prerequisites
- Python 3.8 or higher
- Conda (recommended for environment management)

### Setting up the Environment

1. Create a new Conda environment:
   ```bash
   conda create -n shappley python=3.10
   ```

2. Activate the environment:
   ```bash
   conda activate shappley
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Web Interface

To start the web application locally (accessible only from your machine):
```bash
python main.py
```

Then open your browser to: `http://localhost:7860`

### Creating a Shareable Link

To create a public sharing link that anyone can access:
```bash
python main.py --share
```

Gradio will generate a temporary public URL (valid for 72 hours) that you can share with others.

### Custom Port

To run on a different port:
```bash
python main.py --port 8080
```

### Using the Interface

1. Set the **Number of Airlines** (2-10)
2. Click **"🎲 Generate Random Airlines"** to create airlines with random runway requirements
3. Select the **Algorithm** (exact or approximate)
4. For approximate algorithm, adjust the **number of samples** (more = slower but more accurate)
5. Click **"▶️ Run Simulation"** to calculate fair cost allocation
6. View results showing:
   - Runway length built
   - Total construction cost
   - Each airline's fair share (in dollars and percentage)
   - Visualization bar chart

### Running the Verification Script

To verify the correctness of the implementation against known examples:
```bash
python verify.py
```

## Project Structure

```
src/
├── domain/          # Game logic (Airport Game implementation)
├── infrastructure/  # Shared services (Logger, Config)
├── models/          # Data structures
│   ├── entities/    # Pydantic models (Player, Config, Result)
│   └── enums/       # Enumerations (AlgorithmType)
├── services/        # Shapley calculators (Exact, Approximate)
├── simulation/      # Simulation orchestration
└── ui/              # Web User Interface (Gradio)
```

## Educational Value

This application is ideal for:
- **Economics & Game Theory Courses**: Demonstrates cooperative game theory concepts
- **Operations Research**: Shows practical optimization problems
- **Infrastructure Planning**: Illustrates cost-sharing in shared facilities
- **Algorithm Comparison**: Compare exact vs. approximate calculation methods

## Technical Details

- **UI Framework**: Gradio 6.0+
- **Data Modeling**: Pydantic for type-safe data structures
- **Visualization**: Matplotlib with Gradio integration
- **Architecture**: Clean architecture with clear separation of concerns
- **Design Patterns**: Factory pattern for algorithm selection, Singleton for logger

## License

This project is for educational purposes.

## References

- Shapley, L. S. (1953). "A Value for n-person Games"
- Airport Game: Classic example in cooperative game theory
- Nobel Prize 2012: Alvin Roth and Lloyd Shapley - Theory of Stable Allocations
