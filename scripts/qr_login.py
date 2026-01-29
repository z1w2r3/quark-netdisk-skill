#!/usr/bin/env python3
"""
夸克网盘二维码登录脚本
生成二维码图片供 Claude Code 展示给用户
"""

import json
import sys
import time
import uuid
from pathlib import Path

import httpx
import qrcode


def get_qr_token():
    """获取二维码 token 和 URL"""
    client = httpx.Client(timeout=30.0)
    client.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Accept': 'application/json, text/plain, */*',
    })

    api_url = 'https://uop.quark.cn/cas/ajax/getTokenForQrcodeLogin'
    params = {
        'client_id': '532',
        'v': '1.2',
        'request_id': str(uuid.uuid4())
    }

    response = client.get(api_url, params=params)

    if response.status_code == 200:
        data = response.json()
        if data.get('status') == 2000000:
            token = data.get('data', {}).get('members', {}).get('token')
            if token:
                # 构造二维码 URL
                import urllib.parse
                base_url = "https://su.quark.cn/4_eMHBJ"
                qr_params = {
                    'token': token,
                    'client_id': '532',
                    'ssb': 'weblogin',
                    'uc_param_str': '',
                    'uc_biz_str': 'S:custom|OPT:SAREA@0|OPT:IMMERSIVE@1|OPT:BACK_BTN_STYLE@0'
                }
                qr_url = f"{base_url}?{urllib.parse.urlencode(qr_params)}"
                return token, qr_url, client

    raise Exception("获取二维码失败")


def generate_qr_image(url: str, output_path: str):
    """生成二维码图片"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(output_path)
    return output_path


def check_login_status(client: httpx.Client, qr_token: str):
    """检查登录状态"""
    api_url = 'https://uop.quark.cn/cas/ajax/getServiceTicketByQrcodeToken'
    params = {
        'client_id': '532',
        'v': '1.2',
        'token': qr_token,
        'request_id': str(uuid.uuid4())
    }

    response = client.get(api_url, params=params)

    if response.status_code == 200:
        data = response.json()
        status = data.get('status')

        # 登录成功
        if (status == 2000000 and
            data.get('message') == "ok" and
            data.get('data', {}).get('members', {}).get('service_ticket')):
            return "success", data

        # 明确失败
        if status in [50004002, 50004003, 50004004]:
            return "failed", data

        # 等待扫码
        return "waiting", data

    return "error", None


def complete_login(client: httpx.Client, service_ticket: str):
    """完成登录，获取 Cookie"""
    api_url = 'https://pan.quark.cn/account/info'
    params = {
        'st': service_ticket,
        'lw': 'scan'
    }

    response = client.get(api_url, params=params)

    if response.status_code == 200:
        # 提取 cookies
        cookies = []
        for cookie in client.cookies.jar:
            if cookie.domain and 'quark.cn' in cookie.domain:
                cookies.append(f"{cookie.name}={cookie.value}")

        return "; ".join(cookies)

    return None


def save_cookie(cookie_string: str):
    """保存 Cookie 到配置文件（兼容 quarkpan 格式）"""
    # quarkpan 默认使用当前目录的 config 文件夹
    # 也可以通过环境变量 QUARK_CONFIG_DIR 指定
    import os
    config_dir = os.getenv('QUARK_CONFIG_DIR')
    if config_dir:
        config_dir = Path(config_dir)
    else:
        config_dir = Path.cwd() / "config"

    config_dir.mkdir(parents=True, exist_ok=True)

    # 解析 cookie 字符串为列表格式
    cookies = []
    for pair in cookie_string.split('; '):
        if '=' in pair:
            name, value = pair.split('=', 1)
            cookies.append({
                'name': name,
                'value': value,
                'domain': '.quark.cn',
                'path': '/'
            })

    # 保存为 quarkpan 期望的 JSON 格式
    cookie_file = config_dir / "cookies.json"
    with open(cookie_file, 'w', encoding='utf-8') as f:
        json.dump({
            'cookies': cookies,
            'timestamp': int(time.time()),
            'expires_at': int(time.time()) + (7 * 24 * 3600)  # 7天后过期
        }, f, ensure_ascii=False, indent=2)

    return cookie_file


def main():
    # 输出目录
    output_dir = Path("/tmp/quark_qr")
    output_dir.mkdir(parents=True, exist_ok=True)

    qr_image_path = output_dir / "login_qr.png"
    status_file = output_dir / "status.json"

    if len(sys.argv) > 1:
        action = sys.argv[1]

        if action == "generate":
            # 生成二维码
            token, qr_url, client = get_qr_token()
            generate_qr_image(qr_url, str(qr_image_path))

            # 保存状态
            with open(status_file, 'w') as f:
                json.dump({
                    'token': token,
                    'qr_image': str(qr_image_path),
                    'created_at': time.time()
                }, f)

            print(json.dumps({
                'status': 'ok',
                'qr_image': str(qr_image_path),
                'message': '二维码已生成，请用夸克 APP 扫描'
            }))

        elif action == "check":
            # 检查登录状态
            if not status_file.exists():
                print(json.dumps({'status': 'error', 'message': '请先生成二维码'}))
                return

            with open(status_file) as f:
                state = json.load(f)

            token = state['token']
            client = httpx.Client(timeout=30.0)

            login_status, data = check_login_status(client, token)

            if login_status == "success":
                service_ticket = data.get('data', {}).get('members', {}).get('service_ticket')
                cookie_string = complete_login(client, service_ticket)

                if cookie_string:
                    cookie_file = save_cookie(cookie_string)
                    print(json.dumps({
                        'status': 'success',
                        'message': '登录成功！',
                        'cookie_file': str(cookie_file)
                    }))
                else:
                    print(json.dumps({
                        'status': 'error',
                        'message': '获取 Cookie 失败'
                    }))
            elif login_status == "waiting":
                print(json.dumps({
                    'status': 'waiting',
                    'message': '等待扫码...'
                }))
            else:
                print(json.dumps({
                    'status': 'failed',
                    'message': '登录失败或二维码已过期'
                }))
        else:
            print(json.dumps({'status': 'error', 'message': f'未知操作: {action}'}))
    else:
        print("用法: python qr_login.py [generate|check]")


if __name__ == "__main__":
    main()
