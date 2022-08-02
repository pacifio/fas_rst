from text_sum import summarize
from demos import demo3


def main() -> None:
    text = demo3
    r = summarize(text)
    print(len(text))
    print(len(r))
    print(r)


if __name__ == "__main__":
    main()
