---
id: K-20261107-01
date: 2026-11-07
repo: qa-knowledge
category: test
severity: medium
status: promoted
recurrence: 1
promoted_to: docs/TESTING.md
---

# local-ci の対象は作業ツリーではなくコミット

## 起きたこと

回帰69件の追加後に `local-ci run .` が成功したが、単体件数は既存の147件だった。
追加テストは個別実行では成功していたものの、その local-ci 結果には含まれていなかった。

## 原因

local-ci は HEAD から隔離 worktree を作る。未コミットの変更は検証されない。

## 対処

対象変更をローカルコミットへ確定し、そのリビジョンで local-ci を再実行する。
検証結果のSHAと単体件数を確認する。pushや公開は不要。

## 再発防止案

検証対象の確認手順を docs/TESTING.md に追記した。

## 確認方法

結果JSONの sha が対象コミットと一致し、単体ログが追加テストを収集していることを確認する。
未コミット変更が残る場合は、その実行を最終リビジョンの成功として扱わない。
