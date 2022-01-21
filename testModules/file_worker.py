from google.oauth2 import service_account
from google.cloud import storage
from google.cloud.exceptions import NotFound as blob_not_found
import os
import mimetypes
from uuid import uuid4
import tempfile
import datetime
import io
import json

class FileWorker:
    def __init__(self):
        self.bucket_name = "crawl-bucket"
        self.cred = self._load_client()
        self.tempdir = tempfile.gettempdir()


    # 인증정보 로딩
    def _load_client(self):
        ## local ##
        key_dir_path = os.path.dirname(os.path.abspath(__file__))
        key_path = f"{key_dir_path}/../cred/local_translate.json"
        credentials = service_account.Credentials.from_service_account_file(
            key_path, scopes=["https://www.googleapis.com/auth/devstorage.read_write"],
        )
        self.storage_client = storage.Client(credentials=credentials, project=credentials.project_id)
        self.bucket = self.storage_client.get_bucket(self.bucket_name)

        ## gcp cloud ##
        self.storage_client = storage.Client()
        self.bucket = self.storage_client.get_bucket(self.bucket_name)


    def upload_result(
        self, en_headers :list, translated_headers :list, source_lang :str,
        subject :str, kst :datetime.datetime, result_dic :dict
        ):
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
            translated_headers_blob.upload_from_file(io.StringIO("\n".join(translated_headers)))

        result_json_blob_name = f"{blob_base_path}/result.json"
        result_json_blob = self.bucket.blob(result_json_blob_name)
        result_json_blob.content_type = "text/plain"
        result_json_blob.upload_from_string(json.dumps(result_dic))

    
if(__name__ == "__main__"):
    worker = FileWorker()