# Chapter 2 Conversion Status and Plan

## Overview
Chapter 2 requires converting ~1600 lines of LaTeX content to PreTeXt format to match the LaTeX version verbatim.

## Current Structure (INCORRECT - needs reorganization)
The current ch02.ptx has sections in wrong order:
1. Section 2.1: Case study: Malaria vaccine (should be 2.3)
2. Section 2.2: Considering categorical data (only exercises, missing content)
3. Section 2.3: Examining numerical data (only exercises, missing content)
4. Section 2.4: Review exercises

## Required Structure (from LaTeX)
1. Section 2.1: Examining numerical data (lines 26-1322 in LaTeX, ~1300 lines)
2. Section 2.2: Considering categorical data (lines 1323-2165 in LaTeX, ~300 lines)
3. Section 2.3: Case study: Malaria vaccine (lines 2166+ in LaTeX)
4. Section 2.4: Review exercises

## Section 2.1: Examining numerical data
### Subsections Needed:
1. ✅ **2.1.1 Scatterplots for paired data** (lines 73-166) - CONVERTED
   - Introduction to scatterplots
   - Figure: loan50_amt_vs_income
   - Example: nonlinear relationship
   - Figure: median income vs poverty
   - 2 exercises with solutions

2. ✅ **2.1.2 Dot plots and the mean** (lines 167-435) - CONVERTED
   - Dot plot introduction
   - Figures: loan interest rate dot plots (regular and stacked)
   - Mean definition and calculation
   - Sample mean vs population mean (μ)
   - 2 exercises on notation
   - 3 detailed examples (estimating population mean, comparison uses, weighted means)

3. ❌ **2.1.3 Histograms and shape** (lines 436-649) - NOT STARTED
   - Binning and histograms
   - Figure: binned interest rate table
   - Figure: histogram of interest rates
   - Skewness (right skewed, left skewed, symmetric)
   - Long tail definition box
   - Modes (unimodal, bimodal, multimodal)
   - Figure: modal examples
   - 3 exercises with solutions

4. ❌ **2.1.4 Variance and standard deviation** (lines 650-818) - NOT STARTED
   - Deviation from the mean
   - Variance calculation
   - Standard deviation definition
   - Empirical rule (68-95-99.7)
   - Figure: SD rule visualization
   - Multiple examples and exercises

5. ❌ **2.1.5 Box plots, quartiles, and the median** (lines 819-985) - NOT STARTED
   - Median definition
   - Quartiles (Q1, Q3)
   - IQR calculation
   - Box plot construction
   - Whiskers and outliers
   - Figure: box plot examples
   - Multiple exercises

6. ❌ **2.1.6 Robust statistics** (lines 986-1094) - NOT STARTED
   - Robustness definition
   - Comparing mean vs median
   - Comparing SD vs IQR
   - Examples with outliers
   - Exercises

7. ❌ **2.1.7 Transforming data (special topic)** (lines 1095-1206) - NOT STARTED
   - Log transformations
   - When to use transformations
   - County population examples
   - Figures showing transformed data

8. ❌ **2.1.8 Mapping data (special topic)** (lines 1207-1322) - NOT STARTED
   - Intensity maps
   - Geographic visualization
   - Multiple county map figures

9. ❌ **2.1.9 End-of-section exercises** - EXIST IN CURRENT FILE
   - Need to keep existing exercises from lines 354-563 of current file

## Section 2.2: Considering categorical data  
### Subsections Needed:
1. ❌ **2.2.1 Contingency tables and bar plots** (lines 1344-1460) - NOT STARTED
2. ❌ **2.2.2 Row and column proportions** (lines 1461-1700) - NOT STARTED
3. ❌ **2.2.3 Using a bar plot with two variables** (lines 1701-1871) - NOT STARTED
4. ❌ **2.2.4 Mosaic plots** (lines 1872-1969) - NOT STARTED
5. ❌ **2.2.5 The only pie chart you will see in this book** (lines 1970-2002) - NOT STARTED
6. ❌ **2.2.6 Comparing numerical data across groups** (lines 2003-2144) - NOT STARTED
7. ❌ **2.2.7 End-of-section exercises** - EXIST IN CURRENT FILE
   - Need to keep existing exercises from lines 243-353 of current file

## Section 2.3: Case study malaria vaccine
- ✅ Already exists in current file (lines 22-242)
- Just needs to be moved to correct position (after 2.1 and 2.2)

## Section 2.4: Review exercises
- ✅ Already exists in current file (lines 564-660)
- Keep in place

## Completion Status
- **Completed:** 2 of 14 subsections (14%)
- **Remaining:** 12 subsections (86%)
- **Estimated work:** 12-15 hours for complete conversion

## Files
- **Original:** `source/ch02.ptx.backup`
- **LaTeX source:** `latex/ch_summarizing_data/TeX/ch_summarizing_data.tex`
- **Partial new version:** `/tmp/ch02_partial.ptx` (has first 2 subsections of 2.1)

## Next Steps
1. Continue converting remaining 6 subsections of Section 2.1
2. Convert all 6 subsections of Section 2.2
3. Reorganize sections to correct order
4. Merge existing exercises into appropriate locations
5. Test PreTeXt build
6. Validate all conversions

## Conversion Patterns Established
✅ LaTeX `\term{}` → PreTeXt `<term>`
✅ LaTeX `\var{}` and `\data{}` → PreTeXt `<c>`
✅ LaTeX `$...$` → PreTeXt `<m>...</m>`
✅ LaTeX `\begin{align*}` → PreTeXt `<md><mrow>`
✅ LaTeX figures → PreTeXt `<figure>` with accessibility descriptions
✅ LaTeX examples → PreTeXt `<example>` with statement/solution
✅ LaTeX exercises → PreTeXt `<exercise>` with statement/solution
✅ LaTeX boxes → PreTeXt `<assemblage>`
