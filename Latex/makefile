BUILD_DIR = build
OUT_DIR = out

.PHONY: all clean report

all:
	./make.sh

report: all

clean:
	@rm -rf $(BUILD_DIR) $(OUT_DIR)
	@rm -f *.bbl *.blg *.dvi *~ *.ps *.aux *.log *.pdf *.bak *.toc *.lof *.lot *.out *.fls *.fdb_latexmk *.run.xml
