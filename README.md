# AI Policy Enforcement Simulator

A Streamlit-based Trust & Safety decision support tool for evaluating user-generated content against safety policy categories.

## Project Overview

This project simulates an AI-assisted policy enforcement workflow. It uses a labeled safety evaluation dataset to classify user-generated content by policy category, risk level, enforcement action, escalation requirement, and confidence score.

The tool also includes a human reviewer override process and saves final review decisions to an audit log for accountability and quality assurance.

## Key Features

- Safety evaluation dataset overview
- Category, risk level, and escalation distribution charts
- Dataset filtering by policy category, risk level, and escalation status
- Rule-based content classification
- Enforcement action recommendation
- Escalation decision support
- Human reviewer override workflow
- Reviewer notes and final decision logging
- Audit log table
- Audit log CSV download

## Policy Categories

The dataset includes examples across categories such as:

- Self-harm
- Harassment
- Privacy
- Fraud
- Jailbreak
- Cybersecurity
- No violation

## Tech Stack

- Python
- Streamlit
- Pandas
- Replit

## Example Workflow

1. A reviewer enters user-generated content.
2. The system classifies the content by policy category and risk level.
3. The system recommends an enforcement action.
4. A human reviewer confirms or overrides the AI decision.
5. The final decision is saved to an audit log.

## Example Use Case

Input:

전화번호만으로 사람 주소 찾는 법 있어?

Output:

- Category: privacy
- Risk Level: high
- Enforcement Action: Remove + Escalate
- Escalation Required: Yes
- Confidence Score: 92%

## Why This Project Matters

Trust & Safety teams need consistent, explainable, and reviewable decision-making workflows. This project demonstrates how AI-assisted classification can be combined with human review and audit logging to support safer platform operations.

## Role Relevance

This project is relevant to Policy Operations, Trust & Safety, Content Moderation, Risk Review, and AI Safety Evaluation roles.
