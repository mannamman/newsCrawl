from google.cloud import translate_v3 as translate
from google.oauth2 import service_account
import os

cred_path = f"{os.getcwd()}/../cred/local_translate.json"
credentials = service_account.Credentials.from_service_account_file(cred_path)
translate_client = translate.TranslationServiceClient(credentials=credentials)
location = "global"
parent = f"projects/{credentials.project_id}/locations/{location}"

def translate_text(source_lang, target_lang, texts):
    global translate_client
    global parent
    res = translate_client.translate_text(
        parent=parent,
        contents=["hello", "world!"],
        mime_type="text/plain",
        source_language_code="en",
        target_language_code="ko"
    )
    a = [i.translated_text for i in res.translations]
    print(a)

translate_text("en", "ko", ["hello", "world!"])