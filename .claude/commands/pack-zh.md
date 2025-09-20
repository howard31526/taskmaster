---
allowed-tools: Bash(git branch:*), Bash(git checkout:*), Bash(git add:*), Bash(git status:*), Bash(git commit:*), Bash(git log:*), Bash(git diff:*)
argument-hint: [要新增的檔案] 或使用 "." 代表所有檔案
description: 互動式Git工作流程與分支管理
---

請協助我執行互動式Git工作流程：

**第一步：檢查當前分支**
- 顯示目前所在分支：`git branch --show-current`
- 顯示所有分支：`git branch -a`

**第二步：確認分支**
詢問我：「您確定要在目前分支 [分支名稱] 上新增檔案嗎？（是/否）」

**第三步：如果回答「否」**
- 顯示所有可用分支
- 詢問我要：
  - 輸入現有分支名稱來切換
  - 或輸入「new」來建立新分支

**第四步：如果選擇「new」**
- 詢問新分支的名稱
- 使用 `git checkout -b [分支名稱]` 建立並切換到新分支

**第五步：新增檔案**
新增指定的檔案：$ARGUMENTS（如果沒有參數，預設使用 "."）

**第六步：顯示狀態**
執行 `git status` 顯示即將提交的內容

**第七步：產生提交訊息**
使用 `git diff --staged` 分析變更並建立適當的提交訊息

**第八步：執行提交**
使用產生的訊息執行提交

**第九步：顯示紀錄**
顯示 `git log --oneline -5` 來確認最近的提交

請在每個確認步驟等待我的回應，並使用繁體中文進行互動。