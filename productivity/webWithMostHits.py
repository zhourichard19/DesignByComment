def mostHits(webDict):
    websites = []
    temp = webDict
    if len(webDict) > 3:
        for x in range(3):
            maxKey = max(temp,key=temp.get)
            websites.append(maxKey)
            del temp[maxKey]
    else:
        for y in temp:
            websites.append(y)
    print(websites)
    return websites
