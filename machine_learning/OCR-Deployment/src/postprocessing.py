import re

# Daftar kata kunci penting
important_keywords = {
    "amount_paid": ["Tunai", "Cash", "SHOPEEPAY", "GOPAY", "OVO", "DANA", "LINKAJA", "BRI", "BCA", "MANDIRI", "Pay"],
    "change_amount": ["Kembalian", "Change"],
    "total_price": ["Total", "Jumlah", "Amount", "Grand Total", "Belanja"]
}

def check_keyword_in_word(word, keyword):
    """
    Check if any part of the word matches the keyword.
    """
    word = re.sub(r'\s+', '', word)
    for i in range(len(word) - 2):
        if word[i:i+3].lower() in keyword.lower():
            return True
    return False

def clean_and_extract_keywords(text):
    """
    Clean text and extract keywords by combining fragmented parts.
    """
    words = text.split()
    clean_words = []
    for word in words:
        cleaned_word = re.sub(r'[^a-zA-Z0-9]', '', word)
        clean_words.append(cleaned_word)

    combined_text = ' '.join(clean_words)
    for key, keywords in important_keywords.items():
        for keyword in keywords:
            if keyword.lower() in combined_text.lower():
                combined_text = combined_text.replace(keyword.lower(), keyword)
    return combined_text

def extract_information(extracted_text):
    """
    Extracts relevant information from the extracted text.

    Args:
        extracted_text: The text extracted from the image.

    Returns:
        A dictionary containing the extracted information.
    """
    # Clean the text
    extracted_text = extracted_text.replace("\n", " ").replace("\t", " ").strip()
    extracted_text = re.sub(r"[^a-zA-Z0-9\s]", "", extracted_text)

    # Combine fragmented parts based on keywords
    cleaned_text = clean_and_extract_keywords(extracted_text)

    # Extract the total price
    total_patterns = [
        r"(?:TOTAL|Total|JUMLAH|Jumlah|AMOUNT|Amount|Belanja)\s*[:]*[Rp$]*\s*([\d.,]+)",
        r"(?:BAYAR|Pay|PAY)[\s:]*[Rp$]*\s*([\d.,]+)",
        r"(?:GRAND\s*TOTAL|Grand Total)[\s:]*[Rp$]*\s*([\d.,]+)",
    ]

    total_price = None
    for pattern in total_patterns:
        match = re.search(pattern, cleaned_text, re.IGNORECASE)
        if match:
            total_price = match.group(1)
            total_price = total_price.replace(",", "").replace(".", "")
            try:
                total_price = float(total_price)
            except ValueError:
                print(f"Error: Total price format invalid: {total_price}")
                total_price = None
            break

    if total_price is None:
        print("Warning: Total price not found.")

    # Extract the amount paid and change
    amount_paid = None
    change_amount = None

    # Options for amount_paid (cash, e-money)
    amount_paid_patterns = [
        r"(?:Tunai|Cash|CASH)\s*[:]*\s*([\d.,]+)",
        r"(?:SHOPEEPAY|GOPAY|OVO|DANA|LINKAJA|BRI\s*BCA|MANDIRI)\s*([\d.,]+)",
    ]

    for pattern in amount_paid_patterns:
        amount_paid_match = re.search(pattern, cleaned_text, re.IGNORECASE)
        if amount_paid_match:
            amount_paid = amount_paid_match.group(1).replace(",", "").replace(".", "")
            try:
                amount_paid = float(amount_paid)
            except ValueError:
                print(f"Error: Amount paid format invalid: {amount_paid}")
                amount_paid = None
            break

    # Regex for change with extra spaces
    change_match = re.search(r"Kembal\s*ian\s*[-:]*\s*([\d.,]+)", cleaned_text, re.IGNORECASE)
    if change_match:
        change_amount = change_match.group(1).replace(",", "").replace(".", "")
        try:
            change_amount = float(change_amount)
        except ValueError:
            print(f"Error: Change format invalid: {change_amount}")
            change_amount = None

    # Return the extracted information
    return {
        'total_price': total_price,
        'amount_paid': amount_paid,
        'change_amount': change_amount,
    }
