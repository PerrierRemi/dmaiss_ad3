import requests as rq
import json

from secrets import MICROSOFT_TRANSLATE_API_KEY

# TODO: Add decorator for API call

class Translator():
    API_ROOT = 'https://microsoft-translator-text.p.rapidapi.com'

    def __init__(self):
        self.api_root = Translator.API_ROOT

    def translate_quizz(self, quizz, language):
        tq = quizz.copy()

        for qc in tq:
            tq[qc]['txt'] = self._post_translate(tq[qc]['txt'], language)

            if tq[qc]['question_type'] == 'close':
                for ac in tq[qc]['answers']:
                    tq[qc]['answers'][ac] = self._post_translate(tq[qc]['answers'][ac], language)

        return tq


    def _get_all_laguages(self): # TODO: Decode string
        url = self.api_root + '/languages'

        querystring = {
            "api-version":"3.0",
            "scope":"translation"}

        headers = {
            'x-rapidapi-key': MICROSOFT_TRANSLATE_API_KEY,
            'x-rapidapi-host': "microsoft-translator-text.p.rapidapi.com"
            }

        response = rq.request("GET", url, headers=headers, params=querystring)

        return response.content


    def _post_translate(self, message, language):
        url = self.api_root + '/translate'

        querystring = {
            'to': language,
            'api-version': '3.0',
            'from': 'en', # From English by default
            'profanityAction': 'NoAction',
            'textType': 'plain'
            }

        payload = f"""
            [\r
                {{\r
                    \"Text\": \"{message}"\r
                }}\r
            ]"""

        headers = {
            'content-type': 'application/json',
            'x-rapidapi-key': MICROSOFT_TRANSLATE_API_KEY,
            'x-rapidapi-host': 'microsoft-translator-text.p.rapidapi.com'
            }

        response = rq.request("POST", url, data=payload, headers=headers, params=querystring)
        traduction = json.loads(response.content)
        return traduction[0]['translations'][0]['text']


# Testing
if __name__ == '__main__':
    import json
    from pprint import pprint
    quizz = json.load(open('quizz.json', 'r'))
    tq = Translator().translate_quizz(quizz, 'fr')
    pprint(tq)
