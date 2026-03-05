#!/usr/bin/env python3
"""
读取 projects.json，生成 index.html。
用法：python3 generate.py
"""
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
CONFIG_FILE = BASE_DIR / "projects.json"
OUTPUT_FILE = BASE_DIR / "index.html"

CARD_TEMPLATE = """\
            <a href="{url}" class="link-card" target="_blank" style="--accent: {color};">
                <div class="card-icon">{icon}</div>
                <h2>{name}</h2>
                <p>{description}</p>
                <span class="card-arrow">→</span>
            </a>"""

HTML_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{site_title}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #0f0f17;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 40px 20px;
        }}

        /* 背景装饰光晕 */
        body::before {{
            content: '';
            position: fixed;
            top: -30%;
            left: -20%;
            width: 600px;
            height: 600px;
            background: radial-gradient(circle, rgba(108,99,255,0.15) 0%, transparent 70%);
            pointer-events: none;
        }}
        body::after {{
            content: '';
            position: fixed;
            bottom: -20%;
            right: -10%;
            width: 500px;
            height: 500px;
            background: radial-gradient(circle, rgba(17,153,142,0.12) 0%, transparent 70%);
            pointer-events: none;
        }}

        .container {{
            max-width: 960px;
            width: 100%;
            position: relative;
            z-index: 1;
        }}

        /* 头部 */
        .header {{
            text-align: center;
            margin-bottom: 56px;
        }}
        .header h1 {{
            color: #ffffff;
            font-size: 2.8rem;
            font-weight: 700;
            letter-spacing: -0.5px;
            margin-bottom: 12px;
        }}
        .header h1 span {{
            background: linear-gradient(90deg, #6c63ff, #11998e);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        .header p {{
            color: rgba(255,255,255,0.45);
            font-size: 1rem;
            letter-spacing: 0.5px;
        }}

        /* 卡片网格 */
        .links {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 24px;
        }}

        /* 卡片 */
        .link-card {{
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 16px;
            padding: 32px 28px;
            text-decoration: none;
            color: #fff;
            display: flex;
            flex-direction: column;
            gap: 10px;
            position: relative;
            overflow: hidden;
            transition: transform 0.25s ease, border-color 0.25s ease, background 0.25s ease;
        }}
        /* 顶部彩色高亮条 */
        .link-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: var(--accent, #6c63ff);
            opacity: 0.8;
            border-radius: 16px 16px 0 0;
        }}
        /* 卡片背景光晕 */
        .link-card::after {{
            content: '';
            position: absolute;
            top: -60px;
            right: -60px;
            width: 160px;
            height: 160px;
            background: radial-gradient(circle, var(--accent, #6c63ff) 0%, transparent 70%);
            opacity: 0;
            transition: opacity 0.3s ease;
            pointer-events: none;
        }}
        .link-card:hover {{
            transform: translateY(-6px);
            border-color: rgba(255,255,255,0.18);
            background: rgba(255,255,255,0.07);
        }}
        .link-card:hover::after {{
            opacity: 0.12;
        }}

        .card-icon {{
            font-size: 2rem;
            line-height: 1;
        }}
        .link-card h2 {{
            font-size: 1.15rem;
            font-weight: 600;
            color: #fff;
            margin-top: 4px;
        }}
        .link-card p {{
            font-size: 0.875rem;
            color: rgba(255,255,255,0.5);
            line-height: 1.5;
            flex: 1;
        }}
        .card-arrow {{
            font-size: 1rem;
            color: var(--accent, #6c63ff);
            opacity: 0;
            transform: translateX(-6px);
            transition: opacity 0.2s ease, transform 0.2s ease;
            align-self: flex-end;
        }}
        .link-card:hover .card-arrow {{
            opacity: 1;
            transform: translateX(0);
        }}

        /* 底部 */
        .footer {{
            text-align: center;
            margin-top: 56px;
            color: rgba(255,255,255,0.2);
            font-size: 0.8rem;
        }}

        @media (max-width: 480px) {{
            .header h1 {{ font-size: 2rem; }}
            .links {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{site_title_html}</h1>
            <p>{subtitle}</p>
        </div>
        <div class="links">
{cards}
        </div>
        <div class="footer">
            {project_count} projects · fiaiportal.com
        </div>
    </div>
</body>
</html>
"""


def load_config() -> dict:
    if not CONFIG_FILE.exists():
        raise FileNotFoundError(f"找不到配置文件：{CONFIG_FILE}")
    with open(CONFIG_FILE, encoding="utf-8") as f:
        return json.load(f)


def build_title_html(title: str) -> str:
    """把标题最后一个词变成渐变色"""
    words = title.rsplit(" ", 1)
    if len(words) == 2:
        return f"{words[0]} <span>{words[1]}</span>"
    return f"<span>{title}</span>"


def generate(config: dict) -> str:
    cards = "\n".join(
        CARD_TEMPLATE.format(
            url=p["url"],
            color=p.get("color", "#6c63ff"),
            icon=p.get("icon", "🔗"),
            name=p["name"],
            description=p["description"],
        )
        for p in config["projects"]
    )

    return HTML_TEMPLATE.format(
        site_title=config["site_title"],
        site_title_html=build_title_html(config["site_title"]),
        subtitle=config.get("subtitle", ""),
        cards=cards,
        project_count=len(config["projects"]),
    )


def main():
    print(f"读取配置：{CONFIG_FILE}")
    config = load_config()
    html = generate(config)
    OUTPUT_FILE.write_text(html, encoding="utf-8")
    print(f"✅ 生成成功：{OUTPUT_FILE}")
    print(f"   共 {len(config['projects'])} 个项目：")
    for p in config["projects"]:
        print(f"   {p.get('icon','🔗')} {p['name']} → {p['url']}")


if __name__ == "__main__":
    main()
