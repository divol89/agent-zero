from playwright.async_api import (
    async_playwright,
    TimeoutError as PlaywrightTimeoutError,
)
from python.helpers.tool import Tool, Response
from python.helpers.errors import handle_error
import time


class WebpageContentTool(Tool):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.browser = None
        self.current_page = None
        self.playwright = None
        self.context = None

    async def initialize(self, debug_port: int = 9222):
        try:
            if not self.playwright:
                self.playwright = await async_playwright().start()
            if not self.browser:
                self.browser = await self.playwright.chromium.connect_over_cdp(
                    f"http://localhost:{debug_port}", timeout=30000
                )
            if not self.context:
                self.context = await self.browser.new_context(
                    viewport={"width": 1280, "height": 720},
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                )
                await self.context.route(
                    "**/*.{png,jpg,jpeg,gif,svg}", lambda route: route.abort()
                )
            if not self.current_page or not await self.is_page_valid():
                self.current_page = await self.context.new_page()
        except Exception as e:
            handle_error(e)
            raise

    async def is_browser_connected(self) -> bool:
        if not self.browser:
            return False
        try:
            contexts = self.browser.contexts  # Changed this line
            return len(contexts) > 0
        except Exception:
            return False

    async def is_page_valid(self) -> bool:
        if not self.current_page:
            return False
        try:
            await self.current_page.evaluate("document.body")
            return True
        except Exception:
            return False

    async def execute(
        self,
        action="",
        url="",
        selector="",
        value="",
        search_query="",
        result_index=None,
        **kwargs,
    ):
        try:
            await self.initialize()

            actions = {
                "navigate": self.navigate_to,
                "search": self.perform_search,
                "search_within_page": self.search_within_page,
                "click": self.click,
                "type": self.type,
                "get_text": self.get_text,
                "scroll": self.scroll,
                "screenshot": self.screenshot,
                "select": self.select,
                "hover": self.hover,
                "type_and_search": self.type_and_search,
                "accept_cookies": self.accept_terms,
                "go_back": self.go_back,
                "go_forward": self.go_forward,
                "refresh_page": self.refresh_page,
                "close": self.close,
                "navigate_to_search_result": self.navigate_to_search_result,
            }

            if action in actions:
                if action == "navigate":
                    result = await actions[action](url, **kwargs)
                elif action in ["search", "search_within_page"]:
                    result = await actions[action](search_query, **kwargs)
                elif action == "navigate_to_search_result":
                    result = await actions[action](result_index, **kwargs)
                elif action in ["click", "get_text", "scroll", "hover"]:
                    result = await actions[action](selector, **kwargs)
                elif action in ["type", "select", "type_and_search"]:
                    result = await actions[action](selector, value, **kwargs)
                elif action == "screenshot":
                    result = await actions[action](value, **kwargs)
                else:
                    result = await actions[action](**kwargs)
                return Response(message=result, break_loop=False)
            else:
                return Response(message=f"Unknown action: {action}", break_loop=False)

        except Exception as e:
            handle_error(e)
            return Response(message=f"An error occurred: {str(e)}", break_loop=False)

    async def navigate_to(self, url):
        if self.current_page:
            await self.current_page.goto(
                url, wait_until="domcontentloaded", timeout=10000
            )
            return f"Successfully navigated to {url}"
        return "No active page to navigate"

    async def perform_search(self, search_query):
        if not self.current_page:
            return "No active page to perform search"

        search_selectors = [
            'input[type="search"]',
            'input[name="q"]',
            'input[name="search"]',
            'input[aria-label="Search"]',
            'input[placeholder="Search"]',
            'textarea[name="q"]',
            'textarea[aria-label="Search"]',
        ]

        for selector in search_selectors:
            try:
                await self.current_page.wait_for_selector(selector, timeout=1000)
                await self.current_page.fill(selector, search_query)
                await self.current_page.press(selector, "Enter")
                await self.current_page.wait_for_load_state("networkidle", timeout=1000)
                return f"Searched for '{search_query}' using selector '{selector}'"
            except PlaywrightTimeoutError:
                continue

        return f"Could not find search input for '{search_query}'. Current URL: {self.current_page.url}"

    async def search_within_page(self, search_query):
        if not self.current_page:
            return "No active page to search within"
        try:
            result = await self.current_page.evaluate(f"""
                window.find('{search_query}');
                document.getSelection().toString();
            """)
            return (
                "Found text: {result}"
                if result
                else f"Text '{search_query}' not found on the page"
            )
        except Exception as e:
            return f"Error searching within page: {str(e)}"

    async def click(self, selector):
        if not self.current_page:
            return "No active page to perform click"

        try:
            await self.current_page.wait_for_selector(
                selector, state="visible", timeout=5000
            )
            await self.current_page.click(selector, timeout=1000)
            await self.current_page.wait_for_load_state("networkidle", timeout=5000)
            return f"Successfully clicked element with selector '{selector}'"
        except Exception as e:
            return f"Error clicking element: {str(e)}"

    async def type(self, selector, value):
        if not self.current_page:
            return "No active page to perform type"
        await self.wait_for_selector(selector)
        await self.current_page.fill(selector, value)
        return f"Typed '{value}' into element with selector '{selector}'"

    async def get_text(self, selector):
        if not self.current_page:
            return "No active page to get text"
        await self.wait_for_selector(selector)
        text = await self.current_page.inner_text(selector)
        return f"Text content of element with selector '{selector}': {text}"

    async def scroll(self, selector):
        if not self.current_page:
            return "No active page to perform scroll"
        await self.wait_for_selector(selector)
        await self.current_page.evaluate(
            f'document.querySelector("{selector}").scrollIntoView()'
        )
        return f"Scrolled to element with selector '{selector}'"

    async def screenshot(self, path):
        if not self.current_page:
            return "No active page to take screenshot"
        await self.current_page.screenshot(path=path or "screenshot.png")
        return f"Screenshot saved to {path or 'screenshot.png'}"

    async def select(self, selector, value):
        if not self.current_page:
            return "No active page to perform select"
        await self.wait_for_selector(selector)
        await self.current_page.select_option(selector, value)
        return f"Selected option '{value}' in element with selector '{selector}'"

    async def hover(self, selector):
        if not self.current_page:
            return "No active page to perform hover"
        await self.wait_for_selector(selector)
        await self.current_page.hover(selector)
        return f"Hovered over element with selector '{selector}'"

    async def type_and_search(self, selector, value):
        if not self.current_page:
            return "No active page to perform type and search"
        await self.wait_for_selector(selector)
        await self.current_page.fill(selector, value)
        await self.current_page.press(selector, "Enter")
        await self.current_page.wait_for_load_state("networkidle")
        return (
            f"Typed '{value}' into element with selector '{selector}' and pressed Enter"
        )

    async def wait_for_selector(self, selector):
        if not self.current_page:
            raise Exception("No active page to wait for selector")
        try:
            await self.current_page.wait_for_selector(selector, timeout=15000)
        except PlaywrightTimeoutError:
            raise Exception(f"Timeout while waiting for selector: {selector}")

    async def accept_terms(self):
        if not self.current_page:
            return "No active page to accept terms"

        # Ampliar la lista de selectores para incluir más variaciones y idiomas
        selectors = [
            "button:has-text('Accept All')",
            "button:has-text('I agree')",
            "button:has-text('Accept')",
            "button:has-text('Agree')",
            "button:has-text('OK')",
            "button:has-text('Aceptar todo')",
            "button:has-text('Acepto')",
            "button:has-text('Estoy de acuerdo')",
            "button:has-text('Aceptar')",
            "button:has-text('Accepter tout')",
            "button:has-text('J'accepte')",
            "button:has-text('Tout accepter')",
            "button:has-text('Akzeptieren')",
            "button:has-text('Ich stimme zu')",
            "button:has-text('Alle akzeptieren')",
            "[aria-label='Accept cookies']",
            "[aria-label='Aceptar cookies']",
            "[aria-label='Accepter les cookies']",
            "[aria-label='Cookies akzeptieren']",
            "#accept-cookies",
            "#acceptCookies",
            "#cookie-accept",
            ".cookie-accept",
            ".accept-cookies",
        ]

        for selector in selectors:
            try:
                # Intentar encontrar el elemento
                element = await self.current_page.query_selector(selector)
                if element:
                    # Si el elemento está visible e interactuable
                    if await element.is_visible() and await element.is_enabled():
                        await element.click(timeout=1000)
                        await self.current_page.wait_for_load_state("domcontentloaded")
                        return f"Accepted terms successfully using selector: {selector}"
            except Exception as e:
                print(f"Error trying selector {selector}: {str(e)}")
                continue

        # Si no se encontró ningún botón, intentar cerrar diálogos o banners de cookies
        close_selectors = [
            "button:has-text('Close')",
            "button:has-text('Cerrar')",
            "button:has-text('Fermer')",
            "button:has-text('Schließen')",
            "[aria-label='Close']",
            "[aria-label='Cerrar']",
            "[aria-label='Fermer']",
            "[aria-label='Schließen']",
            ".close-button",
            "#close-button",
            ".cookie-banner__close",
        ]

        for selector in close_selectors:
            try:
                element = await self.current_page.query_selector(selector)
                if element and await element.is_visible():
                    await element.click(timeout=1000)
                    await self.current_page.wait_for_load_state("domcontentloaded")
                    return f"Closed cookie dialog using selector: {selector}"
            except Exception as e:
                print(f"Error trying close selector {selector}: {str(e)}")
                continue

        return "No accept button or close button found for cookie dialog"

    async def go_back(self):
        if not self.current_page:
            return "No active page to go back"
        await self.current_page.go_back()
        await self.current_page.wait_for_load_state("domcontentloaded")
        return "Navigated back"

    async def go_forward(self):
        if not self.current_page:
            return "No active page to go forward"
        await self.current_page.go_forward()
        await self.current_page.wait_for_load_state("domcontentloaded")
        return "Navigated forward"

    async def refresh_page(self):
        if not self.current_page:
            return "No active page to refresh"
        await self.current_page.reload()
        await self.current_page.wait_for_load_state("domcontentloaded")
        return "Page refreshed"

    async def close(self):
        if self.current_page:
            await self.current_page.close()
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        self.current_page = None
        self.context = None
        self.browser = None
        self.playwright = None
        return "Browser closed successfully"

    async def navigate_to_search_result(self, result_index):
        if not self.current_page:
            return "No active page to navigate"

        try:
            await self.current_page.wait_for_selector(".g", timeout=1000)
            result = await self.current_page.evaluate(f"""
                () => {{
                    const elements = document.querySelectorAll('.g');
                    const element = elements[{result_index - 1}];
                    if (element) {{
                        const link = element.querySelector('a');
                        if (link) {{
                            return link.href;
                        }}
                    }}
                    return null;
                }}
            """)

            if result:
                await self.navigate_to(result)
                return f"Successfully navigated to search result #{result_index}"
            else:
                return f"Could not find search result #{result_index}"
        except Exception as e:
            return f"Error navigating to search result: {str(e)}"
