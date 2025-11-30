import gradio as gr
import matplotlib.pyplot as plt
import random
from typing import List, Tuple, Optional

from src.models.entities.player import Player
from src.models.entities.game_configuration import GameConfiguration
from src.models.enums.algorithm_type import AlgorithmType
from src.simulation.simulation_engine import SimulationEngine


class GradioInterface:
    """
    Gradio-based web interface for the Airport Cost-Sharing Game.
    """

    def __init__(self):
        self.simulation_engine = SimulationEngine()
        self.players: List[Player] = []

    def generate_players(self, num_players: int) -> Tuple[str, str]:
        """
        Generate random players with random costs.
        
        Args:
            num_players: Number of players to generate
            
        Returns:
            Tuple of (status message, player list display)
        """
        try:
            if num_players <= 0:
                return "❌ Error: Number of airlines must be positive.", ""
            
            self.players = []
            player_list = []
            
            for i in range(num_players):
                # Generate realistic runway length requirements (1000-4000 meters)
                runway_length = random.randint(1000, 4000)
                player = Player(id=f"P{i+1}", name=f"Airline {i+1}", cost=float(runway_length))
                self.players.append(player)
                player_list.append(f"{player.name}: Requires {player.cost:.0f}m runway")
            
            status = f"✅ Successfully generated {num_players} airlines!"
            players_display = "\n".join(player_list)
            
            return status, players_display
            
        except Exception as e:
            return f"❌ Error: {str(e)}", ""

    def run_simulation(
        self, 
        algorithm: str, 
        num_samples: int
    ) -> Tuple[str, Optional[plt.Figure]]:
        """
        Run the simulation with the current players and settings.
        
        Args:
            algorithm: Algorithm type ("exact" or "approximate")
            num_samples: Number of samples for approximate algorithm
            
        Returns:
            Tuple of (results text, matplotlib figure)
        """
        if not self.players:
            return "⚠️ Warning: Please generate airlines first.", None
        
        try:
            algo = AlgorithmType(algorithm)
            samples = num_samples if algo == AlgorithmType.APPROXIMATE else None
            
            config = GameConfiguration(
                players=self.players,
                algorithm=algo,
                num_samples=samples
            )
            
            result = self.simulation_engine.run_simulation(config)
            
            # Format results text
            results_text = self._format_results(result)
            
            # Create plot
            fig = self._create_plot(result)
            
            return results_text, fig
            
        except Exception as e:
            return f"❌ Error: Simulation failed - {str(e)}", None

    def _format_results(self, result) -> str:
        """Format calculation results as readable text."""
        # Assuming cost per meter is $1000 (typical runway construction cost)
        cost_per_meter = 1000
        total_cost_dollars = result.total_cost * cost_per_meter
        
        lines = [
            "=" * 60,
            "📊 SIMULATION RESULTS",
            "=" * 60,
            f"\n🔧 Algorithm: {result.algorithm_used.value}",
            f"✈️  Runway Length Built: {result.total_cost:.0f} meters",
            f"💰 Total Construction Cost: ${total_cost_dollars:,.0f}",
            f"⏱️  Execution Time: {result.execution_time:.4f} seconds",
            "\n" + "=" * 60,
            "📈 FAIR COST ALLOCATION (Shapley Values)",
            "=" * 60,
            "Each airline's fair share of the runway construction cost:",
            "",
        ]
        
        for pid, val in result.shapley_values.items():
            cost_dollars = val * cost_per_meter
            percentage = (val / result.total_cost * 100) if result.total_cost > 0 else 0
            lines.append(f"{pid}: ${cost_dollars:,.0f} ({percentage:.1f}% of total)")
        
        # Add verification
        total_allocated = sum(result.shapley_values.values())
        total_allocated_dollars = total_allocated * cost_per_meter
        lines.append("\n" + "=" * 60)
        lines.append(f"✓ Total Allocated: ${total_allocated_dollars:,.0f}")
        lines.append(f"✓ Verification: {'PASSED ✅' if abs(total_allocated - result.total_cost) < 0.01 else 'FAILED ❌'}")
        lines.append("=" * 60)
        
        return "\n".join(lines)

    def _create_plot(self, result) -> plt.Figure:
        """Create a bar chart visualization of Shapley values."""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Convert to dollars (assuming $1000 per meter)
        cost_per_meter = 1000
        ids = list(result.shapley_values.keys())
        values_dollars = [v * cost_per_meter for v in result.shapley_values.values()]
        
        bars = ax.bar(ids, values_dollars, color='#4A90E2', alpha=0.8, edgecolor='#2E5C8A', linewidth=2)
        
        # Add value labels on top of bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'${height:,.0f}',
                   ha='center', va='bottom', fontweight='bold')
        
        ax.set_ylabel('Fair Cost Share ($)', fontsize=12, fontweight='bold')
        ax.set_xlabel('Airline', fontsize=12, fontweight='bold')
        ax.set_title('Runway Construction Cost Allocation (Shapley Values)', 
                    fontsize=14, fontweight='bold', pad=20)
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        
        # Format y-axis to show dollar amounts
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
        
        plt.tight_layout()
        return fig

    def create_interface(self) -> gr.Blocks:
        """
        Create the Gradio interface.
        
        Returns:
            Gradio Blocks interface
        """
        with gr.Blocks(
            title="Airport Cost-Sharing Game - Shapley Values"
        ) as interface:
            gr.Markdown(
                """
                # ✈️ Airport Runway Cost-Sharing Problem
                
                ## The Problem
                
                Multiple airlines operate at an airport and need runways of different lengths:
                - **Small aircraft** (regional jets): Need ~1,500m runway
                - **Medium aircraft** (narrow-body): Need ~2,500m runway  
                - **Large aircraft** (wide-body): Need ~3,500m runway
                
                Instead of each airline building their own runway, they can **share one runway** 
                that's long enough for the largest aircraft. Building a runway costs approximately 
                **$1,000 per meter**.
                
                ## The Question
                
                **How should the airlines fairly split the construction cost?**
                
                This application uses **Shapley values** from cooperative game theory to determine 
                a fair cost allocation that considers each airline's runway requirement and their 
                marginal contribution to the shared infrastructure.
                
                ### Example
                - Airline A needs 1,500m → Would cost $1.5M alone
                - Airline B needs 3,000m → Would cost $3M alone
                - **Together**: Build one 3,000m runway for $3M (save $1.5M!)
                - **Shapley values determine**: How much should each pay?
                """
            )
            
            with gr.Row():
                with gr.Column(scale=1):
                    gr.Markdown("## ⚙️ Configuration")
                    
                    num_players_slider = gr.Slider(
                        minimum=2,
                        maximum=10,
                        value=3,
                        step=1,
                        label="Number of Airlines",
                        info="Airlines operating at the airport with different runway needs"
                    )
                    
                    generate_btn = gr.Button(
                        "🎲 Generate Random Airlines",
                        variant="primary",
                        size="lg"
                    )
                    
                    status_box = gr.Textbox(
                        label="Status",
                        interactive=False,
                        lines=1
                    )
                    
                    players_display = gr.Textbox(
                        label="Airlines & Runway Requirements",
                        interactive=False,
                        lines=8,
                        placeholder="Click 'Generate Random Airlines' to start..."
                    )
                    
                    gr.Markdown("---")
                    gr.Markdown("## 🎯 Algorithm Settings")
                    
                    algorithm_radio = gr.Radio(
                        choices=["exact", "approximate"],
                        value="exact",
                        label="Algorithm Type",
                        info="Exact: Precise calculation | Approximate: Faster for many players"
                    )
                    
                    samples_slider = gr.Slider(
                        minimum=100,
                        maximum=10000,
                        value=1000,
                        step=100,
                        label="Samples (for Approximate)",
                        info="More samples = higher accuracy but slower"
                    )
                    
                    run_btn = gr.Button(
                        "▶️ Run Simulation",
                        variant="primary",
                        size="lg"
                    )
                
                with gr.Column(scale=2):
                    gr.Markdown("## 📊 Results")
                    
                    results_text = gr.Textbox(
                        label="Calculation Results",
                        interactive=False,
                        lines=20,
                        placeholder="Results will appear here after running the simulation..."
                    )
                    
                    plot_output = gr.Plot(
                        label="Cost Allocation Visualization"
                    )
            
            gr.Markdown(
                """
                ---
                ### 📚 About Shapley Values
                
                The **Shapley value** is a solution concept in cooperative game theory developed by 
                Lloyd Shapley (Nobel Prize 2012). It fairly distributes costs based on each player's 
                **marginal contribution** to all possible coalitions.
                
                **Key Properties:**
                - ✅ **Efficiency**: The total cost is fully allocated (no surplus or deficit)
                - ✅ **Fairness**: Players with similar contributions pay similar amounts
                - ✅ **Additivity**: Contributions are evaluated across all possible scenarios
                - ✅ **Null player**: Airlines requiring no runway pay nothing
                
                **Why it works for airports:**  
                If a small airline only needs 1,500m but joins others building a 3,500m runway, 
                they shouldn't pay half the cost - Shapley values ensure they pay proportionally 
                to their actual need and contribution.
                """
            )
            
            # Event handlers
            generate_btn.click(
                fn=self.generate_players,
                inputs=[num_players_slider],
                outputs=[status_box, players_display]
            )
            
            run_btn.click(
                fn=self.run_simulation,
                inputs=[algorithm_radio, samples_slider],
                outputs=[results_text, plot_output]
            )
        
        return interface

    def launch(self, share: bool = False, server_port: int = 7860):
        """
        Launch the Gradio interface.
        
        Args:
            share: Whether to create a public sharing link
            server_port: Port to run the server on
        """
        interface = self.create_interface()
        interface.launch(
            share=share,
            server_port=server_port,
            server_name="0.0.0.0"
        )


def create_app(share: bool = False) -> gr.Blocks:
    """
    Factory function to create the Gradio app.
    
    Args:
        share: Whether to enable public sharing
        
    Returns:
        Gradio Blocks interface
    """
    app = GradioInterface()
    return app.create_interface()


if __name__ == "__main__":
    app = GradioInterface()
    app.launch(share=True)
