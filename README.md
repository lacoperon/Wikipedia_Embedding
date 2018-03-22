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

If you want to construct files representing the adjacency list representation of the network from [Wikipedia datadumps obtained from the Internet Archive](https://archive.org/search.php?query=subject%3A"enwiki" AND subject%3A"data dumps" AND collection%3A"wikimediadownloads"&and[]=subject%3A"Wikipedia"),, place your datadump files (`.bz2` compressed format) into the `./input_wikidump/`.

Then, run `sh extractHTML.sh` to obtain the adjacency list files associated with each `.bz2` file. They will be output to `./link_files/`.

## Future Directions

At some point in time (ideally before this project is due), I will do something with the network generated from the whole of Wikipedia. At some point...
