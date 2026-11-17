
import asyncio
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

BASE_DIR = Path(__file__).resolve().parent


async def main():
    parametros = StdioServerParameters(
        command=sys.executable,
        args=["-m", "mcp_server.server"],
        cwd=str(BASE_DIR)
    )

    async with stdio_client(parametros) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            ferramentas = await session.list_tools()

            print("\nFERRAMENTAS MCP DISPONÍVEIS:")

            for ferramenta in ferramentas.tools:
                print(f"- {ferramenta.name}")

            print("\nTESTANDO list_topics...")

            resposta = await session.call_tool(
                "list_topics",
                arguments={}
            )

            for item in resposta.content:
                if item.type == "text":
                    print(item.text)

            print("\nTESTANDO search_knowledge...")

            resposta = await session.call_tool(
                "search_knowledge",
                arguments={
                    "query": "Como preservar evidências digitais?",
                    "top_k": 2
                }
            )

            for item in resposta.content:
                if item.type == "text":
                    print(item.text)


if __name__ == "__main__":
    asyncio.run(main())
