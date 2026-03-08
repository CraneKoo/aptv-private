#!/usr/bin/env python3
"""
GitHub私有仓库自动更新方案
功能：自动从GitHub获取最新的koreatv.json，转换为M3U格式，并通过GitHub Actions实现自动更新
"""

import json
import urllib.request
import os
import time

# GitHub JSON URL
GITHUB_JSON_URL = "https://raw.githubusercontent.com/kenpark76/kenpark76.github.io/main/koreatv.json"
# M3U output file
M3U_FILE = "koreatv_private.m3u"
# Version file
VERSION_FILE = "version.json"


def generate_m3u():
    """生成M3U文件"""
    print("正在从GitHub获取最新的koreatv.json...")
    try:
        # Download JSON from GitHub
        with urllib.request.urlopen(GITHUB_JSON_URL) as response:
            data = json.loads(response.read().decode('utf-8'))
        
        # Create M3U content
        m3u_content = '#EXTM3U\n'
        
        for channel in data:
            name = channel.get('name', '')
            url = channel.get('uris', [''])[0]
            logo = channel.get('logo', '')
            group = channel.get('group', '')
            
            # Add EXTINF line
            extinf = f'#EXTINF:-1 group-title="{group}" tvg-logo="{logo}" tvg-name="{name}"'
            m3u_content += extinf + '\n'
            # Add URL line
            m3u_content += url + '\n'
        
        # Write M3U file
        with open(M3U_FILE, 'w', encoding='utf-8') as f:
            f.write(m3u_content)
        
        # Update version file
        version_info = {
            "last_updated": time.strftime("%Y-%m-%d %H:%M:%S"),
            "channel_count": len(data),
            "version": int(time.time())
        }
        
        with open(VERSION_FILE, 'w', encoding='utf-8') as f:
            json.dump(version_info, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ M3U文件已生成: {os.path.abspath(M3U_FILE)}")
        print(f"\n🎯 共包含 {len(data)} 个频道")
        print(f"\n📅 最后更新时间: {version_info['last_updated']}")
        
        return True
    except Exception as e:
        print(f"❌ 生成M3U时出错: {e}")
        return False


def create_github_actions_config():
    """创建GitHub Actions配置文件"""
    actions_config = '''name: Update APTV Playlist

on:
  schedule:
    - cron: '*/30 * * * *'  # 每30分钟运行一次
  workflow_dispatch:  # 手动触发

jobs:
  update-playlist:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
    
    - name: Update playlist
      run: python github_private_autoupdate.py
    
    - name: Commit changes
      run: |
        git config --global user.name "GitHub Actions"
        git config --global user.email "actions@github.com"
        git add koreatv_private.m3u version.json
        git commit -m "Auto update playlist $(date '+%Y-%m-%d %H:%M:%S')"
        git push
'''
    
    # Create .github/workflows directory if it doesn't exist
    os.makedirs('.github/workflows', exist_ok=True)
    
    # Write the actions config file
    with open('.github/workflows/update.yml', 'w') as f:
        f.write(actions_config)
    
    print("\n✅ GitHub Actions配置文件已创建: .github/workflows/update.yml")
    print("📅 配置为每30分钟自动更新一次")


def show_complete_guide():
    """显示完整的GitHub私有仓库部署指南"""
    print("\n📚 GitHub私有仓库自动更新完整指南:")
    print("=" * 80)
    print("\n步骤1: 创建私有GitHub仓库")
    print("1. 登录GitHub: https://github.com")
    print("2. 创建一个新的私有仓库，例如: 'aptv-private'")
    print("3. 复制仓库的SSH或HTTPS URL")
    
    print("\n步骤2: 初始化本地仓库并上传文件")
    print("1. 在本地创建一个新目录:")
    print("   mkdir aptv-private && cd aptv-private")
    print("2. 初始化Git仓库:")
    print("   git init")
    print("3. 添加远程仓库:")
    print("   git remote add origin <your-repo-url>")
    print("4. 复制以下文件到目录:")
    print("   - github_private_autoupdate.py (此脚本)")
    print("   - .github/workflows/update.yml (Actions配置)")
    print("5. 提交并推送:")
    print("   git add .")
    print("   git commit -m 'Initial commit'")
    print("   git push -u origin main")
    
    print("\n步骤3: 配置GitHub Actions权限")
    print("1. 进入仓库设置 → Actions → General")
    print("2. 在 'Workflow permissions' 部分选择 'Read and write permissions'")
    print("3. 勾选 'Allow GitHub Actions to create and approve pull requests'")
    print("4. 点击 'Save' 保存设置")
    
    print("\n步骤4: 生成Personal Access Token (PAT)")
    print("1. 进入GitHub设置 → Developer settings → Personal access tokens → Tokens (classic)")
    print("2. 点击 'Generate new token' → 'Generate new token (classic)'")
    print("3. 设置token名称，例如: 'APTV Private Access'")
    print("4. 设置过期时间，建议选择 '30 days' 或 '60 days'")
    print("5. 选择权限: 勾选 'repo' 权限")
    print("6. 点击 'Generate token' 生成token")
    print("7. 复制生成的token，妥善保存，这是唯一一次查看的机会")
    
    print("\n步骤5: 生成私有访问链接")
    print("使用以下格式创建私有访问链接:")
    print("https://<PAT>@raw.githubusercontent.com/<username>/<repo>/main/koreatv_private.m3u")
    print("\n例如:")
    print("https://ghp_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX@raw.githubusercontent.com/user/aptv-private/main/koreatv_private.m3u")
    
    print("\n步骤6: 在APTV中添加订阅")
    print("1. 打开APTV应用")
    print("2. 进入 '订阅管理' → '添加订阅'")
    print("3. 选择 '网络URL'")
    print("4. 粘贴生成的私有访问链接")
    print("5. 点击 '添加' 完成订阅")
    print("6. 启用 '自动更新' 选项，设置更新频率为30分钟")
    
    print("\n步骤7: 验证自动更新")
    print("1. 进入GitHub仓库 → Actions")
    print("2. 查看 'Update APTV Playlist' 工作流是否正常运行")
    print("3. 手动触发一次工作流测试")
    print("4. 检查M3U文件是否被更新")
    
    print("\n🔒 安全增强措施:")
    print("1. 定期轮换Personal Access Token (建议每30天)")
    print("2. 为PAT设置合理的过期时间")
    print("3. 不要在任何公开场合分享你的PAT或访问链接")
    print("4. 定期检查GitHub Actions运行日志")
    print("5. 如发现异常访问，立即撤销并重新生成PAT")
    
    print("\n⚡ 实时更新机制:")
    print("- GitHub Actions每30分钟自动运行一次")
    print("- 自动从源GitHub仓库获取最新的koreatv.json")
    print("- 自动生成并更新M3U文件")
    print("- APTV设置30分钟自动更新，确保与GitHub同步")
    
    print("\n📊 监控和管理:")
    print("- 查看version.json文件了解更新状态")
    print("- 通过GitHub Actions日志监控更新过程")
    print("- 手动触发工作流进行即时更新")
    print("=" * 80)


def test_connection():
    """测试GitHub连接"""
    print("\n🔗 测试GitHub连接...")
    try:
        with urllib.request.urlopen(GITHUB_JSON_URL, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
        print(f"✅ GitHub连接成功，获取到 {len(data)} 个频道")
        return True
    except Exception as e:
        print(f"❌ GitHub连接失败: {e}")
        return False


if __name__ == "__main__":
    print("🚀 GitHub私有仓库自动更新方案")
    print("=" * 80)
    print("\n此方案实现：")
    print("1. 🔒 完全私有访问（通过Personal Access Token）")
    print("2. ⚡ 实时自动更新（每30分钟）")
    print("3. 📦 完整的部署和管理流程")
    print("4. 🔍 详细的监控和安全措施")
    
    # 测试连接
    test_connection()
    
    # 生成M3U文件
    generate_m3u()
    
    # 创建GitHub Actions配置
    create_github_actions_config()
    
    # 显示完整指南
    show_complete_guide()
    
    print("\n🎯 部署完成建议:")
    print("1. 按照指南创建私有GitHub仓库")
    print("2. 配置Actions权限和PAT")
    print("3. 在APTV中添加私有订阅链接")
    print("4. 验证自动更新功能")
    print("5. 定期检查和维护系统")
    print("=" * 80)
