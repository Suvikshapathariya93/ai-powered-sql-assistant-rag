# SQL Window Functions

Window functions calculate values across related rows without collapsing rows like GROUP BY.

## ROW_NUMBER, RANK and DENSE_RANK
- ROW_NUMBER assigns a unique sequential number to each row in a partition.
- RANK gives tied rows the same rank and leaves gaps after ties.
- DENSE_RANK gives tied rows the same rank without gaps.

```sql
SELECT employee_id, department_id, salary,
       ROW_NUMBER() OVER (PARTITION BY department_id ORDER BY salary DESC) AS row_num,
       RANK() OVER (PARTITION BY department_id ORDER BY salary DESC) AS salary_rank,
       DENSE_RANK() OVER (PARTITION BY department_id ORDER BY salary DESC) AS dense_salary_rank
FROM employees;
```

## Running total

```sql
SELECT order_date, order_id, amount,
       SUM(amount) OVER (
           ORDER BY order_date, order_id
           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
       ) AS running_total
FROM orders;
```

Use deterministic ordering when repeatable row ordering matters.
