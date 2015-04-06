`import Ember from 'ember'`

currencyFormat = (money) ->
  if money[0] == null or money[0] == undefined
    return new Ember.Handlebars.SafeString('-');

  if money[0] == 0
    return '-';

  re = /\d(?=(\d{3})+\.)/g;
  subst = '$& ';
  formatted = money[0].toFixed(2).replace(re, subst);
  return new Ember.Handlebars.SafeString(formatted.slice(0,-3) + ',- Kč')

CurrencyFormatHelper = Ember.HTMLBars.makeBoundHelper currencyFormat

`export { currencyFormat }`

`export default CurrencyFormatHelper`
