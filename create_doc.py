import re
from pathlib import Path
from pprint import pprint
from subprocess import run
from textwrap import dedent
from typing import Dict, Generator, Iterable, List, Tuple, TypeVar


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
    return re.split("(@@.*\n)", raw)[1:]


T = TypeVar("T")


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


git_hashes = get_git_hashes(slice(1, 16))


DOC_PATH = Path(__file__).parent / "doc"


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


for name, git_hash in zip(range(1, 16), git_hashes.items()):
    git, oneline = git_hash
    path = Path(DOC_PATH / f"{name:02}.md")
    diff = get_diffs(git)
    text = create_text(name, git, oneline, diff)
    path.write_text(text)
    # pprint(diff)
    # print(path)
    # print(text)
