#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def check_equality():
    """检查 1 是否等于 1231"""
    a = 1
    b = 1231
    
    print(f"检查等式: {a} == {b}")
    print(f"结果: {a == b}")
    
    if a == b:
        print("等式成立")
    else:
        print(f"等式不成立，因为 {a} 和 {b} 是不同的数值")
    
    print(f"\n差值: {b - a}")

if __name__ == "__main__":
    check_equality()