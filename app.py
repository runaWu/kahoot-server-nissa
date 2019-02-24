from flask import Flask , request , json , jsonify
import requests
import os
from random import randint
app = Flask(__name__)

historyUser = []

#bikin quizbaru
@app.route('/quiz', methods=['POST'])
def createQuiz():
    body = json.dumps(request.json) 

    quizzesData = {
        "totalQuizAvailable":0,
        "quizzes":[]
    }
    
    if os.path.exists('./quizzes-file.json'): #kalo file ada di quizzes file
        quizzesFile = open('./quizzes-file.json','r') #baca filenya
        print("file ada")
        quizzesData = json.load(quizzesFile) 
    else:
        quizzesFile = open('./quizzes-file.json','x')#tulis

    quizzesData["totalQuizAvailable"] +=1

    quizzesFile = open('./quizzes-file.json','w')
    quizzesData["quizzes"].append(body) 
    quizzesFile.write(str(json.dumps(quizzesData)))

    return str(quizzesData)
       
  

#bikin soalnya

@app.route('/question', methods=['POST'])#bisa nerima dari insom dl(body)l
def createQuestion():
    # loads = dari string ke json
    # dumps = dari singlequotes ke doublequotes
    body = json.dumps(request.json) #dict dengan petik 1 

    questionData = {
        "questions":[] #array of question
    }
    
    if os.path.exists('./question-file.json'):
        questionFile = open('./question-file.json','r')#kalo ada dibaca pakai r
        print("file ada")
        questionData = json.load(questionFile) #itu load kalo dari file, pokoknya yg ga ada s nya hub sm file jadiin json masukin question data
    else:
        questionFile = open('./question-file.json','x')#x bikin file baru
        print("file tidak ada")

    questionFile = open('./question-file.json','w') #nulis file karrena d kondisi if else g bs nulis
    questionData["questions"].append(body) #lien 11 , kalo blm if else kan ksoong, yg dari insomnia dimasukin ke array bodynya
    questionFile.write(str(json.dumps(questionData))) #ngesave data yg udah diperbarui, dumps biar petiknya 2 karena json bisanya petik 2

    return str(questionData)

#minta kuis dan
#apa aja si kuisnya? gabungkan(merge) quiz dan question
@app.route('/quizzes/<quizId>')
def getQuiz(quizId):
    # nyari quiz
    quizzesFile = open('./quizzes-file.json')
    quizzesData = json.load(quizzesFile)

    for quiz in quizzesData["quizzes"]:
        quiz = json.loads(quiz)
        if quiz["quiz-id"] == int(quizId):
            quizData = quiz
            break
    
    # nyari soal
    questionFile = open('./question-file.json')
    questionData = json.load(questionFile)       

    for question in questionData["questions"]:
        question = json.loads(question)
        if question["quiz-id"] == int(quizId):
            quizData['question-list'].append(question)
    
    return jsonify(quizData)    

#minta data sebuah soal
@app.route('/quizzes/<quizId>/questions/<questionNumber>')
def getThatQuestion(quizId, questionNumber):
    quizData = getQuiz(int(quizId)).json #kita punya get quiz yg punya quiz id lalu dijadiin json masuk ke var quizdata

    for question in quizData["question-list"]:
        if question["question-number"] == int(questionNumber):
            return jsonify(question)

@app.route('/game/join',methods=["POST"])
def joinGame():
    #masukin orang itu ke data game
    body = request.json
    #open game data info
    gamesFile = open('./games-file.json')
    gamesData = json.load(gamesFile)

    position = 0
    for i in range(len(gamesData["game-list"])):
        game =gamesData["game-list"][i]

        if game["game-pin"] == int(body["game-pin"]):
            if body["username"] not in game["user-list"]:
                game["user-list"].append(body["username"])
                game["leaderboard"].append({
                    "username":body["username"],
                    "score":0
                })
                gameInfo = game
                position = i
                break

    with open('./games-file.json','w') as gamesFile:
        gamesData["game-list"][position]=(gameInfo) #user list dganti sm game info
        gamesFile.write(str(json.dumps(gamesData))) 

    return jsonify(request.json)

@app.route('/game/leaderboard',methods=["POST"])
def getLeaderboard():
    body = request.json
    #open game data info
    gamesFile = open('./games-file.json')
    gamesData = json.load(gamesFile)
    for game in gamesData["game-list"]:
        if game["game-pin"] == body["game-pin"]:
            varLeaderboard = game["leaderboard"]

    position = 0
    for i in range(len(varLeaderboard)):
        posisi=varLeaderboard[i]
        smallest = varLeaderboard[i]["score"] 
        for j in range(i,len(varLeaderboard)):
            if varLeaderboard[j]["score"] >= smallest:
                smallest = varLeaderboard[j]["score"]
                position = j
                posisi = varLeaderboard[j]

        varLeaderboard[i] , varLeaderboard[position] = posisi , varLeaderboard[i] 
    return jsonify(varLeaderboard)     



@app.route('/registration', methods=['POST'])
def createRegistration():
    body = request.json 

    if body["pass-condition"] == "encrypt":
        body["password"] = encrypt(body["password"])
    elif body["pass-condition"] == "decrypt":
        body["password"] = decrypt(body["password"])

    registrationData = {
        "registrations": []
    }
    
    if os.path.exists('./registration-file.json'):
        registrationFile = open('./registration-file.json','r')#kalo ada dibaca pakai r
        print("sudah ada data register")
        registrationData = json.load(registrationFile) 
    else:
        registrationFile = open('./registration-file.json','x')

    registrationFile = open('./registration-file.json','w') 
    registrationData["registrations"].append(body) 
    registrationFile.write(str(json.dumps(registrationData))) 

    return jsonify(registrationData)

def encrypt(string1):
    alphabet=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","0","1","2","3","4","5","6","7","8","9"]
    encryptStr=""
    strMove=1
    for i in range(len(string1)):
        tempString = alphabet.index(string1[i])+strMove
        encryptStr = encryptStr + alphabet[tempString % 36]
    return(encryptStr)  

def decrypt(string1):
    alphabet=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","0","1","2","3","4","5","6","7","8","9"]
    decryptStr=""
    strMove=1
    for i in range(len(string1)):
        tempString = alphabet.index(string1[i])-strMove
        decryptStr = decryptStr + alphabet[tempString % 36]
    return(decryptStr)

@app.route('/login', methods=["POST"])
def login():
    body = request.json 

    status = False

    registrationFile = open('./registration-file.json')
    registrationData = json.load(registrationFile)

    for register in registrationData["registrations"]:
        if body["pass-condition"] == "decrypt":
        # register = json.loads(register)
            if register["username"] == body["username"] and decrypt(register["password"]) == body["password"]:
                status = True
            else:
                status = False
    return str(status)            
        

@app.route('/deletequestion/<quizId>/questions/<questionNumber>')
def deleteThatQuestion(quizId, questionNumber):
    tobeDeleted = getThatQuestion(quizId, questionNumber)

    for question in quizData["question-list"]:
        if getThatQuestion(quizId) == int(body[""quiz-id""]):
            apusin lah bang gatau dedek cara ngehapusnya


@app.route('/answer', methods = ['POST'])
def submitAnswer():
    isTrue = False
    body = request.json

    questionFile = open('./question-file.json')
    questionData = json.load(questionFile)

    for question in questionData["questions"] :
        question = json.loads(question)
        
        if question["quiz-id"] == int(body["quiz-id"]) and question["question-number"] == int(body["question-number"]):
            if question["answer"] == body["answer"]:
                isTrue = True
    
    #kalo jawaban bener nambah 100
    gamesFile = open('./games-file.json')
    gamesData = json.load(gamesFile)

    gamesPosition = 0
    for i in range(len(gamesData["game-list"])):
        game = gamesData["game-list"][i]

        if game["game-pin"] == int(body["game-pin"]):
            if isTrue:
                userPosition = 0
                for j in range(len(game["leaderboard"])):
                    userData = game["leaderboard"][j]

                    if userData["username"] == body["username"]:
                        userData["score"] +=100

                        userInfo = userData
                        userPosition = j

                game["leaderboard"][userPosition] = userInfo
                gameInfo = game
                gamesPosition = i
                break

    with open('./games-file.json','w') as gamesFile:
        gamesData["game-list"][gamesPosition] = gameInfo #user list dganti sm game info
        gamesFile.write(str(json.dumps(gamesData))) 

    return jsonify(request.json)                              
        
    

@app.route('/game',methods=["POST"])
def createGame():
    #dapatkan info kuis
    body=request.json

    quizzesFile = open('./quizzes-file.json')
    quizzesData = json.load(quizzesFile)

    for quiz in quizzesData["quizzes"]:
        quiz = json.loads(quiz)

        if quiz["quiz-id"] == int(body["quiz-id"]):
            gameInfo = quiz

    gameInfo["game-pin"] = randint(100000,999999)
    gameInfo["user-list"] =[]
    gameInfo["leaderboard"]=[]


    gamesData ={
        "game-list":[]
    }
    #simpan data game
    if os.path.exists('./games-file.json'):
        gamesFile = open('./games-file.json','r')
        gamesData = json.load(gamesFile)
    else:    
        gamesFile = open('./games-file.json','x')


    with open ('./games-file.json','w') as gamesFile:
        gamesData["game-list"].append(gameInfo)
        gamesFile.write(str(json.dumps(gamesData)))

    return jsonify(gameInfo)       




   

if __name__ == "__main__" :#biar gausah set FLASK_ENV, kalo gapake ini py app.py
    app.run(debug = True, port = 5000)

