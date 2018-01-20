for i in *.flv; do ffmpeg -i "$i" "${i/.flv/.mp3}"; done
