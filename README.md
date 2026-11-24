# QueryPulse — MySQL Query Analyzer & Index Advisor

An automated SQL performance profiler built in **Python**, **Django**, and **MySQL** that parses `EXPLAIN` execution plans, detects full table scans (`type=ALL`), flags N+1 query bursts, and recommends composite indexes.

## Key Features
- Parses MySQL `EXPLAIN FORMAT=JSON` output to score query cost.
- Generates copy-paste `CREATE INDEX` statements ranked by selectivity.
- Interactive Bootstrap + JS visual execution tree.
