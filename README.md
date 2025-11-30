# Airport Runway Cost-Sharing Problem with Shapley Values

## Overview

This project implements a simulation of the **Airport Runway Cost-Sharing Problem**, a classic problem in cooperative game theory. The application demonstrates how to fairly distribute the cost of shared infrastructure among multiple stakeholders with different requirements.

### The Real-World Problem

Multiple airlines operate at an airport and need runways of different lengths:
- **Small aircraft** (regional jets): Need ~1,500m runway
- **Medium aircraft** (narrow-body): Need ~2,500m runway  
- **Large aircraft** (wide-body): Need ~3,500m runway

Instead of each airline building their own runway, they can **share one runway** that's long enough for the largest aircraft. Building a runway costs approximately **$1,000 per meter**.

**The Question**: How should the airlines fairly split the construction cost?

The system uses **Shapley Values** from cooperative game theory to determine a fair cost allocation that considers each airline's runway requirement and their marginal contribution to the shared infrastructure.

### Example Scenario

Consider three airlines:
- **Airline A** needs 1,500m runway → Would cost $1.5M if built alone
- **Airline B** needs 2,500m runway → Would cost $2.5M if built alone
- **Airline C** needs 3,500m runway → Would cost $3.5M if built alone

**If they cooperate**: Build one 3,500m runway for $3.5M (saves $3.5M compared to building separately!)

But how should the $3.5M be split? This is where Shapley values provide the answer.

## Why Shapley Values? (Not Simple Proportional Allocation)

You might wonder: Why not just split costs proportionally to runway length requirements?

### The Problem with Proportional Allocation

Simple proportional allocation would calculate each airline's share as:

```
Share = (Airline's requirement / Total of all requirements) × Total cost
```

**Example with proportional split:**
- Airline A (1,500m): (1,500/7,500) × $3.5M = **$700,000** (20%)
- Airline B (2,500m): (2,500/7,500) × $3.5M = **$1,166,667** (33.3%)
- Airline C (3,500m): (3,500/7,500) × $3.5M = **$1,633,333** (46.7%)

### Why This is Unfair

**Problem 1: Ignores Standalone Costs**
- Airline A would only pay $1.5M alone, but proportional method could charge them more
- Airline C could build their own 3,500m runway for $3.5M, so they shouldn't pay more than that

**Problem 2: Doesn't Consider Marginal Contributions**
- If Airline A joins a coalition with B and C, they add **zero cost** (runway is already 3,500m)
- Proportional allocation ignores this - it treats all airlines as equally responsible

**Problem 3: Not Coalition-Proof**
- Airlines might prefer to form smaller coalitions
- Example: B and C might exclude A if A's proportional share seems unfair

### How Shapley Values Fix This

Shapley values calculate each player's **marginal contribution** across all possible coalition formations:

1. **Considers all scenarios**: What happens if airlines join in different orders?
2. **Marginal contribution**: How much does each airline increase the total cost?
3. **Fair averaging**: Takes the average marginal contribution across all possible orderings

**Shapley Value Calculation (simplified):**

For Airline A (1,500m):
- Joins first: Contributes $1.5M
- Joins after B: Contributes $0 (B already needs 2,500m)
- Joins after C: Contributes $0 (C already needs 3,500m)
- Joins after B&C: Contributes $0
- Average contribution ≈ **$500,000** ✅

For Airline C (3,500m):
- Joins first: Contributes $3.5M
- Joins after A: Contributes $2M (3,500m - 1,500m)
- Joins after B: Contributes $1M (3,500m - 2,500m)
- Joins after A&B: Contributes $1M
- Average contribution ≈ **$2,000,000** ✅

### Key Advantages of Shapley Values

✅ **Efficiency**: Total cost is fully allocated (no surplus or deficit)
✅ **Fairness**: Players with similar contributions pay similar amounts  
✅ **Individual Rationality**: No player pays more than their standalone cost
✅ **Null Player**: Players adding zero value pay nothing
✅ **Additivity**: Works consistently across different cost structures
✅ **Coalition-Proof**: No group of players benefits from excluding others

### Mathematical Guarantee

The Shapley value is the **unique allocation** that satisfies all these fairness properties simultaneously. This was proven by Lloyd Shapley (Nobel Prize in Economics, 2012).

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
