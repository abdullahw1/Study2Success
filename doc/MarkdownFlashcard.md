# Markdown Flashcards

For importing flashcard from markdown file, we will uses the specs from [Markdown Flashcards here](https://github.com/StanislawSwierc/markdown-flashcards/blob/master/decks/Markdown%20Flashcards.md). Although it might not be a public specs for markdown flashcard, it seems pretty reasonable to follow the syntax in there, it was claiming that it could support Quizlet, Anki.
**Important**: Currently, we are ignoring sections name (heading2 starts with `##`), and essentially just parse the flashcards (although the parser already parse them, we need database and visual support for it), that will be a enhancement in TODO list.

Quote:
 > Markdown flashcards is a convention from preparing flashcard in Markdown and a suite of tools to export them to the existing flashcard software (e.g. Anki, Quizlet).

## Instructions

### Skeleton
The skeleton of the Markdown Flashcard must look like the following:
```
# Markdown Flashcards

## Section 1
<cards>

## Section2
<cards>

```
 - The beggining of the file must start with `# Markdown Flashcards` as a file verification.
 - Each section must be separated with `## <Section name>` and followed by its `<cards>`.


### Writing cards
For this project, we will only be using `?` as the separator for `<cards>`.

The two different syntax allowed for markdown are:
1. Individual Card Syntax (line spacings are important)
    ```
    ---

    front

    ?

    back

    ---
    ```
2. Tabular Card Syntax:
    ```
    | Front   | Back    |
    | ------- | ------- |
    | front 1 | back 1  |
    | front 2 | back 2  |
    ```


## Example

A written example is in [markdown-flashcard-1.md](../etc/markdown-flashcard-1.md), the format can either be like **Category 1** or using a quick tabular format in **Category 2**.