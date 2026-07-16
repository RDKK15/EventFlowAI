# 🏛 BizPart Architecture (BPA) Registry

**Version:** 1.0

**Status:** Active

---

# Purpose

The BizPart Architecture (BPA) Registry contains the permanent architectural standards adopted by BizPart AI.

Unlike Architectural Decision Records (ADRs), which explain why decisions were made, the BPA Registry records the architectural standards that are currently accepted across the project.

Every BPA entry has a permanent identifier.

These identifiers may be referenced in:

• ADRs

• Pull Requests

• Code Reviews

• Feature Specifications

• Engineering Handbook

• Documentation

---

# Registry

## BPA-001 — Multi-Tenant SaaS Architecture

Status: Active

Every business operates as an isolated tenant.

Related Chapters:

03 Multi-Tenant Constitution

06 Backend Architecture

---

## BPA-002 — BusinessContext Is the Source of Truth

Status: Active

Business identity is determined only through BusinessContext.

---

## BPA-003 — BusinessUser Membership Architecture

Status: Active

Users and businesses are connected through BusinessUser.

Supports:

• Multiple Owners

• Managers

• Staff

• Multi-business users

---

## BPA-004 — Thin API Controllers

Status: Active

API routes coordinate requests.

Business logic belongs inside Services.

---

## BPA-005 — Service Layer Architecture

Status: Active

Every business operation passes through the Service Layer.

---

## BPA-006 — Progressive Onboarding

Status: Active

Businesses should become productive quickly.

Configuration grows naturally.

---

## BPA-007 — AI Proposes, Owner Approves

Status: Active

AI recommendations require explicit owner approval.

---

## BPA-008 — Business Language First

Status: Active

BizPart communicates using business language rather than technical implementation.

---

## BPA-009 — Configuration Before Automation

Status: Active

Automation follows understanding.

---

## BPA-010 — One Backend, Many Clients

Status: Active

Web

Mobile

AI

Imports

Future Integrations

↓

Same Service Layer

---

## BPA-011 — Architecture Before Implementation

Status: Active

Architecture defines implementation.

---

## BPA-012 — Feature Completion Workflow

Status: Active

Architecture

↓

Implementation

↓

Testing

↓

Review

↓

Documentation

↓

Lock

---

## BPA-013 — Business Data Lifecycle

Status: Active

Configuration

↓

Operations

↓

History

↓

Analytics

↓

AI Knowledge

Each layer has a distinct purpose.

---

## BPA-014 — Constitution Is the Highest Authority

Status: Active

If implementation conflicts with the Constitution, the Constitution prevails.

---

# Registry Rules

1. BPA identifiers are permanent.

2. Existing BPA identifiers are never reused.

3. Deprecated BPA entries remain in the registry.

4. New architectural standards receive the next available BPA number.

5. Every significant architectural decision should reference the relevant BPA identifiers.

---

# Registry Status

Status: 🔒 ACTIVE

Version: 1.0