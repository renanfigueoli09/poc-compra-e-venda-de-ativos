cov="$(coverage report | grep -i --color -e "total" | awk '{print $6}' | tr -d '\n')"
text="1c\![check-coverage](https://img.shields.io/badge/Coverage-${cov}25-orange)"
sed -i $text ./README.md