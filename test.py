import unittest

from airtest.core.api import *
from airtest.core.helper import G
from airtest.core.win import Windows
from pywinauto.findwindows import find_elements, find_window


class TestSuite(unittest.TestCase):
    """
    Airtest 版本: 1.2.6（最新）
    企业微信 版本：4.0.8.6604（最新）
    """

    def test_popup_menu(self):
        self.popup_menu()

    def test_popup_menu_without_setting_foreground(self):
        # 禁用 set_foreground 方法
        self.disable_setting_foreground()
        self.popup_menu()

    def popup_menu(self):
        # 保证客户端已登录
        e = find_elements(class_name='WeWorkWindow')[0]
        process = e.process_id
        main_handle = e.handle

        # 连接至主窗口
        main_window = connect_device("Windows:///" + str(main_handle))
        main_window.set_foreground()
        # 点击侧边栏图标[Calendar]
        touch(Template('assets/main_calendar_icon.png'))
        # 点击按钮[Add Calendar]
        touch(Template('assets/calendar_add_btn.png'))

        # 获取菜单窗口 handle 值
        menu_handle = find_window(class_name="DuiMenuWnd", process=process)
        # 连接至菜单窗口
        # 这一步，菜单窗口会因为 set_foreground 消失
        connect_device("Windows:///" + str(menu_handle))
        # 等待 1 秒
        time.sleep(1)
        # 点击菜单选项[Personal/Team Events]
        if not touch(Template('assets/calendar_menu_item_personal.png')):
            self.fail("The menu disappeared")

    def disable_setting_foreground(self):
        class HackingWindows(Windows):
            def connect(self, handle=None, **kwargs):
                if handle:
                    handle = int(handle)
                    self.app = self._app.connect(handle=handle)
                    self._top_window = self.app.window(handle=handle).wrapper_object()
                else:
                    for k in ["process", "timeout"]:
                        if k in kwargs:
                            kwargs[k] = int(kwargs[k])
                    self.app = self._app.connect(**kwargs)
                    self._top_window = self.app.top_window().wrapper_object()
                # self.set_foreground()

        G.CUSTOM_DEVICES['windows'] = HackingWindows
