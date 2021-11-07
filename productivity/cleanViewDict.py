def editViewTimes(viewDict):
    for key in viewDict:
        if key == " ":
            del viewDict[key]
    return viewDict