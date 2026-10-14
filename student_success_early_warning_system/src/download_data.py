"""Download the official UCI Student Performance Mathematics dataset."""
import io
import zipfile
from urllib.request import urlopen
from data_preprocessing import DATA_PATH, load_dataset
UCI_ARCHIVE_URL = "https://archive.ics.uci.edu/static/public/320/student+performance.zip"
def download_dataset(destination=DATA_PATH):
    destination.parent.mkdir(parents=True, exist_ok=True)
    with urlopen(UCI_ARCHIVE_URL, timeout=60) as response: outer_payload = response.read()
    with zipfile.ZipFile(io.BytesIO(outer_payload)) as outer:
        nested = next(item for item in outer.namelist() if item.endswith("student.zip"))
        with outer.open(nested) as source: inner_payload = source.read()
    with zipfile.ZipFile(io.BytesIO(inner_payload)) as archive:
        name = next(item for item in archive.namelist() if item.endswith("student-mat.csv"))
        with archive.open(name) as source, open(destination, "wb") as target: target.write(source.read())
    load_dataset(destination); return destination
if __name__ == "__main__": print(f"Downloaded UCI Mathematics dataset to {download_dataset()}")
