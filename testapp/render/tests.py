import json
from django.test import TestCase
# Create your tests here.
from django.urls import reverse


class RenderTextTestCase(TestCase):

    def setUp(self):
        pass

    def test_can_render_image(self):
        _url = reverse('render_text')
        payload = {
            'timestamp': 1526616756,
            'title': '《华尔街日报》调查显示约 19% ICO 存在「误导甚至欺诈」',
            'content': '《华尔街日报》 5 月 17 日发表研究报告称，对约 1,500 个 ICO 项目调查显示，18.6% 的项目存在「误导性甚至欺诈性信息」。《华尔街日报》 称 1,450 个项目中有 271 个存在上述问题。这些问题的具体表现从发布公司所在地及高管层虚假信息，到虚假财务信息，甚至伪造白皮书不一而足。问题项目中部分已经关张大吉，估计约造成 2.73 亿美元损失。 '
        }

        res = self.client.post(_url, data=json.dumps(payload), content_type='application/json')
        self.assertEqual(res.status_code, 200)
