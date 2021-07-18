from generate_docs.repo import Repo, LanguageCollection
from snake.md import Document, Paragraph, InlineText, MDList


def _get_intro_text(language: LanguageCollection) -> Paragraph:
    text = [
        InlineText(f"Welcome to Sample Programs in {language.get_readable_name()}!"),
        InlineText(f"To find documentation related to the {language.get_readable_name()} code in this repo, look"),
        InlineText("here.", url=language.sample_program_url)
    ]
    if not text[-1].verify_url():
        return Paragraph(text[:1])
    else:
        return Paragraph(text)


def _get_sample_programs_text() -> str:
    return """
    Below, you'll find a list of code snippets in this collection.
    Code snippets preceded by :warning: link to a GitHub 
    issue query featuring a possible article request issue. If an article request issue 
    doesn't exist, we encourage you to create one. Meanwhile, code snippets preceded 
    by :white_check_mark: link to an existing article which provides further documentation.
    """


def _generate_program_list(language: LanguageCollection) -> MDList:
    """
    A helper function which generates a list of programs for the README.
    :param language: a language collection
    :return: a list of sample programs list items
    """
    list_items = list()
    for program in language.sample_programs:
        readable_name = program.normalized_name.replace("-", " ").title()
        program_line = f"- :white_check_mark: {readable_name} in {language.get_readable_name()} [Requirements]"
        doc_link = InlineText(program_line, url=program.sample_program_doc_url)
        if not doc_link.verify_url():
            program_line = program_line.replace(":white_check_mark:", ":warning:")
            doc_link = InlineText(program_line, url=program.sample_program_issue_url)
        list_item = Paragraph([doc_link])
        list_item.insert_link("Requirements", program.sample_program_req_url)
        list_items.append(list_item)
    return MDList(list_items)


def _generate_credit() -> Paragraph:
    p = Paragraph(
        """
        This page was generated automatically by the Sample Programs Docs Generator. 
        Find out how to support this project on Github.
        """
    )
    p.insert_link("this project", "https://github.com/TheRenegadeCoder/sample-programs-docs-generator")
    return p


class ReadMeCatalog:
    """
    An representation of the collection of READMEs in the Sample Programs repo.
    """

    def __init__(self, repo: Repo):
        """
        Constructs an instance of a ReadMeCatalog.
        :param repo: a repository instance
        """
        self.repo: Repo = repo
        self.pages: dict[str, Document] = dict()
        self._build_readmes()

    def _build_readme(self, language: LanguageCollection) -> None:
        """
        Creates a README page from a language collection.
        :param language: a programming language collection (e.g., Python)
        :return: None
        """
        page = Document("README")

        # Introduction
        page.add_header(f"Sample Programs in {language.get_readable_name()}")
        page.add_element(_get_intro_text(language))

        # Sample Programs List
        page.add_header("Sample Programs List", level=2)
        page.add_paragraph(_get_sample_programs_text())
        page.add_element(_generate_program_list(language))

        # Testing
        page.add_header("Testing", level=2)
        test_data = language.get_test_data()
        if not test_data:
            page.add_paragraph(
                """
                This language currently does not feature testing. If you'd like to help in the efforts to test all of 
                the code in this repo, consider creating a testinfo.yml file with the following information:
                """
            )
            page.add_code("folder:\n\textension:\n\tnaming:\n\ncontainer:\n\timage:\n\ttag:\n\tcmd:", lang="yml")
        else:
            page.add_paragraph(
                f"""
                The following list shares details about what we're using to test all Sample Programs in 
                {language.get_readable_name()}.
                """
            )
            page.add_unordered_list([
                f"Docker Image: {test_data['container']['image']}",
                f"Docker Tag: {test_data['container']['tag']}"
            ])
        glotter = page.add_paragraph("See the Glotter project for more information on how to create a testinfo file.")
        glotter.insert_link("Glotter project", "https://github.com/auroq/glotter")
        page.add_horizontal_rule()
        page.add_element(_generate_credit())

        self.pages[language.name] = page

    def _build_readmes(self) -> None:
        """
        Generates all READMEs for the repo.
        :return: None
        """
        for language in self.repo.languages:
            self._build_readme(language)
