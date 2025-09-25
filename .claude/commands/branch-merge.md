---
allowed-tools: Bash(git config:*), Bash(git checkout:*), Bash(git merge:*), Bash(git status:*), Bash(git diff:*), Bash(git add:*), Bash(git commit:*), Bash(git log:*), Read, Edit
argument-hint: <來源分支> <目標分支>
description: 合併指定分支並處理合併衝突
---

# 共用流程
@.claude/commands/pack-zh.md
@.claude/commands/merge-report-template.md

# 分支合併與衝突處理流程

1. **確認分支**  
   - 目前所在分支：!`git branch --show-current`  
   - 顯示所有分支：!`git branch -a`  
   - 確認是否要把 **$1 (來源分支)** 合併到 **$2 (目標分支)**。  

> 請等待我回覆（是/否）再進行下一步。

2. **切換到目標分支**  
   - !`git checkout $2`  

3. **嘗試合併**
   請依照以下方法進行合併，不進行 Fast Forward 合併，且不自動提交:
   - !`git merge --no-ff --no-commit $1`  
   - 如果沒有衝突 → 自動跳至 '完成合併' 步驟，並依照指示進行提交。  
   - 如果有衝突 → 進入下一步。  

---

# 衝突檢查與解析

1. **列出衝突檔案**  
   - !`git status --short`  
   - !`git diff --name-only --diff-filter=U` → 作為 `$FILES`  

2. **顯示衝突內容**  
   - !`git diff`  
   - 請針對每個衝突區段，解析衝突原因，例如：  
     - 是否雙方修改了同一函式/變數  
     - 是否檔案結構或功能需求不同  

3. **給出解決建議**  
   - 保留來源分支版本  
   - 保留目標分支版本  
   - 手動合併（推薦修改方案，指出該如何整合）  

---

# 衝突解決互動
對於每個衝突區段，請提出以下選項：  
- `[1]` 保留來源分支版本（$1）  
- `[2]` 保留目標分支版本（$2）  
- `[3]` 建議人工合併 → 提出合併後的程式碼草案，並與我討論修改方針。

> 請嚴格依照上述互動流程進行，避免在未確認的情況下直接提交修改。 

---

# 人工合併討論
當使用者選擇 [3] 之後，進入「人工合併互動模式」：

1. 產生草案：系統先提供合併後的程式碼草案。
2. 在草案出來後，使用者可輸入以下指令進行互動：
   - confirm → 表示草案正確，可以進入下一步。
   - revise → 提出修改意見，系統依照意見調整草案，並再次提供新的版本。
   - continue → 表示草案已確認，並正式套用修改。

> 請嚴格依照上述互動流程進行，在輸入 continue 前，不會自動將修改正式套用。

---

# 完成合併
提交修改 → 請進行提交，訊息格式如下：
- `Merge branch '<來源分支>' 到 '<目標分支>' - <一句話描述>`
範例： Merge branch 'revised' 到 'main' - 新增登入功能
//
# 獲取提交資訊
- `$COMMIT` → !`git log -1 --pretty=format:"%h"`  
- `$MESSAGE` → !`git log -1 --pretty=format:"%s"`

---
# 合併報告輸出

完成合併後，請依照以下流程生成報告：  
@.claude/commands/merge-report-template.md  

依照以下規則替換模板變數：  
- `$DATE` → 當前日期（!`date +"%Y-%m-%d %H:%M:%S"`)  
- `$SOURCE` → 來源分支（$1 引數）  
- `$TARGET` → 目標分支（$2 引數）  
- `$USER` → 本地 git 使用者（!`git config user.name`）  
- `$FILES` → 衝突檔案列表  
- `$CAUSES` → 衝突原因分析  
- `$RESOLUTIONS` → 衝突解決方式，請同時列出合併後相對於目標分支的新增功能或改動  
- `$TESTS` → 條列式詳細驗證方法（例如「手動測試 GUI 正常」）  
- `$COMMIT` → 最後合併提交的 ID（前 7 碼）  
- `$MESSAGE` → 最後合併提交的訊息  

> 生成一份 `merge_logs/YYYYMMDD_HH-MM_merge_$SOURCE-into-$TARGET.md` 檔案，供團隊共享。

