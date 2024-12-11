import re

def extract_information(extracted_text):
    """
    Extracts relevant information from the extracted text.

    Args:
        extracted_text: The text extracted from the image.

    Returns:
        A dictionary containing the extracted information.
    """
    # Clean the text
    extracted_text = extracted_text.replace("\n", " ").strip()
    extracted_text = re.sub(r"[^a-zA-Z0-9\s]", "", extracted_text)

    # Extract the total price
    total_patterns = [
        r'(?:TOTAL|Total|JUMLAH|Jumlah|AMOUNT|Amount)\s*[:]*[Rp$]*\s*([\d.,]+)',
        r'(?:BAYAR|Pay|PAY)[\s:]*[Rp$]*\s*([\d.,]+)',
        r'(?:GRAND\s*TOTAL|Grand Total)[\s:]*[Rp$]*\s*([\d.,]+)',
    ]

    total_price = None
    for pattern in total_patterns:
        match = re.search(pattern, extracted_text, re.IGNORECASE)
        if match:
            total_price = match.group(1)
            total_price = total_price.replace(",", "").replace(".", "")  # Clean thousand and decimal separators
            total_price = float(total_price)
            break

    # Extract the amount paid
    amount_paid_match = re.findall(r"Tunai\s*:\s*\$(\d+\.\d+)", extracted_text)  # Adjust regex to your receipt text
    if amount_paid_match:
        amount_paid = float(amount_paid_match[0])
    else:
        amount_paid = None

    # Extract the change
    change_match = re.findall(r"Kembali\s*:\s*\$(\d+\.\d+)", extracted_text)  # Adjust regex to your receipt text
    if change_match:
        change = float(change_match[0])
    else:
        change = None

    # Return the extracted information
    return {
        'total_price': total_price,
        'amount_paid': amount_paid,
        'change': change
    }