import sys
import os
import argparse

# Add the project root to the python path to ensure imports work correctly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.ui.gradio_interface import GradioInterface

def main():
    """
    Entry point for the Airport Cost-Sharing Game application.
    """
    parser = argparse.ArgumentParser(
        description="Airport Cost-Sharing Game - Shapley Values Web Interface"
    )
    parser.add_argument(
        "--share",
        action="store_true",
        help="Create a public sharing link (accessible from anywhere)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=7860,
        help="Port to run the web server on (default: 7860)"
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("- Starting Airport Cost-Sharing Game Web Interface...")
    print("=" * 60)
    
    if args.share:
        print("- Public sharing enabled - generating shareable link...")
    else:
        print("- Running locally only")
    
    print(f"Server port: {args.port}")
    print("=" * 60)
    
    app = GradioInterface()
    app.launch(share=args.share, server_port=args.port)

if __name__ == "__main__":
    main()
