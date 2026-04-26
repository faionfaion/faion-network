-- PostgreSQL many-to-many junction table template
-- Composite PK, FK constraints, reverse lookup index

-- Example: student_course (Students M:N Courses)
-- Replace {left_table} and {right_table} with the two entity names

CREATE TABLE {left_table}_{right_table} (
    {left_table}_id   UUID        NOT NULL REFERENCES {left_table}(id) ON DELETE CASCADE,
    {right_table}_id  UUID        NOT NULL REFERENCES {right_table}(id) ON DELETE CASCADE,

    -- Optional: attributes of the relationship itself
    -- assigned_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    -- role           VARCHAR(30),

    created_at        TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    PRIMARY KEY ({left_table}_id, {right_table}_id)
);

-- Forward lookup: all {right_table}s for a given {left_table}
-- Covered by the composite PK above (leftmost column = {left_table}_id)

-- Reverse lookup: all {left_table}s for a given {right_table}
CREATE INDEX idx_{left_table}_{right_table}_reverse
    ON {left_table}_{right_table}({right_table}_id, {left_table}_id);

-- Named constraints for clear error messages
ALTER TABLE {left_table}_{right_table}
    ADD CONSTRAINT fk_{left_table}_{right_table}_{left_table}
        FOREIGN KEY ({left_table}_id) REFERENCES {left_table}(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_{left_table}_{right_table}_{right_table}
        FOREIGN KEY ({right_table}_id) REFERENCES {right_table}(id) ON DELETE CASCADE;

-- Concrete example: student_course
-- CREATE TABLE student_course (
--     student_id   UUID NOT NULL REFERENCES student(id) ON DELETE CASCADE,
--     course_id    UUID NOT NULL REFERENCES course(id)  ON DELETE CASCADE,
--     enrolled_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
--     PRIMARY KEY (student_id, course_id)
-- );
-- CREATE INDEX idx_student_course_reverse ON student_course(course_id, student_id);
