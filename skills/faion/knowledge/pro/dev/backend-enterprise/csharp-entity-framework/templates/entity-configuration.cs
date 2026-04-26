// IEntityTypeConfiguration<T> skeleton
// One file per entity. Replace: TEntity, table name, property names.

using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace MyApp.Data.Configurations;

public class ExampleEntityConfiguration : IEntityTypeConfiguration<ExampleEntity>
{
    public void Configure(EntityTypeBuilder<ExampleEntity> builder)
    {
        builder.ToTable("example_entities");

        builder.HasKey(e => e.Id);

        builder.Property(e => e.Name)
            .IsRequired()
            .HasMaxLength(100);

        builder.Property(e => e.Email)
            .IsRequired()
            .HasMaxLength(255);

        builder.HasIndex(e => e.Email).IsUnique();

        builder.Property(e => e.CreatedAt)
            .HasDefaultValueSql("CURRENT_TIMESTAMP");

        // Optimistic concurrency: required on aggregate roots
        builder.Property(e => e.RowVersion)
            .IsRowVersion();

        // Many-to-many via junction table
        builder.HasMany(e => e.Tags)
            .WithMany(t => t.Entities)
            .UsingEntity<Dictionary<string, object>>(
                "entity_tags",
                j => j.HasOne<Tag>().WithMany().HasForeignKey("TagId"),
                j => j.HasOne<ExampleEntity>().WithMany().HasForeignKey("EntityId")
            );

        // One-to-many (SetNull on parent delete — avoid Cascade to prevent cycles)
        builder.HasMany(e => e.Items)
            .WithOne(i => i.Entity)
            .HasForeignKey(i => i.EntityId)
            .OnDelete(DeleteBehavior.SetNull);

        // Explicitly index FK — EF Core does not always add these
        builder.HasIndex(e => e.CategoryId);
    }
}
