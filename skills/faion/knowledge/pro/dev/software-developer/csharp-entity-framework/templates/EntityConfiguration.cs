// purpose: IEntityTypeConfiguration<T> fluent mapping skeleton
// consumes: EntityTypeBuilder<Order>
// produces: model-builder configuration applied via ApplyConfigurationsFromAssembly
// depends-on: content/01-core-rules.xml, templates/Entity.cs
// token-budget-impact: ~200 tokens when loaded as reference

using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace Faion.Infrastructure.Orders;

public sealed class OrderConfiguration : IEntityTypeConfiguration<Order>
{
    public void Configure(EntityTypeBuilder<Order> builder)
    {
        builder.ToTable("orders");
        builder.HasKey(o => o.Id);
        builder.Property(o => o.CustomerName).IsRequired().HasMaxLength(200);
        builder.Property(o => o.Total).HasPrecision(18, 2).HasDefaultValueSql("0");
        builder.HasIndex(o => o.CustomerName);
        builder.HasMany(o => o.Items)
            .WithOne()
            .HasForeignKey("OrderId")
            .OnDelete(DeleteBehavior.Cascade);
    }
}

public sealed class OrderItemConfiguration : IEntityTypeConfiguration<OrderItem>
{
    public void Configure(EntityTypeBuilder<OrderItem> builder)
    {
        builder.ToTable("order_items");
        builder.HasKey(i => i.Id);
        builder.Property(i => i.Sku).IsRequired().HasMaxLength(64);
        builder.Property(i => i.Price).HasPrecision(18, 2);
        builder.HasIndex(i => i.Sku);
    }
}
