from behave import given, when, then
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

DEFAULT_WAIT = 20

@given("the Appium driver is started")
def step_driver_started(context):
    assert hasattr(context, "driver") and context.driver is not None, "Driver is not started"
    # minimal change: ensure context.wait exists so other steps can use it
    if not hasattr(context, "wait") or context.wait is None:
        context.wait = WebDriverWait(context.driver, DEFAULT_WAIT)


# generic tap by xpath
@when('I tap the element with xpath "{xpath}"')
def step_tap_xpath(context, xpath):
    el = context.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, xpath)))
    el.click()


# generic tap by accessibility id
@when('I tap the element with accessibility id "{aid}"')
def step_tap_accessibility(context, aid):
    el = context.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, aid)))
    el.click()


# generic tap by resource-id
@when('I tap the element with id "{rid}"')
def step_tap_id(context, rid):
    el = context.wait.until(EC.element_to_be_clickable((AppiumBy.ID, rid)))
    el.click()


# type into xpath
@when('I type "{text}" into element with xpath "{xpath}"')
def step_type_xpath(context, text, xpath):
    el = context.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, xpath)))
    el.clear()
    el.send_keys(text)


# type into id
@when('I type "{text}" into element with id "{rid}"')
def step_type_id(context, text, rid):
    el = context.wait.until(EC.element_to_be_clickable((AppiumBy.ID, rid)))
    el.clear()
    el.send_keys(text)


@then('I should see an element with text "{text}"')
def step_see_text(context, text):
    # robust search: either @text or node contains
    xpath = f"//*[contains(@text, \"{text}\") or contains(., \"{text}\")]"
    el = context.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, xpath)))
    assert el is not None, f"Did not find text: {text}"


@then('I should see an element with xpath "{xpath}"')
def step_see_xpath(context, xpath):
    el = context.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, xpath)))
    assert el is not None, f"Did not find element with xpath: {xpath}"


@then('the element with xpath "{xpath}" should disappear')
def step_element_should_disappear(context, xpath):
    """
    Minimal disappearance check to validate successful login:
    waits until the locator is no longer present on the page.
    """
    try:
        context.wait.until_not(EC.presence_of_element_located((AppiumBy.XPATH, xpath)))
    except TimeoutException:
        raise AssertionError(f"Element still present (login may have failed): {xpath}")
