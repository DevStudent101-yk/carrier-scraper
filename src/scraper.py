# src/scraper.py

import time
import random
import re
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
from src.config import REQUEST_DELAY_MIN, REQUEST_DELAY_MAX

FENDERR_BASE = "https://app.fenderr.com"


def random_delay():
    time.sleep(random.uniform(REQUEST_DELAY_MIN, REQUEST_DELAY_MAX))


def extract_text(page, selector):
    """Safely extract text from a CSS selector."""
    try:
        el = page.query_selector(selector)
        if el:
            return el.inner_text().strip()
    except Exception:
        pass
    return ""


def extract_profile_data(page, mc_number: int) -> dict | None:
    try:
        page.wait_for_timeout(3000)
        body_text = page.inner_text("body")

        if str(mc_number) not in body_text:
            return None

        def get_number_after(label):
            """
            Find label in page text, return the FIRST digit-only line after it.
            Stops searching if it hits the next label (all-caps line).
            Returns '0' if no digit found before next label.
            """
            lines = body_text.split("\n")
            found_label = False
            for line in lines:
                stripped = line.strip()
                if not stripped:
                    continue
                if found_label:
                    # Stop at next section label (all caps, no digits)
                    if stripped.isupper() and not any(c.isdigit() for c in stripped):
                        return "0"
                    # Return first digit-only value
                    if stripped.isdigit():
                        return stripped
                if label.lower() == stripped.lower():
                    found_label = True
            return "0"

        def get_text_after(label):
            """Find label, return next non-empty non-label line."""
            lines = body_text.split("\n")
            found_label = False
            for line in lines:
                stripped = line.strip()
                if not stripped:
                    continue
                if found_label:
                    if stripped.lower() != label.lower():
                        return stripped
                if label.lower() == stripped.lower():
                    found_label = True
            return ""

        # ── Company name ──────────────────────────────────────────
        company_name = ""
        h1 = page.query_selector("h1")
        if h1:
            company_name = h1.inner_text().strip()

        # ── Status ────────────────────────────────────────────────
        status = "Inactive"
        if "Active\n" in body_text or "\nActive\n" in body_text:
            # Make sure it is a standalone "Active" not "Inactive"
            lines = body_text.split("\n")
            for line in lines:
                if line.strip() == "Active":
                    status = "Active"
                    break
                if line.strip() == "Inactive":
                    status = "Inactive"
                    break

        # ── Auth status ───────────────────────────────────────────
        auth_status = ""
        for line in body_text.split("\n"):
            stripped = line.strip()
            if "authorized" in stripped.lower() and len(stripped) < 100:
                auth_status = stripped
                break

        # ── Phone ─────────────────────────────────────────────────
        import re
        phone = ""
        phone_match = re.search(
            r'\(?\d{3}\)?[\s\-\.]?\d{3}[\s\-\.]?\d{4}', body_text
        )
        if phone_match:
            phone = phone_match.group().strip()

        # ── Email ─────────────────────────────────────────────────
        email = ""
        email_match = re.search(
            r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}', body_text
        )
        if email_match:
            email = email_match.group().strip()

        # ── Drivers and Trucks ────────────────────────────────────
        # Use digit-only extraction to avoid grabbing label names
        num_drivers = get_number_after("DRIVERS")
        num_trucks  = get_number_after("POWER UNITS")

        # ── MCS-150 Date ──────────────────────────────────────────
        mcs_date = get_text_after("MCS-150 DATE")

        carrier = {
            "mc_number":    str(mc_number),
            "company_name": company_name,
            "phone":        phone,
            "email":        email,
            "status":       status,
            "auth_status":  auth_status,
            "mcs_date":     mcs_date,
            "num_drivers":  num_drivers,
            "num_trucks":   num_trucks,
        }

        return carrier

    except Exception as e:
        print(f"  [Error] Profile extraction: {e}")
        return None


def find_mc_match_and_click(page, mc_number: int) -> bool:
    """
    On the search results page, find the result card
    where MC number matches exactly, then click it.
    Returns True if found and clicked.
    """
    body_text = page.inner_text("body")

    # Find all carrier links on the results page
    links = page.query_selector_all("a[href*='/carrier/']")

    for link in links:
        try:
            link_text = link.inner_text()
            # Only click a result that explicitly says MC {mc_number}
            if f"MC {mc_number}" in link_text:
                print(f"  [Match] Found MC {mc_number} in result — clicking")
                link.click()
                page.wait_for_timeout(4000)
                return True
        except Exception:
            continue

    print(f"  [No Match] MC {mc_number} not found in results")
    return False


def scrape_mc(page, mc_number: int) -> dict | None:
    """
    Search Fenderr for one MC number using the already-open browser page.
    Returns carrier dict or None.
    """
    search_url = f"{FENDERR_BASE}/carrier-search?q={mc_number}"

    try:
        page.goto(search_url, wait_until="domcontentloaded", timeout=30000)
        page.wait_for_timeout(3000)
    except Exception as e:
        print(f"  [Nav Error] MC {mc_number}: {e}")
        return None

    body_text = page.inner_text("body")

    # Check for Cloudflare block
    if "Performing security verification" in body_text:
        print(f"  [Blocked] Cloudflare on MC {mc_number}")
        return None

    # Check for no results
    if "No carriers found" in body_text or "0 Carriers" in body_text:
        return None

    # Find and click the correct MC match
    clicked = find_mc_match_and_click(page, mc_number)

    if not clicked:
        return None

    # Extract data from the profile page
    return extract_profile_data(page, mc_number)