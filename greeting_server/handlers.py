from typing import List

from loguru import logger
from mcp.server.fastmcp import FastMCP


def register_handers(mcp: FastMCP) -> None:
    @mcp.resource("hello://world")
    def get_hello_message() -> str:
        return "Hello world! This is my first MCP resource."
    
    @mcp.resource("file://{file_name}")
    def read_file(file_name: str) -> str:
        logger.info(f"Attempting to read file: {file_name}")
        try:
            with open(f"/Users/btp712/Code/experiments/mcp-learning/filesystem/{file_name}", 'r') as file:
                res = file.read().strip()
            return res
        except FileNotFoundError:
            return f"File {file_name} not found."
        except Exception as e:
            return f"An error occurred: {e}"
        