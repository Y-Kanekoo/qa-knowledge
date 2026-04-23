# Sources Catalog — QA/Testing 情報源カタログ

QA/Testing 関連の優良サイトを分野別に網羅したカタログ。feeds.yml に載るのはこのうち RSS が安定して取れる主要ブログのみで、本ファイルはキュレーション判断の一次ソースとして保持する。

## 運用ポリシー

- **feeds.yml**: 日次自動巡回で新着を Discord/Issue 通知する対象（`scripts/check_rss.py` が読む）
- **本カタログ**: 人間が記事を探すときの出発点。RSSに載せない個人ブログ・カンファレンス・学術・新興領域もここに集約
- 四半期ごとに見直し、feeds.yml への昇格／降格を検討する
- 記号: ★ = 優先度高 / 🆕 = 現状エントリ未収録 / 📡 = feeds.yml に既に登録

---

## 1. 国内企業 Tech Blog

### 1.1 既存カバー（entries 収録済み or feeds.yml 登録済み）

| 企業 | URL | 状態 |
|------|-----|------|
| Cookpad | https://techlife.cookpad.com/ | 📡 |
| Cybozu | https://blog.cybozu.io/ | 📡 |
| DeNA | https://engineering.dena.com/blog/ | 📡 |
| freee | https://developers.freee.co.jp/ | 📡 |
| LayerX | https://tech.layerx.co.jp/ | 📡 |
| LY Corporation | https://techblog.lycorp.co.jp/ja | 📡 |
| Mercari | https://engineering.mercari.com/blog/ | 📡 |
| SmartHR | https://tech.smarthr.jp/ | 📡 |
| ZOZO | https://techblog.zozo.com/ | 📡 |

### 1.2 🆕 新規追加（feeds.yml 登録済み）

| 企業 | URL | 特徴 |
|------|-----|------|
| ★ エムスリー (m3) | https://www.m3tech.blog/ | 全員QA・SET・mabl導入・医療 |
| ★ 食べログ (Tabelog) | https://tech-blog.tabelog.com/ | AI4QA (手動52%削減)、リスクベース |
| ★ CADDi | https://caddi.tech/ | QAカテゴリ、製造×ソフト |
| ★ ANDPAD | https://tech.andpad.co.jp/ | QC組織論、建設SaaS |
| ★ Money Forward | https://moneyforward-dev.jp/ | QA Night、グローバルQA |
| ★ CyberAgent Developers | https://developers.cyberagent.co.jp/blog/ | ABEMA Dark Canary |
| ★ Sansan | https://buildersbox.corp-sansan.com/ | mabl事例、SET |

### 1.3 🆕 未採用（Zenn Publication / RSS不安定だが要ウォッチ）

| 企業 | URL | 備考 |
|------|-----|------|
| LegalOn Technologies | https://tech.legalforce.co.jp/ | リーガルテック×AI Agent testing |
| Timee (タイミー) | https://tech.timee.co.jp/ | 初SET、Enabling Team |
| Ubie | https://zenn.dev/p/ubie_dev | 医療AI×QA (Zenn Pub) |
| Loglass | https://zenn.dev/p/loglass | DDD×品質 |
| 10X | https://product.10x.co.jp/ | 小売DX×QA |
| MIXI | https://mixi-developers.mixi.co.jp/ | TDD、QA再編 |
| Hatena Developer | https://developer.hatenastaff.com/ | 老舗 |
| CARTA HOLDINGS | https://techblog.cartaholdings.co.jp/ | 広告×品質 |
| GMO Ad Tech | https://adengineer.internet.gmo/ | 広告 |
| Rakuten Engineering | https://engineering.rakuten.today/ | EC |
| PayPay | https://blog.paypay.ne.jp/category/tech/ | FinTech |
| pixiv inside | https://inside.pixiv.blog/ | クリエイター基盤 |

### 1.4 🎮 ゲーム業界（独自ドメイン・未カバー）

| 企業 | URL | 備考 |
|------|-----|------|
| SEGA | https://techblog.sega.jp/ | QAエンジニア/クオリティエンジニア |
| Cygames | https://tech.cygames.co.jp/ | |
| GREE | https://labs.gree.jp/blog/ | |
| KLab | https://www.klab.com/jp/blog/ | |
| Nexon | https://www.nexon.co.jp/blog/ | |
| コロプラ | https://blog.colopl.dev/ | |

---

## 2. 海外企業 Tech Blog

### 2.1 既存カバー

Airbnb / Amazon / Google / GitHub / GitLab / Meta / Microsoft / Netflix / Slack / Spotify / Stripe / Uber / Shopify / Thoughtworks / Twitter / LinkedIn / Honeycomb / Grafana / AWS

### 2.2 🆕 新規追加（feeds.yml 登録済み）

| 企業 | URL | 特徴 |
|------|-----|------|
| ★ Dropbox Tech | https://dropbox.tech/ | Athena、sync test |
| ★ Atlassian Engineering | https://www.atlassian.com/blog/atlassian-engineering | Flakinator、Quality Assistance |
| ★ Etsy Code as Craft | https://codeascraft.com/ | CI/CD古典 |
| ★ Lyft Engineering | https://eng.lyft.com/ | Mobile CI、Bazel |

### 2.3 🆕 未採用・要ウォッチ（RSS重複 or 採用見送り）

| 企業 | URL | 備考 |
|------|-----|------|
| Pinterest Engineering | https://medium.com/pinterest-engineering | PinTestLab、MCP ecosystem |
| Coinbase Engineering | https://www.coinbase.com/blog/landing/engineering | 金融×AI Agent |
| DoorDash Engineering | https://careersatdoordash.com/engineering-blog/ | |
| Ramp Engineering | https://engineering.ramp.com/ | FinTech |
| Robinhood | https://newsroom.aboutrobinhood.com/engineering | |
| Canva Engineering | https://canvaengineering.com/ | Bazel大口採用 |
| Figma Engineering | https://www.figma.com/blog/section/engineering/ | |
| Vercel | https://vercel.com/blog | Next.js/Turbo |
| Bloomberg Engineering | https://www.bloomberg.com/company/stories/engineering/ | |
| Twilio | https://www.twilio.com/blog/ | SDK品質 |
| Cloudflare | https://blog.cloudflare.com/ | Workers/Observability |
| HashiCorp | https://www.hashicorp.com/blog | Terraform testing |
| Pulumi | https://www.pulumi.com/blog/ | IaC testing |
| MongoDB Engineering | https://www.mongodb.com/blog/channel/engineering-blog | |
| Elastic | https://www.elastic.co/blog/ | Obs×test |
| Sentry | https://blog.sentry.io/ | エラー駆動 |
| New Relic | https://newrelic.com/blog | |
| Datadog Engineering | https://www.datadoghq.com/blog/engineering/ | |
| JetBrains | https://blog.jetbrains.com/ | IDE×testing |

---

## 3. テストツール / プラットフォーム公式

| ソース | URL | 状態 |
|--------|-----|------|
| ★ Playwright | https://playwright.dev/blog | 📡 |
| Cypress | https://www.cypress.io/blog | |
| Vitest | https://vitest.dev/ | |
| mabl | https://www.mabl.com/blog | AI E2E |
| Autify | https://autify.com/blog/ | 日本語あり |
| BrowserStack | https://www.browserstack.com/blog | |
| Sauce Labs | https://saucelabs.com/blog | |
| LambdaTest (TestMu AI) | https://www.lambdatest.com/blog/ | 2026 AI pivot |
| Applitools | https://applitools.com/blog/ | Visual AI |
| Stagehand / Browserbase | https://www.browserbase.com/blog | 🆕 AI browser agent |
| Browser Use | https://browser-use.com/blog | 🆕 LLM browser |
| QA Wolf / Momentic / Reflect | 各社 | Managed AI E2E |
| k6 / Grafana k6 | https://grafana.com/blog/tags/k6/ | Load test |
| Gatling | https://gatling.io/blog | |
| Locust | https://locust.io/ | |

---

## 4. SRE / Chaos / Incident Management

| ソース | URL |
|--------|-----|
| PagerDuty | https://www.pagerduty.com/blog/ |
| Incident.io | https://incident.io/blog |
| Blameless | https://www.blameless.com/blog |
| Gremlin | https://www.gremlin.com/blog |
| Harness Chaos | https://www.harness.io/blog |
| LitmusChaos / ChaosMesh | OSS |
| Steadybit | https://steadybit.com/blog/ |

---

## 5. Security Testing / DevSecOps

| ソース | URL |
|--------|-----|
| Snyk | https://snyk.io/blog/ |
| Semgrep | https://semgrep.dev/blog |
| GitGuardian | https://blog.gitguardian.com/ |
| Aikido | https://www.aikido.dev/blog |
| GitHub Security Lab | https://github.blog/security/ |

---

## 6. Contract / API Testing

| ソース | URL |
|--------|-----|
| PactFlow | https://pactflow.io/blog/ |
| Postman | https://www.postman.com/blog/ |
| SmartBear | https://smartbear.com/blog/ |
| Microsoft ISE Blog | https://devblogs.microsoft.com/ise/ |

---

## 7. AI Testing / LLM Evaluation（2025-2026 急成長領域）

| ソース | URL | 特徴 |
|--------|-----|------|
| ★ Braintrust | https://www.braintrust.dev/blog | Notion事例、AI eval |
| LangChain / LangSmith | https://blog.langchain.com/ | |
| LangWatch | https://langwatch.ai/blog | |
| Comet | https://www.comet.com/site/blog/ | |
| Arize AI | https://arize.com/blog/ | |
| Anthropic Research | https://www.anthropic.com/research | |
| OpenAI | https://openai.com/blog | |
| AWS ML Blog (Agent Eval) | https://aws.amazon.com/blogs/machine-learning/ | Bedrock AgentCore |

---

## 8. テストコミュニティ / 個人ブログ

| ソース | URL | 備考 |
|--------|-----|------|
| Ministry of Testing | https://www.ministryoftesting.com/ | Podcast、Newsletter |
| Test Masters Academy | https://testmastersacademy.org/ | |
| Martin Fowler Testing | https://martinfowler.com/testing/ | 古典 |
| Kent Beck (Substack) | https://tidyfirst.substack.com/ | TDD創始者 |
| Gojko Adzic | https://gojko.net/ | SBE |
| James Bach | https://www.satisfice.com/blog | 探索的テスト |
| Michael Bolton | https://www.developsense.com/blog/ | RST |
| Tim Deschryver | https://timdeschryver.dev/blog | （エントリ収録済み） |
| ブロッコリー (nihonbuson) | https://nihonbuson.hatenadiary.jp/ | 日本QAコミュニティ重鎮 |
| Cypress Tips (Gleb Bahmutov) | https://cypresstips.substack.com/ | |
| テスト・QA関連ブログRSS (yoshikiito) | https://yoshikiito.github.io/test-qa-rss-feed/blogs/ | アグリゲータ |

---

## 9. カンファレンス / アーカイブ

| イベント | URL |
|----------|-----|
| QCon (InfoQ) | https://qconferences.com/ / https://www.infoq.com/testing/ |
| SRECon (USENIX) | https://www.usenix.org/conferences/ |
| Agile Testing Days | https://agiletestingdays.com/ |
| TestCon Europe | https://testcon.lt/ |
| Selenium Conf | https://seleniumconf.com/ |
| Google GTAC / EngProd | https://testing.googleblog.com/ |
| JaSST | https://www.jasst.jp/ |
| JaSST Review | https://www.jasst.jp/symposium/jasstreview/ |
| WACATE | https://wacate.jp/ |
| DevOpsDays Tokyo | https://www.devopsdaystokyo.org/ |
| CEDEC (ゲーム開発) | https://cedec.cesa.or.jp/ |

---

## 10. 研究 / 学術

| ソース | URL |
|--------|-----|
| Google Testing Blog | https://testing.googleblog.com/ |
| ACM ISSTA | https://www.issta.org/ |
| ICSE | https://www.icse-conferences.org/ |
| USENIX | https://www.usenix.org/ |
| arXiv cs.SE | https://arxiv.org/list/cs.SE/recent |
| DORA Report | https://dora.dev/ |
| DX Core 4 (getdx) | https://getdx.com/blog/ |

---

## 11. メディア / アグリゲータ

| ソース | URL |
|--------|-----|
| InfoQ Testing | https://www.infoq.com/testing/ |
| Pragmatic Engineer | https://newsletter.pragmaticengineer.com/ |
| ByteByteGo | https://bytebytego.com/ |
| Software Testing Magazine | https://www.softwaretestingmagazine.com/ |
| テスト・QA関連ブログRSS (yoshikiito) | https://yoshikiito.github.io/test-qa-rss-feed/blogs/ |
| 企業テックブログRSS (yamadashy) | https://yamadashy.github.io/tech-blog-rss-feed/ |

---

## 統計

- 総候補サイト数: **約 100**
- 内訳: 国内企業 27 / 海外企業 30 / ツール公式 16 / SRE 7 / Security 5 / Contract 4 / AI eval 8 / 個人・コミュニティ 11 / カンファレンス 11 / 研究 7 / メディア 6
- feeds.yml 登録済み（追加前20 + 本カタログ追加12）: **32サイト**

## 見直しトリガー

- 新領域が出現したとき（例: AI Agent testing、Vibe testing）
- feeds.yml の RSS が 404 を返し続けるとき
- 新規企業 Tech Blog の QA/テスト記事が目に付いたとき
- 四半期末（1月/4月/7月/10月）の定期レビュー
