# Lexical Analyzer in Python

## 📌 Overview
This project implements a **simple lexical analyzer** using Python.  
A lexical analyzer is the **first phase of a compiler**, responsible for breaking source code into meaningful units called **tokens**.

The program takes **source code as input from the user** and classifies each token as a:
- Keyword
- Identifier
- Operator
- Number

This implementation is **easy to understand**, making it suitable for **compiler design labs, exams, and viva explanations**.

---

## 🎯 Objectives
- Read source code input from the user
- Perform lexical analysis
- Identify and classify tokens
- Display lexical analysis output in a readable format

---

## 🛠️ Technologies Used
- **Programming Language:** Python
- **Library:** `re` (Regular Expressions)

---

## 🧠 How It Works
1. The user enters multiple lines of source code.
2. Input ends when an empty line is entered.
3. The program uses regular expressions to split the code into tokens.
4. Each token is checked against predefined rules:
   - Keywords → `KEYWORD`
   - Operators → `OPERATOR`
   - Numeric values → `NUMBER`
   - Others → `IDENTIFIER`
5. The token and its type are printed as output.

---

## 📥 Sample Input
