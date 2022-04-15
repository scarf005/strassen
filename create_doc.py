import re
from pathlib import Path
from pprint import pprint
from subprocess import run
from textwrap import dedent
from typing import Dict, Generator, Iterable, List, Tuple, TypeVar

import Terror

T = TypeVar("T")


def get_git_hashes(rng: slice) -> Dict[str, str]:
    result = run(
        "git log --reverse --pretty=%H|%s".split(),
        capture_output=True,
    )
    lines = result.stdout.decode().splitlines()[rng]
    return {
        git: summary for git, summary in (line.split("|") for line in lines)
    }


def get_diffs(git_hash: str) -> List[str]:
    result = run(
        f"git show {git_hash} --pretty=format:%b -- strassen.py".split(),
        capture_output=True,
    )
    raw = result.stdout.decode()
    pprint(re.split("(@@.*@@)", raw)[1:])
    return re.split("(@@.*@@)", raw)[1:]


def grouped(iterable: Iterable[T], n=2) -> Iterable[Tuple[T, ...]]:
    """s -> (s0,s1,s2,...sn-1), (sn,sn+1,sn+2,...s2n-1), ..."""
    iterators = [iter(iterable)]
    return zip(*iterators * n)


def format_diff(diff_text: List[str]) -> Generator[str, None, None]:
    for changed_line, text in grouped(diff_text):
        yield (
            f"""
```diff
{changed_line}
{text}
```
        """
        )


def create_text(name: int, git: str, oneline: str, diff: List[str]) -> str:
    diffs = "\n".join([diff for diff in format_diff(diff)])
    return f"""\
# 챕터 {name:02}:

|   챕터    | 커밋 해시 |  커밋 로그  |
| -------  | -------- | --------- |
|{name:02} | {git} | {oneline} |

## 개요
-
-


## 무엇을 바꿀까?
{diffs}

"""


git_hashes = get_git_hashes(slice(1, 16))
entries = zip(range(1, 16), git_hashes.keys(), git_hashes.values())
DOC_PATH = Path(__file__).parent / "doc"


def genearate_docs():
    for name, git, oneline in entries:
        path = Path(DOC_PATH / f"{name:02}.md")
        diff = get_diffs(git)
        text = create_text(name, git, oneline, diff)
        path.write_text(text)
        # pprint(diff)
        # print(path)
        # print(text)


def generate_readme():
    arr = [
        f"|{name:02}|[{oneline}](./doc/{name:02}.md)|"
        for name, _, oneline in entries
    ]
    contents = "\n".join(arr)
    body = f"""
# Strassen

스트라센 행렬곱 알고리즘 리팩토링

## 목차
|장|요약|
|--|---|
{contents}
"""

    path = Path("README.md")
    path.write_text(body)


if __name__ == "__main__":
	Terror.Terror()
    # generate_readme()

# TODO: create diff-documentation generator tool?
