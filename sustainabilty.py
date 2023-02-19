import requests
from constants import *

def ocr_space_file(filename, overlay=True, language='eng'):

    payload = {'isOverlayRequired': overlay,
               'apikey': OCR_API_KEY,
               'language': language,
               }
    with open(filename, 'rb') as f:
        r = requests.post(OCR_URL,
                          files={filename: f},
                          data=payload,
                          )
    return r.json()

def extract_texts(receipt_path, debug=False):

    resp = ocr_space_file(receipt_path)
    lines = resp["ParsedResults"][0]["TextOverlay"]["Lines"]

    lst = []

    for line_text_list in lines:
        line_text = line_text_list['LineText'].lower()
        if debug:
            print(line_text)
        lst.append(line_text)
    
    return " ".join(lst)

def receipt_contains_company(company_name, texts):
    return company_name.lower() in texts

def extract_sustainabilty_store(company_name, score_map):
    if company_name in score_map:
        return score_map[company_name]
    return 0

def get_sustainability_score(file_path):

    texts = extract_texts(file_path, debug=False)

    for company in company_list:
        if receipt_contains_company(company, texts):
            score = extract_sustainabilty_store(company, score_map)
            return {
                "company": company,
                "score": score
            }

    return None