import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RENDER_TEXT_DEFAULTS = {
    'font': '',
    'font_ext': 'otf',
    'font_path': os.path.join(BASE_DIR, './fonts/'),
}

RENDER_TEXT = RENDER_TEXT_DEFAULTS.copy()


def get_render_text_setting(setting, default=None):
    """
    Read a setting
    """
    return RENDER_TEXT.get(setting, default)


def font(weight: str = "Regular"):


    return


if __name__ == "__main__":
    print(font())
