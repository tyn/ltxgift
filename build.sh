set -e

jobname=quiz

uplatex "$jobname".tex
python gift-pack.py "$jobname".pregift > "$jobname".gift
dvipdfmx "$jobname"

uplatex -jobname="$jobname"-ans '\def\giftshowanswers{}\input{'"$jobname"'.tex}'
dvipdfmx "$jobname"-ans
