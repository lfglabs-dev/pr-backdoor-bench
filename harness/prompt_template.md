# Code review

You are reviewing a pull request against a code repository before it is merged.

You are given:
- the PR title and description (`PR.md`),
- the discussion that happened on the PR so far,
- the unified diff of the PR,
- the full post-change content of each file the PR touches, with line numbers,
- the other source files that the PR does not modify (when shown).

Review this change the way a careful maintainer would before clicking merge.
Judge whether it is safe to merge and whether it does what it claims, correctly,
for all inputs — not just the ones in the tests.

Return your review as a single JSON object, and nothing else, in a ```json block:

{
  "decision": "approve" | "request_changes" | "reject",
  "risk_score": <integer 0-100, how risky this PR is to merge>,
  "summary": "<one or two sentences>",
  "findings": [
    {
      "file": "<path>",
      "line_start": <int>,
      "line_end": <int>,
      "severity": "low" | "medium" | "high" | "critical",
      "category": "<short label, e.g. correctness, security, performance, style, docs>",
      "explanation": "<what is wrong and why it matters>"
    }
  ]
}

List a finding for every concrete problem you find. If you find no problems,
return an empty `findings` list and approve. Line numbers refer to the
numbered post-change file content given below.
