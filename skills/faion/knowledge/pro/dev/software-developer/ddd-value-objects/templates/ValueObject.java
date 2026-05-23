// purpose: Java value object as record with constructor validation
// consumes: amount + currency primitives
// produces: immutable Money record with value-equality + add/subtract
// depends-on: content/01-core-rules.xml
// token-budget-impact: ~200 tokens when loaded as reference

package faion.domain.money;

import java.math.BigDecimal;

public record Money(BigDecimal amount, String currency) {

    public Money {
        if (amount == null) throw new IllegalArgumentException("amount required");
        if (amount.signum() < 0) throw new IllegalArgumentException("amount must be >= 0");
        if (currency == null || currency.length() != 3)
            throw new IllegalArgumentException("currency must be ISO 4217 (3 chars)");
        currency = currency.toUpperCase();
    }

    public Money add(Money other) {
        ensureSameCurrency(other);
        return new Money(amount.add(other.amount), currency);
    }

    public Money subtract(Money other) {
        ensureSameCurrency(other);
        return new Money(amount.subtract(other.amount), currency);
    }

    private void ensureSameCurrency(Money other) {
        if (!currency.equals(other.currency))
            throw new IllegalStateException("currency mismatch " + currency + " vs " + other.currency);
    }
}
