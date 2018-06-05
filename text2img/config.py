import os

from django.conf import settings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 配置项
TOTAL_WIDTH = 720  # 总宽度
CONTENT_MARGIN = int(TOTAL_WIDTH * 0.11)  # 内容区左右留白总宽度百分之11
CONTENT_WIDTH = TOTAL_WIDTH - CONTENT_MARGIN * 2  # 内容区宽度
TITLE_LINE_HEIGHT = 15  # 标题行高
CONTENT_LINE_HEIGHT = 10  # 内容行高
ELEMENT_LINE_HEIGHT = 40  # 元素之间高度
FLOAT_RATE = 0.33  # 按字体大小浮动的上边距，字体大小乘以该浮动率等于该字体大小的上边距
CIRCLE_SIZE = 50

# 字体大小
FNT_MONTH = 22
FNT_DAY = 52
FNT_WEEK = 20
FNT_TITLE = 40
FNT_TITLE_MARGIN_TOP = int(FNT_TITLE * FLOAT_RATE)
FNT_DATE = 24
FNT_DATE_MARGIN_TOP = int(FNT_DATE * FLOAT_RATE)
FNT_CONTENT = 28
FNT_CONTENT_MARGIN_TOP = int(FNT_CONTENT * FLOAT_RATE)
FNT_POINT = 24
FNT_POINT_MARGIN_TOP = int(FNT_POINT * FLOAT_RATE)

RENDER_TEXT_DEFAULTS = {
    'font': 'NotoSansCJKsc',
    'font_ext': 'otf',
    'font_path': os.path.join(BASE_DIR, './fonts/'),

    'font_month_size': FNT_MONTH,
    'font_week_size': FNT_WEEK,
    'font_day_size': FNT_DAY,
    'font_title_size': FNT_TITLE,
    'font_title_margin_top': FNT_TITLE_MARGIN_TOP,
    'font_date': FNT_DATE,
    'font_date_margin_top': FNT_DATE_MARGIN_TOP,
    'font_content_size': FNT_CONTENT,
    'font_content_margin_top': FNT_CONTENT_MARGIN_TOP,
    'font_point': FNT_POINT,
    'font_point_margin_top': FNT_POINT_MARGIN_TOP,

    'header': os.path.join(BASE_DIR, './source/daily-news-header.png'),
    'content': os.path.join(BASE_DIR, './source/daily-news-content.png'),
    'footer': os.path.join(BASE_DIR, './source/daily-news-footer.png'),

    'total_width': TOTAL_WIDTH,
    'content_margin': CONTENT_MARGIN,
    'content_width': CONTENT_WIDTH,
    'title_line_height': TITLE_LINE_HEIGHT,
    'content_line_height': CONTENT_LINE_HEIGHT,
    'element_line_height': ELEMENT_LINE_HEIGHT,
    'float_rate': FLOAT_RATE,
    'circle_width': CIRCLE_SIZE,
}

RENDER_TEXT = RENDER_TEXT_DEFAULTS.copy()

RENDER_TEXT.update(getattr(settings, 'RENDER_TEXT', {}))


def get_render_text_setting(setting, default=None):
    """
    Read a setting
    """
    return RENDER_TEXT.get(setting, default)


def font(weight="Regular"):
    """

    :type weight: str
    """
    return "{font_path}{font}-{weight}.{font_ext}".format(
        font_path=get_render_text_setting('font_path'),
        font=get_render_text_setting('font'),
        weight=weight,
        font_ext=get_render_text_setting('font_ext')
    )


def get_font_bold():
    return font(weight='Bold')


def get_font_medium():
    return font(weight='Medium')


def get_font_regular():
    return font(weight='Regular')


def get_header():
    return get_render_text_setting('header')


def get_content():
    return get_render_text_setting('content')


def get_footer():
    return get_render_text_setting('footer')


if __name__ == "__main__":
    print(get_font_bold())
    print(get_font_medium())
    print(get_font_regular())

    print(get_header())
    print(get_content())
    print(get_footer())
