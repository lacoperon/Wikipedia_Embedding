import os
import ray
from pathlib import Path
from lxml import html
import re
from urllib.parse import unquote
import fcntl
import random
import shutil
import sys
import glob


def writeLinksToFile(article_results):
    rand_bits = random.getrandbits(100)
    f = open('./link_output/link_file_{}.dat'.format(rand_bits), 'w')
    for article in article_results:
        title = article[0]
        f.write(">>>>{}\n".format(title))
        links = article[1]
        for link in links:
            f.write(link+"\n")

def cleanupLinkfiles(filename):
    outfilename = "./link_files/{}_links.dat".format(filename)
    with open(outfilename, 'wb') as outfile:
        for filename in glob.glob('./link_output/*.dat'):
            with open(filename, 'rb') as readfile:
                shutil.copyfileobj(readfile, outfile)


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

    # Each wiki_ file output by WikiExtractor can contain multiple articles
    # This code splits each file into its constitutent articles
    splitter = "<doc"
    doc_list = [splitter + doc for doc in contents.split(splitter)]
    doc_list = list(filter(lambda x : x.strip() != "<doc", doc_list))

    article_results = []

    # For each document in the doc_list associated with each file,
    # we scrape the article title and all links contained therein
    for doc in doc_list:
        # Opens HTML representation of file contents in lxml
        tree = html.fromstring(doc)
        # Gets title associated with the particular article
        title = tree.xpath('//doc/@title')[0]

        # Gets all links within the article
        links = tree.xpath("//a/@href")

        # Decodes special characters (ie from Poincar%C3%A9 to correct format)
        links = [unquote(link) for link in links]

        # Filters out links not internal to Wikipedia
        links = list(filter(lambda x: not re.match("https?:\/\/", x), links))

        article_results.append([title, links])

    writeLinksToFile(article_results)


if __name__ == "__main__":
    ray.init()
# Gets all subdirectories, and all files within those subdirectories,
# using os.walk
    filename = sys.argv[1]
    filename = re.sub(".*\/", "", filename)
    html_dir_list = list(os.walk("./html_extract"))[1:]
    for subdir_tuple in html_dir_list:
        dir_path = subdir_tuple[0] # the path to the subdirectory for dir_tuple
        assert len(subdir_tuple[1]) == 0 # there should exist no subdirectories
        file_list = subdir_tuple[2]
        article_results = [dir_path + "/" + filename for filename in file_list]
        article_results = [parseWikidumpFile.remote(x) for x in article_results]
        results = ray.get(article_results)
    cleanupLinkfiles(filename)
