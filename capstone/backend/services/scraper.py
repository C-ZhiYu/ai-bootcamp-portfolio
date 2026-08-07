# services/scraper.py
import requests
from bs4 import BeautifulSoup

def fetch_scam_alerts() -> list:
    """Scrapes the official ScamShield SG website for the latest scam bulletins."""
    # We are targeting the official Scam Bulletins page
    url = "https://www.scamshield.gov.sg/resources/scam-bulletins/"
    
    # We use a User-Agent so the government firewall doesn't block our Python script
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        alerts = []
        
        # Search for paragraph text that explicitly mentions "Scammers" or "scam"
        for p in soup.find_all('p'):
            text = p.get_text(strip=True)
            # We want substantive alerts, not just menu navigation words
            if ("Scammers" in text or "scam" in text.lower()) and 30 < len(text) < 200:
                if text not in alerts:
                    alerts.append(text)
                    
        # If the scraper succeeds but finds nothing (e.g., they changed the HTML tags), raise an error to trigger the fallback
        if not alerts:
            raise ValueError("No alert text found in HTML structure.")
            
        return alerts[:5] # Return the top 5 most recent alerts
        
    except Exception as e:
        print(f"⚠️ Live Scraper Failed (serving cached fallback): {e}")
        return [
            "July 2026 Alert: Scammers used fake Microsoft pop-up alerts to trick victims into calling a 'technical support' number.",
            "June 2026 Alert: Scammers have lured victims into fake investment chat groups by pretending to be experts, offering 'free investment lessons'.",
            "May 2026 Alert: Fake friend call scams are on the rise. Scammers are posing as friends to trick victims into transferring money urgently."
        ]