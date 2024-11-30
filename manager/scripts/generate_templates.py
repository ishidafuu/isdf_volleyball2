from pathlib import Path
import logging
import yaml
from typing import Dict


class TemplateGenerator:
    def __init__(self, config_dir: Path, templates_source_dir: Path):
        self.config_dir = config_dir
        self.template_dir = config_dir / "templates"
        self.templates_source_dir = templates_source_dir
        self.logger = self._setup_logger()

    @staticmethod
    def _setup_logger():
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        return logging.getLogger(__name__)

    def read_template_file(self, file_path: Path) -> str:
        """テンプレートファイルの読み込み"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            self.logger.error(f"Template source file not found: {file_path}")
            return ""
        except Exception as e:
            self.logger.error(f"Error reading template file {file_path}: {e}")
            return ""

    def get_template_contents(self) -> Dict[str, str]:
        """テンプレートの内容を外部ファイルから読み込み"""
        templates = {}
        try:
            # テンプレート定義ファイルの読み込み
            with open(self.templates_source_dir / "template_definitions.yaml", 'r', encoding='utf-8') as f:
                template_definitions = yaml.safe_load(f)

            # 各テンプレートファイルの読み込み
            for template_name, template_info in template_definitions.items():
                source_file = self.templates_source_dir / template_info['source']
                if source_file.exists():
                    templates[template_name] = self.read_template_file(source_file)
                else:
                    self.logger.error(f"Template source file not found: {source_file}")

        except Exception as e:
            self.logger.error(f"Error loading templates: {e}")

        return templates

    def generate_templates(self):
        """テンプレートファイルの生成"""
        self.template_dir.mkdir(exist_ok=True)

        templates = self.get_template_contents()
        for filename, content in templates.items():
            file_path = self.template_dir / filename if filename.endswith('.md') else self.config_dir / filename

            if not file_path.exists():
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.logger.info(f"Created template: {file_path}")
            else:
                self.logger.info(f"Template already exists: {file_path}")

    def verify_templates(self) -> bool:
        """テンプレートファイルの検証"""
        templates = self.get_template_contents()
        success = True

        for filename in templates.keys():
            file_path = self.template_dir / filename if filename.endswith('.md') else self.config_dir / filename
            if not file_path.exists():
                self.logger.error(f"Missing template: {file_path}")
                success = False

        return success


def main():
    """メイン実行関数"""
    config_dir = Path("characters/_config")
    templates_source_dir = Path("character_manager/templates")

    generator = TemplateGenerator(config_dir, templates_source_dir)
    generator.generate_templates()

    if generator.verify_templates():
        generator.logger.info("All templates created successfully!")
    else:
        generator.logger.error("Some templates are missing")


if __name__ == "__main__":
    main()