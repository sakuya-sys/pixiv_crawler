from setuptools import setup, find_packages

setup(
    name='asyncio_pixiv_crawler',                     # 安装时的项目名
    version='1.5.0',
    description='Pixiv 图片下载命令行工具',
    packages=find_packages(),            # 自动包含 pixiv_download 包
    package_data={
        "asyncio_pixiv_download":["config.yaml"]
    },
    install_requires=[
        'httpx',
        'aiofiles',                     # 依赖
    ],
    entry_points={
        'console_scripts': [
            'asyncio_pixiv_crawler = asyncio_pixiv_download.cli:cli',   # 假设你的 cli 在 main.py 中
        ],
    },
    python_requires='>=3.7',
)