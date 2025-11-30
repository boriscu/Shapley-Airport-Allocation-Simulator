import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from typing import List
import random

from src.models.entities.player import Player
from src.models.entities.game_configuration import GameConfiguration
from src.models.enums.algorithm_type import AlgorithmType
from src.simulation.simulation_engine import SimulationEngine

class MainWindow(tk.Tk):
    """
    Main GUI Window for the Airport Cost-Sharing Game.
    """

    def __init__(self):
        super().__init__()
        self.title("Airport Cost-Sharing Game - Shapley Values")
        self.geometry("1000x800")
        
        self.simulation_engine = SimulationEngine()
        self.players: List[Player] = []
        
        self._create_widgets()
        self._setup_layout()

    def _create_widgets(self):
        # Configuration Frame
        self.config_frame = ttk.LabelFrame(self, text="Configuration")
        
        self.num_players_label = ttk.Label(self.config_frame, text="Number of Players:")
        self.num_players_var = tk.IntVar(value=3)
        self.num_players_entry = ttk.Entry(self.config_frame, textvariable=self.num_players_var)
        
        self.generate_btn = ttk.Button(self.config_frame, text="Generate Random Players", command=self._generate_players)
        
        self.players_listbox = tk.Listbox(self.config_frame, height=10)
        
        self.algo_label = ttk.Label(self.config_frame, text="Algorithm:")
        self.algo_var = tk.StringVar(value=AlgorithmType.EXACT.value)
        self.algo_combo = ttk.Combobox(self.config_frame, textvariable=self.algo_var, values=[e.value for e in AlgorithmType])
        
        self.samples_label = ttk.Label(self.config_frame, text="Samples (Approx):")
        self.samples_var = tk.IntVar(value=1000)
        self.samples_entry = ttk.Entry(self.config_frame, textvariable=self.samples_var)
        
        self.run_btn = ttk.Button(self.config_frame, text="Run Simulation", command=self._run_simulation)
        
        # Results Frame
        self.results_frame = ttk.LabelFrame(self, text="Results")
        self.result_text = tk.Text(self.results_frame, height=10, width=50)
        
        # Plot Frame
        self.plot_frame = ttk.Frame(self)
        self.figure, self.ax = plt.subplots(figsize=(5, 4))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.plot_frame)

    def _setup_layout(self):
        self.config_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        self.num_players_label.pack(pady=5)
        self.num_players_entry.pack(pady=5)
        self.generate_btn.pack(pady=5)
        self.players_listbox.pack(pady=5, fill=tk.X)
        
        self.algo_label.pack(pady=5)
        self.algo_combo.pack(pady=5)
        
        self.samples_label.pack(pady=5)
        self.samples_entry.pack(pady=5)
        
        self.run_btn.pack(pady=20)
        
        self.results_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        self.result_text.pack(fill=tk.BOTH, expand=True)
        
        self.plot_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def _generate_players(self):
        try:
            num = self.num_players_var.get()
            if num <= 0:
                raise ValueError("Number of players must be positive.")
            
            self.players = []
            self.players_listbox.delete(0, tk.END)
            
            for i in range(num):
                cost = random.randint(10, 100)
                player = Player(id=f"P{i+1}", name=f"Airline {i+1}", cost=float(cost))
                self.players.append(player)
                self.players_listbox.insert(tk.END, f"{player.name}: Cost {player.cost}")
                
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def _run_simulation(self):
        if not self.players:
            messagebox.showwarning("Warning", "Please generate players first.")
            return
            
        try:
            algo_str = self.algo_var.get()
            algo = AlgorithmType(algo_str)
            samples = self.samples_var.get() if algo == AlgorithmType.APPROXIMATE else None
            
            config = GameConfiguration(
                players=self.players,
                algorithm=algo,
                num_samples=samples
            )
            
            result = self.simulation_engine.run_simulation(config)
            
            self._display_results(result)
            self._plot_results(result)
            
        except Exception as e:
            messagebox.showerror("Error", f"Simulation failed: {str(e)}")

    def _display_results(self, result):
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, f"Algorithm: {result.algorithm_used}\n")
        self.result_text.insert(tk.END, f"Total Cost: {result.total_cost}\n")
        self.result_text.insert(tk.END, f"Execution Time: {result.execution_time:.4f}s\n\n")
        self.result_text.insert(tk.END, "Shapley Values:\n")
        
        for pid, val in result.shapley_values.items():
            self.result_text.insert(tk.END, f"{pid}: {val:.2f}\n")

    def _plot_results(self, result):
        self.ax.clear()
        ids = list(result.shapley_values.keys())
        values = list(result.shapley_values.values())
        
        self.ax.bar(ids, values, color='skyblue')
        self.ax.set_ylabel('Shapley Value (Cost Share)')
        self.ax.set_title('Cost Allocation per Player')
        
        self.canvas.draw()

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
