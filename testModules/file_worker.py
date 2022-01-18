from google.oauth2 import service_account
from google.cloud import storage
from google.cloud.exceptions import NotFound as blob_not_found
import os
import mimetypes
from uuid import uuid4
import tempfile

class FileWorker:
    def __init__(self):
        self.bucket_name = "crawl-bucket"
        self.cred = self._load_client()
        self.tempdir = tempfile.gettempdir()

    # 인증정보 로딩
    def _load_client(self):
        global cred_base_path
        key_dir_path = os.path.dirname(os.path.abspath(__file__))
        key_path = f"{key_dir_path}/../cred/local_translate.json"
        credentials = service_account.Credentials.from_service_account_file(
            key_path, scopes=["https://www.googleapis.com/auth/devstorage.read_write"],
        )
        self.storage_client = storage.Client(credentials=credentials, project=credentials.project_id)
        self.bucket = self.storage_client.get_bucket(self.bucket_name)

    def _get_mimetypes(self, source_url :str):
        mime = mimetypes.guess_type(source_url)[0]
        if(mime is None):
            mime = "application/octet-stream"
        return mimetypes.guess_type(source_url)[0]

    def _to_uri(self, input_blob_name :str, output_blob_name :str) -> tuple:
        return (f"gs://{self.bucket_name}/{input_blob_name}/", f"gs://{self.bucket_name}/{output_blob_name}/")

    def save_and_upload(self, context_results :list):
        context = "\n".join(context_results)
        uuid = uuid4()
        file_save_path = f"{self.tempdir}/{uuid}.txt"
        with open(file_save_path, "w") as f:
            f.write(context)
        input_blob_name, output_blob_name = self._file_upload(file_save_path)
        os.remove(file_save_path)
        return self._to_uri(input_blob_name, output_blob_name)

    def _file_upload(self, local_source_url :str) -> tuple:
        mime = self._get_mimetypes(local_source_url)
        input_blob_name = f"input/{local_source_url.split('/')[-1]}"
        output_blob_name = f"output/{local_source_url.split('/')[-1]}"
        blob = self.bucket.blob(input_blob_name)
        with open(local_source_url, "rb") as f:
            blob.upload_from_file(f, content_type=mime)
        return (input_blob_name, output_blob_name)
    

    
if(__name__ == "__main__"):
    worker = FileWorker()