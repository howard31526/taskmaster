---
allowed-tools: Read, Edit, Write, Glob, Grep, Bash(git branch:*), Bash(git status:*), Bash(git diff:*), Bash(git log:*), Bash(git add:*), Bash(git commit:*), Bash(git push:*), Bash(gh:*)
argument-hint: <功能名稱或任務描述,例如:登入表單驗證> (選填,僅在首次執行時需要)
description: 逐步執行版本的 auto-fix (GitHub Actions 專用,每次只執行一個項目)
---

# /auto-fix-step - 逐步執行版本

此指令專為 GitHub Actions 環境設計,每次執行只處理一個項目。

## 核心特性

- ✅ 每次執行只處理「一個」項目
- ✅ 保留完整的 PROGRESS.md 追蹤機制
- ✅ 保留 log_history 歸檔
- ✅ 支援斷點續做
- ✅ 無需互動式確認 (完全自動化)
- ✅ 每個項目獨立提交
- ✅ 明確的分支推送步驟（建立 PROGRESS.md 後立即推送）
- ✅ 自動建立 PR 與流程提示機制
- ✅ 斷點式執行與階段提交（每個狀態變更都 commit）

## 執行流程

### 第一步:檢查或創建 PROGRESS.md

**如果 PROGRESS.md 已存在:**
- 讀取檔案
- 找到第一個 [ ] 或 [/] 狀態的項目
- 跳到「第二步」執行該項目

**如果 PROGRESS.md 不存在:**
- 確認 $ARGUMENTS 有提供任務描述
- 根據任務描述生成新的 PROGRESS.md
- 格式要求:
  ```markdown
  # 任務: <任務描述>

  ## 規劃項目 (最小可交付粒度: 3-8 項)

  - [ ] 項目 1: <摘要>
    - 檔案範圍: <相關檔案>
    - 驗收條件: <可手測或測試的條件>

  - [ ] 項目 2: <摘要>
    - 檔案範圍: <相關檔案>
    - 驗收條件: <可手測或測試的條件>

  ...

  ## 狀態說明
  - [ ] 未開始
  - [/] 進行中
  - [x] 已完成
  ```
- 將生成的 PROGRESS.md 寫入檔案
- **立即推送到遠端:**
  1. 執行 `git add PROGRESS.md`
  2. 執行 `git commit -m "chore: 建立任務規劃 - <任務描述>"`
  3. 執行 `git push origin <當前分支>`（確保分支已推送到 GitHub）
- **自動建立 PR:**
  1. 檢查是否已存在 PR（使用 `gh pr list --head <當前分支>`）
  2. 如果不存在 PR，執行：
     ```bash
     gh pr create --title "feat: <任務描述>" \
       --body "## 任務描述\n<任務描述>\n\n## 進度追蹤\n請參考 PROGRESS.md 檔案\n\n🤖 Generated with [Claude Code](https://claude.ai/code)" \
       --base main
     ```
  3. 如果 `gh` 指令不可用，提供手動建立 PR 的連結
- 提示使用者:「✅ PROGRESS.md 已建立並推送，PR 已自動建立。請至 PR 中執行 @claude /auto-fix-step 開始實作第一個項目」
- **結束執行** (不繼續執行項目)

### 第二步:執行單一項目

1. **找到目標項目**
   - 讀取 PROGRESS.md
   - 找到第一個 [ ] 或 [/] 狀態的項目
   - 如果所有項目都是 [x],跳到「第三步:歸檔」

2. **更新狀態為進行中（斷點提交 1）**
   - 將該項目狀態由 [ ] 改為 [/]
   - **立即提交此狀態變更:**
     ```bash
     git add PROGRESS.md
     git commit -m "chore: 開始項目 N - <項目摘要>

Co-authored-by: <使用者名稱> <使用者email>"
     git push origin <當前分支>
     ```

3. **執行修改**
   - 根據項目的「檔案範圍」和「摘要」進行修改
   - 使用 Edit 或 Write 工具修改相關檔案

4. **提交修改（斷點提交 2）**
   - 遵循 Conventional Commits 規範
   - 提交訊息格式: `<type>: <description>`
   - 常用 type: feat, fix, docs, refactor, test, chore
   - 包含 Co-authored-by 標記
   - **立即執行:**
     ```bash
     git add <修改的檔案>
     git commit -m "<type>: <項目摘要>

Co-authored-by: <使用者名稱> <使用者email>"
     git push origin <當前分支>
     ```

5. **更新 PROGRESS.md（斷點提交 3）**
   - 使用 `git log -1 --pretty=format:%h` 取得最新的 commit 前 7 碼
   - 將該項目狀態改為 [x]
   - 在該項目下方新增一行,記錄:
     ```markdown
     - [x] 項目 1: <摘要>
       - 檔案範圍: <相關檔案>
       - 驗收條件: <條件>
       - ✅ Commit: `<前7碼>` - <提交訊息摘要>
     ```
   - **立即提交此狀態更新:**
     ```bash
     git add PROGRESS.md
     git commit -m "chore: 完成項目 N - <項目摘要>

Co-authored-by: <使用者名稱> <使用者email>"
     git push origin <當前分支>
     ```

6. **回報進度**
   - 在 GitHub 評論中顯示:
     - 已完成的項目（包含 commit hash）
     - 剩餘的項目數量
     - 提示:「✅ 項目 N 已完成並推送。請再次執行 @claude /auto-fix-step 繼續下一個項目」

7. **結束執行** (不繼續下一個項目)

**重要:** 每個項目會產生 3 個 commit（開始、修改、完成），確保每個階段都有明確的紀錄。

### 第三步:歸檔與生成歷程紀錄 (所有項目完成時)

當 PROGRESS.md 中所有項目都是 [x] 時:

1. **生成歷程紀錄檔案**
   - 格式: `YYYYMMDD_<任務描述>.md`
   - 例如: `20251016_登入表單驗證.md`
   - 基於 PROGRESS.md 內容，增加以下資訊：
     - 任務開始時間（第一個 commit 的時間）
     - 任務完成時間（最後一個 commit 的時間）
     - 所有相關的 commit 列表（使用 `git log --oneline --grep="<任務相關關鍵字>"`）
     - 修改的檔案統計

2. **歸檔到 log_history/**
   - 檢查 log_history/ 資料夾是否存在
   - 如果不存在，執行 `mkdir -p log_history`
   - 將生成的歷程紀錄檔案移動到 log_history/
   - 刪除原本的 PROGRESS.md

3. **提交歸檔變更（最終提交）**
   - **立即執行:**
     ```bash
     git add log_history/ PROGRESS.md
     git commit -m "chore: 歸檔任務歷程 - <任務描述>

Co-authored-by: <使用者名稱> <使用者email>"
     git push origin <當前分支>
     ```

4. **回報完成**
   - 在 GitHub 評論中顯示:
     - ✅ 任務全部完成!
     - 所有已完成的項目（包含 commit hash）
     - 總共的提交數量
     - 歷程紀錄檔案的位置: `log_history/YYYYMMDD_<任務描述>.md`
     - 建議:「可以合併此 PR 到主分支」

## 使用範例

### 首次執行 (創建 PROGRESS.md):
```
@claude /auto-fix-step 實作使用者登入功能
```

### 繼續執行下一個項目:
```
@claude /auto-fix-step
```

### 中途執行 (有未完成的項目):
```
@claude /auto-fix-step
```

## 與 /auto-fix 的差異

| 特性 | /auto-fix | /auto-fix-step |
|------|----------|---------------|
| 互動式確認 | ✅ 有 (本機環境) | ❌ 無 (自動執行) |
| 每次執行項目數 | 全部 | 一個 |
| 適用環境 | 本機 Claude Code CLI | GitHub Actions |
| 控制程度 | 高 (逐步確認) | 中 (每項目之間確認) |
| PROGRESS.md | ✅ 有 | ✅ 有 |
| log_history | ✅ 有 | ✅ 有（增強版） |
| 分支推送 | 手動 | ✅ 自動（每個斷點） |
| PR 建立 | 手動 | ✅ 自動 |
| 斷點提交 | 部分 | ✅ 完整（3個/項目） |
| 歷程紀錄 | 簡單 | ✅ 詳細（含時間、commit統計） |

## 重構重點說明

### 1. 明確分支推送步驟
- ✅ 建立 PROGRESS.md 後立即推送到 GitHub
- ✅ 每個斷點（狀態變更）都自動推送
- ✅ 確保 GitHub 上隨時都有最新狀態

### 2. 自動建立 PR 與流程提示
- ✅ 使用 `gh pr create` 自動建立 PR
- ✅ PR 標題與內容自動生成
- ✅ 提示使用者可於 PR 中繼續操作

### 3. 斷點式執行與階段提交
- ✅ 每個項目 3 個 commit（開始/修改/完成）
- ✅ 每個 commit 立即推送
- ✅ 確保可追溯性與階段性保存

### 4. 歷程紀錄生成機制
- ✅ 完成後自動生成詳細的 log_history 檔案
- ✅ 包含時間、commit 列表、檔案統計
- ✅ 歸檔到 log_history/ 資料夾

## 注意事項

- 此指令設計為「無互動」模式，適合 GitHub Actions 環境
- 每次執行只處理一個項目，需要多次觸發才能完成整個任務
- 透過 PROGRESS.md 檔案保持狀態，支援斷點續做
- 所有提交都遵循 Conventional Commits 規範
- 每個項目會產生 3 個 commit，確保完整的修改歷程
- 需要 GitHub CLI (`gh`) 工具來自動建立 PR
- 如果需要完整的互動式控制，請在本機環境使用 /auto-fix
