def QuoteExtraction(Filename):
    with open(Filename, 'r') as file:
        text = file.read()

    quotes = []  
    names = []

    i = 0
    n = len(text)

    desc = [
        "said","says","asked","added","remarked","replied",
        "answered","whispered","mumbled","muttered",
        "shouted","yelled","screamed"
    ]

    while i < n:
        if text[i] == '"':
            start = i + 1
            end = start
            while end < n and text[end] != '"':
                end += 1

            quote = text[start:end]

            before = text[max(0, i - 50):i]
            after = text[end + 1:min(n, end + 50)]

            speaker = None

            before_words = before.split()
            for j in range(len(before_words) - 1):
                if before_words[j][0].isupper() and before_words[j + 1] in desc:
                    speaker = before_words[j]
                    break

            if speaker is None:
                after_words = after.split()
                for j in range(len(after_words) - 1):
                    if after_words[j] in desc and after_words[j + 1][0].isupper():
                        speaker = after_words[j + 1]
                        break

            if speaker is None:
                speaker = "Narrator"

            quotes.append((speaker, quote))

            if speaker != "Narrator" and speaker not in names:
                names.append(speaker)

            i = end + 1
        else:
            i += 1

    return quotes, names