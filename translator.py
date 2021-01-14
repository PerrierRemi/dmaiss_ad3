import http.client
import json

from secrets import MICROSOFT_TRANSLATE_API_KEY

# TODO: Add decorator for API call

class Translator():
    API_ROOT = 'microsoft-translator-text.p.rapidapi.com'

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


    def _get_all_languages(self): 
        conn = http.client.HTTPSConnection(self.api_root)

        headers = {
            'x-rapidapi-key': MICROSOFT_TRANSLATE_API_KEY,
            'x-rapidapi-host': "microsoft-translator-text.p.rapidapi.com"
            }

        conn.request("GET", "/languages?api-version=3.0", headers=headers)

        res = conn.getresponse()
        data = json.loads(res.read().decode("utf-8"))

        data = data['translation']
        map_name_id = {data[key]['nativeName']: key for key in data}

        return map_name_id
        

    def _post_translate(self, message, language):
        conn = http.client.HTTPSConnection(self.api_root)

        payload = f"""
            [\r
                {{\r
                    \"Text\": \"{message}"\r
                }}\r
            ]"""

        headers = {
            'content-type': "application/json",
            'x-rapidapi-key': MICROSOFT_TRANSLATE_API_KEY,
            'x-rapidapi-host': "microsoft-translator-text.p.rapidapi.com"
            }

        conn.request("POST", f"/translate?to={language}&api-version=3.0&from=en&profanityAction=NoAction&textType=plain", payload, headers)

        res = conn.getresponse()
        data = json.loads(res.read().decode("utf-8"))

        return data[0]['translations'][0]['text']



# Testing
if __name__ == '__main__':
    print(Translator()._get_all_languages())