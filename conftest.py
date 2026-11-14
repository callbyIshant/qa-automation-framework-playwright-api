"""
Root conftest.py — Playwright fixtures with automatic failure artifacts.

On ANY UI test failure, this conftest automatically captures:
  1. A full-page screenshot  (attached to Allure report)
  2. A Playwright trace .zip (attached to Allure report)
  3. The current page URL      (logged in Allure report)

Complies with AGENT_CONTEXT rule #6 (FAILURE ARTIFACTS).
"""

import pytest
import allure
from pathlib import Path
from playwright.sync_api import sync_playwright

from config.settings import BASE_URL, HEADLESS, SLOW_MO, BROWSER


# ── Directory for failure artifacts ──
ARTIFACTS_DIR = Path(__file__).parent / "test-results"


# ──────────────────────────────────────────────
#  Playwright browser / context / page fixtures
# ──────────────────────────────────────────────

@pytest.fixture(scope="session")
def browser_instance():
    """Launch a single browser instance for the entire test session."""
    with sync_playwright() as pw:
        browser_type = getattr(pw, BROWSER)
        browser = browser_type.launch(headless=HEADLESS, slow_mo=SLOW_MO)
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def context(browser_instance, request):
    """
    Create a fresh browser context per test with tracing enabled.
    Tracing starts before the test and is saved on failure.
    """
    ctx = browser_instance.new_context(
        base_url=BASE_URL,
        viewport={"width": 1280, "height": 720},
    )
    # Start tracing BEFORE the test runs (screenshots + snapshots + sources)
    ctx.tracing.start(screenshots=True, snapshots=True, sources=True)
    yield ctx
    # ── Post-test: always stop tracing; capture artifacts only on failure ──
    _handle_post_test(request, ctx)
    ctx.close()


@pytest.fixture(scope="function")
def page(context):
    """Provide a fresh page from the per-test context."""
    pg = context.new_page()
    yield pg


# ──────────────────────────────────────────────
#  Post-test helper — stop tracing & save on fail
# ──────────────────────────────────────────────

def _handle_post_test(request, ctx):
    """Always stop tracing. On failure: save screenshot, trace, and URL."""
    failed = hasattr(request.node, "rep_call") and request.node.rep_call.failed

    if failed:
        test_name = (
            request.node.nodeid
            .replace("::", "_")
            .replace("/", "_")
            .replace("\\", "_")
        )
        artifacts_dir = ARTIFACTS_DIR / test_name
        artifacts_dir.mkdir(parents=True, exist_ok=True)

        # Grab the first page in the context (if any)
        pages = ctx.pages
        if pages:
            current_page = pages[0]

            # 1. Screenshot
            screenshot_path = artifacts_dir / "screenshot.png"
            current_page.screenshot(path=str(screenshot_path), full_page=True)
            allure.attach.file(
                str(screenshot_path),
                name="failure-screenshot",
                attachment_type=allure.attachment_type.PNG,
            )

            # 2. Current URL
            allure.attach(
                current_page.url,
                name="failure-url",
                attachment_type=allure.attachment_type.TEXT,
            )

        # 3. Playwright Trace (stop + save)
        trace_path = artifacts_dir / "trace.zip"
        ctx.tracing.stop(path=str(trace_path))
        allure.attach.file(
            str(trace_path),
            name="failure-trace",
            attachment_type=allure.attachment_type.ZIP,
        )
    else:
        # Discard the trace for passing tests (avoid resource leak)
        ctx.tracing.stop()


# ──────────────────────────────────────────────
#  pytest hook: store test result on the node
#  so fixtures can inspect pass/fail status
# ──────────────────────────────────────────────

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach the call-phase report to the test item so fixtures can read it."""
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)
