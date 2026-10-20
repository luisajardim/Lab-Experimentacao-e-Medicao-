from metrics import DORAVariant, classify_dora


def test_category_uses_median_of_metric_tiers() -> None:
    # ENUNCIADO example: (Elite, High, High, Low) -> High.
    result = classify_dora(
        DORAVariant.C1,
        lead_time_a=48.0,
        lead_time_b=48.0,
        cfr=0.20,
        recovery_hours=200.0,
        deploy_freq_releases=8.0,
        deploy_freq_with_tags=8.0,
    )
    assert result.category() == "High"


def test_category_preserves_medium_and_low_tiers() -> None:
    medium = classify_dora(DORAVariant.C1, 200.0, 200.0, 0.40, 100.0, 0.5, 0.5)
    low = classify_dora(DORAVariant.C1, 800.0, 800.0, 0.60, 200.0, 0.1, 0.1)
    assert medium.category() == "Medium"
    assert low.category() == "Low"
