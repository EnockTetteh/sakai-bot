import os
from playwright.sync_api import sync_playwright

SAKAI_URL = "https://sakai.ug.edu.gh"

def get_data():
    username = os.getenv("SAKAI_USERNAME")
    password = os.getenv("SAKAI_PASSWORD")

    results = {
        "announcements": [],
        "assignments": [],
        "grades": [],
        "messages": []
    }

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        try:
            # ── Login ──────────────────────────────────────────────────
            page.goto(f"{SAKAI_URL}/portal/login", timeout=30000)
            page.fill('input[name="eid"]', username)
            page.fill('input[name="pw"]', password)
            page.click('input[type="submit"]')
            page.wait_for_load_state("networkidle", timeout=15000)

            if "login" in page.url:
                print("[Sakai] Login failed — check your credentials")
                browser.close()
                return None

            print("[Sakai] Logged in successfully")

            # ── Announcements ──────────────────────────────────────────
            try:
                page.goto(f"{SAKAI_URL}/portal/site/~{username}/page/announcements", timeout=15000)
                page.wait_for_load_state("networkidle", timeout=10000)
                items = page.query_selector_all(".announcementBody, .itemSummary, td.specialLink a")
                for item in items[:10]:
                    text = item.inner_text().strip()
                    if text:
                        results["announcements"].append(text)
            except Exception as e:
                print(f"[Sakai] Announcements error: {e}")

            # Try direct announcements tool URL
            if not results["announcements"]:
                try:
                    page.goto(f"{SAKAI_URL}/direct/announcement/user.json?n=10&d=7", timeout=15000)
                    import json
                    content = page.content()
                    # Extract JSON from page content
                    start = content.find('{')
                    end = content.rfind('}') + 1
                    if start != -1:
                        data = json.loads(content[start:end])
                        for item in data.get("announcement_collection", []):
                            title = item.get("title", "")
                            site = item.get("siteTitle", "")
                            if title:
                                results["announcements"].append(f"[{site}] {title}")
                except Exception as e:
                    print(f"[Sakai] Announcements JSON error: {e}")

            # ── Assignments ────────────────────────────────────────────
            try:
                page.goto(f"{SAKAI_URL}/direct/assignment/user.json?n=10", timeout=15000)
                import json
                content = page.content()
                start = content.find('{')
                end = content.rfind('}') + 1
                if start != -1:
                    data = json.loads(content[start:end])
                    for item in data.get("assignment_collection", []):
                        title = item.get("title", "")
                        due = item.get("dueTimeString", "")
                        site = item.get("context", "")
                        if title:
                            results["assignments"].append(f"[{site}] {title} — Due: {due}")
            except Exception as e:
                print(f"[Sakai] Assignments error: {e}")

            # ── Grades ─────────────────────────────────────────────────
            try:
                page.goto(f"{SAKAI_URL}/direct/gradebook/user.json", timeout=15000)
                import json
                content = page.content()
                start = content.find('{')
                end = content.rfind('}') + 1
                if start != -1:
                    data = json.loads(content[start:end])
                    for item in data.get("gradebook_collection", []):
                        name = item.get("itemName", "")
                        grade = item.get("grade", "")
                        site = item.get("siteTitle", "")
                        if name and grade:
                            results["grades"].append(f"[{site}] {name}: {grade}")
            except Exception as e:
                print(f"[Sakai] Grades error: {e}")

            # ── Messages ───────────────────────────────────────────────
            try:
                page.goto(f"{SAKAI_URL}/direct/message/user.json?n=5", timeout=15000)
                import json
                content = page.content()
                start = content.find('{')
                end = content.rfind('}') + 1
                if start != -1:
                    data = json.loads(content[start:end])
                    for item in data.get("message_collection", []):
                        subject = item.get("subject", "")
                        sender = item.get("createdByDisplayName", "")
                        if subject:
                            results["messages"].append(f"From {sender}: {subject}")
            except Exception as e:
                print(f"[Sakai] Messages error: {e}")

        except Exception as e:
            print(f"[Sakai] General error: {e}")
        finally:
            browser.close()

    return results
