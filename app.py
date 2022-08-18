from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/latvia')
def latvia():
    return render_template('latvia.html')

@app.route('/latvia/viscentr')       
def latvia_visacent():
    return render_template('latvia_viscentr.html')

@app.route('/latvia/embassy')       
def latvia_embassy():
    return render_template('latvia_embassy.html')


@app.route('/norway')
def norway():
    return render_template('norway.html') 


@app.route('/poland')
def poland():
    return render_template('poland.html') 


@app.route('/lithuania')
def lithuania():
    return render_template('lithuania.html') 


@app.route('/thailand')
def thailand():
    return render_template('thailand.html') 

@app.route('/spain')
def spain():
    return render_template('spain.html') 


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    # app.run(host="0.0.0.0", port=5000, debug=True)
