// static/js/main.js
// JavaScript для взаимодействия с API и динамической загрузки товаров

// Глобальные переменные
let currentPage = 1;
let isLoading = false;

// Функция для показа уведомлений (Задание 6.3)
function showNotification(message, type = 'success') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed top-0 end-0 m-3`;
    alertDiv.style.zIndex = '9999';
    alertDiv.style.minWidth = '300px';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.body.appendChild(alertDiv);
    
    // Автоматическое скрытие через 3 секунды
    setTimeout(() => {
        alertDiv.remove();
    }, 3000);
}

// Функция показа/скрытия спиннера (Задание 6.4)
function toggleSpinner(show) {
    const spinner = document.getElementById('loading-spinner');
    if (spinner) {
        spinner.style.display = show ? 'block' : 'none';
    }
}

// Функция загрузки товаров из API (Задание 6.1)
async function loadProductsFromAPI(filters = {}) {
    toggleSpinner(true);
    isLoading = true;
    
    try {
        // Строим URL с параметрами фильтрации
        let apiUrl = '/api/products/';
        const params = new URLSearchParams();
        
        if (filters.category) params.append('category', filters.category);
        if (filters.manufacturer) params.append('manufacturer', filters.manufacturer);
        if (filters.search) params.append('search', filters.search);
        if (filters.page) params.append('page', filters.page);
        
        if (params.toString()) {
            apiUrl += '?' + params.toString();
        }
        
        const response = await fetch(apiUrl);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        renderProducts(data.results || data);
        
        // Показываем уведомление об успешной загрузке
        const count = data.results ? data.results.length : data.length;
        showNotification(`Загружено ${count} товаров`, 'info');
        
    } catch (error) {
        console.error('Ошибка загрузки товаров:', error);
        // Обработка ошибок (Задание 6.5)
        showNotification('Не удалось загрузить товары. Проверьте соединение.', 'danger');
        
        // Показываем сообщение об ошибке в контейнере
        const container = document.getElementById('products-container');
        if (container) {
            container.innerHTML = `
                <div class="col-12">
                    <div class="alert alert-danger text-center">
                        <i class="fas fa-exclamation-triangle"></i>
                        Ошибка загрузки товаров. Пожалуйста, обновите страницу.
                    </div>
                </div>
            `;
        }
    } finally {
        toggleSpinner(false);
        isLoading = false;
    }
}

// Функция рендеринга товаров
function renderProducts(products) {
    const container = document.getElementById('products-container');
    if (!container) return;
    
    if (!products || products.length === 0) {
        container.innerHTML = `
            <div class="col-12">
                <div class="alert alert-info text-center">
                    <i class="fas fa-info-circle"></i> Товары не найдены
                </div>
            </div>
        `;
        return;
    }
    
    let html = '';
    products.forEach(product => {
        const imageUrl = product.image || '/static/images/placeholder.jpg';
        const stockStatus = product.stock_quantity > 0 
            ? `<span class="badge bg-success">В наличии: ${product.stock_quantity} шт.</span>`
            : `<span class="badge bg-danger">Нет в наличии</span>`;
        
        html += `
            <div class="col-sm-6 col-md-6 col-lg-4 mb-4">
                <div class="card h-100 shadow-sm product-card">
                    <img src="${imageUrl}" class="card-img-top" alt="${product.name}" style="height: 200px; object-fit: cover;">
                    <div class="card-body">
                        <h5 class="card-title">${escapeHtml(product.name)}</h5>
                        <p class="card-text text-muted small">${escapeHtml(product.manufacturer_name || 'Производитель не указан')}</p>
                        <p class="card-text h4 text-primary">${product.price} ₽</p>
                        ${stockStatus}
                    </div>
                    <div class="card-footer bg-white border-top-0">
                        <button class="btn btn-outline-primary w-100 add-to-cart-btn" data-product-id="${product.id}">
                            Добавить в корзину
                        </button>
                    </div>
                </div>
            </div>
        `;
    });
    
    container.innerHTML = html;
    
    // Привязываем обработчики к кнопкам добавления в корзину
    document.querySelectorAll('.add-to-cart-btn').forEach(btn => {
        btn.removeEventListener('click', handleAddToCart);
        btn.addEventListener('click', handleAddToCart);
    });
}

// Функция для экранирования HTML (безопасность)
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Обработчик добавления в корзину (Задание 6.2)
async function handleAddToCart(event) {
    const button = event.currentTarget;
    const productId = button.getAttribute('data-product-id');
    
    // Проверяем, авторизован ли пользователь
    const isAuthenticated = document.body.getAttribute('data-user-authenticated') === 'true';
    
    if (!isAuthenticated) {
        showNotification('Пожалуйста, войдите в систему', 'warning');
        setTimeout(() => {
            window.location.href = '/accounts/login/';
        }, 1500);
        return;
    }
    
    // Сохраняем оригинальный текст кнопки
    const originalText = button.innerHTML;
    button.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Добавление...';
    button.disabled = true;
    
    try {
        // Получаем CSRF токен
        const csrftoken = getCookie('csrftoken');
        
        const response = await fetch(`/cart/add/${productId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
                'X-Requested-With': 'XMLHttpRequest'
            },
            credentials: 'same-origin'
        });
        
        if (response.redirected) {
            // Если произошел редирект, значит товар добавлен
            showNotification('Товар успешно добавлен в корзину!', 'success');
            button.innerHTML = '<i class="fas fa-check"></i> Добавлено';
            setTimeout(() => {
                button.innerHTML = originalText;
                button.disabled = false;
            }, 2000);
        } else if (response.ok) {
            const data = await response.json();
            showNotification(data.message || 'Товар добавлен в корзину', 'success');
        } else {
            throw new Error('Ошибка при добавлении');
        }
        
    } catch (error) {
        console.error('Ошибка:', error);
        showNotification('Не удалось добавить товар. Попробуйте позже.', 'danger');
        button.innerHTML = originalText;
        button.disabled = false;
    }
}

// Функция для получения CSRF cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    // Устанавливаем флаг аутентификации
    const userAuthenticated = document.body.getAttribute('data-user-authenticated') === 'true';
    
    // Проверяем, находимся ли мы на странице каталога
    const isCatalogPage = window.location.pathname.includes('/catalog/');
    
    if (isCatalogPage) {
        // Получаем параметры фильтров из URL
        const urlParams = new URLSearchParams(window.location.search);
        const filters = {
            category: urlParams.get('category'),
            manufacturer: urlParams.get('manufacturer'),
            search: urlParams.get('search'),
            page: urlParams.get('page')
        };
        
        // Загружаем товары через API
        loadProductsFromAPI(filters);
    }
    
    // Добавляем обработчики для форм фильтрации
    const filterForm = document.getElementById('filter-form');
    if (filterForm) {
        filterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(filterForm);
            const params = new URLSearchParams();
            
            for (let [key, value] of formData.entries()) {
                if (value) params.append(key, value);
            }
            
            window.location.href = `/catalog/?${params.toString()}`;
        });
    }
});

// Экспортируем функции для использования в других местах
window.showNotification = showNotification;
window.loadProductsFromAPI = loadProductsFromAPI;
window.handleAddToCart = handleAddToCart;