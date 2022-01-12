export const formatCurrencyValue = totalValue => {
      var formatter = new Intl.NumberFormat("en-US", {
        style: "currency",
        currency: "USD"
      });
      return formatter.format(totalValue).slice(0, -3);
    }
