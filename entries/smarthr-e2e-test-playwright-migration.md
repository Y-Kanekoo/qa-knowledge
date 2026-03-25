---
title: "E2Eテストを Playwright で作り直して開発プロセスに組み込む話"
company: "SmartHR"
url: "https://tech.smarthr.jp/entry/playwright"
published_at: "2024-01-17"
content_type: "blog"
qa_domains:
  - "test-automation"
tags:
  - "e2e-testing"
  - "playwright"
  - "selenium-migration"
  - "test-infrastructure"
  - "developer-ownership"
language: "ja"
added_at: "2026-03-24"
industry: "saas"
difficulty: "intermediate"
deprecated: false
---

## 概要

SmartHRの届出書類機能チームが、Capybara + SeleniumベースのE2Eテスト基盤をPlaywrightに移行した事例を紹介している。ブラウザ起動時間の短縮（7秒→1秒）やアクセシビリティ属性を活用したテスト記述の改善など、具体的な技術的メリットと、開発チーム自身がテスト基盤のオーナーシップを持つことの重要性を解説している。

## 何が学べるか

- Capybara + SeleniumからPlaywrightへの移行における具体的な課題と解決策
- Playwrightの`getByRole`等のAPIによるユーザー視点のテスト記述の利点
- E2Eテスト基盤のオーナーシップを開発チームに移すことで得られる積極的なテスト文化の醸成方法
- ステージング環境でのE2Eテスト自動実行の運用設計
- チームディスカッションを通じた段階的な移行の進め方

## 関連エントリ
