test_result="$(pytest /code | grep -i "passed" | sed 's/=//g')"
encodeurl="$(urlencode.sh $test_result)"
text="2c\![check-tests](https://img.shields.io/badge/Tests-${encodeurl}-orange)"
sed -i $text ./README.md
