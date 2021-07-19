from unittest.mock import patch

from app.model import Member
from app.service import birthdays_report, marriage_report

mockMember = Member(_id="xx", birth_date_short="xx-xx", marriage_date_short="xx-xx", first_name="Test",
                    last_name="Mock")


@patch('app.service.send_notification')
@patch('app.service.find_last_birthdays', return_value=[mockMember])
def test_birthdays_report(patched_find_last_birthdays, patched_send_notification):
    birthdays_report()
    patched_find_last_birthdays.assert_called()
    patched_send_notification.assert_called()


@patch('app.service.send_notification')
@patch('app.service.find_last_marriages', return_value=[mockMember])
def test_marriage_report(patched_find_last_marriages, patched_send_notification):
    marriage_report()
    patched_find_last_marriages.assert_called()
    patched_send_notification.assert_called()
