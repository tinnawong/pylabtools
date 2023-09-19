from minio import Minio
from tqdm import tqdm
import os
from multiprocessing import Pool, cpu_count
from typing import List, Tuple
import logging
from concurrent.futures import ThreadPoolExecutor

class MinioWrapper:
    """
    Wrapper class for MinIO operations.

    Attributes:
    - minio_client (Minio): The Minio client object.
    - endpoint (str): Minio server endpoint.
    - access_key (str): Access key for Minio server.
    - secret_key (str): Secret key for Minio server.
    """
    def __init__(self, endpoint: str, access_key: str = None, secret_key: str = None, secure: bool = True):
        self.minio_client = Minio(endpoint, access_key=access_key, secret_key=secret_key, secure=secure)
        logging.info(f"Minio client created for endpoint: {endpoint}")
        self.endpoint = endpoint
        self.access_key = access_key
        self.secret_key = secret_key

    @staticmethod
    def get_all_file_paths(directory: str) -> Tuple[List[str], List[str]]:
        """
        Retrieves the absolute paths and relative paths of all files in the given directory.

        Parameters:
        - directory (str): The directory whose files' paths are to be retrieved.

        Returns:
        - Tuple[List[str], List[str]]: A tuple containing two lists:
          1. A list of absolute file paths.
          2. A list of relative file paths from the input directory.
        """
        directory = os.path.abspath(directory)
        abspath_files = [os.path.join(root, filename) 
                        for root, _, files in os.walk(directory) for filename in files]
        relative_paths = [file[len(directory)+1:] for file in abspath_files]
        return abspath_files, relative_paths

    @staticmethod
    def upload_file(args: Tuple[str, str, str, str, str, str]) -> str:
        """
        Uploads a single file to a MinIO bucket.

        Parameters:
        - args (Tuple[str, str, str, str, str, str]): A tuple containing the following:
          1. Minio server endpoint.
          2. Access key for Minio server.
          3. Secret key for Minio server.
          4. Target Minio bucket name.
          5. Local path of the file to be uploaded.
          6. Remote path (including filename) where the file will be stored in the bucket.

        Returns:
        - str: A string indicating the success status ("Success") or the error message.
        """
        minio_endpoint, minio_access_key, minio_secret_key, bucket_name, local_path, remote_path = args
        minio_client = Minio(minio_endpoint, minio_access_key, minio_secret_key)
        try:
            minio_client.fput_object(bucket_name, remote_path, local_path)
            return "Success"
        except Exception as err:
            return f"Upload Error for {local_path} : {err}"

    def upload(self, bucket_name: str, path_local_upload: str, prefix: str = "") -> None:
        """
        Uploads files or directories to a specified MinIO bucket.

        If the provided path represents a directory, all files within it are uploaded with their
        relative paths maintained in the bucket. If the path represents a single file, only that file 
        is uploaded. The upload leverages multiprocessing for enhanced speed.

        Parameters:
        - bucket_name (str): The target Minio bucket where the files/directories will be uploaded.
        - path_local_upload (str): The local path of the file or directory to be uploaded.
        - prefix (str, optional): The prefix or folder name within the bucket where the files will be uploaded. Defaults to "".

        Returns:
        - None: Files are uploaded to the MinIO bucket and no explicit return value is provided.

        Raises:
        - Exceptions related to file upload will be logged.

        Example:
        >>> client = MinioWrapper(endpoint="localhost:9000", access_key="YOUR_ACCESS_KEY", secret_key="YOUR_SECRET_KEY")
        >>> client.upload(bucket_name="mybucket", path_local_upload="/path/to/local/data", prefix="remote/folder/")
        """
        path_local_upload = os.path.abspath(path_local_upload)
        upload_args = []
        
        if os.path.isdir(path_local_upload):
            prefix = os.path.join(prefix, os.path.basename(path_local_upload))
            files = MinioWrapper.get_all_file_paths(path_local_upload)
            upload_args = [(self.endpoint, self.access_key, self.secret_key, bucket_name, local_file, os.path.join(prefix, remote_file).replace("\\", "/")) 
                           for local_file, remote_file in zip(files[0], files[1])]
        else:
            remote_path = os.path.join(prefix, os.path.basename(path_local_upload)).replace("\\", "/")
            upload_args.append((self.endpoint, self.access_key, self.secret_key, bucket_name, path_local_upload, remote_path))

        # Use multiprocessing for the uploads
        with Pool(processes=cpu_count()) as pool:
            results = list(tqdm(pool.imap_unordered(MinioWrapper.upload_file, upload_args), total=len(upload_args), desc="Files Uploaded", unit="file"))
        
        # Handle and display errors
        errors = [result for result in results if result != "Success"]
        for error in errors:
            logging.error(error)
            

    def download_files(self, bucket_name, prefix="", recursive=False, destination_path="", max_workers=10):
        """
        Download all files from the specified bucket with optional prefix and recursion.

        Args:
        - bucket_name (str): Name of the bucket in minio.
        - prefix (str, optional): Prefix or folder name within the bucket. Defaults to "".
        - recursive (bool, optional): Whether or not to download files recursively. Defaults to False.
        - destination_path (str, optional): Local directory where the files will be downloaded to. Defaults to the current directory.
        - max_workers (int, optional): Maximum number of threads to use for concurrent downloads. Defaults to 10.
        """

        os.makedirs(destination_path, exist_ok=True)
        objects_to_download = [obj.object_name for obj in self.minio_client.list_objects(bucket_name, prefix=prefix, recursive=recursive)]
        
        def _download_to_dest(bucket_name, object_name, destination, pbar=None):
            dest_file_path = os.path.join(destination, object_name)
            os.makedirs(os.path.dirname(dest_file_path), exist_ok=True)
            self.minio_client.fget_object(bucket_name, object_name, dest_file_path)
            if pbar:
                pbar.update(1)

        with tqdm(total=len(objects_to_download), desc="Downloading files", unit="file") as pbar:
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                executor.map(_download_to_dest, [bucket_name]*len(objects_to_download), objects_to_download, [destination_path]*len(objects_to_download), [pbar]*len(objects_to_download))
    
    def download_file(self, bucket_name: str, file_name: str, file_output: str = None) -> None:
        """
        Downloads a specific file from the given MinIO bucket.

        Args:
        - bucket_name (str): The name of the bucket in MinIO from which the file needs to be downloaded.
        - file_name (str): The name (or path) of the file within the bucket to download.
        - file_output (str, optional): The desired local name (or path) for the downloaded file. 
            If not provided, the file will be saved with its original name from the bucket.

        Returns:
        - None: The function saves the downloaded file to the local filesystem and does not return any value.

        Raises:
        - S3Error: If there is an issue related to the S3 operation, e.g., a file or bucket does not exist.
        - ResponseError: If there is a network-related error during the call.

        Example:
        >>> client = MinioClient(endpoint="localhost:9000", access_key="YOUR_ACCESS_KEY", secret_key="YOUR_SECRET_KEY")
        >>> client.download_file(bucket_name="mybucket", file_name="data.txt", file_output="local_data.txt")
        """


        file_output_name = file_name
        if file_output is not None:
            file_output_name = file_output
        self.minio_client.fget_object(bucket_name, file_name, file_output_name)