#! /usr/bin/env python3.6

from optparse import OptionParser
import requests
import json
import xml.etree.cElementTree as ET


class CurrencyConverter:
    URL = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml"

    def __init__(self):
        self.codes = self.get_codes()
        self.rates = self.get_data_rates()

    def convert_to_code(self, currency):
        """
        If currency symbol was given on input then the symbol is converted to currency code.
        :param currency: Symbol or code of given currency.
        :return: Code of given currency.
        """

        if currency in ['EUR', '\u20ac']:
            return 'EUR'

        code = self.codes.get(currency)

        if code is None:
            code = currency

        if code not in self.rates:
            self.handle_error('Bad input/output symbol/code')

        return code

    def parse_arguments(self, arg_parser):
        """
        Parse arguments and prepares basic output object in json format.
        :param arg_parser: Object for parsing arguments.
        :return: Basic output object in json format.
        """
        (options, args) = arg_parser.parse_args()

        if options.amount is None:
            self.handle_error('Argument amount is missing!')

        if options.input_currency is None:
            self.handle_error('Argument input_currency is missing!')

        if options.output_currency is not None:
            output_symb = self.convert_to_code(options.output_currency)
            if output_symb not in self.rates:
                self.handle_error("Bad output currency symbol / code")
        else:
            output_symb = None

        input_symb = self.convert_to_code(options.input_currency)

        if input_symb not in self.rates:
            self.handle_error("Bad input currency symbol / code")

        cli_output = {
            'input': {
                'amount': options.amount,
                'currency': input_symb
            },
            'output': output_symb
        }

        return cli_output

    def get_data_rates(self):
        """
        Retrieves data about currency rates from hard coded url in xml format
        and converts it to json.
        :return: Currency rates json object.
        """
        response = requests.get(self.URL)

        if response.status_code != 200:
            self.handle_error('Failed to get currency rates')

        root = ET.fromstring(response.text)

        result_json_rates = {}

        try:
            for child in root[2][0]:
                result_json_rates[child.attrib.get('currency')] = float(child.attrib.get('rate'))
        except IndexError:
            raise Exception("Index out of bound exception")
        except ValueError:
            raise Exception("Bad currency value format")

        # Need to explicitly add EUR to EUR
        result_json_rates['EUR'] = float(1)
        return json.loads(json.dumps(result_json_rates, indent=4))

    def get_codes(self):
        """
        Reads currency symbols and their codes from file 'symbols_codes'.
        :return: Currency symbols and their codes json object.
        """
        try:
            with open('symbols_codes', 'r') as file:
                result = json.loads(file.read())
                file.close()
        except IOError:
            self.handle_error("Symbols_codes file missing in directory.")

        return result

    def compute(self, cli_output):
        """
        Compute converted value in given output currency. If output currency was not given, function converts
        to all supported currencies.
        :param cli_output: Basic output object in json format.
        """
        output_symb = cli_output['output']
        result_json = {}

        if output_symb is not None:
            result = cli_output['input']['amount'] / self.rates[cli_output['input']['currency']] * self.rates[
                output_symb]
            result_json[output_symb] = result
        else:
            for rate in self.rates:
                if rate == cli_output['input']['currency']:
                    continue
                result = cli_output['input']['amount'] / self.rates[cli_output['input']['currency']] * self.rates[
                    rate]
                result_json[rate] = result

        cli_output['output'] = result_json

        return cli_output

    @staticmethod
    def print_result(result):
        print(json.dumps(result, indent=4))

    @staticmethod
    def handle_error(error_message):
        print(error_message)
        exit(-1)


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('--amount', type="float")
    parser.add_option('--input_currency')
    parser.add_option('--output_currency')

    converter = CurrencyConverter()

    output = converter.parse_arguments(parser)
    output = converter.compute(output)
    converter.print_result(output)
