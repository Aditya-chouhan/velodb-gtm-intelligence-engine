from __future__ import annotations

import argparse
import csv
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path

MODELS = ["claude-sonnet", "gpt-5", "gemini-pro", "open-model"]
EVENT_TYPES = ["llm_call", "tool_call", "retrieval", "agent_step", "guardrail"]
MESSAGES = ["ok", "timeout", "rate limit", "tool completed", "retrieval completed", "validation failed"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rows", type=int, default=100_000)
    parser.add_argument("--output", default="benchmark/doris/events.csv")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    start = datetime.now(timezone.utc).replace(microsecond=0) - timedelta(hours=24)

    with output.open("w", newline="") as handle:
        writer = csv.writer(handle)
        for i in range(args.rows):
            event_time = start + timedelta(seconds=rng.randint(0, 86_400))
            trace_num = rng.randint(1, max(100, args.rows // 5))
            session_num = rng.randint(1, max(50, args.rows // 20))
            tenant = rng.randint(1, 250)
            model = rng.choice(MODELS)
            event_type = rng.choice(EVENT_TYPES)
            success = rng.random() > 0.035
            latency = max(5, int(rng.lognormvariate(5.0, 0.65)))
            input_tokens = rng.randint(100, 8_000)
            output_tokens = rng.randint(20, 2_500)
            cost = (input_tokens * 0.000003) + (output_tokens * 0.000015)
            message = "ok" if success else rng.choice(MESSAGES[1:])
            writer.writerow([
                event_time.strftime("%Y-%m-%d %H:%M:%S"),
                f"trace-{trace_num:08d}",
                f"session-{session_num:08d}",
                tenant,
                model,
                event_type,
                latency,
                input_tokens,
                output_tokens,
                f"{cost:.6f}",
                "1" if success else "0",
                message,
            ])

    print(f"wrote {args.rows:,} deterministic synthetic events to {output}")


if __name__ == "__main__":
    main()
