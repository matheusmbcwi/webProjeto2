from flask import Flask, render_template, request
import requests
import json
import base64

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('login.html', erro=False)

@app.route('/lista', methods=['post'])
def lista_animes():  # put application's code here

    lista = {}
    dados = requests.get('https://animechan.vercel.app/api/available/anime').json()

    for i in range(len(dados)):
        lista[i] = dados[i]

    dici = {'BRUNO':['ADMIN','123'],
            'LAURO':['USUARIO','123'],
            'MATHEUS':['SUPORTE', '123']}
    usuario = request.form.get('username')
    senha = request.form.get('password')
    validacao = dici.get(usuario,['ERRO','AUTH'])

    if validacao[1]==senha:
        return render_template('Lista.html', dados=[usuario, validacao[0]], lista=lista)
    else:
        return render_template('login.html', erro=True)



@app.route('/detalhes/')
def lista_frases():

    frases = {}
    frasesBR = "wind"
    nome = request.args.get('nome')
    dadosfrases = requests.get('https://animechan.vercel.app/api/quotes/anime?title=' + nome + '&page=1').json()

    for i in range(len(dadosfrases)):

        # url = 'https://api.gotit.ai/Translation/v1.1/Translate'
        # data = {"T": dadosfrases[i]['quote'], "SL": "EnUs", "TL": "PtBr"}
        # data_json = json.dumps(data)
        # userAndPass = base64.b64encode(b"2202-OXYD/a0Z:PwzCVSxbJEBK0xk6Ok7TqtNwoSFXlMtBtE3knpfjkXrU").decode("ascii")
        # headers = {'Content-type': 'application/json', "Authorization": "Basic %s" % userAndPass}
        # response = requests.post(url, data=data_json, headers=headers)

        # frasesBR[i] = response.json()

        frases[i] = dadosfrases[i]

    qtd = len(dadosfrases)

    return render_template('Frases.html', frases=frases, frasesBR=frasesBR, qtd=qtd, nome=nome)

@app.context_processor
def utility_processor():

    def traduzir2(frase):

        url = 'https://api.gotit.ai/Translation/v1.1/Translate'
        data = {"T": frase, "SL": "EnUs", "TL": "PtBr"}
        data_json = json.dumps(data)
        userAndPass = base64.b64encode(b"2202-OXYD/a0Z:PwzCVSxbJEBK0xk6Ok7TqtNwoSFXlMtBtE3knpfjkXrU").decode("ascii")
        headers = {'Content-type': 'application/json', "Authorization": "Basic %s" % userAndPass}
        response = requests.post(url, data=data_json, headers=headers)

        print(response.json()['result'])

        return response.json()['result']

    return dict(traduzir2=traduzir2)

if __name__ == '__main__':
    app.run()