from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

klippning_och_priser = {
    "skinfade": 500,
    "skägg": 300,
    "klassisk klippning": 400
}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/klippningar', methods=['GET'])
def visa_klippningar():
    return jsonify(klippning_och_priser)


def är_rabattkod_giltig(rabatt):
    giltiga_koder = ["kompispris123", "broderpris"]
    return rabatt in giltiga_koder


@app.route('/boka', methods=['POST'])
def boka():
    data = request.json
    önskemål = data.get('önskemål')
    rabatt = data.get('rabatt')

    if önskemål in klippning_och_priser:
        if rabatt and not är_rabattkod_giltig(rabatt):
            return jsonify({"error": "Ogiltig rabattkod"}), 400

        pris = beräkna_pris(klippning_och_priser[önskemål], rabatt)
        return jsonify({"önskemål": önskemål, "pris": pris})
    else:
        return jsonify({"error": "Vi har inte den behandlingen här"}), 404


def beräkna_pris(pris, rabattkod):
    rabattbelopp = 0
    if rabattkod == "kompispris123":
        rabattbelopp = 50
    elif rabattkod == "broderpris":
        rabattbelopp = 100

    slutligt_pris = max(pris - rabattbelopp, 0)
    return slutligt_pris


if __name__ == '__main__':
    app.run(debug=True)
