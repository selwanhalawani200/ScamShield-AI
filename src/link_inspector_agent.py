import re

class LinkInspectorAgent:
    def __init__(self):
        self.url_pattern = re.compile(
            r'https?://[^\s]+|www\.[^\s]+'
        )

        self.suspicious_keywords = [
            "verify",
            "login",
            "secure",
            "update",
            "account",
            "claim",
            "reward",
            "prize",
            "bank"
        ]

    def inspect_links(self, message: str) -> dict:
        links = self.url_pattern.findall(message)

        if not links:
            return {
                "has_link": False,
                "suspicious": False,
                "links": []
            }

        suspicious = False

        for link in links:
            lower_link = link.lower()

            if any(word in lower_link for word in self.suspicious_keywords):
                suspicious = True

        return {
            "has_link": True,
            "suspicious": suspicious,
            "links": links
        }
        
if __name__ == "__main__":
    agent = LinkInspectorAgent()

    msg = "Verify your account here https://secure-bank-verify.com"

    print(agent.inspect_links(msg))