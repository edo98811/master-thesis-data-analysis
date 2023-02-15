import pathlib
import pandas as pd
import dropbox
from dropbox.exceptions import AuthError

DROPBOX_ACCESS_TOKEN = "sl.BY0lS_EBBE-_UjKytoL2LslKhcOOKmioPOntpeGgpTrJSxz01-6C10SMcoZw4_a5y45nLWHC8AUKJ5vT-akVsEeL65_fD76fas9orQ5FJtyCL1StUGMj80TVtkHCdGM-azTAD4U:EUR"

def dropbox_connect():
    """Create a connection to Dropbox."""

    try:
        dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
    except AuthError as e:
        print('Error connecting to Dropbox with access token: ' + str(e))
    return dbx


def dropbox_upload_file(local_path, local_file, dropbox_file_path, file_from_dataframe, FINAL_FILENAME_EXCEL):
    """Upload a file from the local machine to a path in the Dropbox app directory.

    Args:
        local_path (str): The path to the local file.
        local_file (str): The name of the local file.
        dropbox_file_path (str): The path to the file in the Dropbox app directory.

    Example:
        dropbox_upload_file('.', 'test.csv', '/stuff/test.csv')

    Returns:
        meta: The Dropbox file metadata.
    """

    try:
        dbx = dropbox_connect()

        local_file_path = pathlib.Path(local_path) / local_file

        with local_file_path.open("rb") as f:
            # meta = dbx.files_upload(f.read(), dropbox_file_path, mode=dropbox.files.WriteMode("overwrite"))


        meta = dbx.files_upload(file_from_dataframe.to_excel(FINAL_FILENAME_EXCEL), dropbox_file_path, mode=dropbox.files.WriteMode("overwrite"))
        return meta

    except Exception as e:
        print('Error uploading file to Dropbox: ' + str(e))

if __name__ == "__main__":
        local_path = ""
        local_file = ""
        dropbox_file_path = ""
        file_from_dataframe= ""


        # dropbox_manager.dropbox_upload_file(local_path, local_file, dropbox_file_path, file_from_dataframe, FINAL_FILENAME_EXCEL)