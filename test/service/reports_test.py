import unittest
from app import model

from unittest.mock import patch
from app.service.reports import birthdays_report, marriage_report

mockMember = model.Member(_id="xx", birth_date_short="xx-xx",marriage_date_short="xx-xx", first_name="Test", last_name="Mock")


class ReportsTestCase(unittest.TestCase):
    @patch('app.service.reports.send_notification')
    @patch('app.service.reports.find_last_birthdays', return_value=[mockMember])
    def test_birthdays_report(self, patched_find_last_birthdays, patched_send_notification):
        birthdays_report()
        patched_find_last_birthdays.assert_called()
        patched_send_notification.assert_called()

    @patch('app.service.reports.send_notification')
    @patch('app.service.reports.find_last_marriages', return_value=[mockMember])
    def test_marriage_report(self, patched_find_last_marriages, patched_send_notification):
        marriage_report()
        patched_find_last_marriages.assert_called()
        patched_send_notification.assert_called()


if __name__ == '__main__':
    unittest.main()
