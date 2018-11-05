from flask import Flask, jsonify, render_template, request, redirect
from config import Config
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, BooleanField, SubmitField
from wtforms.validators import DataRequired


# from yourmodule import function_that_return_xml
import requests
import json
import urllib
app = Flask(__name__)
app.config.from_object(Config)

class MyForm(FlaskForm):
    Gender = SelectField('Gender', choices=[('M', 'Male'), ('F','Female')], validators=[DataRequired()])
    IsReshare = BooleanField('Is Reshare', validators=[DataRequired()])
    RetweetCount = IntegerField('RetweetCount', validators=[DataRequired()])
    Klout = IntegerField('Klout', validators=[DataRequired()])
    Sentiment = IntegerField('Sentiment', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = MyForm()
    if form.validate_on_submit():
        data = {

            "Inputs": {

            "input1": {
                "ColumnNames": ["Gender", "IsReshare", "RetweetCount", "Klout", "Sentiment"],
                "Values": [
                [form.Gender.data, form.IsReshare.data, form.RetweetCount.data, form.Klout.data, form.Sentiment.data],
                [form.Gender.data, form.IsReshare.data, form.RetweetCount.data, form.Klout.data, form.Sentiment.data]
                ]
            },
            },
            "GlobalParameters": {}
        }

        body = str.encode(json.dumps(data))

        url = 'https://ussouthcentral.services.azureml.net/workspaces/049d240c5a8945c4a3cfccf74adeb683/services/e659a95cbb5d40129835133c3f6f02a2/execute?api-version=2.0&details=true'
        api_key = '6kTsCBmeCNMT/dOUfmUJumJqlBOKD1JkqbMlEAHgNxLUfXbOtE8HFoQIsthPZXO04dnPzQ03ooLwU/IYSKzhwA==' # Replace this with the API key for the web service
        headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

        req = urllib.request.Request(url, body, headers) 

        try:
            response = urllib.request.urlopen(req)
            # If you are using Python 3+, replace urllib with urllib.request in the above code:
            # req = urllib.request.Request(url, body, headers) 
            # response = urllib.request.urlopen(req)

            result = json.loads(response.read().decode('utf-8'))
            print(result)
            # return render_template('test.html', movies=json.loads(result))
            return render_template('index.html',result=result)
        except urllib.error.HTTPError as error:
            print("The request failed with status code: " + str(error.code))

            # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
            print(error.info())

            print(json.loads(error.read()))      
    return render_template('index.html', form=form)

@app.route('/result')
def result():
    result = request.args['result']
    return render_template('result.html', result=result)
# @app.route("/")
# def hello():
#     # xml = function_that_return_xml()
#     # make fancy operations if you want
#     return 'hello'

if __name__ == "__main__":
    app.run()




@app.route('/test')
def test():
    # r = request.get('http://www.google.com')
    # params = {
    # 'api_key': '{API_KEY}',
    # }
    # r = requests.get(
    #     'https://www.parsehub.com/api/v2/projects/{PROJECT_TOKEN}/last_ready_run/data',
    #     params=params)
    # return render_template('movies.html', movies=json.loads(r.text)['movies'])
    data = {

        "Inputs": {

        "input1": {
            "ColumnNames": ["Gender", "IsReshare", "RetweetCount", "Klout", "Sentiment"],
            "Values": [
            ["value", "0", "0", "0", "0"],
            ['value', '0', '0', '0', '0']
            ]
        },
        },
        "GlobalParameters": {}
    }

    body = str.encode(json.dumps(data))

    url = 'https://ussouthcentral.services.azureml.net/workspaces/049d240c5a8945c4a3cfccf74adeb683/services/e659a95cbb5d40129835133c3f6f02a2/execute?api-version=2.0&details=true'
    api_key = '6kTsCBmeCNMT/dOUfmUJumJqlBOKD1JkqbMlEAHgNxLUfXbOtE8HFoQIsthPZXO04dnPzQ03ooLwU/IYSKzhwA==' # Replace this with the API key for the web service
    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

    req = urllib.request.Request(url, body, headers) 

    try:
        response = urllib.request.urlopen(req)
        # If you are using Python 3+, replace urllib with urllib.request in the above code:
        # req = urllib.request.Request(url, body, headers) 
        # response = urllib.request.urlopen(req)

        result = response.read().decode('utf-8')
        print(result)
        # return render_template('test.html', movies=json.loads(result))
        return jsonify(result=result)
    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))

        # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        print(error.info())

        print(json.loads(error.read()))          
