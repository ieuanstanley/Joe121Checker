from playwright.sync_api import sync_playwright

URL = "https://bookwhen.com/jacricket"

def check_sessions():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True) # run headless
        page = browser.new_page()
        page.goto(URL, timeout=60000)
        
        # Wait for agenda items
        page.wait_for_selector("tbody", timeout=30000)
        
        
        # Get agenda list items
        rows = page.query_selector_all("tbody tr")
        results = []
       
        for r in rows:
        
            classes = r.get_attribute("class") or ""
        
            if "month_title" in classes:
                current_month = r.inner_text().strip()
                continue
            
            #TODO: Make day and date be state held
            
            date = r.query_selector("td.dom")
            day = r.query_selector("td.dow")
            duration = r.query_selector("td.duration")
            summary = r.query_selector("td.summary button")
            
            
            
            duration_text = duration.inner_text().strip() if duration else "N/A"
            summary_text = summary.inner_text().strip() if summary else "N/A"
            date_text = date.inner_text().strip() if date else date_text
            day_text = day.inner_text().strip() if day else day_text
            
            sold_out_icon = r.query_selector(".sold_out")
            status = "Fully Booked" if sold_out_icon else "Available!"
            
            if summary_text == "N/A":
                continue
                
            if status == "Fully Booked":
                continue
            
            results.append({
                "time": duration_text,
                "summary": summary_text,
                "status": status,
                "day": day_text,
                "date": date_text,
                "month": current_month
            })
        
        browser.close()
        return results
        
if __name__ == "__main__":
    sessions = check_sessions()
    print(f"Available Sessions:")
    for s in sessions:
        print(f"{s['month']} {s['date']} {s['day']} - {s['time']} - {s['summary']}")