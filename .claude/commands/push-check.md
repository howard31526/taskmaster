---
allowed-tools: Bash(git fetch:*), Bash(git status:*), Bash(git branch:*), Bash(git diff:*), Bash(git pull:*), Bash(git push:*), Bash(git log:*), Read, Write
argument-hint: <目標分支>
description: 上傳前的自動化分支檢查與安全推送
---

# 共用流程
@.claude/commands/branch-merge.md
@.claude/commands/pack-zh.md

# 上傳前分支檢查與自動化推送

1. **確認分支狀態**  
   - 顯示本地當前分支：!`git branch --show-current` → $本地分支  
   - 顯示所有分支：!`git branch -a`  

   - 判斷 $本地分支 與 $目標分支：  
     - 若相同 → 進入正常流程。  
     - 若不同 → 提示：  
       ```
       你目前在本地分支 $本地分支，但指定推送目標為 $目標分支。
       這將執行：git push origin $本地分支:$目標分支
       是否確認要這樣推送？
       [1] 確認推送
       [2] 改為切換到 $目標分支 分支
       [3] 取消
       ```

2. **檢查本地狀態**  
   - !`git status -s`
   - **檢查 `.gitignore`**  
     - 若不存在 → 自動建立並加入基礎規則（如 `.env`、`*.key`、`__pycache__/`）。  
     - 若已存在 → 檢查當前分支是否包含其他敏感檔案未歸入規則內，缺少時詢問是否補上。

   - 如果有未追蹤或未提交的檔案 → 詢問是否先提交（呼叫 @.claude/commands/pack-zh.md）。  

3. **檢查遠端同步**  

   - 僅在 $本地分支 = $目標分支 時執行以下檢查：  
     - !`git fetch origin`  
     - !`git status -uno`  

     - 若本地 **落後於遠端**：  
       - 嘗試 `git pull --rebase origin $目標分支`  
         - rebase 成功 → 繼續推送  
         - rebase 衝突 → 進入互動式解決：  
           - [1] `/branch-merge origin/$目標分支 $目標分支`  
           - [2] 手動處理→ 結束流程，交由使用者自行採用其他策略（例如 squash、cherry-pick、patch）

     - 若本地 **超前或同步** → 可直接推送。  

   - 若 $本地分支 ≠ $目標分支 → 跳過 rebase/merge，直接進入推送步驟。  

4. **推送分支**  
   - 若 $本地分支 = $目標分支 →  
     !`git push $遠端 $目標分支`  

   - 若 $本地分支 ≠ $目標分支 →  
     !`git push $遠端 $本地分支:$目標分支`  

   - **若推送被拒絕**：  
     - 表示遠端 $目標分支 上有新的提交，必須先同步。  
     - 系統詢問如何處理：  
       - `[1]` 嘗試 `git pull --rebase origin $目標分支` → 若衝突則交給 `/branch-merge origin/$目標分支 $目標分支`  
       - `[2]` 使用 `/branch-merge origin/$目標分支 $目標分支` → 保留完整歷史並處理衝突  
       - `[3]` 手動處理 → 結束流程，交由使用者自行採用其他策略（例如 squash、cherry-pick、patch）


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

