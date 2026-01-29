# Chapter 2 Conversion Guide

## Quick Reference for Completing the Conversion

### Source Files
- **LaTeX source:** `latex/ch_summarizing_data/TeX/ch_summarizing_data.tex` (2579 lines)
- **Current PreTeXt:** `source/ch02.ptx` (660 lines - mostly exercises)
- **Backup:** `source/ch02.ptx.backup`
- **Partial new version:** `/tmp/ch02_partial.ptx` (345 lines with first 2 subsections)

### LaTeX Line Ranges for Each Subsection

#### Section 2.1: Examining numerical data (lines 26-1322)
| Subsection | Lines | Status | Key Content |
|------------|-------|--------|-------------|
| 2.1.1 Scatterplots | 73-166 | ✅ DONE | 2 figures, 1 example, 2 exercises |
| 2.1.2 Dot plots & mean | 167-435 | ✅ DONE | 2 figures, 5 exercises/examples, mean formula |
| 2.1.3 Histograms | 436-649 | ❌ TODO | 3 figures, skewness, modes, 4 exercises |
| 2.1.4 Variance & SD | 650-818 | ❌ TODO | Variance, SD, empirical rule, 3 figures |
| 2.1.5 Box plots | 819-985 | ❌ TODO | Median, quartiles, IQR, box plots, 5 exercises |
| 2.1.6 Robust stats | 986-1094 | ❌ TODO | Robustness comparison, 3 examples |
| 2.1.7 Transformations | 1095-1206 | ❌ TODO | Log transforms, 4 figures |
| 2.1.8 Mapping | 1207-1322 | ❌ TODO | Intensity maps, 7 county map figures |

#### Section 2.2: Considering categorical data (lines 1323-2165)
| Subsection | Lines | Status | Key Content |
|------------|-------|--------|-------------|
| 2.2.1 Contingency tables | 1344-1460 | ❌ TODO | Tables, bar plots, 2 examples |
| 2.2.2 Proportions | 1461-1700 | ❌ TODO | Row/column proportions, 4 figures |
| 2.2.3 Bar plots (2 vars) | 1701-1871 | ❌ TODO | Grouped/stacked bars, 3 figures |
| 2.2.4 Mosaic plots | 1872-1969 | ❌ TODO | Mosaic visualization, 2 figures |
| 2.2.5 Pie charts | 1970-2002 | ❌ TODO | When to use pies, 1 figure |
| 2.2.6 Comparing groups | 2003-2144 | ❌ TODO | Box plots by category, 3 figures |

### Common LaTeX → PreTeXt Conversions

#### Text Formatting
```
LaTeX                   PreTeXt
\term{...}         →    <term>...</term>
\emph{...}         →    <em>...</em>
\textbf{...}       →    <strong>...</strong>
\var{...}          →    <c>...</c>
\data{...}         →    <c>...</c>
```

#### Math
```
LaTeX                   PreTeXt
$...$              →    <m>...</m>
\begin{align*}     →    <md><mrow>
x\us{}rate         →    x_rate  (underscore)
\$100              →    $100    (dollar sign)
\%                 →    %       (percent)
```

#### Structures
```
LaTeX                               PreTeXt
\begin{figure}                 →    <figure xml:id="...">
  \Figure[desc]{size}{name}    →      <image source="path" width="...">
  \caption{...}                →        <description>...</description>
\end{figure}                   →      </image>
                                     <caption>...</caption>
                                   </figure>

\begin{examplewrap}            →    <example xml:id="...">
\begin{nexample}{statement}    →      <title>...</title>
  solution                     →      <statement><p>...</p></statement>
\end{nexample}                 →      <solution><p>...</p></solution>
\end{examplewrap}              →    </example>

\begin{exercisewrap}           →    <exercise xml:id="...">
\begin{nexercise}              →      <title>...</title>
  question\footnotemark{}      →      <statement><p>...</p></statement>
\end{nexercise}                →      <solution><p>...</p></solution>
\end{exercisewrap}             →    </exercise>
\footnotetext{answer}

\begin{onebox}{title}          →    <assemblage>
  content                      →      <title>...</title>
\end{onebox}                   →      <p>...</p>
                                   </assemblage>
```

#### Figures Path Mapping
LaTeX figure references like `{loan50_amt_vs_income}` should map to:
```
<image source="ch_summarizing_data/figures/loan50_amt_vs_income/loan50_amt_vs_income.png" width="80%">
```

Check `latex/ch_summarizing_data/figures/` directory for actual figure locations.

### Conversion Workflow

For each subsection:

1. **Extract LaTeX content**
   ```bash
   sed -n '436,649p' latex/ch_summarizing_data/TeX/ch_summarizing_data.tex > /tmp/subsection.tex
   ```

2. **Convert text** (use `/tmp/convert_ch02.py` as starting point)

3. **Handle figures**
   - Find figure in `latex/ch_summarizing_data/figures/`
   - Extract alt text from `\Figure[...]` first parameter
   - Create `<figure>` with proper `<image>` and `<description>`

4. **Convert examples**
   - Extract statement from `\begin{nexample}{...}`
   - Extract solution from body
   - Create `<example>` with `<statement>` and `<solution>`

5. **Convert exercises**
   - Extract question
   - Find corresponding `\footnotetext{...}` for answer
   - Create `<exercise>` with proper structure

6. **Convert special boxes**
   - `\begin{onebox}` → `<assemblage>`
   - Preserve important definitions

7. **Test build**
   ```bash
   pretext build web
   ```

### XML IDs Convention
Use kebab-case for IDs:
- Figures: `fig-name-of-figure`
- Examples: `ex-short-description`
- Exercises: `ex-short-description`  
- Subsections: `subsec-short-name`
- Assemblages: `def-concept-name` or `assemblage-title`

### Testing Checklist
After converting each subsection:
- [ ] All figures display correctly
- [ ] All math renders properly
- [ ] All examples have solutions
- [ ] All exercises have solutions
- [ ] Cross-references work
- [ ] No XML errors in build

### Integration Steps (After All Conversions Complete)
1. Take `/tmp/ch02_partial.ptx` as base
2. Add remaining subsections 2.1.3 through 2.1.8
3. Add Section 2.2 content (all subsections)
4. Copy Section 2.3 (Malaria vaccine) from lines 22-242 of backup
5. Integrate existing exercises from backup file:
   - Lines 354-563: Section 2.1 exercises (goes after 2.1.8)
   - Lines 243-353: Section 2.2 exercises (goes after 2.2.6)
6. Copy Section 2.4 (Review) from lines 564-660 of backup
7. Test complete file build

### Common Issues to Watch
- **Unclosed tags:** Every `<p>` needs `</p>`, etc.
- **Special characters:** `&` must be `&amp;`, `<` must be `&lt;`, `>` must be `&gt;`
- **Math mode:** Don't put `<m>` inside `<c>` or vice versa
- **Figure paths:** Verify actual file exists in `source/images/ch_summarizing_data/figures/...`
- **Cross-references:** Use `<xref ref="..."/>` not `\ref{...}`

### Estimated Time Per Subsection
- Small subsection (~100 lines LaTeX): 1-1.5 hours
- Medium subsection (~150 lines LaTeX): 1.5-2 hours
- Large subsection (~200+ lines LaTeX): 2-3 hours

**Total remaining:** approximately 12-15 hours of focused work

### Resources
- PreTeXt Guide: https://pretextbook.org/doc/guide/html/
- PreTeXt examples: Check `source/ch01.ptx` for patterns
- LaTeX source: `latex/ch_summarizing_data/TeX/ch_summarizing_data.tex`
- Figures directory: `latex/ch_summarizing_data/figures/`
