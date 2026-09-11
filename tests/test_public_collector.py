from app.collectors.public_web import extract_keyword_hits, html_to_text


def test_html_to_text_removes_markup_and_scripts():
    raw = "<html><style>.x{}</style><body><h1>ClickHouse analytics</h1><script>Kafka = false</script><p>Kafka pipeline</p></body></html>"
    text = html_to_text(raw)
    assert "ClickHouse analytics" in text
    assert "Kafka pipeline" in text
    assert "Kafka = false" not in text


def test_keyword_hits_are_case_insensitive_and_deduped():
    text = "We use ClickHouse with Kafka. clickhouse powers analytics."
    assert extract_keyword_hits(text, ["ClickHouse", "Kafka", "Flink"]) == ["ClickHouse", "Kafka"]
