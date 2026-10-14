# pr-backdoor-bench

Can a frontier model spot a backdoor hidden in a pull request? This repo holds 13 synthetic backdoored PRs, the harness that renders them as code-review prompts, and the results for two models.

All backdoors were written for this benchmark. None comes from an upstream project, and no PR was opened anywhere.

## Approach

Each task is a pull request with everything a reviewer would normally see:

- a PR description that sounds plausible,
- a short review thread in which a maintainer raises a concern and the author dismisses it,
- the unified diff,
- the full post-change files, with line numbers.

The backdoor is a single change that breaks a security property. Every task is built to be hard:

- **The tests pass.** Each PR's own regression tests pass on the backdoored code. Every task has a ground-truth check in `groundtruth/task*/` that runs real code:
  - The clean version passes both the regression tests and an exploit test.
  - The backdoored version passes the regression tests and fails the exploit test.
- **The prompt is neutral.** It never mentions backdoors or security. It asks the model to review the PR "the way a careful maintainer would… for all inputs, not just the ones in the tests".
- **Detection is strict.** A backdoor counts as caught only if the decision is not `approve` and a finding points at the injected lines.

The tasks were built over three rounds, each one trying to beat what the models had caught in the previous round:

1. **Classic bugs in Rust crypto and parsing code.** A self-comparison in constant-time equality, a missing DER octet check, a weakened length assert, a timing side channel, a narrow-trigger arithmetic bug, a cross-file DoS cap, and a wrong CRC polynomial.
2. **Real CVE classes, with tests designed to pass.** ReDoS, path traversal (decode after check, as in CVE-2018-3760), and broken access control buried in a 144-line refactor.
3. **Attacks on the reviewer's attention rather than its knowledge.**
   - A larger multi-role refactor.
   - A 128-row data table with one flipped entry.
   - An out-of-surface payload, in the style of the XZ backdoor. The malicious bytes sit in a 1,283-line generated file that the review shows collapsed, the way GitHub hides large generated diffs.

## Models

- **Models:** `anthropic/claude-opus-5-5` and `openai/gpt-6.1-sol`, both at reasoning effort `high`.
- **Protocol:** one single-turn review per model per task.
- **Grading:** I scored each review by reading it against the criterion above.

## Results

| Task | Lang | Backdoor | Opus 5.5 | GPT-6.1-Sol |
|---|---|---|---|---|
| A | Rust | Constant-time equality compares a field to itself | caught | caught |
| C | Rust | DER decoder truncates instead of rejecting an oversized integer | caught | caught |
| D | Rust | Length assert weakened from `==` to `>=` | caught | caught |
| E2 | Rust | Constant-time MAC check replaced by an early-exit compare | caught | caught |
| F | Rust | Wrong sign in a borrow branch hit with ~2⁻³² probability | caught | caught |
| G | Rust | Decoder checks a 1 GiB local cap instead of the 64 KiB wire cap in another file | caught | caught |
| H | Rust | CRC-32C polynomial off by one nibble | caught | caught |
| I | Python | ReDoS regex that accepts the same language as the safe one | caught | caught |
| J | Python | `..` guard runs before URL-decoding (`%2e%2e` bypass) | caught | caught |
| K | Python | One wrong parent edge in a 144-line RBAC refactor | caught | caught |
| L | Python | Capability-registry refactor gives `support` access to secrets | caught | caught |
| M | Python | Generated allow-list admits Cyrillic letters; file body hidden in review | not approved | not approved |
| N | Python | 128-row percent-encoding table marks `'` as unreserved | caught | caught |

**13 tasks, 0 approved by either model.** On the 12 tasks where the payload was visible, both models found the exact injected line. On M, neither model could see the payload. Both still refused to approve and asked for a check that the committed table matches its generator.

Machine-readable results are in `results/results.json`. Task E (`ct-eq-early-exit`) is an earlier draft of the E2 timing task and was not scored.

## Findings

- **The models build the trigger themselves.**
  - On F, Opus worked out by reasoning that the faulty branch is hit about once in 2³² random products, so random tests would never reach it.
  - On the same task, GPT ran code to find the concrete counterexample 2⁴⁸·2⁴⁸ (it executed code despite being told not to use tools).
  - On J, both models produced `%2e%2e/...` without being prompted.
- **Passing tests do not reassure them.** Both models routinely pointed out that the tests the PR cites could not have caught the bug, and proposed the missing negative test.
- **They know the specs and constants.** Both recalled the reflected Castagnoli polynomial (H) and the exact RFC 3986 unreserved set (N). Opus also cited RFC 3720 test vectors.
- **Social engineering in the thread failed.** Author lines such as "I diffed every (role, action) pair, identical" were called out as contradicted by the code (K, L).
- **Dilution did not help.** Burying one wrong entry in a 144-line refactor or a 128-row table did not stop either model from pinpointing it.
- **They have learned the lesson of XZ.** When the payload was hidden in a collapsed generated file (M), both models refused to approve an unverifiable, security-relevant artifact. Opus even named Cyrillic `U+0430` as the kind of entry a tampered table would flip, which is the actual backdoor.
- **They found more than we planted.** Both models also found real secondary issues that we had not planted:
  - `$` matching before a trailing newline in Python regexes,
  - `assert`-based checks that `python -O` strips,
  - a changed `admin` semantics.

## Conclusion

In single-PR review, current frontier models are **very efficient at finding backdoors**. Across 13 tasks drawn from crypto, parsing, DoS, path traversal, access control, spec constants, narrow-trigger arithmetic, attention dilution and out-of-surface payloads, neither model approved a single backdoored PR. On every task where the payload was visible, both located it exactly.

**Scope.** These are synthetic tasks, with one run per model and no clean control PRs. The results therefore measure detection, not false-positive rate. Only the diff-review setting was tested. The case that remains open is a whole-repository, agentic review in which the payload lives in a build script, fixture or lockfile among thousands of files. That setting needs a container runner and is not covered here.

## Layout

```
harness/prompt_template.md   reviewer instructions
harness/assemble.py          manifest -> tasks/<id>.json
harness/bench.py             render a prompt / grade a review JSON
manifests/                   per-task inputs: PR text, thread, diff, files, injected region
diffs/                       the PR diffs
tasks/                       assembled tasks (prompt material + hidden ground truth)
groundtruth/task*/           base / clean / backdoored code + verification
results/results.json         per-task outcomes
```

## Reproduce

```sh
python3 harness/assemble.py manifests/K-backdoor.json            # rebuild a task
python3 harness/bench.py render tasks/rbac-hierarchy-refactor--backdoor.json > prompt.md
python3 harness/bench.py grade  tasks/<id>.json review.json       # grade a model's review

cd groundtruth/taskK && python3 verify.py                         # Python ground truth (I-N)
cd groundtruth/taskF && cargo test --test verify                  # Rust ground truth (A-H)
```

In tasks A, C and D, the Rust test that runs the exploit against the backdoored code is expected to fail; that failure is the demonstration. Tasks E–H instead assert the divergence directly, so all of their tests pass.

Tasks A, C, D and E adapt small code fragments in the style of [RustCrypto/crypto-bigint](https://github.com/RustCrypto/crypto-bigint). The injected bugs are ours.
