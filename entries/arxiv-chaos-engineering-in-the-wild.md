---
title: "Chaos Engineering in the Wild: Findings from GitHub"
company: "Jheronimus Academy of Data Science"
url: "https://arxiv.org/html/2505.13654v1"
published_at: "2025-05-19"
content_type: "blog"
qa_domains:
  - "reliability"
  - "test-strategy"
tags:
  - "chaos-engineering"
  - "toxiproxy"
  - "chaos-mesh"
  - "litmuschaos"
  - "gremlin"
  - "empirical-study"
  - "kubernetes"
language: "en"
added_at: "2026-03-24"
industry: "general"
difficulty: "intermediate"
speaker: "Joshua Owotogbe, Indika Kumara, Dario Di Nucci, Damian Andrew Tamburri, Willem-Jan van den Heuvel"
deprecated: false
---

## 概要

GitHubの971リポジトリを分析し、10種類の主要カオスエンジニアリングツールの採用パターンを調査した学術論文。Toxiproxy（243リポジトリ）とChaos Mesh（225リポジトリ）が最も採用されており、上位3ツールが全体の64.57%を占める。リポジトリ用途は開発（58%）・教育（10.3%）・学習（9.9%）で、障害注入シナリオではネットワーク障害（40.9%）が最多であることなど、業界全体のカオスエンジニアリング採用実態を定量的に明らかにしている。

## 何が学べるか

- Toxiproxy・Chaos Mesh・LitmusChaosなど主要カオスエンジニアリングツールの採用率と特徴の比較
- ネットワーク障害（40.9%）・インスタンス終了（32.7%）・リソースストレス（23.4%）など障害注入シナリオの実践的な優先順位
- 業界主導（43.2%）・個人（31.7%）・公的機関（17.8%）・学術（7.3%）という所有者分布から見るカオスエンジニアリングの普及状況
- LitmusChaosのCNCF Incubating段階への到達や、Chaos Meshの74回リリースなどKubernetes-nativeツールの急速な進化
- Netflix以外の企業（ICA Gruppen AB等）におけるカオスエンジニアリングの実践事例

## 関連エントリ

- [Netflix - Chaos Monkey](netflix-chaosmonkey.md)
- [Netflix - FIT: Failure Injection Testing](netflix-fit-failure-injection-testing.md)
- [Google Cloud - Chaos Engineering Framework](google-cloud-chaos-engineering-framework.md)
