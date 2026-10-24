#!/bin/sh
set -e

mkdir -p /config/calibre-library /config/cwa-book-ingest

for pair in "/calibre-library:/config/calibre-library" "/cwa-book-ingest:/config/cwa-book-ingest"; do
  link="${pair%%:*}"
  target="${pair#*:}"

  # Zaten link ise (yeniden başlatma) dokunma
  [ -L "$link" ] && continue

  # Ayrı bir mount olarak bağlanmışsa olduğu gibi bırak
  if mountpoint -q "$link" 2>/dev/null; then
    echo "[railway] $link ayrı bir mount, link kurulmadı"
    continue
  fi

  # İmajdan gelen içerik varsa volume'a taşı (var olanın üstüne yazmadan), sonra linkle değiştir
  if [ -d "$link" ]; then
    cp -an "$link"/. "$target"/ 2>/dev/null || true
    rm -rf "$link"
  fi
  ln -s "$target" "$link"
  echo "[railway] $link -> $target"
done

exec /init "$@"
