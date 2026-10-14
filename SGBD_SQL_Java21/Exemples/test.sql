CREATE TABLE students (id INT, name VARCHAR, age INT);
INSERT INTO students (id, name, age) VALUES (1, "Alice", 22);
INSERT INTO students (id, name, age) VALUES (2, "Bob", 19);
INSERT INTO students (id, name, age) VALUES (3, "Charlie", 21);

CREATE TABLE grades (student_id INT, course VARCHAR, grade INT);
INSERT INTO grades (student_id, course, grade) VALUES (1, "Math", 15);
INSERT INTO grades (student_id, course, grade) VALUES (2, "Math", 12);
INSERT INTO grades (student_id, course, grade) VALUES (1, "CS", 18);

SELECT * FROM students;
SELECT name, age FROM students WHERE age > 20;
SELECT students.name, grades.course, grades.grade FROM students, grades WHERE students.id = grades.student_id;
exit;
EXIT;




-- RESULTATS D'EXECUTION :
-- -----------------------
-- Student Gotham Bat Database v19.39 - Connecté à mabase
-- Tapez vos commandes SQL terminées par ';' (ou 'exit;' pour quitter)
-- > Table students créée.
-- > 1 ligne insérée dans students
-- > 1 ligne insérée dans students
-- > 1 ligne insérée dans students
-- > Table grades créée.
-- > 1 ligne insérée dans grades
-- > 1 ligne insérée dans grades
-- > 1 ligne insérée dans grades
-- > Table: students
-- | id              | name            | age             |
-- |-----------------|-----------------|-----------------|
-- | 1               | Alice           | 22              |
-- | 2               | Bob             | 19              |
-- | 3               | Charlie         | 21              |
-- 
-- > Table: students_selection_projection
-- | name            | age             |
-- |-----------------|-----------------|
-- | Alice           | 22              |
-- | Charlie         | 21              |
-- 
-- > Table: students_grades_selection_projection
-- | students.name   | grades.course   | grades.grade    |
-- |-----------------|-----------------|-----------------|
-- | Alice           | Math            | 15              |
-- | Alice           | CS              | 18              |
-- | Bob             | Math            | 12              |
-- 
-- > Au revoir !
