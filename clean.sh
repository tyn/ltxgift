for ext in aux dvi log nav out snm pregift gift toc vrb pdf
do
  for f in quiz sample1
  do
    rm -f "$f"."$ext"
    rm -f "$f"-ans."$ext"
  done
done
