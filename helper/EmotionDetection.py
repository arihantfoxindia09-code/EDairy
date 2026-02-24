import text2emotion as te



def predict_emotion(text):
    result = te.get_emotion(text)  # returns dict like: {'Happy':0.17,'Sad':0.42...}

    # get emotion with highest value
    emotion = max(result, key=result.get)

    return emotion
