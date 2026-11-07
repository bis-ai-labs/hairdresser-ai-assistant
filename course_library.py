import re
from dataclasses import dataclass
from pathlib import Path


COURSE_MATERIALS_DIR = Path(__file__).parent / "data" / "course_materials"
WORD_PATTERN = re.compile(r"[a-z0-9]+", re.IGNORECASE)
HEADING_PATTERN = re.compile(r"^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$")
STOP_WORDS = {
    "a",
    "about",
    "an",
    "and",
    "are",
    "can",
    "do",
    "for",
    "from",
    "how",
    "i",
    "in",
    "is",
    "it",
    "me",
    "of",
    "on",
    "or",
    "should",
    "tell",
    "that",
    "the",
    "this",
    "to",
    "what",
    "when",
    "where",
    "which",
    "with",
    "would",
    "you",
}


@dataclass(frozen=True)
class CoursePassage:
    title: str
    heading: str
    content: str
    source: str


def _terms(text: str) -> set[str]:
    return {
        word.casefold()
        for word in WORD_PATTERN.findall(text)
        if word.casefold() not in STOP_WORDS
    }


def _read_passages(path: Path, source: str) -> list[CoursePassage]:
    title = path.stem.replace("-", " ").title()
    heading = title
    content_lines: list[str] = []
    passages: list[CoursePassage] = []

    def add_passage() -> None:
        content = "\n".join(content_lines).strip()
        if content:
            passages.append(
                CoursePassage(
                    title=title,
                    heading=heading,
                    content=content,
                    source=source,
                )
            )

    for line in path.read_text(encoding="utf-8").splitlines():
        match = HEADING_PATTERN.match(line)
        if match:
            add_passage()
            content_lines.clear()
            heading = match.group(1).strip()
            if line.lstrip().startswith("# ") and not passages:
                title = heading
            continue
        content_lines.append(line)

    add_passage()
    return passages


def search_course_materials(
    question: str,
    course_materials_dir: str | Path = COURSE_MATERIALS_DIR,
    max_results: int = 3,
) -> list[CoursePassage]:
    """Return passages ranked by simple keyword overlap with the question.

    This is a deterministic keyword search, not semantic search. A missing or
    empty course-materials directory returns no matches.
    """
    if max_results < 1:
        raise ValueError("max_results must be at least 1")

    query_terms = _terms(question)
    if not query_terms:
        return []

    directory = Path(course_materials_dir)
    if not directory.is_dir():
        return []

    ranked: list[tuple[int, str, CoursePassage]] = []
    for path in sorted(directory.rglob("*.md")):
        source = path.relative_to(directory).as_posix()
        for passage in _read_passages(path, source):
            title_matches = query_terms & _terms(passage.title)
            heading_matches = query_terms & _terms(passage.heading)
            content_matches = query_terms & _terms(passage.content)
            score = (
                len(content_matches)
                + 2 * len(title_matches)
                + len(heading_matches)
            )
            if score:
                ranked.append((score, source, passage))

    ranked.sort(key=lambda result: (-result[0], result[1], result[2].heading))
    results: list[CoursePassage] = []
    seen_sources: set[str] = set()
    for _, source, passage in ranked:
        if source in seen_sources:
            continue
        results.append(passage)
        seen_sources.add(source)
        if len(results) == max_results:
            break
    return results
