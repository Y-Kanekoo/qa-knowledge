---
title: "GTAC 2016: How Flaky Tests in Continuous Integration - Current Practice at Google and Future Directions"
company: "Google"
url: "https://youtu.be/CrzpkF1-VsA?list=PLSIUOFhnxEiAeGHYoBZCvEMY5wCOIpyOM"
published_at: "2016-11-15"
content_type: "conference_talk"
qa_domains:
  - "test-automation"
  - "ci-cd"
tags:
  - "flaky-tests"
  - "continuous-integration"
  - "test-reliability"
  - "machine-learning"
language: "en"
added_at: "2026-04-13"
industry: "web-service"
difficulty: "advanced"
speaker: "John Micco, Atif Memon"
conference: "GTAC 2016"
video_url: "https://youtu.be/CrzpkF1-VsA?list=PLSIUOFhnxEiAeGHYoBZCvEMY5wCOIpyOM"
slide_url: "https://docs.google.com/presentation/d/1iVf-TogkdoIcvs8OpRMMWx76s9Zk4_f0JJ-e1sZIxog/edit#slide=id.p659"
related_tools: []
deprecated: false
---

## 概要

GoogleのEngineering Productivity ManagerであるJohn Miccoとメリーランド大学のAtif Memonが、Google社内における350万以上のテストケースのフレイキーテスト（不安定テスト）の実態と対策について発表した。84%のテスト失敗がフレイキーテストに起因し、CIリソースの2〜16%がフレイキーテストの再実行に費やされているという具体的なデータを公開している。機械学習を活用してフレイキーテストを90%の精度で検出する手法も紹介されている。

## 何が学べるか

- Google規模（350万テスト）でのフレイキーテストの実態データ（16%のテストに何らかのフレイキー性がある）を把握できる
- PASS→FAIL遷移の84%がフレイキーテストによるものという事実から、テスト信頼性の重要性を理解できる
- 機械学習を用いたフレイキーテスト自動検出アプローチ（10回再実行せずに90%の精度で判定）を学べる
- フレイキーテストがリリースプロセスのブロッカーとなるメカニズムと、組織的な緩和戦略を知ることができる
- CIリソースの無駄遣いを定量化し、テスト基盤改善のROIを経営層に説明する方法を学べる

## 関連エントリ

