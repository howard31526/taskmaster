---
allowed-tools: Bash(git fetch:*), Bash(git checkout:*), Bash(git merge:*), Bash(git status:*), Bash(git diff:*), Bash(git add:*), Bash(git commit:*), Read, Edit
argument-hint: <來源分支> <目標分支>
description: 合併指定分支並處理合併衝突
---

# 共用流程
@.claude/commands/pack-zh.md
@.claude/commands/commit-rules.md
@.claude/commands/merge-report-template.md

# 分支合併與衝突處理流程

1. **確認分支**  
   - 目前所在分支：!`git branch --show-current`  
   - 顯示所有分支：!`git branch -a`  
   - 確認是否要把 **$1 (來源分支)** 合併到 **$2 (目標分支)**。  

2. **切換到目標分支**  
   - !`git checkout $2`  

3. **嘗試合併**  
   - !`git merge $1`  
   - 如果沒有衝突 → 自動完成合併，並顯示 `git log --oneline -5`。  
   - 如果有衝突 → 進入下一步。  

---

# 衝突檢查與解析

1. **列出衝突檔案**  
   - !`git status --short`  
   - !`git diff --name-only --diff-filter=U`  

2. **顯示衝突內容**  
   - !`git diff`  
   - 請針對每個衝突區段，解析衝突原因，例如：  
     - 是否雙方修改了同一函式/變數  
     - 是否檔案結構或功能需求不同  

3. **給出解決建議**  
   - 保留來源分支版本 (`theirs`)  
   - 保留目標分支版本 (`ours`)  
   - 手動合併（推薦修改方案，指出該如何整合）  

---

# 衝突解決互動
對於每個衝突區段，請提出以下選項：  
- `[1]` 保留來源分支版本（$1）  
- `[2]` 保留目標分支版本（$2）  
- `[3]` 建議人工合併 → 提出合併後的程式碼草案供我確認  

> 請等待我回覆選項後再進行修改。  

---

# 完成合併
提交修改 → 完整依照 @.claude/commands/pack-zh.md 的流程，但提交訊息必須依 @.claude/commands/commit-rules.md 格式。 

---
# 合併報告輸出

完成合併後，請依照以下流程生成報告：  
@.claude/commands/merge-report-template.md  

> 自動替換模板中的 $DATE、$SOURCE、$TARGET、$USER、$FILES、$CAUSES、$RESOLUTIONS、$TESTS、$COMMIT、$MESSAGE，  
> 生成一份 `merge_logs/YYYYMMDD_merge_$SOURCE-into-$TARGET.md` 檔案，供團隊共享。
