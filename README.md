# Kiwi-currency_converter
## CLI application
### Usage
chmod +x currency_converter.py

./currency_converter.py [options]

Options:
  -h, --help            show this help message and exit
  
  --amount=AMOUNT
  
  --input_currency=INPUT_CURRENCY
  
  --output_currency=OUTPUT_CURRENCY => If missing, converts to all supported currencies
## WEB API application
Running by default on http://127.0.0.1:5000
### Usage
chmod +x api.py

./api.py

/currency_converter?amount=0.9&input_currency=¥&output_currency=AUD

output_currency => If missing, converts to all suported currencies

### Docker

## Supported currencies
Symbol|Code
----- | ---
"$" | "USD",
"CA$" | "CAD",
"\u20ac" | "EUR",
"AU$" | "AUD", 
"BGN" | "BGN", 
"R$" | "BRL",
"CHF" | "CHF",
"CN\u00a5" | "CNY",
"K\u010d" | "CZK",
"Dkr" | "DKK",
"\u00a3" | "GBP",
"HK$" | "HKD",
"Rp" | "IDR",
"\u20aa" | "ILS",
"Rs" | "INR",
"Ikr" | "ISK",
"\u00a5" | "JPY",
"\u20a9" | "KRW",
"MX$" | "MXN",
"RM" | "MYR",
"Nkr" | "NOK",
"NZ$" | "NZD",
"\u20b1" | "PHP",
"z\u0142" | "PLN",
"RON" | "RON",
"RUB" | "RUB",
"Skr" | "SEK",
"S$" | "SGD",
"\u0e3f" | "THB",
"TL" | "TRY",
"R" | "ZAR",
