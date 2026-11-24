import json
import re

class MySQLPlanAnalyzer:
    """Analyzes MySQL EXPLAIN JSON plans and suggests index optimizations."""
    def analyze_explain_json(self, explain_raw: str) -> dict:
        data = json.loads(explain_raw)
        query_block = data.get("query_block", {})
        findings = []
        self._walk_plan(query_block, findings)
        return {
            "total_cost": query_block.get("cost_info", {}).get("query_cost", "N/A"),
            "issues_found": len(findings),
            "recommendations": findings,
        }

    def _walk_plan(self, node, findings):
        if isinstance(node, dict):
            if "table" in node:
                tbl = node["table"]
                access_type = tbl.get("access_type")
                rows = tbl.get("rows_examined_per_scan", 0)
                if access_type == "ALL" and rows > 500:
                    cols = tbl.get("attached_condition", "")
                    guessed_cols = re.findall(r"`(\w+)`\s*=", cols)
                    idx_hint = f"CREATE INDEX idx_{tbl['table_name']}_{'_'.join(guessed_cols)} ON {tbl['table_name']}({', '.join(guessed_cols)});" if guessed_cols else "Review WHERE clause selectivity."
                    findings.append({
                        "table": tbl.get("table_name"),
                        "severity": "HIGH",
                        "issue": f"Full table scan examining ~{rows} rows",
                        "suggested_fix": idx_hint
                    })
            for v in node.values():
                self._walk_plan(v, findings)
        elif isinstance(node, list):
            for item in node:
                self._walk_plan(item, findings)

if __name__ == "__main__":
    sample = '{"query_block":{"cost_info":{"query_cost":"4210.50"},"table":{"table_name":"orders","access_type":"ALL","rows_examined_per_scan":42000,"attached_condition":"(`orders`.`customer_id` = 42)"}}}'
    print(json.dumps(MySQLPlanAnalyzer().analyze_explain_json(sample), indent=2))
