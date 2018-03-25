for file in ./input_wikidump/*.bz2
do
  echo "Running script for $file"
  echo "Running Wikipedia extractor... (will take 5-10 min)";
  python WikiExtractor.py -o ./html_extract -q --templates template.txt --html "$file" > log/wiki.log 2>log/wiki_err.log;
  rm "$file";
  echo "Running Link Extractor...";
  python extract_links.py "$file" > log/extractLinks.log 2> log/extractLinks_err.log;
  rm -rf ./link_output/*.dat;
  rm -rf ./html_extract/*/;
done
