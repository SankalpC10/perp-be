import re


def extract_citation_numbers(sentence):
    print(sentence)
    pattern = r'\[citation:(\d+)\]'
    citation_numbers = re.findall(pattern,sentence)
    return citation_numbers


def fetch_json_attributes(json_data,print=False):
    names = []
    urls = []
    snippets = []
    for item in json_data:
        names.append(item['name'])
        urls.append(item['url'])
        snippets.append(item['snippet'])
    return names,urls,snippets