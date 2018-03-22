import os
import ray
from pathlib import Path
from lxml import html
import re
import matplotlib.pyplot as plt
from urllib.parse import unquote

@ray.remote
def parseWikidumpFile(file_path):
    # Reads text from wikidump file
    contents = Path(file_path).read_text()

    # Substitutes necessary characters to correctly deal with Wiki Links
    contents = re.sub("&lt;", "<", contents)
    contents = re.sub("&gt;", ">", contents)
    contents = re.sub("%20", " ", contents)
    contents = re.sub("%28", "(", contents)
    contents = re.sub("%29", ")", contents)
    contents = re.sub("%2C", ",", contents)

    splitter = "<doc"
    doc_list = [splitter + doc for doc in contents.split(splitter)]
    doc_list = list(filter(lambda x : x.strip() != "<doc", doc_list))
    link_num = []
    for doc in doc_list:
        # Opens HTML representation of file contents in lxml
        tree = html.fromstring(doc)
        # Gets id numbers associated with each article in the file
        titles = tree.xpath('//doc/@title')

        links = tree.xpath("//a/@href")
        links = list(filter(lambda x: not re.match("https?://", x), links))
        links = [unquote(link) for link in links]
        link_num.append(len(links))

    # Seems to have a power law distribution, we'll see
    print("{} links for {} docs for average degree of {}".format(sum(link_num), len(link_num), sum(link_num)/len(link_num)))
    # plt.hist(link_num)
    # plt.show()
    return (sum(link_num) / len(link_num))

@ray.remote
def parseWikidumpDir(dir_path):
    pass

if __name__ == "__main__":
    ray.init()
# Gets all subdirectories, and all files within those subdirectories,
# using os.walk
    html_dir_list = list(os.walk("./html_extract"))[1:]
    for subdir_tuple in html_dir_list:
        dir_path = subdir_tuple[0] # the path to the subdirectory for dir_tuple
        assert len(subdir_tuple[1]) == 0 # there should exist no subdirectories
        file_list = subdir_tuple[2]
        article_results = [dir_path + "/" + filename for filename in file_list]
        article_results = [parseWikidumpFile.remote(x) for x in article_results]
        results = ray.get(article_results)
        print("Overall average degree is {}".format(sum(results) / len(results)))
