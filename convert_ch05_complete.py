#!/usr/bin/env python3
"""
Comprehensive conversion of Chapter 5 (Foundations for Inference) from LaTeX to PreTeXt.
This script converts the main chapter file and integrates content from section files.
"""

import re
import os

def convert_latex_commands(text):
    """Convert LaTeX commands to PreTeXt equivalents."""
    
    # Convert \emph{...} to <em>...</em>
    text = re.sub(r'\\emph\{([^}]+)\}', r'<em>\1</em>', text)
    
    # Convert \term{...} to <term>...</term>
    text = re.sub(r'\\term\{([^}]+)\}', r'<term>\1</term>', text)
    
    # Convert \texttt{...} to <c>...</c> (code/monospace)
    text = re.sub(r'\\texttt\{([^}]+)\}', r'<c>\1</c>', text)
    
    # Convert \textbf{...} to <strong>...</strong>
    text = re.sub(r'\\textbf\{([^}]+)\}', r'<strong>\1</strong>', text)
    
    # Handle \R{} command for R software
    text = text.replace(r'\R{}', 'R')
    
    # Remove \index{...} commands
    text = re.sub(r'\\index\{[^}]*\}', '', text)
    
    # Convert \footnote{...} to <fn>...</fn>
    text = re.sub(r'\\footnote\{([^}]+)\}', r'<fn>\1</fn>', text)
    
    # Convert inline math $ ... $
    text = re.sub(r'\$([^$]+)\$', r'<m>\1</m>', text)
    
    # Handle displayed math environments
    text = re.sub(r'\\begin\{align\*\}(.*?)\\end\{align\*\}', 
                  lambda m: '<md>' + m.group(1) + '</md>', 
                  text, flags=re.DOTALL)
    
    text = re.sub(r'\\begin\{align\}(.*?)\\end\{align\}', 
                  lambda m: '<md>' + m.group(1) + '</md>', 
                  text, flags=re.DOTALL)
    
    text = re.sub(r'\\begin\{eqnarray\*\}(.*?)\\end\{eqnarray\*\}', 
                  lambda m: '<md>' + m.group(1) + '</md>', 
                  text, flags=re.DOTALL)
    
    # Convert enumerate/itemize to lists
    text = re.sub(r'\\begin\{enumerate\}\[(a\.\)\]', '<ol marker="a">', text)
    text = text.replace(r'\end{enumerate}', '</ol>')
    text = re.sub(r'\\begin\{itemize\}', '<ul>', text)
    text = text.replace(r'\end{itemize}', '</ul>')
    text = re.sub(r'\\item\s+', '<li>', text)
    text = text.replace('</li>\n<li>', '</li>\n<li>')
    text = re.sub(r'<li>([^\n]*)\n', r'<li>\1</li>\n', text)
    
    # Convert \label{...} to xml:id
    # (These are already handled in section structure)
    text = re.sub(r'\\label\{([^}]+)\}', '', text)
    
    # Remove backslashes before special characters
    text = text.replace('\\&', '&amp;')
    text = text.replace('\\%', '%')
    text = text.replace('\\$', '$')
    text = text.replace('\\#', '#')
    text = text.replace('\\{', '{')
    text = text.replace('\\}', '}')
    
    # Convert ~  (non-breaking space) to regular space
    text = text.replace('~', ' ')
    
    # Remove %% comments and % single-line comments
    text = re.sub(r'%.*?$', '', text, flags=re.MULTILINE)
    
    # Clean up excessive whitespace
    text = re.sub(r'\n\s*\n\s*\n', '\n\n', text)
    text = text.strip()
    
    return text

def create_pretext_chapter():
    """Create the complete PreTeXt chapter 5 file."""
    
    chapter_intro = """<?xml version="1.0" encoding="UTF-8"?>
<chapter xml:id="ch-foundations-for-inference" xmlns:xi="http://www.w3.org/2001/XInclude">
  <title>Foundations for Inference</title>
  
  <introduction>
    <p>
      Statistical inference is primarily concerned with understanding and quantifying the
      uncertainty of parameter estimates. While the equations and details change depending on
      the setting, the foundations for inference are the same throughout all of statistics.
    </p>
    
    <p>
      We start with a familiar topic: the idea of using a sample proportion to estimate
      a population proportion. Next, we create what's called a <term>confidence interval</term>,
      which is a range of plausible values where we may find the true population value.
      Finally, we introduce the <term>hypothesis testing framework</term>, which allows us to
      formally evaluate claims about the population, such as whether a survey provides strong
      evidence that a candidate has the support of a majority of the voting population.
    </p>
  </introduction>
  
  <!-- Section 1: Point Estimates and Sampling Variability -->
  <section xml:id="sec-point-estimates">
    <title>Point Estimates and Sampling Variability</title>
    
    <introduction>
      <p>
        Companies such as Pew Research frequently conduct polls as a way to understand the
        state of public opinion or knowledge on many topics, including politics, scientific
        understanding, brand recognition, and more. The ultimate goal in taking a poll is
        generally to use the responses to estimate the opinion or knowledge of the broader
        population.
      </p>
    </introduction>
    
    <subsection xml:id="subsec-point-estimates-error">
      <title>Point Estimates and Error</title>
      
      <p>
        Suppose a poll suggested the US President's approval rating is 45%. We would consider
        45% to be a <term>point estimate</term> of the approval rating we might see if we
        collected responses from the entire population. This entire-population response
        proportion is generally referred to as the <term>parameter of interest</term>.
      </p>
      
      <p>
        When the parameter is a proportion, it is often denoted by <m>p</m>, and we often
        refer to the sample proportion as <m>\hat{p}</m> (pronounced <em>p-hat</em>). Unless
        we collect responses from every individual in the population, <m>p</m> remains
        unknown, and we use <m>\hat{p}</m> as our estimate of <m>p</m>. The difference we
        observe from the poll versus the parameter is called the <term>error</term> in the
        estimate.
      </p>
      
      <p>
        Generally, the error consists of two aspects: <term>sampling error</term> and
        <term>bias</term>.
      </p>
      
      <definition>
        <statement>
          <p>
            <term>Sampling error</term>, sometimes called <em>sampling uncertainty</em>,
            describes how much an estimate will tend to vary from one sample to the next.
            For instance, the estimate from one sample might be 1% too low while in another
            it may be 3% too high. The <term>sample size</term> is often represented by the
            letter <m>n</m>.
          </p>
        </statement>
      </definition>
      
      <definition>
        <statement>
          <p>
            <term>Bias</term> describes a systematic tendency to over- or under-estimate
            the true population value. We try to minimize bias through thoughtful data
            collection procedures.
          </p>
        </statement>
      </definition>
    </subsection>
    
    <subsection xml:id="subsec-variability-point-estimate">
      <title>Understanding the Variability of a Point Estimate</title>
      
      <p>
        To understand how a sample proportion behaves, consider a scenario where the
        proportion of American adults who support expanding solar energy is <m>p = 0.88</m>.
        If we were to take a poll of 1000 American adults on this topic, how close might we
        expect the sample proportion to be to 0.88?
      </p>
      
      <p>
        We can simulate responses we would get from a simple random sample of 1000 American
        adults through the following steps:
      </p>
      
      <ol>
        <li>Create a set of entries representing all American adults, where 88% say "support"
            and 12% say "not".</li>
        <li>Mix up the entries and pull out 1000 entries to represent our sample.</li>
        <li>Compute the fraction that say "support".</li>
      </ol>
      
      <p>
        If we conduct this simulation 10,000 times, we create a <term>sampling distribution</term>
        of the sample proportions. This distribution has important characteristics:
      </p>
      
      <ul>
        <li><strong>Center:</strong> The center of the distribution equals the population proportion.</li>
        <li><strong>Spread:</strong> The standard deviation is called the <term>standard error (SE)</term>.</li>
        <li><strong>Shape:</strong> The distribution is approximately normal (bell-shaped).</li>
      </ul>
      
      <important>
        <p>
          Sampling distributions are never observed in practice, but we keep them in mind
          as they help us understand and characterize the point estimates we do observe.
        </p>
      </important>
    </subsection>
    
    <subsection xml:id="subsec-central-limit-theorem">
      <title>Central Limit Theorem</title>
      
      <theorem xml:id="thm-central-limit-theorem">
        <statement>
          <p>
            When observations are independent and the sample size is sufficiently large,
            the sample proportion <m>\hat{p}</m> will tend to follow a normal distribution with:
          </p>
          <md>
            \mu_{\hat{p}} = p \qquad\text{and}\qquad SE_{\hat{p}} = \sqrt{\frac{p(1-p)}{n}}
          </md>
          <p>
            The sample size is typically considered sufficiently large when <m>np \geq 10</m> and
            <m>n(1-p) \geq 10</m>, which is called the <term>success-failure condition</term>.
          </p>
        </statement>
      </theorem>
      
      <p>
        The Central Limit Theorem is incredibly important and provides a foundation for much
        of statistics. Be mindful of the two technical conditions: the observations must be
        independent, and the sample size must be sufficiently large.
      </p>
    </subsection>
    
    <subsection xml:id="subsec-clt-real-world">
      <title>Applying the Central Limit Theorem to Real-World Settings</title>
      
      <p>
        When we don't know the population proportion and must use <m>\hat{p}</m> in place
        of <m>p</m>, we use the <term>substitution approximation</term> (also called the
        <em>plug-in principle</em>). This allows us to estimate the standard error:
      </p>
      
      <md>
        SE_{\hat{p}} \approx \sqrt{\frac{\hat{p}(1-\hat{p})}{n}}
      </md>
      
      <p>
        We also use <m>\hat{p}</m> in place of <m>p</m> when checking the success-failure
        condition in practical applications where we don't know the true population proportion.
      </p>
    </subsection>
    
    <subsection xml:id="subsec-extending-framework">
      <title>Extending the Framework for Other Statistics</title>
      
      <p>
        The strategy of using a sample statistic to estimate a parameter is quite common and
        can be applied to other statistics besides a proportion. For instance, to estimate
        the average salary for graduates from a particular college, we could survey a random
        sample of recent graduates and use the sample mean <m>\bar{x}</m> to estimate the
        population mean <m>\mu</m>.
      </p>
      
      <p>
        The principles and general ideas are the same across different contexts, even if
        the details change. While this chapter emphasizes a single proportion context, these
        methods will be applied to many different contexts throughout this book.
      </p>
    </subsection>
  </section>
  
  <!-- Section 2: Confidence Intervals -->
  <section xml:id="sec-confidence-intervals">
    <title>Confidence Intervals for a Proportion</title>
    
    <introduction>
      <p>
        The sample proportion <m>\hat{p}</m> provides a single plausible value for the
        population proportion <m>p</m>. However, the sample proportion isn't perfect and
        will have some standard error associated with it. When stating an estimate for the
        population proportion, it is better practice to provide a plausible range of values
        instead of supplying just the point estimate.
      </p>
    </introduction>
    
    <subsection xml:id="subsec-capturing-parameter">
      <title>Capturing the Population Parameter</title>
      
      <p>
        A <term>confidence interval</term> is a range of plausible values where we are
        likely to find the population parameter. Using a confidence interval is like fishing
        with a net instead of a spear: we have a good chance of catching the fish.
      </p>
    </subsection>
    
    <subsection xml:id="subsec-95-ci">
      <title>Constructing a 95% Confidence Interval</title>
      
      <p>
        Our sample proportion <m>\hat{p}</m> is the most plausible value of the population
        proportion, so it makes sense to build a confidence interval around this point estimate.
        The standard error provides a guide for how large we should make the confidence interval.
      </p>
      
      <p>
        In a normal distribution, 95% of the data is within 1.96 standard deviations of the mean.
        Using this principle, we can construct a confidence interval that extends 1.96 standard
        errors from the sample proportion to be 95% confident that the interval captures the
        population proportion:
      </p>
      
      <md>
        \text{point estimate} \pm 1.96 \times SE = \hat{p} \pm 1.96 \times \sqrt{\frac{p(1-p)}{n}}
      </md>
      
      <p>
        When we say we are 95% confident, we mean: suppose we took many samples and built a
        95% confidence interval from each. Then about 95% of those intervals would contain
        the parameter, <m>p</m>.
      </p>
      
      <definition>
        <statement>
          <p>
            A <term>95% confidence interval</term> for a parameter is constructed as:
          </p>
          <md>
            \text{point estimate} \pm 1.96 \times SE
          </md>
          <p>
            This confidence interval accounts for sampling error but not bias.
          </p>
        </statement>
      </definition>
    </subsection>
    
    <subsection xml:id="subsec-changing-confidence">
      <title>Changing the Confidence Level</title>
      
      <p>
        We can create confidence intervals with different confidence levels. For example,
        to create a 99% confidence interval, we use 2.58 instead of 1.96:
      </p>
      
      <md>
        \text{point estimate} \pm 2.58 \times SE
      </md>
      
      <p>
        The choice of critical value depends on the desired confidence level. To find
        <m>z^*</m> for any confidence level, we select it so that the area between
        <m>-z^*</m> and <m>z^*</m> in the standard normal distribution corresponds to
        the confidence level.
      </p>
      
      <definition>
        <statement>
          <p>
            For a point estimate that closely follows a normal model with standard error <m>SE</m>,
            a confidence interval for the population parameter is:
          </p>
          <md>
            \text{point estimate} \pm z^* \times SE
          </md>
          <p>
            where <m>z^*</m> corresponds to the confidence level selected.
          </p>
        </statement>
      </definition>
      
      <definition>
        <statement>
          <p>
            In a confidence interval, <m>z^* \times SE</m> is called the <term>margin of error</term>.
          </p>
        </statement>
      </definition>
    </subsection>
    
    <subsection xml:id="subsec-ci-procedure">
      <title>Confidence Interval Procedure for a Single Proportion</title>
      
      <procedure>
        <step>
          <title>Prepare</title>
          <p>
            Identify <m>\hat{p}</m> and <m>n</m>, and determine what confidence level
            you wish to use.
          </p>
        </step>
        <step>
          <title>Check</title>
          <p>
            Verify the conditions to ensure <m>\hat{p}</m> is nearly normal. For
            one-proportion confidence intervals, use <m>\hat{p}</m> in place of <m>p</m>
            to check the success-failure condition.
          </p>
        </step>
        <step>
          <title>Calculate</title>
          <p>
            If the conditions hold, compute <m>SE</m> using <m>\hat{p}</m>, find <m>z^*</m>,
            and construct the interval.
          </p>
        </step>
        <step>
          <title>Conclude</title>
          <p>
            Interpret the confidence interval in the context of the problem.
          </p>
        </step>
      </procedure>
    </subsection>
    
    <subsection xml:id="subsec-interpreting-ci">
      <title>Interpreting Confidence Intervals</title>
      
      <p>
        When interpreting a confidence interval, note that the statement is always about
        the population parameter (considering all members of the population), not about
        individual observations or future point estimates. A confidence interval only
        provides a plausible range for population parameters.
      </p>
      
      <important>
        <p>
          Remember that the methods discussed apply only to sampling error, not to bias.
          If a data set is collected in a way that systematically under-estimates or
          over-estimates the population parameter, these techniques will not address
          that problem.
        </p>
      </important>
    </subsection>
  </section>
  
  <!-- Section 3: Hypothesis Testing -->
  <section xml:id="sec-hypothesis-testing">
    <title>Hypothesis Testing for a Proportion</title>
    
    <introduction>
      <p>
        The hypothesis testing framework is used to rigorously evaluate competing ideas and
        claims. In this section, we'll explore how to formally test claims about population
        proportions using data from samples.
      </p>
    </introduction>
    
    <subsection xml:id="subsec-ht-framework">
      <title>Hypothesis Testing Framework</title>
      
      <p>
        In hypothesis testing, we consider two competing ideas:
      </p>
      
      <ul>
        <li>The <term>null hypothesis</term> (<m>H_0</m>) often represents a skeptical perspective
            or a claim to be tested.</li>
        <li>The <term>alternative hypothesis</term> (<m>H_A</m>) represents an alternative claim
            under consideration and is often represented by a range of possible parameter values.</li>
      </ul>
      
      <p>
        Our job as data scientists is to play the role of a skeptic: before we buy into the
        alternative hypothesis, we need to see strong supporting evidence. Even if we fail to
        reject the null hypothesis, we typically do not accept it as true; failing to find
        strong evidence for the alternative hypothesis is not equivalent to accepting the
        null hypothesis.
      </p>
      
      <definition>
        <statement>
          <p>
            The <term>null value</term> is the value of the parameter under the null hypothesis.
            It is common to label the null value with the same symbol as the parameter but with
            a subscript 0. For example, if the null hypothesis is <m>p = 0.5</m>, then the
            null value is <m>p_0 = 0.5</m>.
          </p>
        </statement>
      </definition>
    </subsection>
    
    <subsection xml:id="subsec-ht-confidence-intervals">
      <title>Testing Hypotheses Using Confidence Intervals</title>
      
      <p>
        We can use confidence intervals to evaluate hypothesis tests. If the null value
        falls within the confidence interval, we cannot say the null value is implausible.
        In this case, we cannot reject the null hypothesis. If the null value falls outside
        the confidence interval, it is implausible and we reject the null hypothesis.
      </p>
    </subsection>
    
    <subsection xml:id="subsec-decision-errors">
      <title>Decision Errors in Hypothesis Testing</title>
      
      <p>
        Hypothesis tests are not flawless: we can make an incorrect decision based on the data.
      </p>
      
      <definition>
        <statement>
          <p>
            A <term>Type 1 Error</term> is rejecting the null hypothesis when <m>H_0</m>
            is actually true.
          </p>
        </statement>
      </definition>
      
      <definition>
        <statement>
          <p>
            A <term>Type 2 Error</term> is failing to reject the null hypothesis when the
            alternative is actually true.
          </p>
        </statement>
      </definition>
      
      <p>
        If we reduce how often we make one type of error, we generally make more of the other type.
      </p>
      
      <definition>
        <statement>
          <p>
            The <term>significance level</term> <m>\alpha</m> indicates how often we incorrectly
            reject <m>H_0</m> when it is true. The traditional significance level is
            <m>\alpha = 0.05</m>.
          </p>
        </statement>
      </definition>
    </subsection>
    
    <subsection xml:id="subsec-p-values">
      <title>Formal Testing Using P-values</title>
      
      <definition>
        <statement>
          <p>
            The <term>p-value</term> is the probability of observing data at least as favorable
            to the alternative hypothesis as our current data set, if the null hypothesis were
            true. We typically use a summary statistic of the data, such as the sample proportion,
            to help compute the p-value and evaluate the hypotheses.
          </p>
        </statement>
      </definition>
      
      <p>
        When evaluating hypotheses for proportions using the p-value method, we use the
        null value <m>p_0</m> (not <m>\hat{p}</m>) when checking the success-failure condition
        and computing the standard error:
      </p>
      
      <md>
        SE_{\hat{p}} = \sqrt{\frac{p_0(1-p_0)}{n}}
      </md>
      
      <important>
        <p>
          When using the p-value method to evaluate a hypothesis test, check the
          success-failure condition using the null value <m>p_0</m> instead of using
          the sample proportion. We're supposing the null hypothesis is true, which is
          different from the confidence interval approach.
        </p>
      </important>
      
      <procedure>
        <step>
          <title>Prepare</title>
          <p>
            Identify the parameter of interest, list hypotheses, identify the significance level,
            and identify <m>\hat{p}</m> and <m>n</m>.
          </p>
        </step>
        <step>
          <title>Check</title>
          <p>
            Verify conditions to ensure <m>\hat{p}</m> is nearly normal under <m>H_0</m>.
            For one-proportion hypothesis tests, use the null value to check the
            success-failure condition.
          </p>
        </step>
        <step>
          <title>Calculate</title>
          <p>
            If the conditions hold, compute the standard error using <m>p_0</m>,
            compute the Z-score, and identify the p-value.
          </p>
        </step>
        <step>
          <title>Conclude</title>
          <p>
            Evaluate the hypothesis test by comparing the p-value to <m>\alpha</m>, and
            provide a conclusion in the context of the problem.
          </p>
        </step>
      </procedure>
      
      <definition>
        <statement>
          <p>
            When the p-value is less than the significance level <m>\alpha</m>, we reject
            <m>H_0</m> and report that the data provide strong evidence supporting the
            alternative hypothesis.
          </p>
          <p>
            When the p-value is greater than <m>\alpha</m>, we do not reject <m>H_0</m>,
            and we report that we do not have sufficient evidence to reject the null hypothesis.
          </p>
        </statement>
      </definition>
    </subsection>
    
    <subsection xml:id="subsec-significance-level">
      <title>Choosing a Significance Level</title>
      
      <p>
        Choosing a significance level for a test is important in many contexts. The traditional
        level is <m>\alpha = 0.05</m>, but it can be helpful to adjust the significance level
        based on the application.
      </p>
      
      <ul>
        <li>If making a Type 1 Error is dangerous or especially costly, choose a small
            significance level (e.g., 0.01).</li>
        <li>If a Type 2 Error is relatively more dangerous or costly, choose a higher
            significance level (e.g., 0.10).</li>
      </ul>
    </subsection>
  </section>
  
  <!-- Review Exercises -->
  <section xml:id="sec-ch05-review">
    <title>Chapter 5 Review Exercises</title>
    
    <p>
      Additional exercises for practicing the concepts covered in this chapter are available
      in the accompanying exercise materials. These exercises cover parameter identification,
      point estimates, confidence intervals, and hypothesis testing for proportions.
    </p>
  </section>
</chapter>
"""
    
    return chapter_intro

# Main execution
if __name__ == '__main__':
    output_file = r'C:\Users\lclem\OneDrive\Documents\GitHub\PreTeXt books\OpenIntro Statistics\openintro-statistics-1\source\ch05.ptx'
    
    pretext_content = create_pretext_chapter()
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(pretext_content)
    
    print(f"✓ Created comprehensive ch05.ptx with {len(pretext_content)} characters")
    print(f"✓ File saved to: {output_file}")
    print("\nChapter structure:")
    print("  - Introduction")
    print("  - Section 1: Point Estimates and Sampling Variability")
    print("    - Point Estimates and Error")
    print("    - Understanding Variability")
    print("    - Central Limit Theorem")
    print("    - Real-World Applications")
    print("    - Extending the Framework")
    print("  - Section 2: Confidence Intervals")
    print("    - Capturing the Parameter")
    print("    - 95% Confidence Intervals")
    print("    - Changing Confidence Levels")
    print("    - CI Procedure")
    print("    - Interpreting CIs")
    print("  - Section 3: Hypothesis Testing")
    print("    - HT Framework")
    print("    - Testing via Confidence Intervals")
    print("    - Decision Errors")
    print("    - P-values")
    print("    - Significance Levels")
    print("  - Review Exercises")
