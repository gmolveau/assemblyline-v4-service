import re

from typing import Dict, List

# TODO: Would prefer this mapping to be dynamic from trusted sources (ie. import from library), but will copy-paste for now
OCR_INDICATORS_MAPPING = {
    'ransomware': [
        # https://github.com/cuckoosandbox/community/blob/master/modules/signatures/windows/ransomware_message.py
        "your files", "your data", "your documents", "restore files",
        "restore data", "restore the files", "restore the data", "recover files",
        "recover data", "recover the files", "recover the data", "has been locked",
        "pay fine", "pay a fine", "pay the fine", "decrypt", "encrypt",
        "recover files", "recover data", "recover them", "recover your",
        "recover personal", "bitcoin", "secret server", "secret internet server",
        "install tor", "download tor", "tor browser", "tor gateway",
        "tor-browser", "tor-gateway", "torbrowser", "torgateway", "torproject.org",
        "ransom", "bootkit", "rootkit", "payment", "victim", "AES128", "AES256",
        "AES 128", "AES 256", "AES-128", "AES-256", "RSA1024", "RSA2048",
        "RSA4096", "RSA 1024", "RSA 2048", "RSA 4096", "RSA-1024", "RSA-2048",
        "RSA-4096", "private key", "personal key", "your code", "private code",
        "personal code", "enter code", "your key", "unique key"
    ],
    'macros': [
        # https://github.com/cuckoosandbox/community/blob/17d57d46ccbca0327a8299cb93abba8604b74df7/modules/signatures/windows/office_enablecontent_ocr.py
        "enable macro",
        "enable content",
        "enable editing",
    ]
}


def ocr_detections(image_path: str) -> Dict[str, List[str]]:
    try:
        import pytesseract
        from PIL import Image
    except ImportError:
        raise ImportError('In order to scan for OCR detections, ensure you have the following installed:\n'
                          'tesseract, pytesseract, and Pillow')

    # Use OCR library to extract strings from an image file
    detection_output = dict()
    ocr_output = pytesseract.image_to_string(Image.open(image_path))

    # Iterate over the different indicators and include lines of detection in response
    for indicator, list_of_terms in OCR_INDICATORS_MAPPING.items():
        regex_exp = re.compile('|'.join(list_of_terms).lower())
        list_of_strings = [line for line in ocr_output.split('\n') if regex_exp.search(line.lower())]
        if list_of_strings:
            detection_output[indicator] = list_of_strings

    return detection_output