#!/usr/bin/env python3
"""
Comprehensive LaTeX to PreTeXt XML conversion
Handles: $...$, aligned equations, unescaped < >, LaTeX environments
"""

import re

def comprehensive_fix():
    with open('source/ch05.ptx', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Replace aligned equations <me>...&...&...</me> with <md><mrow>...</mrow><mrow>...</mrow></md>
    def fix_aligned_me_tags(match):
        inner = match.group(1)
        if '&' in inner and '<mrow>' not in inner:
            # Split by & and create mrows
            parts = inner.split('&')
            mrows = []
            for part in parts:
                part = part.strip()
                if part:
                    # Replace & with \amp if it's an alignment operator
                    part = part.replace('= ', '= ')
                    mrows.append(f'          <mrow>{part}</mrow>')
            if len(mrows) > 1:
                return f'        <md>\n' + '\n'.join(mrows) + '\n        </md>'
        return match.group(0)
    
    # First fix <me> tags with multiple & (aligned equations)
    content = re.sub(r'<me>([^<]*?&[^<]*?&[^<]*?)</me>', fix_aligned_me_tags, content, flags=re.DOTALL)
    
    # 2. Fix unescaped < and > that are comparison operators
    # Pattern: "n <" or "< 0.1" or "> 10" 
    content = re.sub(r'(?<![&<])\s+<\s+(?=[\d\w\\])', r' &lt; ', content)
    content = re.sub(r'(?<![&>])\s+>\s+(?=[\d\w\\])', r' &gt; ', content)
    content = re.sub(r'(?<![&<])\s+<\s+(?=0\.)', r' &lt; ', content)
    content = re.sub(r'(?<![&>])>\s+$', r' &gt;', content, flags=re.MULTILINE)
    
    # 3. Fix LaTeX environments
    content = re.sub(r'\\begin\{center\}.*?\\end\{center\}', '', content, flags=re.DOTALL)
    content = re.sub(r'\\begin\{tabular\}[^}]*\}.*?\\end\{tabular\}', '', content, flags=re.DOTALL)
    content = re.sub(r'\}\s*\\end\{quote\}', '}', content)
    content = re.sub(r'\\hline\s*', '', content)
    
    # 4. Fix \geq and \leq
    content = re.sub(r'\\geq', ' \\geq ', content)
    content = re.sub(r'\\leq', ' \\leq ', content)
    
    with open('source/ch05.ptx', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Applied comprehensive LaTeX to PreTeXt fixes")

if __name__ == '__main__':
    comprehensive_fix()
