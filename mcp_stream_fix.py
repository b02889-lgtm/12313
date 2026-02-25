# -*- coding: utf-8 -*-
"""
MCP 工具流式执行 rawChunkTracker 修复示例

问题描述：
在流式执行过程中，rawChunkTracker 被过早清理，导致在处理最后的数据或完成回调时发生异常。

主要问题：
1. 在流式传输尚未完成时就清理了 rawChunkTracker
2. 异步回调尝试访问已清理的 tracker 数据
3. 缺少适当的生命周期管理
"""

import time
import threading
from typing import Dict, List, Optional

# ==================== 有问题的实现 ====================

class BuggyMCPStreamHandler:
    """有 Bug 的 MCP 流式处理器 - 过早清理 rawChunkTracker"""
    
    def __init__(self):
        self.rawChunkTracker: Dict[str, List[str]] = {}
        self.lock = threading.Lock()

    def start_request(self, request_id: str):
        """开始处理请求"""
        print(f"[Buggy] START 开始请求 {request_id}")
        with self.lock:
            self.rawChunkTracker[request_id] = []

    def process_chunk(self, request_id: str, chunk: str):
        """处理数据块"""
        with self.lock:
            if request_id in self.rawChunkTracker:
                self.rawChunkTracker[request_id].append(chunk)
                print(f"[Buggy] CHUNK 处理数据块 {request_id}: {chunk}")
            else:
                print(f"[Buggy] ERROR 错误：找不到 tracker for {request_id}")

    def finish_request(self, request_id: str):
        """完成请求 - 问题：过早清理 tracker"""
        print(f"[Buggy] FINISH 完成请求 {request_id}")
        with self.lock:
            # 过早清理 tracker！
            if request_id in self.rawChunkTracker:
                del self.rawChunkTracker[request_id]
                print(f"[Buggy] CLEANUP 清理 tracker {request_id}")

    def delayed_callback(self, request_id: str):
        """延迟回调 - 尝试访问已清理的 tracker"""
        time.sleep(0.1)  # 模拟异步延迟
        with self.lock:
            if request_id in self.rawChunkTracker:
                chunks = self.rawChunkTracker[request_id]
                print(f"[Buggy] SUCCESS 回调成功：{len(chunks)} 个数据块")
                return chunks
            else:
                print(f"[Buggy] FAILED 回调失败：tracker 已被清理！")
                raise KeyError(f"rawChunkTracker for {request_id} was prematurely cleared")


# ==================== 修复后的实现 ====================

class FixedMCPStreamHandler:
    """修复后的 MCP 流式处理器 - 正确管理 rawChunkTracker 生命周期"""
    
    def __init__(self):
        self.rawChunkTracker: Dict[str, Dict] = {}
        self.lock = threading.Lock()

    def start_request(self, request_id: str):
        """开始处理请求"""
        print(f"[Fixed] START 开始请求 {request_id}")
        with self.lock:
            self.rawChunkTracker[request_id] = {
                'chunks': [],
                'completed': False,
                'pending_callbacks': 0  # 跟踪待处理的回调
            }

    def process_chunk(self, request_id: str, chunk: str):
        """处理数据块"""
        with self.lock:
            if request_id in self.rawChunkTracker:
                self.rawChunkTracker[request_id]['chunks'].append(chunk)
                print(f"[Fixed] CHUNK 处理数据块 {request_id}: {chunk}")
            else:
                print(f"[Fixed] WARNING 警告：找不到 tracker for {request_id}")

    def register_callback(self, request_id: str):
        """注册一个待处理的回调"""
        with self.lock:
            if request_id in self.rawChunkTracker:
                self.rawChunkTracker[request_id]['pending_callbacks'] += 1
                print(f"[Fixed] REGISTER 注册回调 {request_id} (待处理: {self.rawChunkTracker[request_id]['pending_callbacks']})")

    def finish_request(self, request_id: str):
        """完成请求 - 标记为完成但不立即清理"""
        print(f"[Fixed] FINISH 完成请求 {request_id}")
        with self.lock:
            if request_id in self.rawChunkTracker:
                self.rawChunkTracker[request_id]['completed'] = True
                print(f"[Fixed] MARK 标记为已完成 {request_id}")
                # 尝试清理（如果没有待处理的回调）
                self._try_cleanup(request_id)

    def _try_cleanup(self, request_id: str):
        """尝试清理 tracker - 仅在安全时清理"""
        if request_id in self.rawChunkTracker:
            tracker = self.rawChunkTracker[request_id]
            if tracker['completed'] and tracker['pending_callbacks'] == 0:
                del self.rawChunkTracker[request_id]
                print(f"[Fixed] CLEANUP 安全清理 tracker {request_id}")
            else:
                print(f"[Fixed] DELAY 延迟清理 {request_id} (待处理回调: {tracker['pending_callbacks']})")

    def delayed_callback(self, request_id: str):
        """延迟回调 - 正确处理回调完成"""
        time.sleep(0.1)  # 模拟异步延迟
        with self.lock:
            if request_id in self.rawChunkTracker:
                chunks = self.rawChunkTracker[request_id]['chunks']
                print(f"[Fixed] SUCCESS 回调成功：{len(chunks)} 个数据块")
                
                # 减少待处理回调计数
                self.rawChunkTracker[request_id]['pending_callbacks'] -= 1
                print(f"[Fixed] COMPLETE 回调完成 {request_id} (剩余: {self.rawChunkTracker[request_id]['pending_callbacks']})")
                
                # 尝试清理
                self._try_cleanup(request_id)
                return chunks
            else:
                print(f"[Fixed] FAILED 回调失败：tracker 不存在")
                raise KeyError(f"rawChunkTracker for {request_id} not found")


# ==================== 测试代码 ====================

def test_buggy_handler():
    """测试有 Bug 的处理器"""
    print("\n" + "="*60)
    print("测试有 Bug 的实现 (过早清理)")
    print("="*60 + "\n")
    
    handler = BuggyMCPStreamHandler()
    request_id = "req-buggy-001"
    
    # 1. 开始请求
    handler.start_request(request_id)
    
    # 2. 处理数据块
    handler.process_chunk(request_id, "chunk-1")
    handler.process_chunk(request_id, "chunk-2")
    handler.process_chunk(request_id, "chunk-3")
    
    # 3. 完成请求（过早清理 tracker）
    handler.finish_request(request_id)
    
    # 4. 在新线程中执行延迟回调
    print("\n[Buggy] LAUNCH 启动延迟回调线程...")
    callback_thread = threading.Thread(target=lambda: handler.delayed_callback(request_id))
    callback_thread.start()
    callback_thread.join()
    
    print("\n[Buggy] WARNING 结果：回调失败，因为 tracker 被过早清理\n")


def test_fixed_handler():
    """测试修复后的处理器"""
    print("\n" + "="*60)
    print("测试修复后的实现 (正确的生命周期管理)")
    print("="*60 + "\n")
    
    handler = FixedMCPStreamHandler()
    request_id = "req-fixed-001"
    
    # 1. 开始请求
    handler.start_request(request_id)
    
    # 2. 注册回调
    handler.register_callback(request_id)
    
    # 3. 处理数据块
    handler.process_chunk(request_id, "chunk-1")
    handler.process_chunk(request_id, "chunk-2")
    handler.process_chunk(request_id, "chunk-3")
    
    # 4. 完成请求（不会清理因为有待处理的回调）
    handler.finish_request(request_id)
    
    # 5. 在新线程中执行延迟回调
    print("\n[Fixed] LAUNCH 启动延迟回调线程...")
    callback_thread = threading.Thread(target=lambda: handler.delayed_callback(request_id))
    callback_thread.start()
    callback_thread.join()
    
    print("\n[Fixed] SUCCESS 结果：回调成功，tracker 在安全时刻被清理\n")


def test_multiple_callbacks():
    """测试多个回调的场景"""
    print("\n" + "="*60)
    print("测试多个并发回调场景")
    print("="*60 + "\n")
    
    handler = FixedMCPStreamHandler()
    request_id = "req-fixed-002"
    
    # 1. 开始请求
    handler.start_request(request_id)
    
    # 2. 注册多个回调
    handler.register_callback(request_id)
    handler.register_callback(request_id)
    handler.register_callback(request_id)
    
    # 3. 处理数据块
    handler.process_chunk(request_id, "chunk-1")
    handler.process_chunk(request_id, "chunk-2")
    
    # 4. 完成请求
    handler.finish_request(request_id)
    
    # 5. 启动多个回调线程
    print("\n[Fixed] LAUNCH 启动 3 个并发回调线程...")
    threads = []
    for i in range(3):
        thread = threading.Thread(
            target=lambda idx=i: (
                time.sleep(idx * 0.05),  # 错开执行时间
                handler.delayed_callback(request_id)
            )
        )
        threads.append(thread)
        thread.start()
    
    # 等待所有回调完成
    for thread in threads:
        thread.join()
    
    print("\n[Fixed] SUCCESS 结果：所有回调成功完成，tracker 最终被清理\n")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("MCP 工具流式执行 rawChunkTracker 修复演示".center(60))
    print("=" * 60)
    
    # 测试有 Bug 的实现
    test_buggy_handler()
    
    # 测试修复后的实现
    test_fixed_handler()
    
    # 测试多个回调场景
    test_multiple_callbacks()
    
    print("\n" + "="*60)
    print("总结")
    print("="*60)
    print("""
修复方案关键点：

1. [OK] 使用状态标记而非立即删除
   - 添加 'completed' 标志标记请求完成
   - 添加 'pending_callbacks' 计数跟踪待处理回调

2. [OK] 延迟清理机制
   - 仅在请求完成且无待处理回调时清理
   - 使用 _try_cleanup() 方法安全检查

3. [OK] 回调注册机制
   - 在启动回调前注册，增加计数
   - 回调完成后减少计数并尝试清理

4. [OK] 线程安全
   - 所有操作都在锁保护下进行
   - 避免竞态条件

这样可以确保即使在高并发、异步回调的场景下，
rawChunkTracker 也不会被过早清理，避免访问异常。
""")
    print("=" * 60 + "\n")