import os

from django.conf import settings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RENDER_TEXT_DEFAULTS = {
    'font': 'NotoSansCJKsc',
    'font_ext': 'otf',
    'font_path': os.path.join(BASE_DIR, './fonts/'),
}

RENDER_TEXT = RENDER_TEXT_DEFAULTS.copy()


# RENDER_TEXT.update(getattr(settings, 'RENDER_TEXT', {}))


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


if __name__ == "__main__":
    print(get_font_bold())
    print(get_font_medium())
    print(get_font_regular())
