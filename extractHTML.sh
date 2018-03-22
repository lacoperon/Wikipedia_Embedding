for file in ./input_wikidump/*
do
  python WikiExtractor.py -o ./html_extract --html --no-templates "$file"
  rm "$file"
done
