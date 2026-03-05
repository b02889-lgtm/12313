import asyncio
from playwright.async_api import async_playwright

async def fetch_page_content(url: str):
    """获取指定URL的页面内容"""
    async with async_playwright() as p:
        # 启动浏览器
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        try:
            # 访问页面
            print(f"正在打开: {url}")
            await page.goto(url, wait_until='networkidle', timeout=30000)
            
            # 等待页面加载完成
            await page.wait_for_load_state('domcontentloaded')
            
            # 获取页面标题
            title = await page.title()
            print(f"页面标题: {title}")
            
            # 获取页面内容
            content = await page.content()
            
            # 获取页面文本内容（去除HTML标签）
            text_content = await page.evaluate('() => document.body.innerText') 
            
            # 关闭浏览器
            await browser.close()
            
            return {
                'url': url,
                'title': title,
                'html': content,
                'text': text_content
            }
            
        except Exception as e:
            await browser.close()
            raise e

if __name__ == "__main__":
    # 示例：获取百度首页内容
    url = "https://www.baidu.com"
    result = asyncio.run(fetch_page_content(url))
    
    print(f"\n=== 页面信息 ===")
    print(f"URL: {result['url']}")
    print(f"标题: {result['title']}")
    print(f"\n=== 页面文本内容（前500字符）===")
    print(result['text'][:500])
    print(f"\n=== HTML内容（前500字符）===")
    print(result['html'][:500])

