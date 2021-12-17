import six
from google.cloud import translate_v2 as translate
from google.oauth2 import service_account
import os

cred_path = f"{os.getcwd()}/../cred/local_translate.json"
credentials = service_account.Credentials.from_service_account_file(cred_path)
translate_client = translate.Client(credentials=credentials)

def translate_text(target, text):
    """Translates text into the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """
    global translate_client
    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(text, target_language=target)

    print(u"Text: {}".format(result["input"]))
    print(u"Translation: {}".format(result["translatedText"]))
    print(u"Detected source language: {}".format(result["detectedSourceLanguage"]))


def list_languages():
    global translate_client

    results = translate_client.get_languages()

    for language in results:
        print(u"{name} ({language})".format(**language))

translate_text("ko", "hello world!")