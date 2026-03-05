import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto('https://www.baidu.com')
        await page.screenshot(path='baidu_screenshot.png')
        await browser.close()

asyncio.run(main())