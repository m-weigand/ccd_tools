Homepage for the Cole-Cole decomposition tools
----------------------------------------------

Updating the documentation
--------------------------

on the master branch, build the html documentation
::

	git checkout gh-pages
	rm -r doc_ccd/
	mv docs/doc/_build/html/ doc_ccd
	git add doc_ccd/
	git commit -m "update documentation"
	git checkout master

