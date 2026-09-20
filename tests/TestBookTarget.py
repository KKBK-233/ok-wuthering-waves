import unittest
from types import SimpleNamespace
from unittest.mock import Mock

from src.task.BaseWWTask import BaseWWTask


class BookTargetTask(BaseWWTask):
    """提供固定画面尺寸，隔离验证 F2 列表定位算法。"""

    @property
    def height(self):
        return 1000


class TestBookTarget(unittest.TestCase):

    def make_task(self, buttons):
        task = BookTargetTask.__new__(BookTargetTask)
        task.sleep = Mock()
        task._find_book_scroll_top = Mock(return_value=0.2)
        task.click = Mock()
        task.box_of_screen = Mock(return_value=object())
        task.find_feature = Mock(return_value=buttons)
        task.draw_boxes = Mock()
        task.wait_feature = Mock(return_value=SimpleNamespace(name='fast_travel_custom'))
        task.log_info = Mock()
        return task

    def test_structured_boundary_selects_matching_last_button(self):
        buttons = [
            SimpleNamespace(y=200),
            SimpleNamespace(y=404),
            SimpleNamespace(y=546),
            SimpleNamespace(y=688),
        ]
        task = self.make_task(buttons)

        is_team = task.click_on_book_target(5, 23, [2, 4, 7, 1, 9])

        self.assertFalse(is_team)
        self.assertIs(task.click.call_args_list[-1].args[0], buttons[-1])
        self.assertIn('selection=boundary_offset_0', task.log_info.call_args.args[0])

    def test_rejects_out_of_range_target(self):
        task = self.make_task([])

        with self.assertRaisesRegex(ValueError, 'invalid book target'):
            task.click_on_book_target(24, 23, [2, 4, 7, 1, 9])

    def test_rejects_structure_with_wrong_total(self):
        task = self.make_task([])

        with self.assertRaisesRegex(ValueError, 'invalid book structure'):
            task.click_on_book_target(5, 23, [2, 4, 7, 1, 8])


if __name__ == '__main__':
    unittest.main()
