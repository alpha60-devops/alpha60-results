# Information Genesis

Workflow for creating a GitHub Pages site from a empty git repository.

## Define Partition

## Create Repository

1. [alpha60-devops](https://github.com/alpha60-devops)
2. use "alpha60-results-" prefix for naming
3. Set to "public" visibility and use GitHub Pages
   a. built from GitHub Actions
   b. Jekyll
   c. should have .github/workflows when done
4. Copy in configure files from KGR (Known Good Repository).
   a. _config.yml
   b. cp -r _layouts
   c. mkdir _includes resources
   d. cp index.md, adjust text for slice name
   e. mkdir docs, cp in slice.md
   f. mkdir data, cp in data files

## Notebook-based analysis and data table generation

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

## WASM-based graph and table generation
1. Update binaries
a60-meta-collection.exe
a60-meta-collection.wasm

2. Run generation script while in bin
../scripts/generate-graphs.sh

3. Move generated output files into _includes/
mv *.html *.svg ../_includes/

4. Renenerate list of media objects
	../scripts/listify-collection-key-in-cumulative-json.sh

	then edit into

	../_include/aapi-media-objects-list.html

5. Update links, if needed, in doc/*.md files
