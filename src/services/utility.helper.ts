export class CurrencyFormatter {
  static USDollar = new Intl.NumberFormat('en-US', {
    // TODO move this.
    style: 'currency',
    currency: 'USD',
    maximumFractionDigits: 0,
  })
}
