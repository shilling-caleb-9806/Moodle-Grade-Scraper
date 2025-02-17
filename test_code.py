"""
Used for testing scraper.py and application.py.
scraper.py:
    __init__()
    start()
    get_grades()
    scrape_grades() - Good/Bad input
    login() - Bad input only
Timeout (in scraper.py):
    __init__()
    exceeded() - Good/Bad input
application.py:
    __init__()
    set_background() - Good/Bad input
    pull_data()
KivyApp (Here to make sure program builds to start with):
    __init__()
    build()
    close()

Caleb Shilling
"""
from scraper import Gradescraper as gs
from scraper import Timeout
import time
from application import Screen
from application import pull_data
import os
import pytest
import configparser


test_path = "http://htmlpreview.github.io/?https://github.com/\
shilling-caleb-9806/Moodle-Grade-Scraper/blob/master/Grades.html"
expected_result = [['HST103', ''], ['ENG104', '90.64'], ['CS162', '91.67']]


def test_scrape_good():
    """Test __init__, start(), get_grades(), and scrape_grades()."""
    # This tests the entire scraping function aside from logging in.
    # This is done using Grades.html, a HTML file stored in Github.
    grades = gs()
    grades.start()
    assert grades.get_grades(test_url=test_path) == expected_result
    grades.end_session()


def test_scrape_bad():
    """Bad input counterpart to test_scrape_good."""
    # This tests the entire scraping function aside from logging in.
    # This is done using Grades.html, a HTML file stored in Github.
    grades = gs()
    grades.start()
    assert grades.get_grades(test_url="no_path") == "E"
    grades.end_session()


CONTENT = [
    "moodle_username=X000000\n\
moodle_password=password\n\
app_background=background.bm",
    "moodle_username=X00\n\
moodle_password=passwrd\n\
app_background=backgrund.m"
]


TARGETS = [
    {
        'moodle_username': 'X000000',
        'moodle_password': 'password',
        'app_background': 'background.bm'
    },
    {
        'moodle_username': 'X00',
        'moodle_password': 'passwrd',
        'app_background': 'backgrund.m'
    }
]


def test_get_data(tmpdir):
    """Test __init__ and pull_data()."""
    # Tests pulling data from a config file using temp files.
    d = tmpdir.mkdir("dir").join("test_config.cfg")
    d.write(CONTENT[0])
    d2 = tmpdir.mkdir("dir2").join("test_config2.cfg")
    d2.write(CONTENT[1])

    assert pull_data(file_=d) == TARGETS[0]
    assert pull_data(file_=d2) == TARGETS[1]


bad_content = "app_background=backgrund.m"
bad_out = "Background link incorrect. Not using a background.\n"


def test_background_pull_bad(capsys, tmpdir):
    "Test a bad background search."
    temp_file = tmpdir.mkdir("dir").join("test_config.cfg")
    temp_file.write(bad_content)
    Screen(test_mode=True).set_background(config=temp_file)
    captured = capsys.readouterr()
    assert captured.out == bad_out


good_out = "Background added successfully.\n"


def test_background_pull_good(capsys, tmpdir):
    "Test a good background search."
    Screen(test_mode=True).set_background()
    captured = capsys.readouterr()
    assert captured.out == good_out


def test_log_write():
    grades = gs()
    grades.write_log("This is a test log output from test_code.py!")

    with open("log.txt", "r") as log:
        for line in log.read().splitlines():
            pass
        last = line

    assert last == "This is a test log output from test_code.py!"


def test_timeout():
    timeout = Timeout(4)
    time.sleep(2)
    assert not timeout.exceeded()
    time.sleep(3)
    assert timeout.exceeded()


def test_login_bad():
    """Test a bad login to Moodle."""
    """Unable do a good version of this test, as I would be giving away
    my moodle login credentials.
    This test takes about 30 seconds to run."""
    grades = gs()
    grades.start()
    assert not grades.login("bad", "credentials")
