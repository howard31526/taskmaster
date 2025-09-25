---
allowed-tools: Read, Edit, Bash(git branch:*), Bash(git status:*), Bash(git diff:*), Bash(git log:*), Bash(git add:*), Bash(git commit:*), Bash(git push:*)
argument-hint: <功能名稱或任務描述，例如：登入表單驗證>
description: 規劃→實作→逐步提交的工作流（一次一個功能，提交訊息標準化）
---

# 共用流程
@.claude/commands/pack-zh.md
@.claude/commands/commit-rules.md

# 規劃階段（先不要改碼，使用 plan mode）
在開始規劃前，請先檢查當前目錄是否存在 PROGRESS.md。

- 如果存在 PROGRESS.md → 請讀取它：
  - 對於 [ ] 的項目 → 照常使用，等待後續實作。  
  - 對於 [/] 的項目 → 問我是否要「重新規劃」這一項，還是「繼續上次的進度」。  
    - 若選擇重新規劃 → 覆寫該項的摘要與檔案範圍，狀態保持 [/]。  
    - 若選擇繼續 → 沿用原有規劃內容。  
- 如果不存在 PROGRESS.md → 請根據 $ARGUMENTS 的任務，生成一份新的 PROGRESS.md 草稿，格式需包含：  
  - 任務清單（[ ] 狀態）  
  - 每項任務的檔案範圍  
  - 每項任務的摘要（簡述要修改什麼）  
  - 狀態更新規則（[ ] → 未開始；[/] → 進行中；[x] → 完成）

在規劃時，請同時將最小可交付粒度限制在3-8項，以及有對應的驗收條件（可手測或極薄測試）

> 在輸出草稿後，請等待我的回覆：
> - 「confirm」 → 正式寫入 PROGRESS.md  
> - 「revise」 → 根據我的補充修改重新規劃


# 實作階段（一次只做一項）
在開始實作前，請先讀取 @PROGRESS.md，找到第一個狀態為 [ ] 或 [/] 的項目。

流程如下：
1) 根據 PROGRESS.md 的檔案範圍與摘要，先描述預計修改內容。  
2) 將該項目狀態由 [ ] 改為 [/]（表示進行中）。  
3) 使用 !`git diff` 比較修改前後差異，並解釋細節。  
4) 詢問我是否要套用（是/否）。  
   - **否** → 將該項保持為 [/]，暫停修改，等待我接下來的輸入。  
       - 如果我輸入「leave」 → 直接退出指令，下次再執行時會檢查 PROGRESS.md 裡的 [/] 項目，並詢問是否要重新規劃或繼續進行。
       - 如果我輸入「continue」 → 請參考我的建議再重新提交一次修改提案。
       - 其他輸入 → 請與我討論修改方針，直到輸入「continue」。
   - **是** → 執行修改。  
5) 提交修改 → 完整依照 @.claude/commands/pack-zh.md 的流程，但提交訊息必須依 @.claude/commands/commit-rules.md 格式。  
6) 更新 @PROGRESS.md，把該項目狀態改為 [x]，在該項目下方新增一行，記錄「Commit 編號（前 7 碼）」與「提交訊息摘要」。  
7) 如果 @PROGRESS.md 中全部完成：將 PROGRESS.md 重新命名為 YYYYMMDD_revisedContent.md（以當天日期命名）。
   - 如果有 log_history 資料夾，就幫我把此檔案儲存至其中，並刪除 @PROGRESS.md。
   - 如果沒有log_history 資料夾就幫我創建此檔案夾，並將檔案存至其中，並刪除 @PROGRESS.md。  

> 若我回覆「next」，繼續下一個項目；若我回覆「end」，則結束當前指令。