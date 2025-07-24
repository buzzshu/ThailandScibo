#!/bin/bash
mkdir -p templates
# 確保 setuptools 是最新版本
pip install --upgrade pip setuptools wheel
# 安裝其他依賴
pip install -r requirements.txt
