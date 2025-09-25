// TaskMaster 前端 JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // 初始化功能
    initializeApp();
});

function initializeApp() {
    // 初始化 tooltips
    initializeTooltips();

    // 設置表單驗證
    setupFormValidation();

    // 設置確認對話框
    setupConfirmDialogs();

    // 添加動畫效果
    addAnimations();
}

function initializeTooltips() {
    // 初始化 Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

function setupFormValidation() {
    const createTaskForm = document.getElementById('createTaskForm');
    if (createTaskForm) {
        createTaskForm.addEventListener('submit', function(e) {
            const titleInput = document.getElementById('title');
            if (!titleInput.value.trim()) {
                e.preventDefault();
                showAlert('請輸入任務標題', 'error');
                titleInput.focus();
            }
        });
    }
}

function setupConfirmDialogs() {
    // 刪除確認對話框
    const deleteButtons = document.querySelectorAll('.btn-delete');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const taskTitle = this.dataset.taskTitle || '此任務';

            if (confirm(`確定要刪除「${taskTitle}」嗎？此操作無法復原。`)) {
                // 提交刪除表單
                const form = this.closest('form');
                if (form) {
                    form.submit();
                }
            }
        });
    });
}

function addAnimations() {
    // 為新載入的元素添加淡入動畫
    const animatedElements = document.querySelectorAll('.stats-card, .task-card');
    animatedElements.forEach((element, index) => {
        element.style.animationDelay = `${index * 0.1}s`;
        element.classList.add('fade-in');
    });
}

function showAlert(message, type = 'info') {
    // 創建 alert 元素
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type === 'error' ? 'danger' : 'success'} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

    // 插入到頁面頂部
    const container = document.querySelector('.container');
    const firstChild = container.firstElementChild;
    container.insertBefore(alertDiv, firstChild);

    // 自動消失
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}

function updateTaskStatus(taskId, newStatus) {
    // 使用 AJAX 更新任務狀態
    const formData = new FormData();
    formData.append('status', newStatus);

    fetch(`/tasks/${taskId}/update`, {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            location.reload(); // 重新載入頁面以更新顯示
        } else {
            throw new Error('更新失敗');
        }
    })
    .catch(error => {
        showAlert('更新任務狀態失敗', 'error');
        console.error('Error:', error);
    });
}

function scrollToSection(sectionId) {
    const element = document.getElementById(sectionId);
    if (element) {
        element.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

// 快速狀態切換功能
function quickStatusToggle(taskId, currentStatus) {
    let newStatus;

    switch(currentStatus) {
        case 'pending':
            newStatus = 'in_progress';
            break;
        case 'in_progress':
            newStatus = 'completed';
            break;
        case 'completed':
            newStatus = 'pending';
            break;
        default:
            newStatus = 'pending';
    }

    updateTaskStatus(taskId, newStatus);
}

// 鍵盤快捷鍵支援
document.addEventListener('keydown', function(e) {
    // Ctrl + N: 聚焦到新任務輸入框
    if (e.ctrlKey && e.key === 'n') {
        e.preventDefault();
        const titleInput = document.getElementById('title');
        if (titleInput) {
            titleInput.focus();
        }
    }

    // ESC: 清空表單
    if (e.key === 'Escape') {
        const form = document.getElementById('createTaskForm');
        if (form && document.activeElement.tagName === 'INPUT' || document.activeElement.tagName === 'TEXTAREA') {
            form.reset();
        }
    }
});

// 自動刷新統計數據（可選功能）
function autoRefreshStats() {
    fetch('/api/stats')
        .then(response => response.json())
        .then(data => {
            updateStatsDisplay(data);
        })
        .catch(error => {
            console.error('Failed to refresh stats:', error);
        });
}

function updateStatsDisplay(stats) {
    const totalElement = document.querySelector('.stats-card.total .stats-number');
    const pendingElement = document.querySelector('.stats-card.pending .stats-number');
    const inProgressElement = document.querySelector('.stats-card.in-progress .stats-number');
    const completedElement = document.querySelector('.stats-card.completed .stats-number');

    if (totalElement) totalElement.textContent = stats.total;
    if (pendingElement) pendingElement.textContent = stats.pending;
    if (inProgressElement) inProgressElement.textContent = stats.in_progress;
    if (completedElement) completedElement.textContent = stats.completed;
}

// 每30秒自動刷新統計數據（可根據需要調整或移除）
// setInterval(autoRefreshStats, 30000);