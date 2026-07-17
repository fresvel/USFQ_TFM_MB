#! /bin/bash
set -euo pipefail

IMAGE="usfq-tex"
BUILD_DIR="build"
OUT_DIR="out"

if ! docker image inspect "$IMAGE" >/dev/null 2>&1 || [ "${BUILD_IMAGE:-0}" = "1" ]; then
  docker build -t "$IMAGE" -f docker/Dockerfile docker
fi

mkdir -p "$BUILD_DIR" "$OUT_DIR"
rm -f "$BUILD_DIR"/main.{aux,bbl,blg,loa,lof,log,lot,out,toc}

# Directorio de trabajo fuera del árbol sincronizado por Insync. Al compilar
# dentro de la carpeta de OneDrive, Insync sincroniza los auxiliares mientras
# xelatex los escribe y a veces los trunca: si main.aux pierde \bibdata y
# \bibstyle, bibtex no encuentra las citas y todas salen "undefined". Aquí solo
# se copian los archivos ya terminados.
SCRATCH="$(mktemp -d "${TMPDIR:-/tmp}/usfq-tex-XXXXXX")"
trap 'rm -rf "$SCRATCH"' EXIT

docker run --rm -e TZ=America/Guayaquil -u "$(id -u)":"$(id -g)" \
  -v "$(pwd)":/workdir -v "$SCRATCH":/workdir/"$BUILD_DIR" -w /workdir "$IMAGE" \
  bash -lc "xelatex -interaction=nonstopmode -halt-on-error -output-directory=$BUILD_DIR main.tex && \
  bibtex $BUILD_DIR/main && \
  xelatex -interaction=nonstopmode -halt-on-error -output-directory=$BUILD_DIR main.tex && \
  xelatex -interaction=nonstopmode -halt-on-error -output-directory=$BUILD_DIR main.tex && \
  xelatex -interaction=nonstopmode -halt-on-error -output-directory=$BUILD_DIR main.tex"

cp "$SCRATCH"/main.* "$BUILD_DIR"/
cp "$BUILD_DIR/main.pdf" "$OUT_DIR/main.pdf"
gs -o "$OUT_DIR/report.pdf" -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 "$OUT_DIR/main.pdf"
