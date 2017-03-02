for ext in aux dvi log nav out snm pregift gift toc vrb pdf
do
  for f in quiz quiz-ans
  do
    rm -f "$f"."$ext"
  done
done
