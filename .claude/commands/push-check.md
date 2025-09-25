---
allowed-tools: Bash(git fetch:*), Bash(git status:*), Bash(git branch:*), Bash(git diff:*), Bash(git pull:*), Bash(git push:*), Bash(git log:*), Read, Write
argument-hint: <目標分支>
description: 上傳前的自動化分支檢查與安全推送
---

# 共用流程
@.claude/commands/branch-merge.md

# 上傳前分支檢查與自動化推送

1. **確認當前分支**  
   - 顯示目前所在分支：!`git branch --show-current`    
   - 顯示所有分支：!`git branch -a`  
   - 詢問是否確定要將當前分支推送到遠端（或改推送到 $1 分支）。  

2. **檢查本地狀態**  
   - !`git status -s`  
   - 如果有未追蹤或未提交的檔案 → 詢問是否先提交（呼叫 @.claude/commands/pack-zh.md）。  

3. **檢查遠端同步**  
   - !`git fetch origin`  
   - !`git status -uno`  

   - 如果本地 **落後於遠端**：  
     - 首先嘗試 `git pull --rebase origin <分支>`：  
       - 如果 rebase 成功 → 繼續進入推送步驟。  
       - 如果 rebase 過程中發生衝突 → 進入互動式解決，讓使用者選擇：  
         - `[1]` `/branch-merge origin/<分支> <分支>` → 使用自訂合併流程，保留完整歷史並處理衝突。  
         - `[2]` 手動處理 → 結束腳本，交給使用者自行處理（例如特殊策略：squash、cherry-pick、patch）。  

        > 請等待我作決定（[1]/[2]）

   - 如果本地 **超前或同步** → 可直接推送。  

4. **推送分支**  
   - !`git push origin <分支名稱>`  
   - 完成後顯示 `git log --oneline -5`，確認最新紀錄。  

---

# 推送安全規範
- 禁止自動使用 `--force`，除非使用者明確輸入「force」。  
- 若出現推送被拒絕的錯誤，必須提示先行同步遠端再推送。  

---

# 額外輸出
- 推送完成後，自動輸出一份簡單報告，包含：  
  - $DATE：當前日期（!`date +"%Y-%m-%d %H:%M:%S"`)    
  - $BRANCH：推送分支  
  - $USER：本地 git 使用者（!`git config user.name`）
  - $COMMITS：此次推送的 commit 紀錄（前 5 筆）  
- 檔案輸出至 `push_logs/YYYYMMDD_HH-MM_push_$BRANCH.md`，供團隊追蹤。  

