// Spring Data JPA repository skeleton
// Replace: User, Role, UserRepository

package com.example.repository;

import com.example.entity.User;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.Optional;

@Repository
public interface UserRepository extends JpaRepository<User, Long> {

    // Derived methods — no @Query needed
    Optional<User> findByEmail(String email);
    boolean existsByEmail(String email);

    // JOIN FETCH — load roles in one query, avoid N+1
    @Query("SELECT u FROM User u JOIN FETCH u.roles WHERE u.id = :id")
    Optional<User> findByIdWithRoles(@Param("id") Long id);

    // Pageable search with nullable filters
    @Query("""
        SELECT u FROM User u
        WHERE (:name IS NULL OR LOWER(u.name) LIKE LOWER(CONCAT('%', :name, '%')))
        AND (:isActive IS NULL OR u.isActive = :isActive)
        """)
    Page<User> search(
        @Param("name") String name,
        @Param("isActive") Boolean isActive,
        Pageable pageable
    );

    // Bulk update — must clear L1 cache after
    @Modifying(clearAutomatically = true, flushAutomatically = true)
    @Query("UPDATE User u SET u.isActive = false WHERE u.lastLoginAt < :cutoff")
    int deactivateInactive(@Param("cutoff") LocalDateTime cutoff);
}
