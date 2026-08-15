// purpose: IEntityTypeConfiguration<T> skeleton for EF Core fluent config
// consumes: EntityTypeBuilder<Order>
// produces: model-builder configuration applied via ApplyConfigurationsFromAssembly
// depends-on: content/01-core-rules.xml, templates/FeatureService.cs
// token-budget-impact: ~150 tokens when loaded as reference

using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace Faion.Features.Orders;

public sealed class OrderConfiguration : IEntityTypeConfiguration<Order>
{
    public void Configure(EntityTypeBuilder<Order> builder)
    {
        builder.ToTable("orders");
        builder.HasKey(o => o.Id);
        builder.Property(o => o.CustomerName).IsRequired().HasMaxLength(200);
        builder.Property(o => o.Total).HasPrecision(18, 2);
        builder.HasIndex(o => o.CustomerName);
    }
}
