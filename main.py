from flask import Flask, render_template,request,jsonify
import requests
from repositories.diaryRepository import DiaryRepo
from helper.EmotionDetection import predict_emotion
import datetime
#from helper.FileWriter import FileWriter
'''
pip install requests
pip install flask
pip install tensorflow
pip install numpy 
pip install transformers
pip install text2emotion
'''

EMOJI_MAP = {
    "Happy": "😊",
    "Sad": "😢",
    "Angry": "😡",
    "Fear": "😨",
    "Surprise": "🤯",
    "Calm": "😌",
    "Excited": "🤩"
}

app = Flask(__name__)

@app.route('/signin')
def getSignin():
    return render_template('signin.html')

@app.route('/signup')
def getSingup():
    return render_template('signup.html')

@app.route('/page')
def getHome():
    userid = request.args.get('userid', type=int, default=0)
    if userid!=0:
        return  render_template('mainpage.html',uid=userid)
    else:
        return render_template('home.html')

@app.route('/mainpage')
def getMainpage():
    return render_template('mainpage.html')


@app.route('/save_diary_entry', methods=['POST'])
def save_diary_entry():
    data = request.get_json()
    content = data['content']
    # call here and save

    return {"message": "Diary entry saved successfully!"}, 200



@app.route('/add', methods=['POST'])
def signup():
    data = request.get_json()  # Get the JSON data from the request
    # Simple validation checks
    if not data:
        return jsonify({"error": "All fields are required!"}), 400

    name =data.get('fullName')
    mail= data.get('email')
    paswd=data.get('confirmPassword')

    data=DiaryRepo()
    response=data.create_user(name,mail,paswd)
    if response=="success":
        return jsonify({"success": "Registration succeeded"}), 200
    else:
        return jsonify({"error": "Registration failed"}), 400


@app.route('/login',methods=['POST'])
def login():
    data = request.get_json()  # Get the JSON data from the request
    if not data:
        return jsonify({"error": "All fields are required!"}), 400

    email=data.get('email')
    password=data.get('password')

    # dairy repository
    datarepo = DiaryRepo()
    response,uid = datarepo.verify_user(email,password)
    if response == "success" and uid:
        return jsonify({"success": "Registration succeeded","userid":uid}), 200
    else:
        return jsonify({"error": "Registration failed"}), 400


@app.route('/get',methods=['POST'])
def GetUserData():
    data = request.get_json()
    if not data:
        return jsonify({"error": "All fields are required!"}), 400

    u_id=data.get('Uid')
    datarepo = DiaryRepo()
    response,user_data = datarepo.get_user_details(u_id)

    if response == "success" and len(user_data)>0:
        return jsonify({"success": "Registration succeeded","fname":user_data[0],"mail":user_data[1]}), 200
    else:
        return jsonify({"error": "Registration failed"}), 400


@app.route('/deleteuser',methods=['POST'])
def DeleteAccount():
    data = request.get_json()
    if not data:
        return jsonify({"error": "All fields are required!"}), 400

    u_id = data.get('Uid')
    print("request received ")
    datarepo = DiaryRepo()
    response = datarepo.delete_account(u_id)

    if response == "success":
        return jsonify({"success": "Account deleted"}), 200
    else:
        return jsonify({"error": "Delete failed"}), 400


@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_msg = data.get("message", "")

    bot_reply = chat_with_ai(user_msg)

    return jsonify({"reply": bot_reply})


@app.route('/predict', methods=['POST'])
def predict():
    text = request.json.get("text", "")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    predicted = predict_emotion(text)
    emoji_icon = EMOJI_MAP.get(predicted, "🙂")

    entry = {
        "date": datetime.datetime.now().strftime("%B %d, %Y %I:%M %p"),
        "emotion": predicted,
        "emoji": emoji_icon,
        "preview": text[:100] + "..."
    }
    return jsonify(entry),200


def chat_with_ai(prompt):
    url = "http://localhost:11434/api/generate"

    payload = {
        "model": "llama3.1",
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(url, json=payload)
    result = response.json()
    return result.get("response", "")


@app.route('/updateuser', methods=['POST'])
def UpdateUser():
    data = request.get_json()
    if not data:
        return jsonify({"error": "All fields are required!"}), 400

    u_id = data.get('Uid')
    username = data.get('Username')
    email = data.get('Email')

    if not u_id or not username or not email:
        return jsonify({"error": "All fields are required!"}), 400

    datarepo = DiaryRepo()
    status, affected = datarepo.update_user(u_id, username, email)

    if status == "success":
        return jsonify({"success": "User updated", "rows": affected}), 200
    else:
        return jsonify({"error": "Update failed"}), 400



@app.route('/')
def hello():
    return render_template('home.html')

if __name__ == '__main__':
    #file_writer = FileWriter()
    #file_writer.clear_content()
    app.run(debug=True)
