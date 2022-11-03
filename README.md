1. `pip install "simfile>=2.0.0"`
2. crawl.sh (if needed to download new simfiles)
3. copy all the simfile directories to the 'simfiles' dir
4. run './card-render.py | sort > practice-cards.txt'
5. for RATING in `seq 10 19`; do (grep -e "^${RATING}" practice-cards.txt > _raw-practice-cards-$RATING.txt); done
6. for RATING in `seq 10 19`; do cat _raw-practice-cards-$RATING.txt | cut -d ' ' -f 2- > practice-cards-$RATING.txt; done
7. profit?
