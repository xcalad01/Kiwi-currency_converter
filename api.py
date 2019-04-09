#! /usr/bin/env python3.6

from flask import Flask, request, make_response, jsonify
from currency_converter import CurrencyConverter

app = Flask(__name__)


@app.route('/currency_converter', methods=['GET'])
def currency_converter():
    amount = request.args.get('amount', default=None, type=float)
    input_currency = request.args.get('input_currency', default=None)
    output_currency = request.args.get('output_currency', default=None)

    if amount is None:
        return make_response("Amount arguments is missing !")
    if input_currency is None:
        return make_response("Input currency argument is missing!")

    converter = CurrencyConverter()
    input_currency = converter.convert_to_code(input_currency)
    if output_currency is not None:
        output_currency = converter.convert_to_code(output_currency)

    output = {
        'input': {
            'amount': amount,
            'currency': input_currency
        },
        'output': output_currency
    }

    output = converter.compute(output)

    return make_response(jsonify(output), 200)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
