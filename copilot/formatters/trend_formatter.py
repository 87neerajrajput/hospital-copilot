class TrendFormatter:

    @staticmethod
    def format(trend: dict) -> str:

        report = f"""
#### 📈 Clinical Trend Analysis

##### Overall Status

**{trend.get("overall_status","Unknown")}**

---

##### 📝 Summary

{trend.get("summary","")}

---

##### 📈 Improving Domains
"""

        improving = trend.get("improving_domains", [])

        if improving:
            for item in improving:
                report += f"\n- {item}"
        else:
            report += "\n- None"

        report += """

---

##### ⚖️ Plateaued Domains
"""

        plateau = trend.get("plateaued_domains", [])

        if plateau:
            for item in plateau:
                report += f"\n- {item}"
        else:
            report += "\n- None"

        report += """

---

##### ⚠️ Regression Risks
"""

        risks = trend.get("regression_risk", [])

        if risks:
            for item in risks:
                report += f"\n- {item}"
        else:
            report += "\n- None"

        report += """

---

##### 🔍 Clinical Observations

"""

        report += trend.get(
            "clinical_observations",
            "None",
        )

        report += """

---

##### 🎯 Recommended Priorities
"""

        priorities = trend.get(
            "recommended_priorities",
            [],
        )

        if priorities:
            for item in priorities:
                report += f"\n- {item}"
        else:
            report += "\n- None"

        report += f"""

---

##### 🔮 Prognosis

{trend.get("prognosis","")}

"""

        return report.strip()