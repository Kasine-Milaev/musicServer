console.log('[api_validate.js] LOADED');

window.initRealtimeValidation = function() {
    const form = document.getElementById('registerForm');
    if (!form) { console.error('form#registerForm not found'); return; }
    
    const validateUrl = form.dataset.validateUrl;
    const csrfToken = form.dataset.csrf;
    if (!validateUrl) { console.error('validateUrl not found'); return; }
    
    const API_FIELDS = ['username', 'email', 'password1'];
    const timers = {};
    
    function debounce(func, delay, key) {
        return function(...args) {
            clearTimeout(timers[key]);
            timers[key] = setTimeout(() => func.apply(this, args), delay);
        };
    }
    
    function validateClientSide(field) {
        const group = field.closest('.form-group');
        const oldErr = group?.querySelector('.error-inline');
        if (oldErr) oldErr.remove();
        group?.classList.remove('has-error');
        
        const value = field.value.trim();
        let errorMsg = '';
        
        if (field.required && !value) {
            errorMsg = 'Это поле обязательно для заполнения';
        } else if (field.minLength && value.length > 0 && value.length < field.minLength) {
            errorMsg = `Минимум ${field.minLength} символов`;
        } else if (field.type === 'email' && value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
            errorMsg = 'Введите корректный email';
        } else if (field.id === 'password2') {
            const pass1 = document.getElementById('password1');
            if (pass1 && value && pass1.value !== value) {
                errorMsg = 'Пароли не совпадают';
            }
        }
        
        if (errorMsg) {
            const errEl = document.createElement('p');
            errEl.className = 'error-inline';
            errEl.textContent = errorMsg;
            group?.appendChild(errEl);
            group?.classList.add('has-error');
            return false;
        }
        return true;
    }
    
    async function checkFieldAPI(field) {
        const value = field.value.trim();
        if (!value) return;
        
        const group = field.closest('.form-group');
        const backendField = (field.id === 'password1') ? 'password' : field.id;
        const payload = { field: backendField, value: value };
        
        try {
            const res = await fetch(validateUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken || '' },
                body: JSON.stringify(payload)
            });
            const data = await res.json();
            
            if (data.valid === false && data.message) {
                const oldErr = group?.querySelector('.error-inline');
                if (oldErr) oldErr.remove();
                const errEl = document.createElement('p');
                errEl.className = 'error-inline';
                errEl.textContent = data.message;
                group?.appendChild(errEl);
                group?.classList.add('has-error');
            }
        } catch (err) {
            console.error('fetch error:', err);
        }
    }
    
    async function handleField(field) {
        const clientValid = validateClientSide(field);
        if (clientValid && API_FIELDS.includes(field.id)) {
            await checkFieldAPI(field);
        }
    }
    
    const debouncedCheck = debounce(handleField, 400, 'fieldCheck');
    const allFields = [...API_FIELDS, 'password2'];
    
    allFields.forEach(fieldId => {
        const input = document.getElementById(fieldId);
        if (input) {
            input.addEventListener('input', () => debouncedCheck(input));
            input.addEventListener('blur', () => handleField(input));
        }
    });
    
    console.log('[api_validate] listeners attached');
};