1. crawl.sh (if needed to download new simfiles)
2. copy all the simfile directories to the 'simfiles' dir
3. run './card-render.py | sort > practice-cards.txt'
4. for RATING in `seq 10 19`; do (grep -e "^${RATING}" practice-cards.txt > _raw-practice-cards-$RATING.txt); done
5. for RATING in `seq 10 19`; do cat _raw-practice-cards-$RATING.txt | cut -d ' ' -f 2- > practice-cards-$RATING.txt; done
6. profit?
