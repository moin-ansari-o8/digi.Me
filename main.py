#!/usr/bin/env python3
"""Main entry point for digi.Me bot"""

import sys
import argparse
from src.bot import DigiMeBot
from src.dashboard.app import run_dashboard


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='digi.Me - Your AI Twin for WhatsApp',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py bot                    # Start the WhatsApp bot
  python main.py dashboard              # Start the web dashboard
  python main.py both                   # Start both (requires separate terminals)

Before running:
  1. Copy .env.example to .env
  2. Fill in your API keys and configuration
  3. Add approved contacts to APPROVED_CONTACTS
        """
    )
    
    parser.add_argument(
        'mode',
        choices=['bot', 'dashboard', 'both'],
        help='Run mode: bot (WhatsApp automation), dashboard (web interface), or both'
    )
    
    parser.add_argument(
        '--host',
        default=None,
        help='Dashboard host (default: from .env)'
    )
    
    parser.add_argument(
        '--port',
        type=int,
        default=None,
        help='Dashboard port (default: from .env)'
    )
    
    args = parser.parse_args()
    
    if args.mode == 'bot':
        print("=" * 50)
        print("Starting digi.Me Bot")
        print("=" * 50)
        
        try:
            bot = DigiMeBot()
            bot.start()
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
    
    elif args.mode == 'dashboard':
        print("=" * 50)
        print("Starting digi.Me Dashboard")
        print("=" * 50)
        
        try:
            run_dashboard(host=args.host, port=args.port)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
    
    elif args.mode == 'both':
        print("=" * 50)
        print("Starting digi.Me - Both Bot and Dashboard")
        print("=" * 50)
        print("\nNote: It's recommended to run bot and dashboard in separate terminals.")
        print("The dashboard will start first, then the bot.")
        print("\nPress Ctrl+C to stop both services.\n")
        
        import threading
        
        def run_bot():
            try:
                bot = DigiMeBot()
                bot.start()
            except Exception as e:
                print(f"Bot error: {e}")
        
        # Start dashboard in a separate thread
        dashboard_thread = threading.Thread(target=lambda: run_dashboard(host=args.host, port=args.port))
        dashboard_thread.daemon = True
        dashboard_thread.start()
        
        # Give dashboard time to start
        import time
        time.sleep(3)
        
        # Run bot in main thread
        run_bot()


if __name__ == '__main__':
    main()
