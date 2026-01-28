#!/usr/bin/env python3
"""
Comprehensive LaTeX to PreTeXt XML conversion
"""

import re

def comprehensive_fix():
    with open('source/ch05.ptx', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace comparison operators < and >
    content = content.replace('n < 0.1', 'n &lt; 0.1')
    content = content.replace('< 0.1', '&lt; 0.1')
    content = content.replace('n (1-p) < 10', 'n (1-p) &lt; 10')
    content = content.replace('np < 10', 'np &lt; 10')
    
    # Fix LaTeX environments  
    content = re.sub(r'\\begin\{center\}.*?\\end\{center\}', '', content, flags=re.DOTALL)
    content = re.sub(r'\\begin\{tabular\}[^}]*?\}.*?\\end\{tabular\}', '', content, flags=re.DOTALL)
    content = re.sub(r'\}\s*\\end\{quote\}', '}', content)
    
    with open('source/ch05.ptx', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Applied comprehensive fixes to ch05.ptx")

if __name__ == '__main__':
    comprehensive_fix()
