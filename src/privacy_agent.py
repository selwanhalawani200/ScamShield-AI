import re

class PrivacyAgent:
    def __init__(self):
        # Balanced regex patterns for detecting PII
        
        # Matches standard email addresses
        self.email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        
        # Matches phone numbers with optional country code, parentheses, spaces, and dashes
        # e.g., +1-555-019-3827, (555) 123-4567, +966512345678
        self.phone_pattern = re.compile(r'(?:\+?\d{1,3}[\s-]?)?\(?\d{3}\)?[\s-]?\d{3}[\s-]?\d{4,5}\b')
        
        # Matches common credit card formats (13 to 19 digits with optional spaces or dashes)
        # We use a pattern that looks for groups of 4 digits, or 15 digit AMEX formats
        self.card_pattern = re.compile(r'\b(?:\d[ -]*?){13,19}\b')
        
        # Matches standard IBAN formats (2 letters, 2 digits, followed by up to 30 alphanumeric characters)
        self.iban_pattern = re.compile(r'\b[A-Z]{2}\d{2}[A-Z0-9]{11,30}\b')

    def sanitize_message(self, message: str) -> str:
        """
        Sanitizes a message by replacing sensitive information with masking tokens.
        
        Args:
            message (str): The raw input message.
            
        Returns:
            str: The sanitized message.
        """
        if not message:
            return message

        sanitized = message
        
        # Apply masks in order. 
        # Note: Order can matter if patterns overlap, but these are generally distinct.
        
        # Mask Emails
        sanitized = self.email_pattern.sub('[EMAIL]', sanitized)
        
        # Mask IBANs before credit cards or phones to prevent partial matches
        sanitized = self.iban_pattern.sub('[IBAN]', sanitized)
        
        # Mask Credit Cards
        # Using a custom replacement to ensure we only mask things that are mostly digits
        def card_repl(match):
            text = match.group(0)
            digit_count = sum(c.isdigit() for c in text)
            if 13 <= digit_count <= 19:
                return '[CARD]'
            return text
            
        sanitized = self.card_pattern.sub(card_repl, sanitized)
        
        # Mask Phone Numbers
        def phone_repl(match):
            text = match.group(0)
            digit_count = sum(c.isdigit() for c in text)
            # A valid phone number usually has between 7 and 15 digits
            if 7 <= digit_count <= 15:
                return '[PHONE]'
            return text
            
        sanitized = self.phone_pattern.sub(phone_repl, sanitized)
        
        return sanitized

if __name__ == "__main__":
    agent = PrivacyAgent()
    sample = "Contact me at john@example.com or +966512345678. My IBAN is SA1234567890123456789012 and card is 4123-4567-8901-2345."
    print("Original:", sample)
    print("Sanitized:", agent.sanitize_message(sample))
