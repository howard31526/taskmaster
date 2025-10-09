---
allowed-tools: Read, Edit, Write, Glob, Grep, Bash(git branch:*), Bash(git status:*), Bash(git diff:*), Bash(git log:*), Bash(git add:*), Bash(git commit:*), Bash(git push:*)
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
- 執行 git add, commit, push
- 提示使用者:「PROGRESS.md 已創建,請再次執行 /auto-fix-step 開始實作第一個項目」
- **結束執行** (不繼續執行項目)

### 第二步:執行單一項目

1. **找到目標項目**
   - 讀取 PROGRESS.md
   - 找到第一個 [ ] 或 [/] 狀態的項目
   - 如果所有項目都是 [x],跳到「第三步:歸檔」

2. **更新狀態為進行中**
   - 將該項目狀態由 [ ] 改為 [/]
   - 提交此狀態變更 (commit message: `chore: 開始項目 N - <項目摘要>`)

3. **執行修改**
   - 根據項目的「檔案範圍」和「摘要」進行修改
   - 使用 Edit 或 Write 工具修改相關檔案

4. **提交修改**
   - 遵循 Conventional Commits 規範
   - 提交訊息格式: `<type>: <description>`
   - 常用 type: feat, fix, docs, refactor, test, chore
   - 包含 Co-authored-by 標記

5. **更新 PROGRESS.md**
   - 將該項目狀態改為 [x]
   - 在該項目下方新增一行,記錄:
     ```markdown
     - [x] 項目 1: <摘要>
       - 檔案範圍: <相關檔案>
       - 驗收條件: <條件>
       - ✅ Commit: `<前7碼>` - <提交訊息摘要>
     ```
   - 提交此狀態更新 (commit message: `chore: 完成項目 N - <項目摘要>`)

6. **推送到遠端**
   - 執行 git push origin <當前分支>

7. **回報進度**
   - 在 GitHub 評論中顯示:
     - 已完成的項目
     - 剩餘的項目數量
     - 提示:「請再次執行 @claude /auto-fix-step 繼續下一個項目」

8. **結束執行** (不繼續下一個項目)

### 第三步:歸檔 (所有項目完成時)

當 PROGRESS.md 中所有項目都是 [x] 時:

1. **重新命名 PROGRESS.md**
   - 格式: `YYYYMMDD_<任務描述>.md`
   - 例如: `20251008_登入表單驗證.md`

2. **歸檔到 log_history/**
   - 檢查 log_history/ 資料夾是否存在
   - 如果不存在,創建該資料夾
   - 將重新命名的檔案移動到 log_history/
   - 刪除原本的 PROGRESS.md

3. **提交歸檔變更**
   - commit message: `chore: 歸檔任務 - <任務描述>`
   - 推送到遠端

4. **回報完成**
   - 在 GitHub 評論中顯示:
     - 所有已完成的項目
     - 總共的提交數量
     - 歸檔檔案的位置
     - ✅ 任務全部完成!

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
| log_history | ✅ 有 | ✅ 有 |

## 注意事項

- 此指令設計為「無互動」模式,適合 GitHub Actions 環境
- 每次執行只處理一個項目,需要多次觸發才能完成整個任務
- 透過 PROGRESS.md 檔案保持狀態,支援斷點續做
- 所有提交都遵循 Conventional Commits 規範
- 如果需要完整的互動式控制,請在本機環境使用 /auto-fix
