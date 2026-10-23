from analysis.rq04_hypothesis import valid_runs


def test_valid_runs_counts_only_push_on_default_branch_with_success_or_failure():
    payload = {
        "repository": {"default_branch": "main"},
        "runs_by_month": {
            "2026-01": [
                {"branch": "main", "event": "push", "conclusion": "success"},
                {"branch": "main", "event": "push", "conclusion": "failure"},
                {"branch": "main", "event": "push", "conclusion": "timed_out"},
                {"branch": "main", "event": "push", "conclusion": "cancelled"},
                {"branch": "main", "event": "schedule", "conclusion": "success"},
                {"branch": "dev", "event": "push", "conclusion": "success"},
            ],
        },
    }
    assert valid_runs(payload) == 3
