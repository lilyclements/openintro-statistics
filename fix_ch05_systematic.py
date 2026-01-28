#!/usr/bin/env python3
"""
Systematic LaTeX to PreTeXt XML conversion for ch05.ptx
"""

import re

def fix_ch05_systematic():
    with open('source/ch05.ptx', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    fixed_lines = []
    
    for i, line in enumerate(lines, 1):
        # Skip if line is too short
        if len(line) < 2:
            fixed_lines.append(line)
            continue
        
        # Fix unescaped < and > in XML
        # Only fix < that looks like comparison operators (not XML tags)
        # Pattern: n < or > number or variable
        line = re.sub(r'(?<![<&])<\s+(?=[\d\\])', '&lt; ', line)
        line = re.sub(r'(?<![>])\s+>(?=\s|$|;)', ' &gt;', line)
        
        # Fix LaTeX begin/end
        line = re.sub(r'\\begin\{center\}', '', line)
        line = re.sub(r'\\end\{center\}', '', line)
        line = re.sub(r'\\begin\{tabular\}[^}]*\}', '', line)
        line = re.sub(r'\\end\{tabular\}', '', line)
        line = re.sub(r'\\hline', '', line)
        
        # Fix \end{quote}
        line = re.sub(r'\}\s*\\end\{quote\}', '}', line)
        
        fixed_lines.append(line)
    
    with open('source/ch05.ptx', 'w', encoding='utf-8') as f:
        f.writelines(fixed_lines)
    
    print("Systematically fixed ch05.ptx")

if __name__ == '__main__':
    fix_ch05_systematic()
