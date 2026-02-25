#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NPM 文档获取工具
用于获取 npm 包的最新文档信息
"""

import requests
import json
from typing import Dict, Any, Optional
from datetime import datetime


class NPMDocsTool:
    """NPM 文档工具类"""
    
    def __init__(self):
        self.registry_url = "https://registry.npmjs.org"
        self.npmjs_url = "https://www.npmjs.com"
    
    def get_package_info(self, package_name: str) -> Dict[str, Any]:
        """
        获取 npm 包的完整信息
        
        Args:
            package_name: npm 包名
            
        Returns:
            包含包信息的字典
        """
        url = f"{self.registry_url}/{package_name}"
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"获取包信息失败: {str(e)}"}
    
    def get_latest_version(self, package_name: str) -> Optional[str]:
        """
        获取包的最新版本
        
        Args:
            package_name: npm 包名
            
        Returns:
            最新版本号
        """
        info = self.get_package_info(package_name)
        if "error" in info:
            return None
        return info.get("dist-tags", {}).get("latest")
    
    def get_package_readme(self, package_name: str) -> Optional[str]:
        """
        获取包的 README 文档
        
        Args:
            package_name: npm 包名
            
        Returns:
            README 内容
        """
        info = self.get_package_info(package_name)
        if "error" in info:
            return None
        return info.get("readme")
    
    def get_package_metadata(self, package_name: str) -> Dict[str, Any]:
        """
        获取包的元数据摘要
        
        Args:
            package_name: npm 包名
            
        Returns:
            包含元数据的字典
        """
        info = self.get_package_info(package_name)
        
        if "error" in info:
            return info
        
        latest_version = info.get("dist-tags", {}).get("latest")
        versions = info.get("versions", {})
        latest_info = versions.get(latest_version, {})
        
        return {
            "name": info.get("name"),
            "version": latest_version,
            "description": latest_info.get("description", "无描述"),
            "author": latest_info.get("author", "未知"),
            "license": latest_info.get("license", "未知"),
            "homepage": latest_info.get("homepage", ""),
            "repository": latest_info.get("repository", {}).get("url", ""),
            "keywords": latest_info.get("keywords", []),
            "maintainers": [
                {
                    "name": m.get("name", ""),
                    "email": m.get("email", "")
                }
                for m in info.get("maintainers", [])
            ],
            "time": info.get("time", {}),
            "links": {
                "npm": f"{self.npmjs_url}/package/{package_name}",
                "registry": f"{self.registry_url}/{package_name}",
                "homepage": latest_info.get("homepage", ""),
                "repository": latest_info.get("repository", {}).get("url", "")
            }
        }
    
    def search_packages(self, query: str, limit: int = 10) -> Dict[str, Any]:
        """
        搜索 npm 包
        
        Args:
            query: 搜索关键词
            limit: 返回结果数量
            
        Returns:
            搜索结果
        """
        url = f"{self.registry_url}/-/v1/search"
        params = {
            "text": query,
            "size": limit
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            results = []
            for item in data.get("objects", []):
                package = item.get("package", {})
                results.append({
                    "name": package.get("name"),
                    "version": package.get("version"),
                    "description": package.get("description", ""),
                    "keywords": package.get("keywords", []),
                    "author": package.get("author", {}).get("name", "未知"),
                    "date": item.get("score", {}).get("detail", {}).get("created", "")
                })
            
            return {
                "total": data.get("total", 0),
                "results": results
            }
        except requests.exceptions.RequestException as e:
            return {"error": f"搜索失败: {str(e)}"}
    
    def get_dependencies(self, package_name: str, version: Optional[str] = None) -> Dict[str, Any]:
        """
        获取包的依赖关系
        
        Args:
            package_name: npm 包名
            version: 版本号（可选，默认最新版本）
            
        Returns:
            依赖信息
        """
        info = self.get_package_info(package_name)
        
        if "error" in info:
            return info
        
        if version is None:
            version = info.get("dist-tags", {}).get("latest")
        
        versions = info.get("versions", {})
        version_info = versions.get(version, {})
        
        return {
            "package": package_name,
            "version": version,
            "dependencies": version_info.get("dependencies", {}),
            "devDependencies": version_info.get("devDependencies", {}),
            "peerDependencies": version_info.get("peerDependencies", {}),
            "optionalDependencies": version_info.get("optionalDependencies", {})
        }
    
    def format_package_info(self, package_name: str) -> str:
        """
        格式化输出包信息
        
        Args:
            package_name: npm 包名
            
        Returns:
            格式化的字符串
        """
        metadata = self.get_package_metadata(package_name)
        
        if "error" in metadata:
            return f"❌ {metadata['error']}"
        
        output = []
        output.append("=" * 60)
        output.append(f"📦 包名: {metadata['name']}")
        output.append(f"🏷️  版本: {metadata['version']}")
        output.append(f"📝 描述: {metadata['description']}")
        output.append(f"👤 作者: {metadata['author']}")
        output.append(f"📄 许可证: {metadata['license']}")
        
        if metadata['keywords']:
            output.append(f"🔑 关键词: {', '.join(metadata['keywords'])}")
        
        if metadata['maintainers']:
            output.append("\n👥 维护者:")
            for m in metadata['maintainers']:
                output.append(f"  - {m['name']} ({m['email']})")
        
        output.append("\n🔗 链接:")
        output.append(f"  - NPM: {metadata['links']['npm']}")
        if metadata['links']['homepage']:
            output.append(f"  - 主页: {metadata['links']['homepage']}")
        if metadata['links']['repository']:
            output.append(f"  - 仓库: {metadata['links']['repository']}")
        
        time_info = metadata.get('time', {})
        if 'modified' in time_info:
            modified_time = datetime.fromisoformat(time_info['modified'].replace('Z', '+00:00'))
            output.append(f"\n📅 最后更新: {modified_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        output.append("=" * 60)
        
        return "\n".join(output)


def main():
    """主函数 - 命令行接口"""
    import sys
    import io
    
    # 设置 UTF-8 编码输出（Windows 兼容）
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  npm_docs_tool.py <package_name>              # 获取包信息")
        print("  npm_docs_tool.py <package_name> readme       # 获取 README")
        print("  npm_docs_tool.py <package_name> deps         # 获取依赖")
        print("  npm_docs_tool.py search <query>              # 搜索包")
        sys.exit(1)
    
    tool = NPMDocsTool()
    command = sys.argv[1]
    
    if command == "search" and len(sys.argv) >= 3:
        query = sys.argv[2]
        results = tool.search_packages(query)
        
        if "error" in results:
            print(f"❌ {results['error']}")
        else:
            print(f"找到 {results['total']} 个结果:\n")
            for i, pkg in enumerate(results['results'], 1):
                print(f"{i}. {pkg['name']} (v{pkg['version']})")
                print(f"   {pkg['description']}")
                print()
    
    else:
        package_name = command
        action = sys.argv[2] if len(sys.argv) > 2 else "info"
        
        if action == "readme":
            readme = tool.get_package_readme(package_name)
            if readme:
                print(readme)
            else:
                print("❌ 未找到 README")
        
        elif action == "deps":
            deps = tool.get_dependencies(package_name)
            if "error" in deps:
                print(f"❌ {deps['error']}")
            else:
                print(f"📦 {deps['package']} v{deps['version']} 的依赖:\n")
                
                if deps['dependencies']:
                    print("生产依赖:")
                    for name, version in deps['dependencies'].items():
                        print(f"  - {name}: {version}")
                    print()
                
                if deps['devDependencies']:
                    print("开发依赖:")
                    for name, version in deps['devDependencies'].items():
                        print(f"  - {name}: {version}")
                    print()
                
                if deps['peerDependencies']:
                    print("对等依赖:")
                    for name, version in deps['peerDependencies'].items():
                        print(f"  - {name}: {version}")
        
        else:  # info
            print(tool.format_package_info(package_name))


if __name__ == "__main__":
    main()
