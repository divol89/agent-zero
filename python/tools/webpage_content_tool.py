# import requests
# from bs4 import BeautifulSoup
# from urllib.parse import urlparse
# from newspaper import Article
# from python.helpers.tool import Tool, Response
# from python.helpers.errors import handle_error


# class WebpageContentTool(Tool):
#     async def execute(self, url="", **kwargs):
#         if not url:
#             return Response(message="Error: No URL provided.", break_loop=False)

#         try:
#             # Validate URL
#             parsed_url = urlparse(url)
#             if not all([parsed_url.scheme, parsed_url.netloc]):
#                 return Response(message="Error: Invalid URL format.", break_loop=False)

#             # Fetch webpage content
#             response = requests.get(url, timeout=10)
#             response.raise_for_status()

#             # Use newspaper3k for article extraction
#             article = Article(url)
#             article.download()
#             article.parse()

#             # If it's not an article, fall back to BeautifulSoup
#             if not article.text:
#                 soup = BeautifulSoup(response.content, 'html.parser')
#                 text_content = ' '.join(soup.stripped_strings)
#             else:
#                 text_content = article.text

#             return Response(message=f"Webpage content:\n\n{text_content}", break_loop=False)

#         except requests.RequestException as e:
#             return Response(message=f"Error fetching webpage: {str(e)}", break_loop=False)
#         except Exception as e:
#             handle_error(e)
#             return Response(message=f"An error occurred: {str(e)}", break_loop=False)


# from urllib.parse import urlparse
# from python.helpers.tool import Tool, Response
# from python.helpers.errors import handle_error

# # import asyncio
# from playwright.async_api import async_playwright


# class WebpageContentTool(Tool):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.browser = None
#         self.page = None
#         self.playwright = None

#     async def execute(self, url="", **kwargs):
#         if not url:
#             return Response(message="Error: No URL provided.", break_loop=False)

#         try:
#             # Validate URL
#             parsed_url = urlparse(url)
#             if not all([parsed_url.scheme, parsed_url.netloc]):
#                 return Response(message="Error: Invalid URL format.", break_loop=False)

#             # Initialize Playwright if not already done
#             if not self.playwright:
#                 self.playwright = await async_playwright().start()

#             # Launch the browser if not already done
#             if not self.browser:
#                 self.browser = await self.playwright.chromium.launch(
#                     headless=False, args=["--remote-debugging-port=9222"]
#                 )

#             # Create a new page if not already done
#             if not self.page:
#                 self.page = await self.browser.new_page()

#             await self.navigate_to(url)

#             # Extract text content from the page
#             text_content = await self.page.evaluate("document.body.innerText")

#             return Response(
#                 message=f"Webpage content:\n\n{text_content}", break_loop=False
#             )

#         except Exception as e:
#             handle_error(e)
#             return Response(message=f"An error occurred: {str(e)}", break_loop=False)

#     async def navigate_to(self, url):
#         try:
#             if self.page:
#                 await self.page.goto(url)
#             else:
#                 raise Exception("Page is not initialized.")
#             if self.page:
#                 await self.page.wait_for_load_state("domcontentloaded")
#             else:
#                 raise Exception("Page is not initialized.")
#         except Exception as e:
#             handle_error(e)
#             raise e

#     async def click_element(self, selector):
#         try:
#             if self.page:
#                 await self.page.click(selector)
#             else:
#                 raise Exception("Page is not initialized.")
#             await self.page.wait_for_load_state("domcontentloaded")
#         except Exception as e:
#             handle_error(e)
#             raise e

#     # async def close_browser(self):
#     #     if self.browser:
#     #         await self.browser.close()

#     async def close(self):
#         if self.page:
#             await self.page.close()
#         if self.browser:
#             await self.browser.close()
#         if self.playwright:
#             await self.playwright.stop()

#     async def close_browser(self):
#         if self.page:
#             await self.page.close()
#         if self.browser:
#             await self.browser.close()
#         if self.playwright:
#             await self.playwright.stop()
#         self.page = None
#         self.browser = None
#         self.playwright = None


# # Example of running the tool with navigation and interaction
# async def main():
#     tool = WebpageContentTool(None, name="Webpage Content Fetcher", args={}, message="")

#     # Navigate to first website
#     response = await tool.execute(url="https://www.example.com")
#     print(response.message)

#     # Navigate to another website
#     await tool.navigate_to("https://www.wikipedia.org")

#     # Perform some interaction
#     await tool.click_element("strong a")  # Example selector

#     # When you're completely done, close the browser
#     await tool.close()


# # Run the example
# # asyncio.run(main())

from urllib.parse import urlparse
from python.helpers.tool import Tool, Response
from python.helpers.errors import handle_error
import asyncio
from playwright.async_api import async_playwright


class WebpageContentTool(Tool):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.browser = None
        self.page = None
        self.playwright = None

    async def execute(self, url="", action="", selector="", value="", **kwargs):
        if not url and not action:
            return Response(
                message="Error: No URL or action provided.", break_loop=False
            )

        try:
            if action == "close":
                await self.close()
                return Response(
                    message="Browser closed successfully.", break_loop=False
                )

            # Initialize Playwright if not already done
            if not self.playwright:
                self.playwright = await async_playwright().start()

            # Launch the browser if not already done
            if not self.browser:
                self.browser = await self.playwright.chromium.launch(
                    headless=False, args=["--remote-debugging-port=9222"]
                )

            # Create a new page if not already done
            if not self.page:
                self.page = await self.browser.new_page()

            if url:
                await self.navigate_to(url)

            if action:
                if action == "click":
                    await self.click_element(selector)
                elif action == "type":
                    await self.type_text(selector, value)
                elif action == "get_text":
                    return Response(
                        message=await self.get_element_text(selector), break_loop=False
                    )
                elif action == "scroll":
                    await self.scroll_to_element(selector)
                elif action == "screenshot":
                    await self.take_screenshot(value or "screenshot.png")
                elif action == "select":
                    await self.select_option(selector, value)
                elif action == "hover":
                    await self.hover_element(selector)
                return Response(
                    message=f"Action '{action}' completed successfully.",
                    break_loop=False,
                )

            # Extract text content from the page
            text_content = await self.page.evaluate("document.body.innerText")
            return Response(
                message=f"Webpage content:\n\n{text_content}", break_loop=False
            )

        except Exception as e:
            handle_error(e)
            return Response(message=f"An error occurred: {str(e)}", break_loop=False)

    async def navigate_to(self, url):
        try:
            if self.page:
                await self.page.goto(url)
                await self.page.wait_for_load_state("domcontentloaded")
            else:
                raise Exception("Page is not initialized.")
        except Exception as e:
            handle_error(e)
            raise e

    async def click_element(self, selector):
        try:
            if self.page:
                await self.page.click(selector)
                await self.page.wait_for_load_state("domcontentloaded")
            else:
                raise Exception("Page is not initialized.")
        except Exception as e:
            handle_error(e)
            raise e

    async def type_text(self, selector, text):
        try:
            if self.page:
                await self.page.fill(selector, text)
            else:
                raise Exception("Page is not initialized.")
        except Exception as e:
            handle_error(e)
            raise e

    async def get_element_text(self, selector):
        try:
            if self.page:
                element_text = await self.page.inner_text(selector)
                return element_text
            else:
                raise Exception("Page is not initialized.")
        except Exception as e:
            handle_error(e)
            raise e

    async def scroll_to_element(self, selector):
        try:
            if self.page:
                await self.page.scroll_into_view_if_needed(selector)
            else:
                raise Exception("Page is not initialized.")
        except Exception as e:
            handle_error(e)
            raise e

    async def take_screenshot(self, path="screenshot.png"):
        try:
            if self.page:
                await self.page.screenshot(path=path)
            else:
                raise Exception("Page is not initialized.")
        except Exception as e:
            handle_error(e)
            raise e

    async def select_option(self, selector, value):
        try:
            if self.page:
                await self.page.select_option(selector, value)
            else:
                raise Exception("Page is not initialized.")
        except Exception as e:
            handle_error(e)
            raise e

    async def hover_element(self, selector):
        try:
            if self.page:
                await self.page.hover(selector)
            else:
                raise Exception("Page is not initialized.")
        except Exception as e:
            handle_error(e)
            raise e

    async def close(self):
        if self.page:
            await self.page.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        self.page = None
        self.browser = None
        self.playwright = None


# Example of running the tool with navigation and interaction
async def main():
    tool = WebpageContentTool(None, name="Webpage Content Fetcher", args={}, message="")

    # Navigate to first website
    response = await tool.execute(url="https://www.example.com")
    print(response.message)

    # Navigate to another website
    response = await tool.execute(url="https://www.wikipedia.org")
    print(response.message)

    # Perform some interaction
    response = await tool.execute(action="click", selector="strong a")
    print(response.message)

    # Type text in a search box
    response = await tool.execute(
        action="type", selector="input[name='search']", value="Artificial Intelligence"
    )
    print(response.message)

    # Get text of an element
    response = await tool.execute(action="get_text", selector="h1")
    print(f"Text of the element: {response.message}")

    # Scroll to an element
    response = await tool.execute(action="scroll", selector="#content")
    print(response.message)

    # Take a screenshot
    response = await tool.execute(action="screenshot", value="wikipedia_screenshot.png")
    print(response.message)

    # Select an option from a dropdown
    response = await tool.execute(
        action="select", selector="select[name='language']", value="en"
    )
    print(response.message)

    # Hover over an element
    response = await tool.execute(action="hover", selector="a[title='English']")
    print(response.message)

    # When you're completely done, close the browser
    response = await tool.execute(action="close")
    print(response.message)


# Run the example
if __name__ == "__main__":
    import nest_asyncio

    nest_asyncio.apply()
    asyncio.get_event_loop().run_until_complete(main())
