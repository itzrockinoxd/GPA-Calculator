from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Flask! 🎉 Your GPA project is starting!"

if __name__ == '__main__':
    app.run(debug=True)
