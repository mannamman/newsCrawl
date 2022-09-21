from google.cloud import storage
# from google.cloud.exceptions import NotFound as blob_not_found
import tempfile
import datetime
import json
from typing import List, Dict

class FileWorker:
    def __init__(self) -> None:
        self.bucket_name = "crawl-bucket"
        self._load_client()
        self.tempdir = tempfile.gettempdir()

    # 인증정보 로딩
    def _load_client(self) -> None:
        ## gcp cloud ##
        self.storage_client = storage.Client()
        self.bucket = self.storage_client.get_bucket(self.bucket_name)

    def upload_result(
        self, en_headers: List[str], translated_headers: List[str], source_lang: str,
        subject: str, kst: datetime.datetime, result_dic: Dict[str,any]
        ) -> None:
        kst_str = kst.strftime("%Y-%m-%d_%H:%M:00")
        blob_base_path = f"{subject}/{source_lang}/{kst_str}"

        en_header_blob_name = f"{blob_base_path}/en_header.txt"
        en_header_blob = self.bucket.blob(en_header_blob_name)
        en_header_blob.content_type = "text/plain"
        en_header_blob.upload_from_string("\n".join(en_headers))

        if(translated_headers):
            translated_headers_blob_name = f"{blob_base_path}/translated_headers.txt"
            translated_headers_blob = self.bucket.blob(translated_headers_blob_name)
            translated_headers_blob.content_type = "text/plain"
            translated_headers_blob.upload_from_string("\n".join(translated_headers))

        result_json_blob_name = f"{blob_base_path}/result.json"
        result_json_blob = self.bucket.blob(result_json_blob_name)
        result_json_blob.content_type = "text/plain"
        result_json_blob.upload_from_string(json.dumps(result_dic))

# test code
if(__name__ == "__main__"):
    worker = FileWorker()