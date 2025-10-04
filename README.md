# Static Site Generator

A custom-built static site generator written in Python that converts Markdown files into a fully functional static website. This project implements a complete pipeline from Markdown parsing to HTML generation with support for inline formatting, code blocks, lists, quotes, and more.

## Features

- **Full Markdown Support**
  - Headings (H1-H6)
  - Bold (`**text**`) and Italic (`_text_`)
  - Inline code (`` `code` ``)
  - Code blocks (` ```code``` `)
  - Links `[text](url)`
  - Images `![alt](src)`
  - Ordered and unordered lists
  - Block quotes

- **Recursive Directory Processing**
  - Automatically processes nested directory structures
  - Preserves folder hierarchy in output

- **Template System**
  - Uses HTML templates with variable substitution
  - Automatically extracts page titles from H1 headers
  - Easy to customize site-wide styling

- **Static Asset Copying**
  - Copies CSS, images, and other static files to output directory
  - Maintains directory structure

## Project Structure

```
staticSiteGenerator/
├── content/           # Markdown source files
│   ├── index.md
│   ├── blog/
│   └── contact/
├── static/            # Static assets (CSS, images)
│   ├── index.css
│   └── images/
├── public/            # Generated HTML output (created by build)
├── src/               # Source code
│   ├── main.py                  # Entry point
│   ├── build.py                 # Directory copying utilities
│   ├── generatepage.py          # Page generation logic
│   ├── blocks.py                # Markdown block parsing
│   ├── textnode.py              # Text node representation
│   ├── split_delimitter.py      # Inline markdown parsing
│   ├── htmlnode.py              # HTML node base class
│   ├── leafnode.py              # HTML leaf nodes (no children)
│   ├── parentnode.py            # HTML parent nodes (with children)
│   └── test_*.py                # Unit tests
├── template.html      # HTML template
├── main.sh            # Build and serve script
└── test.sh            # Test runner script
```

## Architecture

The generator follows a pipeline architecture:

1. **Markdown Parsing** (`blocks.py`)
   - Splits markdown into blocks (paragraphs, headings, lists, etc.)
   - Identifies block types using regex patterns

2. **Text Node Processing** (`textnode.py`, `split_delimitter.py`)
   - Parses inline markdown (bold, italic, code, links, images)
   - Creates text nodes with type information

3. **HTML Node Generation** (`htmlnode.py`, `leafnode.py`, `parentnode.py`)
   - Converts text nodes and blocks into HTML node tree
   - Renders final HTML output

4. **Page Generation** (`generatepage.py`)
   - Extracts page title from first H1 heading
   - Converts markdown to HTML
   - Injects content into template

5. **Build Process** (`build.py`, `main.py`)
   - Copies static assets to public directory
   - Recursively processes all markdown files
   - Generates complete static site

## Installation

No external dependencies required! This project uses only Python standard library.

**Requirements:**
- Python 3.10+ (uses match/case statements)

## Usage

### Build and Serve

Generate the site and start a local development server:

```bash
./main.sh
```

This will:
1. Build the site (convert markdown to HTML)
2. Serve it locally at `http://localhost:8888`

### Build Only

Generate the static site without serving:

```bash
python3 src/main.py
```

### Run Tests

Execute all unit tests:

```bash
./test.sh
```

Or run tests manually:

```bash
python3 -m unittest discover -s src
```

## Creating Content

### Add a New Page

1. Create a markdown file in the `content/` directory:

```markdown
# Page Title

Your content here with **bold** and _italic_ text.
```

2. Run the build process:

```bash
python3 src/main.py
```

3. The HTML file will be generated in `public/` with the same directory structure.

### Markdown Syntax Examples

**Headings:**
```markdown
# H1 Heading
## H2 Heading
### H3 Heading
```

**Text Formatting:**
```markdown
**bold text**
_italic text_
`inline code`
```

**Links and Images:**
```markdown
[Link text](https://example.com)
![Alt text](/images/photo.png)
```

**Lists:**
```markdown
- Unordered item 1
- Unordered item 2

1. Ordered item 1
2. Ordered item 2
```

**Code Blocks:**
````markdown
```
code here
```
````

**Block Quotes:**
```markdown
> This is a quote
```

## Adding Static Assets

1. Place CSS, images, or other static files in the `static/` directory
2. Reference them in your markdown or template using absolute paths (e.g., `/index.css`, `/images/photo.png`)
3. The build process automatically copies everything to `public/`

## Customization

### Modify the Template

Edit `template.html` to change the site structure. Use these placeholders:
- `{{ Title }}` - Replaced with the page title (from first H1)
- `{{ Content }}` - Replaced with the generated HTML content

### Styling

Edit `static/index.css` to customize the site appearance. Changes will be reflected after rebuilding.

## Testing

The project includes comprehensive unit tests for all major components:

- `test_textnode.py` - Text node functionality
- `test_htmlnode.py` - HTML node base class
- `test_leafnode.py` - Leaf node rendering
- `test_parentnode.py` - Parent node rendering
- `test_split_delimitter.py` - Inline markdown parsing
- `test_blocks.py` - Block-level markdown parsing

Run all tests with:
```bash
./test.sh
```

## How It Works

### Build Process

1. **Clean and Copy Static Assets**
   - Delete existing `public/` directory
   - Copy all files from `static/` to `public/`

2. **Process Markdown Files**
   - Recursively scan `content/` directory
   - For each `.md` file:
     - Parse markdown into blocks
     - Convert blocks to HTML nodes
     - Extract title from first H1
     - Inject into template
     - Write HTML to `public/`

3. **Maintain Directory Structure**
   - Nested folders in `content/` are preserved in `public/`
   - Example: `content/blog/post.md` → `public/blog/post.html`

### Markdown to HTML Conversion

```
Markdown File
    ↓
Block Parser (identify paragraphs, headings, lists, etc.)
    ↓
Text Node Parser (handle inline formatting)
    ↓
HTML Node Tree
    ↓
HTML String Output
    ↓
Template Injection
    ↓
Final HTML Page
```

## Development

### Key Classes

- **`TextNode`** - Represents a piece of text with type (plain, bold, italic, code, link, image)
- **`HTMLNode`** - Base class for HTML elements
- **`LeafNode`** - HTML elements with no children (e.g., `<b>`, `<a>`, `<img>`)
- **`ParentNode`** - HTML elements with children (e.g., `<div>`, `<p>`, `<ul>`)
- **`BlockType`** - Enum of markdown block types (paragraph, heading, quote, code, lists)

### Key Functions

- **`markdown_to_blocks(text)`** - Split markdown into blocks
- **`block_to_block_type(block)`** - Identify block type using regex
- **`text_to_textnodes(text)`** - Parse inline markdown into text nodes
- **`markdown_to_html_node(markdown)`** - Convert markdown to HTML node tree
- **`generate_page(from_path, template_path, to_path)`** - Generate single HTML page
- **`generate_all_pages(markdown_dir, template_path, public_dir)`** - Recursively generate all pages
- **`copy_directory_contents(src, dst)`** - Recursively copy directory contents

## Contributing

This is a learning project built as part of the [Boot.dev](https://www.boot.dev) static site generator course.

## License

This project is for educational purposes.

## Acknowledgments

Built following the curriculum from [Boot.dev's "Build a Static Site Generator" course](https://www.boot.dev/courses/build-static-site-generator-python).

