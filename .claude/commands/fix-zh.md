---
allowed-tools: Read, Edit, Bash(git branch:*), Bash(git status:*), Bash(git diff:*), Bash(git log:*), Bash(git add:*), Bash(git commit:*), Bash(git push:*)
argument-hint: <功能名稱或任務描述，例如：登入表單驗證>
description: 規劃→實作→逐步提交的工作流（一次一個功能，提交訊息標準化）
---

# 共用流程
@.claude/commands/pack-zh.md

# 規劃階段（先不要改碼，使用 plan mode）
你現在的任務是：$ARGUMENTS

請先「只輸出」以下內容，不要修改任何檔案：
1) 受影響檔案與關鍵區塊（路徑＋行數範圍）
2) 要補齊的子功能清單（最小可交付粒度，約 3–7 項）
3) 風險與回滾策略
4) 驗收條件（可手測或極薄測試）

（提示：目前分支：!`git branch --show-current`；工作樹狀態：!`git status -s`）

> 等我回覆「確認第 N 項」後，才開始實作第 N 項。未授權前禁止編輯檔案。


# 實作階段（一次只做一項）
當我回覆「確認第 N 項」，請依序執行：
1) 先在文字中說明「預期的修改方式」與「影響檔案」
2) 使用 !`git diff` 顯示修改前後的差異
3) 解釋這些修改的細節，並在最後詢問我：「是否要套用這些修改？請回覆 是 或 否」
4) 如果我回覆「是」，才進行 Edit 修改並繼續後續流程
5) 如果我回覆「否」，則暫停修改，等待我提供手動調整；當我輸入「restart」，才繼續往下
6)  **提交修改**  
   - 請完全依照 @.claude/commands/pack-zh.md 的提交流程進行互動（包含分支確認、新建分支、顯示狀態等步驟）。  
   - 唯一的差異：當進入「產生提交訊息」的步驟時，請覆蓋使用 @.claude/commands/commit-rules.md 中定義的訊息格式。 

> 若我回覆「next」，重複上面流程；若我回覆「end」，才跳出當前指令

