## Document Summarisation bot for Falcon Academy

## What is `fas_rst`

FAS is the shorthand for Falcon Academy of Sciences and RST stands for Research paper Summarisation Tool , written in pure python leveraging the `spacy` library

## How to run

Paste the commands below to your terminal

```bash
git clone https://github.com/pacifio/fas_rst
cd fas_rst
pip install -r requirements.txt
python3 main.py mypdf.pdf
```

Please note that the `main.py` takes one argument which is the filename , replace `mypdf.pdf` with your filename , the text extracted from your pdf will be saved to `original.txt` and the summmary will be saved to `summary.txt`

## Further plans

- [ ] Use `BART` NLP model
- [ ] Better replacement for the `tika` library cause it's dependent on JAVA
- [ ] More arguments to the script to accept generic text files , can be used for any sort of textual summarization

> version 0.0.1
