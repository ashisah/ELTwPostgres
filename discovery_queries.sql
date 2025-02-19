SELECT table_schema, table_name, column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'employees';


SELECT DISTINCT country
FROM employees;

SELECT DISTINCT UPPER(country)
FROM employees;


SELECT DISTINCT UPPER(dept)
FROM employees;

SELECT *
FROM employees
WHERE id IN 
    (SELECT id 
     FROM employees
     GROUP BY id
     HAVING COUNT(*) >1)
ORDER BY id;

SELECT a.id
FROM employees a
JOIN employees b ON a.id = b.id AND a.ctid != b.ctid
WHERE NOT ((a.name IS NOT DISTINCT FROM b.name) AND  
            (a.age IS NOT DISTINCT FROM b.age) AND  
            (a.dept IS NOT DISTINCT FROM b.dept) AND  
            (a.join_date IS NOT DISTINCT FROM b.join_date) AND  
            (a.year_xp IS NOT DISTINCT FROM b.year_xp) AND  
            (a.country IS NOT DISTINCT FROM b.country) AND  
            (a.salary IS NOT DISTINCT FROM b.salary) AND 
            (a.performance_rating IS NOT DISTINCT FROM b.performance_rating))
GROUP BY a.id                                                                                                                                                                        
HAVING COUNT(*) > 1;

