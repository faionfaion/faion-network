// purpose: C# value object as readonly record struct with constructor validation
// consumes: amount + currency primitives
// produces: immutable Money type with value-equality + Add/Subtract
// depends-on: content/01-core-rules.xml
// token-budget-impact: ~200 tokens when loaded as reference

namespace Faion.Domain.Money;

public readonly record struct Money
{
    public decimal Amount { get; }
    public string Currency { get; }

    public Money(decimal amount, string currency)
    {
        if (amount < 0) throw new ArgumentOutOfRangeException(nameof(amount), "amount must be >= 0");
        if (string.IsNullOrEmpty(currency) || currency.Length != 3)
            throw new ArgumentException("currency must be ISO 4217 (3 chars)", nameof(currency));
        Amount = amount;
        Currency = currency.ToUpperInvariant();
    }

    public Money Add(Money other)
    {
        EnsureSameCurrency(other);
        return new Money(Amount + other.Amount, Currency);
    }

    public Money Subtract(Money other)
    {
        EnsureSameCurrency(other);
        return new Money(Amount - other.Amount, Currency);
    }

    private void EnsureSameCurrency(Money other)
    {
        if (Currency != other.Currency)
            throw new InvalidOperationException($"currency mismatch {Currency} vs {other.Currency}");
    }
}
