import yaml
import frontmatter
from pathlib import Path
from typing import Dict, Tuple, Any


class FileHandler:
    @staticmethod
    def read_markdown(file_path: Path) -> Tuple[Dict[str, Any], str]:
        """Read markdown file with front matter"""
        post = frontmatter.load(file_path)
        return post.metadata, post.content

    @staticmethod
    def write_markdown(file_path: Path, metadata: Dict[str, Any], content: str) -> None:
        """Write markdown file with front matter"""
        post = frontmatter.Post(content, **metadata)
        with open(file_path, 'wb') as f:
            frontmatter.dump(post, f)