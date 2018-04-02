# Wikipedia Link Extractor

Constructing the complete Wikipedia article link network from Internet Archive datadump.

## What is this project?

This project contains a self-contained implementation that constructs a directed Wikipedia article-link network, in which articles themselves are nodes, and edges represent links from one article to another article.

Once this network is constructed, I plan to do some data analysis on it, and then attempt to embed it using some algorithm (perhaps Hyperbolic Embedding, perhaps some simpler embedding, or something).

## Setup

To install the Python dependencies, run
`pip3 install -r requirements.txt`.

The `extractHTML.sh` script itself is written in BASH, so you should have access to a UNIX-based Terminal to run this project.

## Running the Linkfile Constructor

If you want to construct files representing the adjacency list representation of the network from [Wikipedia datadumps obtained from the Internet Archive](https://archive.org/search.php?query=subject%3A%22enwiki%22%20AND%20subject%3A%22data%20dumps%22%20AND%20collection%3A%22wikimediadownloads%22&and[]=subject%3A%22Wikipedia%22),, place your datadump files (`.bz2` compressed format) into the `./input_wikidump/`.

Then, run `sh extractHTML.sh` to obtain the adjacency list files associated with each `.bz2` file. They will be output to `./link_files/`.

## Analysis of the Wikipedia Network

Find my extensive (and still incomplete) analysis of the Wikipedia network within [this Jupyter Notebook](./data_analysis.ipynb). The analysis includes visualizations of the most linked-to articles, subsets of the articles with the most outgoing links, as well as an interesting visualization of Wikipedian interest in each year from 1700 to 2018.

## Future Directions

I want to embed this network to allow for a highly efficient methodology for playing the [Wikipedia Game](https://en.wikipedia.org/wiki/Wikipedia:Wiki_Game). 

Additionally, I am currently in the process of developing a D3.js visualization of these results, allowing easy interpretation of any arbitrary article within the network, interacting with the articles it links to (and is linked from).
