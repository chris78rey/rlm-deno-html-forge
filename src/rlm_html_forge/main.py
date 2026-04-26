from __future__ import annotations
import argparse, asyncio
from dotenv import load_dotenv
from .config import AppConfig
from .orchestrator import HtmlRLMOrchestrator

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(); parser.add_argument('--config', default='config.yaml'); return parser.parse_args()

def main() -> None:
    load_dotenv(); args = parse_args(); config = AppConfig.from_yaml(args.config); asyncio.run(HtmlRLMOrchestrator(config).run())
if __name__ == '__main__': main()
