Step one is opening up the collab, setting it to the right repo and generating files.

1. Open "Alpha60 2026 H1 data analysis" notebook
https://colab.research.google.com/github/alpha60-devops/alpha60-results-star-wars-universe/blob/main/analysis/notebooks/explore-2026h1.ipynb

2. Run through "Setup" cells, some of which require interaction

 login
- github user is: alpha60devops
- shared key: (xxx)

 Setup.reponame set it to the github repo you're working on.

 3. Compare week JSON
   just to 5/15 html generation

4. Compare Cumulative JSON
 - hit allow to download generated files

5. Move notebook-generated files into github repo's bin directory
aapi-led-geo-slices-africa.tbody.html
aapi-led-geo-slices-asia.tbody.html
aapi-led-geo-slices-usa-weeks-1-5-10-20.tbody.html

7. Update binaries
a60-meta-collection.exe
a60-meta-collection.wasm

8. Run generation script while in bin
../scripts/generate-graphs.sh

9. Move generated output files into _includes/
mv *.html *.svg ../_includes/

10. Renenerate list of media objects
	../scripts/listify-collection-key-in-cumulative-json.sh
	
	then edit into
	
	../_include/aapi-media-objects-list.html

10. Update links, if needed, in doc/*.md files
