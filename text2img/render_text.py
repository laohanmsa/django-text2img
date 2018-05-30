import logging
from datetime import datetime
# from hashlib import md5
from io import BytesIO
from PIL import (
    Image, ImageDraw, ImageFont, ImageFilter
)
import re
from .config import (
    get_render_text_setting,
    get_font_bold, get_font_medium, get_font_regular,
    get_header, get_content, get_footer
)

logger = logging.getLogger(__file__)

Weekday = [
    '星期一',
    '星期二',
    '星期三',
    '星期四',
    '星期五',
    '星期六',
    '星期日',
]


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
        _timestamp = kwargs.pop('timestamp')
        assert _timestamp is not None, "need timestamp"

        self.title = kwargs.pop('title')
        self.content = kwargs.pop('content')
        self.datetime = datetime.fromtimestamp(_timestamp)
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
        header_h = self._get_img_h(self.header)
        footer_h = self._get_img_h(self.footer)
        elh = get_render_text_setting('element_line_height') * 5
        fpmt = get_render_text_setting('font_point_margin_top')
        fcmt = get_render_text_setting('font_content_margin_top')
        ftmt = get_render_text_setting('font_title_margin_top')
        fdmt = get_render_text_setting('font_date_margin_top')
        _r = header_h + self._get_img_title_height() + self._get_img_content_height()
        _r += footer_h + elh
        _r -= fpmt + ftmt + fcmt + fdmt
        return _r

    @property
    def image_width(self):
        return get_render_text_setting('total_width')

    @property
    def date_string(self):
        return self.datetime.strftime('%Y-%m-%d %H:%M')

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
    def content_line_height(self):
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
        _ch = self.content_line_height * len(self.content_lines) - clh
        logger.info("------- content {h} height ----------".format(h=_ch))
        return _ch

    def _split_line(self, font, text, width):
        suffix = ["，", ",", "。", ".", "！", "!", "？", "?", "；", ";", "：", ":", "”", "’", "』", "」", "）", ")", "》", ">"
            , "、", "%"]
        prefix = ["（", "(", "『", "「", "“", "‘", "《", "<"]
        line = ''
        lines = [];
        textArray = text.split(' ')
        pattern = r'^[a-zA-Z\'‘’\"“”\.\,，]{2,}$'
        for _text in textArray:
            if (re.match(pattern, _text)):
                line += _text
                if font.getsize(line)[0] > width:
                    lines.append(line[:-len(_text)].strip())
                    line = _text
                pass
            else:
                for i in range(len(_text) + 1):
                    line += _text[i - 1:i];
                    if font.getsize(line)[0] > width:
                        # 处理行尾字符是否是允许字符
                        if (_text[i - 1:i] in suffix):
                            lines.append(line.strip())
                            line = ''
                        elif (text[i - 2:i - 1] in prefix):
                            lines.append(line[:len(line) - 2].strip())
                            line = line[len(line) - 2:]
                        else:
                            lines.append(line[:len(line) - 1].strip())
                            line = line[len(line) - 1:]
            line += ' '
        if line.strip() != '':
            lines.append(line.strip())
        return lines

    # def _get_weekday_name(self, index):
    def draw_image(self):

        logger.info("------- create new image ------------")
        new_img = Image.new('RGB', (self.image_width, self.image_height), (255, 255, 255))
        logger.info("------- new image is created (w, h) ------------".format(w=self.image_width,
                                                                              h=self.image_height))

        draw = ImageDraw.Draw(new_img)
        new_img.paste(self.background, (0, 0))

        # draw header
        new_img.paste(self.header, (0, 0))
        x, y = 585, 70  # define month pos
        # print(self.datetime.month)
        month_string = "- {:02d} -".format(self.datetime.month)
        draw.text((x, y), month_string, font=self.fnt_month, fill=(255, 255, 255))

        # cal day pos
        w, h = self.fnt_month.getsize("{}".format(self.datetime.month))
        x = 580
        y += h - 12
        # print (x, y)
        day_string = "{:02d}".format(self.datetime.day)
        draw.text((x, y), day_string, font=self.fnt_day, fill=(255, 255, 255))

        # cal week pos
        w, h = self.fnt_day.getsize(day_string)
        y += h + 5
        weekday_string = Weekday[self.datetime.weekday()]
        draw.text((x, y), weekday_string, font=self.fnt_week, fill=(255, 255, 255))

        # cal point pos
        x = get_render_text_setting('content_margin')
        header_h = self._get_img_h(self.header)
        elh = get_render_text_setting('element_line_height')
        y = header_h + elh
        draw.text((x, y), self.point, font=self.fnt_point, fill=(0x00, 0x56, 0xff))

        # cal title pos
        fpmt = get_render_text_setting('font_point_margin_top')
        w, h = self.fnt_point.getsize(self.point)
        y += h + elh - fpmt

        for row in self.title_lines:
            draw.text((x, y), row, font=self.fnt_title, fill=(0x3b, 0x3b, 0x3b))
            y += self.title_line_height

        ftmt = get_render_text_setting('font_title_margin_top')
        y += self.title_line_height - elh - ftmt
        draw.text((x, y), self.date_string, font=self.fnt_date, fill=(0x87, 0x87, 0x87))

        # cal content pos
        fdmt = get_render_text_setting('font_date_margin_top')
        w, h = self.fnt_date.getsize(self.date_string)
        y += h + elh - fdmt
        for row in self.content_lines:
            draw.text((x, y), row, font=self.fnt_content, fill=(0x54, 0x54, 0x54))
            y += self.content_line_height

        # cal footer pos
        fcmt = get_render_text_setting('font_content_margin_top')
        x = 0
        # y += elh - self.content_line_height
        clh = get_render_text_setting('content_line_height')
        y += elh - clh
        # y = self.image_height - self._get_img_h(self.footer)
        logger.info("---------- footer ({x}, {y}) --------------".format(x=x, y=y))
        new_img.paste(self.footer, (x, y))
        new_img.show()
        return new_img

    def draw_image_output(self):
        _img = self.draw_image()
        _image_fp = BytesIO()
        _img.save(_image_fp, format='JPEG', quality=100)
        _img.close()
        return _image_fp.getvalue()


if __name__ == "__main__":
    logging.basicConfig(level='INFO')
    detailData = {
        'timestamp': 1526616756,
        'title': '《华尔街日报》调查显示约 19% ICO 存在「误导甚至欺诈」',
        'content': '《华尔街日报》 5 月 17 日发表研究报告称，对约 1,500 个 ICO 项目调查显示，18.6% 的项目存在「误导性甚至欺诈性信息」。《华尔街日报》 称 1,450 个项目中有 271 '
                   '个存在上述问题。这些问题的具体表现从发布公司所在地及高管层虚假信息，到虚假财务信息，甚至伪造白皮书不一而足。问题项目中部分已经关张大吉，估计约造成 2.73 亿美元损失。 '
    }

    r = RenderText(**detailData)
    print(r.draw_image_output())
