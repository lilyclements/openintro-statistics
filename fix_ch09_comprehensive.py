#!/usr/bin/env python3
"""
Comprehensive post-processor for Chapter 9 XML
Fixes structural and content issues from LaTeX conversion
"""

import re

def fix_xml_comprehensive(content):
    """Apply comprehensive fixes to the XML content"""
    
    # 1. Fix unclosed math tags - find <m>text\ at end of line and close it
    content = re.sub(r'(<m>[^<]*?)\\(\s*\n)', r'\1</m>\2', content)
    
    # 2. Remove LaTeX commands that weren't properly converted
    content = re.sub(r'\\newpage\b', '', content)
    content = re.sub(r'\\vref\{[^}]+\}', '', content)
    content = re.sub(r'\\data\{([^}]+)\}', r'\1', content)
    content = re.sub(r'\\var\{([^}]+)\}', r'\1', content)
    content = re.sub(r'\\FigureFullPath\[[^\]]*\]\{[^}]*\}\{[^}]*\}', '[Figure]', content)
    
    # 3. Fix paragraph structures - close paragraphs before display math
    lines = content.split('\n')
    fixed_lines = []
    for i, line in enumerate(lines):
        # If line has unclosed <p> and next line starts with display math
        if '<p>' in line and not '</p>' in line and i + 1 < len(lines):
            next_line = lines[i + 1]
            if re.match(r'\s*<(me|md|mrow)>', next_line):
                line = line.rstrip() + '</p>'
        fixed_lines.append(line)
    content = '\n'.join(fixed_lines)
    
    # 4. Remove LaTeX table environments from exercises
    content = re.sub(r'\\begin\{center\}.*?\\end\{center\}', '', content, flags=re.DOTALL)
    content = re.sub(r'\\begin\{parts\}', '', content)
    content = re.sub(r'\\end\{parts\}', '', content)
    content = re.sub(r'\\begin\{tabular\}.*?\\end\{tabular\}', '', content, flags=re.DOTALL)
    
    # 5. Clean up \\item markers
    content = re.sub(r'^\s*\\item\s+', '', content, flags=re.MULTILINE)
    
    # 6. Remove R code comments (lines starting with %)
    content = re.sub(r'%[^\n]*\n', '\n', content)
    
    # 7. Fix broken references and indicators
    content = re.sub(r'\\multicolumn\{[^}]+\}\{[^}]+\}\{([^}]*)\}', r'\1', content)
    content = re.sub(r'\\cline\{[^}]+\}', '', content)
    content = re.sub(r'\\hline\b', '', content)
    
    # 8. Remove footnote commands
    content = re.sub(r'\\footnotesize\b', '', content)
    content = re.sub(r'\\footnotemark\{\}', '', content)
    content = re.sub(r'\\footnotetext\{', '', content)
    
    # 9. Clean up line breaks
    content = re.sub(r'\s*\\\\\s*', ' ', content)
    
    # 10. Fix double ampersands
    content = re.sub(r'&amp;amp;', '&amp;', content)
    
    # 11. Remove __MATH_DISPLAY__ placeholders
    content = re.sub(r'__MATH_DISPLAY_\d+__', '', content)
    
    # 12. Fix paragraphs that end with }
    content = re.sub(r'(\})\s*</p>', r'</p>', content)
    
    # 13. Remove stray closing braces in paragraphs
    content = re.sub(r'<p>\s*\}\s*</p>', '', content)
    
    # 14. Clean up LaTeX align environments that didn't convert
    content = re.sub(r'\balign\b', '', content)
    
    # 15. Remove empty paragraphs
    content = re.sub(r'<p>\s*</p>', '', content)
    
    # 16. Fix broken math with curly braces - convert {text} to subscript notation
    content = re.sub(r'incomever\{([^}]+)\}', r'\\text{income_ver}_{\\text{\1}}', content)
    content = re.sub(r'debttoincome', r'\\text{debt_to_income}', content)
    content = re.sub(r'creditutil', r'\\text{credit_util}', content)
    content = re.sub(r'creditchecks', r'\\text{credit_checks}', content)
    content = re.sub(r'issued\{([^}]+)\}', r'\\text{issued}_{\\text{\1}}', content)
    
    # 17. Fix special quote marks
    content = re.sub(r'"([^"]*?)"', r'"\1"', content)
    
    # 18. Clean up extra whitespace
    content = re.sub(r'\n\n\n+', '\n\n', content)
    
    return content

def main():
    input_file = 'source/ch09.ptx'
    
    print(f"Comprehensive Post-processing Chapter 9 XML")
    print(f"=" * 50)
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_lines = len(content.split('\n'))
    print(f"Original lines: {original_lines}")
    
    # Apply fixes
    content = fix_xml_comprehensive(content)
    
    # Write output
    with open(input_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    final_lines = len(content.split('\n'))
    print(f"Final lines: {final_lines}")
    print(f"Output: {input_file}")
    
    # Try to parse XML
    import xml.etree.ElementTree as ET
    try:
        tree = ET.parse(input_file)
        print("\n✓ XML is well-formed!")
        root = tree.getroot()
        
        # Count elements
        sections = root.findall('.//{*}section')
        subsections = root.findall('.//{*}subsection')
        examples = root.findall('.//{*}example')
        exercises = root.findall('.//{*}exercise')
        
        print(f"\n✓ Structure:")
        print(f"    Sections: {len(sections)}")
        print(f"    Subsections: {len(subsections)}")
        print(f"    Examples: {len(examples)}")
        print(f"    Exercises: {len(exercises)}")
        
    except ET.ParseError as e:
        print(f"\n✗ XML Parse Error: {e}")
        line_num = int(str(e).split('line ')[1].split(',')[0])
        lines = content.split('\n')
        print(f"\nContext around error (line {line_num}):")
        for i in range(max(0, line_num-3), min(len(lines), line_num+2)):
            print(f"  {i+1}: {lines[i][:100]}")
    
    print("=" * 50)

if __name__ == '__main__':
    main()
