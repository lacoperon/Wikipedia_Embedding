import os
import ray
from pathlib import Path
from lxml import html

@ray.remote
def parseWikidumpFile(file_path):
    contents = Path(file_path).read_text()
    print(contents)

if __name__ == "__main__":
    ray.init()
# Gets all subdirectories, and all files within those subdirectories,
# using os.walk
    html_dir_list = list(os.walk("./html_extract"))[1:]
    for subdir_tuple in html_dir_list:
        html_dir_path = subdir_tuple[0] # the path to the subdirectory for dir_tuple
        assert len(subdir_tuple[1]) == 0 # there should exist no subdirectories
        file_list = subdir_tuple[2]
        ray.get(parseWikidumpFile.remote(html_dir_path + "/" + file_list[0]))
