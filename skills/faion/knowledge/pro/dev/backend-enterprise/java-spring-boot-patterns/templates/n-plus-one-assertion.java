// N+1 detection helper for Spring Boot integration tests using Hibernate Statistics.
// Wire in a @TestConfiguration that enables statistics, then call in @Test methods.
//
// Usage:
//   1. Enable stats in test config:
//      sessionFactory.unwrap(SessionFactory.class).getStatistics().setStatisticsEnabled(true);
//   2. Call NPlusOneAssertion.assertNoNPlusOne(stats, User.class.getName(), 1);

package com.example.app.test;

import org.hibernate.stat.Statistics;

public final class NPlusOneAssertion {

    private NPlusOneAssertion() {}

    /**
     * Asserts that the given entity was fetched at most {@code max} times.
     * Fails with an AssertionError if the fetch count exceeds the allowed maximum.
     *
     * @param stats      Hibernate Statistics (must have setStatisticsEnabled(true))
     * @param entityName Fully-qualified entity class name (e.g. "com.example.app.entity.User")
     * @param max        Maximum allowed fetch count (typically 1 for a single-load test)
     */
    public static void assertNoNPlusOne(Statistics stats, String entityName, int max) {
        long count = stats.getEntityStatistics(entityName).getFetchCount();
        if (count > max) {
            throw new AssertionError(
                "N+1 detected on " + entityName + ": fetched " + count
                + " times, max allowed is " + max
            );
        }
    }
}
