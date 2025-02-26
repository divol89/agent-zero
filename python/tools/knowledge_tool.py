# import os
# import asyncio
# from python.helpers import memory, duckduckgo_search
# from python.helpers.tool import Tool, Response
# from python.helpers.print_style import PrintStyle
# from python.helpers.errors import handle_error
# from python.tools.tool_router import ToolRouter  # Importa ToolRouter


# class Knowledge(Tool):
#     async def execute(self, question="", **kwargs):
#         tool_router = ToolRouter(self.agent)

#         # First, try to use the webpage_content_tool
#         if tool_router.tools.get("webpage_content_tool"):
#             try:
#                 search_url = (
#                     f"https://www.google.com/search?q={question.replace(' ', '+')}"
#                 )
#                 response = await tool_router.execute(task="navigate", url=search_url)

#                 # Extract the search results
#                 search_results = await self.extract_search_results(response.message)

#                 # If we have search results, navigate to the first one
#                 if search_results:
#                     first_result_url = search_results[0]["url"]
#                     content_response = await tool_router.execute(
#                         task="navigate", url=first_result_url
#                     )
#                     return content_response
#                 else:
#                     # If no search results, fall back to DuckDuckGo and memory search
#                     return await self.fallback_search(question)
#             except Exception as e:
#                 print(f"Error using webpage_content_tool: {str(e)}")
#                 # If an error occurs, fall back to DuckDuckGo and memory search
#                 return await self.fallback_search(question)
#         else:
#             # If webpage_content_tool is not available, fall back to DuckDuckGo and memory search
#             return await self.fallback_search(question)

#     async def fallback_search(self, question):
#         # Create tasks for DuckDuckGo and memory search
#         tasks = [self.duckduckgo_search(question), self.mem_search(question)]

#         # Run all tasks concurrently
#         results = await asyncio.gather(*tasks, return_exceptions=True)

#         duckduckgo_result, memory_result = results

#         # Format the results
#         duckduckgo_result = self.format_result(duckduckgo_result, "DuckDuckGo")
#         memory_result = self.format_result(memory_result, "Memory")

#         # Combine the results
#         combined_result = f"DuckDuckGo Search:\n{duckduckgo_result}\n\nMemory Search:\n{memory_result}"

#         msg = self.agent.read_prompt(
#             "tool.knowledge.response.md",
#             online_sources=combined_result,
#             memory=memory_result,
#         )
#         return Response(message=msg, break_loop=False)

#     async def extract_search_results(self, page_content):
#         # Implement a method to extract search results from the Google search page
#         # This is a simplified example and may need to be adjusted based on the actual page structure
#         results = []
#         lines = page_content.split("\n")
#         for i, line in enumerate(lines):
#             if line.startswith("http") and i + 1 < len(lines):
#                 results.append({"url": line, "title": lines[i + 1]})
#         return results

#     async def duckduckgo_search(self, question):
#         return await asyncio.to_thread(duckduckgo_search.search, question)

#     async def mem_search(self, question: str):
#         db = await memory.Memory.get(self.agent)
#         docs = await db.search_similarity_threshold(
#             query=question, limit=5, threshold=0.5
#         )
#         text = memory.Memory.format_docs_plain(docs)
#         return "\n\n".join(text)

#     def format_result(self, result, source):
#         if isinstance(result, Exception):
#             handle_error(result)
#             return f"{source} search failed: {str(result)}"
#         return result if result else ""

#     async def initiate_browser_navigation(self, search_results):
#         # Extract the first URL from the search results
#         urls = [line for line in search_results.split("\n") if line.startswith("http")]
#         if urls:
#             url = urls[0]  # Assume we take the first URL for simplicity
#             tool_response = await self.agent.tools["webpage_content_tool"].execute(
#                 url=url
#             )
#             return tool_response.message
#         return "No valid URLs found in search results."


import os
import asyncio
from python.helpers import memory, perplexity_search, duckduckgo_search
from python.helpers.tool import Tool, Response
from python.helpers.print_style import PrintStyle
from python.helpers.errors import handle_error


class Knowledge(Tool):
    async def execute(self, question="", **kwargs):
        # Create tasks for all three search methods
        tasks = [
            self.perplexity_search(question),
            self.duckduckgo_search(question),
            self.mem_search(question),
        ]

        # Run all tasks concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)

        perplexity_result, duckduckgo_result, memory_result = results

        # Handle exceptions and format results
        perplexity_result = self.format_result(perplexity_result, "Perplexity")
        duckduckgo_result = self.format_result(duckduckgo_result, "DuckDuckGo")
        memory_result = self.format_result(memory_result, "Memory")

        msg = self.agent.read_prompt(
            "tool.knowledge.response.md",
            online_sources=((perplexity_result + "\n\n") if perplexity_result else "")
            + str(duckduckgo_result),
            memory=memory_result,
        )

        await self.agent.handle_intervention(
            msg
        )  # wait for intervention and handle it, if paused

        return Response(message=msg, break_loop=False)

    async def perplexity_search(self, question):
        if os.getenv("API_KEY_PERPLEXITY"):
            return await asyncio.to_thread(
                perplexity_search.perplexity_search, question
            )
        else:
            PrintStyle.hint(
                "No API key provided for Perplexity. Skipping Perplexity search."
            )
            self.agent.context.log.log(
                type="hint",
                content="No API key provided for Perplexity. Skipping Perplexity search.",
            )
            return None

    async def duckduckgo_search(self, question):
        return await asyncio.to_thread(duckduckgo_search.search, question)

    async def mem_search(self, question: str):
        db = await memory.Memory.get(self.agent)
        docs = await db.search_similarity_threshold(
            query=question, limit=5, threshold=0.5
        )
        text = memory.Memory.format_docs_plain(docs)
        return "\n\n".join(text)

    def format_result(self, result, source):
        if isinstance(result, Exception):
            handle_error(result)
            return f"{source} search failed: {str(result)}"
        return result if result else ""
