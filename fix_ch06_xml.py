#!/usr/bin/env python3
"""
Post-processor to fix XML well-formedness issues in ch06.ptx
"""

import re

def fix_xml(content):
    """Fix common XML issues"""
    
    # Fix unescaped & in single-line math equations (me tags)
    # These are alignment characters that should be removed for single-line equations
    def fix_me_ampersands(match):
        me_content = match.group(1)
        # Remove alignment & characters but preserve &amp;
        me_content = re.sub(r'(?<!&)\s*&\s*(?!amp;)', ' ', me_content)
        return f'<me>{me_content}</me>'
    
    content = re.sub(r'<me>(.*?)</me>', fix_me_ampersands, content, flags=re.DOTALL)
    
    # Fix incomplete example titles - look for pattern like "826{" at end of title
    content = re.sub(r'<title>([^<]*?)\{</title>', r'<title>\1</title>', content)
    
    # Remove \footnotetext{ commands that appear in paragraphs
    content = re.sub(r'<p>\\footnotetext\{([^}]+)\}</p>', r'<!-- Footnote: \1 -->', content)
    
    # Fix incomplete chapter references
    content = re.sub(r'Chapter \\ref\{([^}]+)\}', r'<xref ref="\1"/>', content)
    
    # Clean up unconverted LaTeX environments that appear inline
    # Remove \begin{center} and \end{center}
    content = re.sub(r'\\begin\{center\}', '', content)
    content = re.sub(r'\\end\{center\}', '', content)
    
    # Fix eqnarray* environments - convert to md (multi-line display)
    def convert_eqnarray(match):
        eqn_content = match.group(1)
        # Remove alignment & but keep as separator
        lines = []
        for line in eqn_content.split('\\\\'):
            line = line.strip()
            if line:
                # Remove & alignment markers
                line = re.sub(r'\s*&\s*', ' ', line)
                if line:
                    lines.append(f'          <mrow>{line}</mrow>')
        if lines:
            return '<md>\n' + '\n'.join(lines) + '\n        </md>'
        return ''
    
    content = re.sub(r'\\begin\{eqnarray\*\}(.*?)\\end\{eqnarray\*\}', 
                     convert_eqnarray, content, flags=re.DOTALL)
    
    # Fix any remaining unexpanded macro patterns
    # Replace common patterns with placeholders
    content = re.sub(r'\\paydayN\{\}', '826', content)
    content = re.sub(r'\\paydayNHalf\{\}', '413', content)  
    content = re.sub(r'\\paydayRegProp\{\}', '0.70', content)
    content = re.sub(r'\\paydayRegSE\{\}', '0.016', content)
    content = re.sub(r'\\paydayCCSE\{\}', '0.0174', content)
    content = re.sub(r'\\paydayCCProp\{\}', '0.51', content)
    content = re.sub(r'\\paydayCCZ\{\}', '0.57', content)
    content = re.sub(r'\\paydayCCOneTail\{\}', '0.2776', content)
    content = re.sub(r'\\paydayCCPvalue\{\}', '0.5552', content)
    
    # Fix macro patterns that have trailing text
    content = re.sub(r'826Half', '413', content)
    
    # Clean up summary commands
    content = re.sub(r'\\onepropconfintsummary\{\}', '<!-- One proportion CI summary box -->', content)
    content = re.sub(r'\\oneprophtsummary\{\}', '<!-- One proportion HT summary box -->', content)
    content = re.sub(r'\\CalculatorVideos\{([^}]+)\}', r'<!-- Calculator video: \1 -->', content)
    
    # Clean up oiRedirect commands  
    content = re.sub(r'\\oiRedirect\{([^}]+)\}\s*\{([^}]+)\}', r'<url href="\2">\1</url>', content)
    
    # Remove \D{} commands (page break hints)
    content = re.sub(r'\\D\{[^}]*\}', '', content)
    
    # Fix broken example structures - remove closing } that appear after title
    # Pattern: </title>\n<p>text...} should be </title>\n<p>text...</p>
    content = re.sub(r'(<title>[^<]+</title>\s*<p>[^}]+)\}', r'\1</p>\n      <p>', content)
    
    # Clean up any stray LaTeX commands left in text
    content = re.sub(r'\\setlength\{[^}]+\}\{[^}]+\}', '', content)
    content = re.sub(r'\\vspace\{[^}]+\}', '', content)
    content = re.sub(r'\\hspace\{[^}]+\}', '', content)
    
    # Fix \resp{} that might have been missed
    content = re.sub(r'\\resp\{([^}]+)\}', r'"\1"', content)
    
    # Fix \Figures commands (these are figure references with alt text)
    content = re.sub(r'\\Figures\[([^\]]+)\]\{[^}]*\}\{([^}]+)\}\{([^}]+)\}', 
                     r'<!-- Figure: \2 - \1 -->', content)
    
    return content

def main():
    input_file = 'source/ch06.ptx'
    output_file = 'source/ch06.ptx'
    
    print("Post-processing ch06.ptx to fix XML issues...")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"  Original size: {len(content)} characters")
    
    fixed_content = fix_xml(content)
    
    print(f"  Fixed size: {len(fixed_content)} characters")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    
    print(f"  Written to: {output_file}")
    print("Done!")

if __name__ == '__main__':
    main()
