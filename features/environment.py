# features/environment.py
import os
import traceback
from dotenv import load_dotenv
from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.support.ui import WebDriverWait

load_dotenv()

def before_all(context):
    # mandatory BrowserStack vars
    context.username = os.getenv("BROWSERSTACK_USERNAME")
    context.access_key = os.getenv("BROWSERSTACK_ACCESS_KEY")
    context.app_url = os.getenv("BROWSERSTACK_APP_URL")

    if not context.username or not context.access_key or not context.app_url:
        raise RuntimeError("Missing BROWSERSTACK_USERNAME / BROWSERSTACK_ACCESS_KEY / BROWSERSTACK_APP_URL in .env")

    # devices from your browserstack.yml (kept here since you don't want browserstack.yml)
    context.devices = [  
        {"deviceName": "Samsung Galaxy S22 Ultra", "platformVersion": "12.0"},
        # {"deviceName": "Google Pixel 7 Pro",        "platformVersion": "13.0"},
        # {"deviceName": "OnePlus 9",                 "platformVersion": "11.0"}
    ]
    # simple round-robin index for scenarios
    context.device_index = 0

    # static bstack values from your YAML
    context.bstack_project_name = "BrowserStack Sample" 
    context.bstack_build_name = "bstack-demo"
    # custom build tag from YAML:
    context.build_tag = "You can set a custom Build Tag here"

def _mask_bstack_options(bopts):
    # produce a minimal safe dict for printing (no credentials)
    masked = {k: v for k, v in bopts.items() if k not in ("userName", "accessKey")}
    # keep buildName visible to help debugging
    return masked 

def before_scenario(context, scenario):
    device = context.devices[context.device_index]
    context.device_index = (context.device_index + 1) % len(context.devices)

    # bstack:options assembled from your YAML
    bstack_options = {
        "userName": context.username,
        "accessKey": context.access_key,
        "projectName": context.bstack_project_name,
        "buildName": context.bstack_build_name,
        "sessionName": scenario.name,
        "deviceName": device["deviceName"],
        "platformVersion": device["platformVersion"],
        "debug": True,
        "networkLogs": True,
        "local": False,
        # note: YAML used CUSTOM_TAG_1 — here we pass a single buildTag value
        "buildTag": context.build_tag
    }

    # Build Appium options using the Appium-provided UiAutomator2Options
    options = UiAutomator2Options()
    # basic app/platform settings
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.app = context.app_url

    # Attach BrowserStack options under bstack:options
    options.set_capability("bstack:options", bstack_options)

    remote_url = f"https://{context.username}:{context.access_key}@hub-cloud.browserstack.com/wd/hub"

    try:
        # Use "options=options" (works with Appium-Python-Client 5.x + selenium 4.30)
        context.driver = webdriver.Remote(
            command_executor=remote_url,
            options=options
        )

        if context.driver is None:
            raise RuntimeError("webdriver.Remote returned None (session didn't start).")

        context.wait = WebDriverWait(context.driver, 30)
        print(f"Started BrowserStack session on {device['deviceName']} (platform {device['platformVersion']})")
        print("session_id:", getattr(context.driver, "session_id", None))

    except Exception:
        print("Failed to start BrowserStack session.")
        print("Remote URL:", remote_url)
        # show only safe/diagnostic capability info
        try:
            caps = options.to_capabilities()
        except Exception:
            caps = {"app": context.app_url, "bstack:options": _mask_bstack_options(bstack_options)}
        # mask credentials
        if "bstack:options" in caps:
            caps["bstack:options"] = _mask_bstack_options(caps["bstack:options"])
        print("Capabilities used (masked):", caps)
        print("Exception traceback:")
        traceback.print_exc()
        # re-raise so behave reports hook error
        raise

def after_scenario(context, scenario):
    if hasattr(context, "driver") and context.driver:
        try:
            context.driver.quit()
        except Exception:
            pass

def after_all(context):
    pass
