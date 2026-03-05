import asyncio
from playwright.async_api import async_playwright

async def capture_baidu():
    async with async_playwright() as p:
        # 启动浏览器
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # 访问百度
        print("正在打开百度...")
        await page.goto('https://www.baidu.com', wait_until='networkidle')
        
        # 等待页面加载完成
        await page.wait_for_selector('#su', timeout=10000)
        
        # 设置视口大小
        await page.set_viewport_size({'width': 1920, 'height': 1080})
        
        # 截图
        screenshot_path = 'baidu_screenshot.png'
        await page.screenshot(path=screenshot_path, full_page=True)
        print(f"截图已保存到: {screenshot_path}")
        
        # 关闭浏览器
        await browser.close()
        return screenshot_path

if __name__ == "__main__":
    result = asyncio.run(capture_baidu())
    print(f"完成！截图文件: {result}")
