#!/usr/bin/env python3
"""
Post-processor for Chapter 9 XML to fix conversion issues
"""

import re

def fix_xml(content):
    """Apply fixes to the XML content"""
    
    # Fix __MATH_DISPLAY_0__ and similar placeholders
    content = re.sub(r'__MATH_DISPLAY_\d+__', '', content)
    
    # Remove stray closing braces
    content = re.sub(r'^\s*<p>\}</p>\s*$', '', content, flags=re.MULTILINE)
    
    # Fix unclosed figure captions with LaTeX code
    content = re.sub(r'<caption>First six rows from the \\data\{loans\}</caption>', 
                     '<caption>First six rows from the loans data set</caption>', content)
    
    # Remove remaining LaTeX table environments from exercises (they should be converted or removed)
    # Pattern: \begin{center} ... \end{center} blocks within <p> tags
    content = re.sub(r'\\begin\{center\}.*?\\end\{center\}', '', content, flags=re.DOTALL)
    
    # Remove \begin{parts} and \end{parts} and \item
    content = re.sub(r'\\begin\{parts\}', '', content)
    content = re.sub(r'\\end\{parts\}', '', content)
    content = re.sub(r'\\item\s+', '', content)
    
    # Remove LaTeX commands that weren't converted
    content = re.sub(r'\\newpage', '', content)
    content = re.sub(r'\\vref\{[^}]+\}', '', content)
    content = re.sub(r'\\var\{([^}]+)\}', r'\1', content)
    content = re.sub(r'\\data\{([^}]+)\}', r'\1', content)
    content = re.sub(r'\\FigureFullPath\[[^\]]*\]\{[^}]*\}\{[^}]*\}', '', content)
    
    # Clean up any remaining LaTeX macros
    content = re.sub(r'\\[a-zA-Z]+\{([^}]*)\}', r'\1', content)
    
    # Fix multicolumn in tables - just remove it
    content = re.sub(r'\\multicolumn\{[^}]+\}\{[^}]+\}\{([^}]*)\}', r'\1', content)
    content = re.sub(r'\\cline\{[^}]+\}', '', content)
    content = re.sub(r'\\hline', '', content)
    
    # Remove footnotesize, footnotetext
    content = re.sub(r'\\footnotesize', '', content)
    content = re.sub(r'\\footnotemark\{\}', '', content)
    content = re.sub(r'\\footnotetext\{', '', content)
    
    # Clean up empty paragraphs
    content = re.sub(r'<p>\s*</p>', '', content)
    
    # Clean up paragraphs with only whitespace and punctuation
    content = re.sub(r'<p>\s*[\\,.\s]*\s*</p>', '', content)
    
    # Remove \\ line breaks
    content = re.sub(r'\s*\\\\\s*', ' ', content)
    
    # Fix amp; that should be &amp;
    content = re.sub(r'&amp;amp;', '&amp;', content)
    
    # Remove R code comments (start with %)
    content = re.sub(r'%[^\n]*', '', content)
    
    # Fix < and > that aren't XML tags (need to be escaped)
    # This is tricky - we need to escape < and > that are NOT part of XML tags
    # For now, let's escape common cases like <- in R code
    content = re.sub(r'(?<!</)(?<!<)([-+*/]\s*<-?\s*[0-9])', lambda m: m.group(1).replace('<', '&lt;'), content)
    
    return content

def main():
    input_file = 'source/ch09.ptx'
    output_file = 'source/ch09.ptx'
    
    print(f"Post-processing Chapter 9 XML")
    print(f"=" * 50)
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_lines = len(content.split('\n'))
    
    # Apply fixes
    content = fix_xml(content)
    
    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    final_lines = len(content.split('\n'))
    
    print(f"Original lines: {original_lines}")
    print(f"Final lines: {final_lines}")
    print(f"Output: {output_file}")
    print("=" * 50)

if __name__ == '__main__':
    main()
