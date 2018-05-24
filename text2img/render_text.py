import logging
from datetime import datetime
from hashlib import md5
from io import BytesIO
from PIL import (
    Image, ImageDraw, ImageFont, ImageFilter
)

from config import (
    get_render_text_setting,
    get_font_bold, get_font_medium, get_font_regular,
    get_header, get_content, get_footer
)

logger = logging.getLogger(__file__)


# resize image
# ----------------------------------
def _image_resize(img):
    _img = img
    try:
        w, h = _img.size
        _width = get_render_text_setting('total_width', 720)
        _height = int(h * _width / w)

        _size = (_width, _height)
        _img = _img.resize(_size, Image.ANTIALIAS)
    except Exception as e:
        logger.error(e)
    return _img


def _get_background():
    _background = Image.open(get_content(), mode='r')
    return _image_resize(_background)


def _get_header():
    _header = Image.open(get_header(), mode='r')
    return _image_resize(_header)


def _get_footer():
    _footer = Image.open(get_footer(), mode='r')
    return _image_resize(_footer)


class RenderText(object):

    def __init__(self, **kwargs):
        self.title = kwargs.pop('title')
        self.content = kwargs.pop('content')
        self.timestamp = kwargs.pop('timestamp')
        self.point = '快讯'

        self.fnt_title = ImageFont.truetype(get_font_bold(), get_render_text_setting('font_title_size'))
        self.fnt_content = ImageFont.truetype(get_font_medium(), get_render_text_setting('font_content_size'))
        self.fnt_point = ImageFont.truetype(get_font_bold(), get_render_text_setting('font_point'))
        self.fnt_date = ImageFont.truetype(get_font_regular(), get_render_text_setting('font_date'))

        self.fnt_month = ImageFont.truetype(get_font_bold(), get_render_text_setting('font_month_size'))
        self.fnt_week = ImageFont.truetype(get_font_bold(), get_render_text_setting('font_week_size'))
        self.fnt_day = ImageFont.truetype(get_font_bold(), get_render_text_setting('font_day_size'))

        self.background = _get_background()
        self.header = _get_header()
        self.footer = _get_footer()

    def _get_img_h(self, image):
        w, h = image.size
        return h

    @property
    def image_height(self):
        footer_h = self._get_img_h(self.footer)
        elh = get_render_text_setting('element_line_height') * 3
        fpmt = get_render_text_setting('font_point_margin_top')
        fcmt = get_render_text_setting('font_content_margin_top')
        _r = self._get_img_title_height() + self._get_img_content_height()
        _r += footer_h + elh
        _r -= fpmt + fcmt
        return _r

    @property
    def image_width(self):
        return get_render_text_setting('total_width')

    @property
    def date_string(self):
        assert type(self.timestamp) is int, "timestamp must be int"
        return datetime.fromtimestamp(
            self.timestamp
        ).strftime('%Y-%m-%d %H:%M')

    @property
    def title_lines(self):
        _title_width = get_render_text_setting('content_width')
        return self._split_line(
            font=self.fnt_title,
            text=self.title,
            width=_title_width
        )

    @property
    def title_line_height(self):
        w, h = self.fnt_title.getsize(self.title)
        return h + get_render_text_setting('title_line_height')

    @property
    def content_lines(self):
        _content_width = get_render_text_setting('content_width')
        return self._split_line(
            font=self.fnt_content,
            text=self.content,
            width=_content_width,
        )

    @property
    def content_list_height(self):
        w, h = self.fnt_content.getsize(self.content)
        return h + get_render_text_setting('content_line_height')

    def _get_img_title_height(self):
        tlh = get_render_text_setting('title_line_height')
        point_w, point_h = self.fnt_point.getsize(self.point)
        logger.info("-------- point {h} height -------------".format(h=point_h))
        date_w, date_h = self.fnt_date.getsize(self.date_string)
        return self.title_line_height * len(self.title_lines) - tlh + point_h + date_h

    def _get_img_content_height(self):
        clh = get_render_text_setting('content_line_height')
        return self.content_list_height * len(self.content_lines) - clh

    def _split_line(self, font, text, width):
        s = 0
        lines = []
        for i in range(len(text)):
            if font.getsize(text[s:i])[0] > width:
                lines.append(text[s:i - 1])
                s = i - 1
        if i > s:
            lines.append(text[s:i + 1])
        return lines

    def draw_image(self):

        new_img = Image.new('RGB', (self.image_width, self.image_height), (255, 255, 255))

        draw = ImageDraw.Draw(new_img)
        new_img.paste(self.background, (0, 0))

        new_img.paste(self.header, (0, 0))


        return new_img


if __name__ == "__main__":
    detailData = {
        'timestamp': 1526616756,
        'title': '《华尔街日报》调查显示约 19% ICO 存在「误导甚至欺诈」',
        'content': '《华尔街日报》 5 月 17 日发表研究报告称，对约 1,500 个 ICO 项目调查显示，18.6% 的项目存在「误导性甚至欺诈性信息」。《华尔街日报》 称 1,450 个项目中有 271 '
                   '个存在上述问题。这些问题的具体表现从发布公司所在地及高管层虚假信息，到虚假财务信息，甚至伪造白皮书不一而足。问题项目中部分已经关张大吉，估计约造成 2.73 亿美元损失。 '
    }

    r = RenderText(**detailData)

    print (r.title_lines)
    print (r.title_line_height)

    print (r.content_lines)
    print (r.content_list_height)
    # print (r.image_width, r.image_height)
    r.draw_image().show()