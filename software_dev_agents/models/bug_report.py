#!/usr/bin/env python3
"""Bug report model with workflow methods."""

from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

from .enums import Severity


@dataclass
class BugReport:
    id: str
    title: str
    description: str
    severity: str
    file_path: str
    line_number: Optional[int]
    steps_to_reproduce: List[str]
    expected_result: str
    actual_result: str
    created_at: str
    fixed_at: Optional[str] = None
    fix_notes: Optional[str] = None

    def mark_fixed(self, fix_notes: str = ""):
        """Mark bug as fixed with optional notes."""
        self.fixed_at = datetime.now().isoformat()
        self.fix_notes = fix_notes

    def is_critical(self) -> bool:
        """Check if bug is critical severity."""
        return self.severity == Severity.CRITICAL.value

    def get_severity_priority(self) -> int:
        """Get numeric priority based on severity."""
        severity_map = {
            Severity.CRITICAL.value: 1,
            Severity.HIGH.value: 2,
            Severity.MEDIUM.value: 3,
            Severity.LOW.value: 4
        }
        return severity_map.get(self.severity, 5)


@dataclass
class TestResult:
    test_name: str
    status: str  # "pass", "fail", "error"
    message: str
    file_path: str

    def is_passing(self) -> bool:
        """Check if test is passing."""
        return self.status == "pass"

    def is_failing(self) -> bool:
        """Check if test is failing."""
        return self.status in ["fail", "error"]