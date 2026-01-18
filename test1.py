def QuoteExtraction(filename):
    with open(filename, "r", encoding="utf-8") as file:
        text = file.read()


    quotes = []
    names = []


    desc = {
        "said", "says", "asked", "added", "remarked", "replied",
        "answered", "whispered", "mumbled", "muttered",
        "shouted", "yelled", "screamed"
    }


    i = 0
    n = len(text)


    while i < n:
        if text[i] == '"':
            start = i + 1
            end = start


            while end < n and text[end] != '"':
                end += 1


            quote = text[start:end].strip()


            before = text[max(0, i - 80):i]
            after = text[end + 1:min(n, end + 80)]


            speaker = None


            # Speaker BEFORE quote
            before_words = before.split()
            for j in range(len(before_words) - 1):
                if (
                    before_words[j][0].isupper()
                    and before_words[j + 1].lower().strip(".,") in desc
                ):
                    speaker = before_words[j]
                    break


            # Speaker AFTER quote
            if speaker is None:
                after_words = after.split()
                for j in range(len(after_words) - 1):
                    if (
                        after_words[j].lower().strip(".,") in desc
                        and after_words[j + 1][0].isupper()
                    ):
                        speaker = after_words[j + 1]
                        break


            if speaker is None:
                speaker = "Narrator"


            quotes.append((speaker, quote))


            if speaker not in names:
                names.append(speaker)


            i = end + 1
        else:
            i += 1


    return quotes, names


