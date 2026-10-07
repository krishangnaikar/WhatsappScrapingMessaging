import io
import runpy
from pathlib import Path
from unittest.mock import MagicMock, patch

def execute():
    names = ['qrcode','qrcode_terminal','selenium','selenium.webdriver','selenium.webdriver.common','selenium.webdriver.common.by','selenium.webdriver.support','selenium.webdriver.support.ui','selenium.webdriver.support.expected_conditions','undetected_chromedriver']
    dependencies = {name:MagicMock() for name in names}
    browser = dependencies['undetected_chromedriver']
    browser.Chrome.return_value.find_elements.return_value = []
    with patch.dict('sys.modules',dependencies), patch('builtins.open',return_value=io.StringIO('')), patch('time.sleep'):
        module = runpy.run_path(str(Path(__file__).resolve().parents[1] / 'message.py'))
    return module, browser

def test_empty_contacts_close_browser_without_sending():
    module, browser = execute()
    driver = browser.Chrome.return_value
    driver.quit.assert_called_once()
    driver.find_element.assert_not_called()

def test_message_is_typed_for_each_contact_and_browser_closed():
    module, browser = execute()
    driver = browser.Chrome.return_value
    driver.reset_mock()
    with patch('time.sleep'):
        module['message_phones'](['15550000001','15550000002'],'test message')
    visits = [call.args[0] for call in driver.get.call_args_list]
    assert any('phone=15550000001' in url for url in visits)
    assert any('phone=15550000002' in url for url in visits)
    typed = [call.args[0] for call in driver.find_element.return_value.send_keys.call_args_list]
    assert typed.count('test message') == 2
    driver.quit.assert_called_once()
