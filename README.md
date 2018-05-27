# django-text2img


[![GitHub license](https://img.shields.io/github/license/Bit03/django-text2img.svg)](https://github.com/Bit03/django-text2img/blob/master/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/Bit03/django-text2img.svg)](https://github.com/Bit03/django-text2img/issues)
[![GitHub forks](https://img.shields.io/github/forks/Bit03/django-text2img.svg)](https://github.com/Bit03/django-text2img/network)
[![GitHub stars](https://img.shields.io/github/stars/Bit03/django-text2img.svg)](https://github.com/Bit03/django-text2img/stargazers)



## 安装

```.bash
python setup.py install
```


## 配置
在 django settings 中增加 一下配置
```.python
RENDER_TEXT = {
    'font': 'NotoSansCJKsc',
    'font_ext': 'otf',
    'font_path': os.path.join(BASE_DIR, '../fonts/'),

    'header': os.path.join(BASE_DIR, '../source/daily-news-header.png'),
    'content': os.path.join(BASE_DIR, '../source/daily-news-content.png'),
    'footer': os.path.join(BASE_DIR, '../source/daily-news-footer.png'),
}
```
