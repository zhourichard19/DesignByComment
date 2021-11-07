def mostHits(webDict):
    websites = []
    if len(webDict) > 3:
        for x in range(3):
            maxKey = max(webDict,key=webDict.get)
            websites.append(maxKey)
            del webDict[maxKey]
    else:
        for y in webDict:
            websites.append(y)
    print(websites)
    return websites
