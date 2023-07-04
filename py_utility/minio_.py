from typing import List
from minio import Minio
from minio.error import S3Error
import os
from tqdm import tqdm
from py_utility.progress import Progress

def get_all_file_paths(directory):
    directory = os.path.abspath(directory)
    file_paths = []

    for root, directories, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)
    file_paths_ = [file[len(directory)+1:] for file in file_paths]
    return file_paths, file_paths_

class MinioClient(Minio):
    def __init__(self, endpoint, access_key=None, secret_key=None, session_token=None, secure=True, region=None, http_client=None, credentials=None, cert_check=True):
        super().__init__(endpoint, access_key, secret_key, session_token, secure, region, http_client, credentials, cert_check)
    
    def upload(self,bucket_name: str,prefix:str, path_local_upload:str):
        """
        Uploads a file or directory to a Minio bucket.

        Args:
            bucket_name (str): The name of the Minio bucket.
            prefix (str): The prefix to be added to the file(s) in the bucket.
            path_local_upload (str): The path of the file or directory to be uploaded.
        """
        path_local_upload = os.path.abspath(path_local_upload)
        if os.path.isdir(path_local_upload):
            prefix = os.path.join(prefix, os.path.basename(path_local_upload))
        
        # Check if bucket already exists, if not create it.
        found = self.bucket_exists(bucket_name)
        if not found:
            self.make_bucket(bucket_name)
        else:
            print(f"Bucket '{bucket_name}' already exists")
            
        if os.path.isdir(path_local_upload):
            files = get_all_file_paths(path_local_upload)
            for file, file_ in tqdm(zip(files[0], files[1]), total=len(files[0]), desc="Uploading", unit="file"):
                path_drive = os.path.join(prefix, file_).replace("\\", "/")
                self.fput_object(
                    bucket_name, path_drive, file,
                )
        else:
            path_local_upload = os.path.abspath(path_local_upload)
            path_drive = os.path.join(prefix, os.path.basename(path_local_upload)).replace("\\", "/")
            self.fput_object(
                bucket_name, path_drive, path_local_upload,
            )

    def download(self,bucket_name: str,prefix:str, dir_local_storage:str):
        """Download a file or directory from a Minio bucket.

        Args:
            bucket_name (str): The name of the Minio bucket.
            prefix (str): The prefix to be added to the file(s) in the bucket.
            dir_local_storage (str): The directory to be downloaded.
        """
        for obj in self.list_objects(bucket_name, prefix=prefix, recursive=True):
            self.fget_object(bucket_name, obj.object_name, os.path.join(dir_local_storage, obj.object_name),progress=Progress())
    
if __name__ == "__main__":
    import os    
    endpoint = os.environ["MINIO_ENDPOINT"]
    access_key = os.environ["MINIO_ACCESS_KEY"]
    secret_key = os.environ["MINIO_SECRET_KEY"]
    client = MinioClient(endpoint, access_key, secret_key)
    
    bucket_name = "fine-tuned-model"
    prefix = "test/test/test/corrector_for_measure_accuracy/google-mt5-base-corrector-8-10(4)+full_testset_answer.csv"
    path_local = "./"
    client.download(bucket_name, prefix, path_local)