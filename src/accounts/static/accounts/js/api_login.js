document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('loginForm');
    const submitBtn = form?.querySelector('button[type="submit"]');
    
    if (!form) return;

    const inputs = form.querySelectorAll('input');
    
    inputs.forEach(input => {
        ['input', 'blur'].forEach(event => {
            input.addEventListener(event, function() {
                validateFieldRealtime(this);
            });
        });
    });

    function validateFieldRealtime(field) {
        const group = field.closest('.form-group');
        let errorInline = group?.parentElement?.querySelector('.error-inline');
        const value = field.value.trim();
        let errorMsg = '';

        if (field.required && !value) {
            errorMsg = 'Это поле обязательно для заполнения';
        }
        else if (field.minLength && value.length > 0 && value.length < field.minLength) {
            errorMsg = `Минимум ${field.minLength} символов`;
        }
        else if (field.type === 'email' && value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
            errorMsg = 'Введите корректный email';
        }

        if (errorMsg) {
            if (!errorInline) {
                errorInline = document.createElement('p');
                errorInline.className = 'error-inline';
                group.parentElement.appendChild(errorInline);
            }
            errorInline.textContent = errorMsg;
            group?.classList.add('has-error');
            return false;
        } else {
            if (errorInline && errorInline.classList.contains('error-inline')) errorInline.remove();
            group?.classList.remove('has-error');
            return true;
        }
    }

    function showFieldErrors(errors) {
        document.querySelectorAll('.error-server').forEach(el => el.remove());
        
        for (const field in errors) {
            const messages = Array.isArray(errors[field]) ? errors[field] : [errors[field]];
            let targetInput = null;
            
            if (field === 'username') targetInput = document.getElementById('username');
            else if (field === 'password') targetInput = document.getElementById('password');
            
            if (targetInput) {
                const group = targetInput.closest('.form-group');
                messages.forEach(msg => {
                    const p = document.createElement('p');
                    p.className = 'error-server';
                    p.textContent = msg;
                    group.parentElement.insertBefore(p, group.nextElementSibling || group.parentElement.lastElementChild.nextSibling);
                });
            }
        }
        
        if (errors.__all__) {
            errors.__all__.forEach(msg => {
                const p = document.createElement('p');
                p.className = 'error-server';
                p.textContent = msg;
                form.parentNode.insertBefore(p, form);
            });
        }
    }

    {% comment %} form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        let allValid = true;
        inputs.forEach(input => {
            if (!validateFieldRealtime(input)) allValid = false;
        });
        if (!allValid) return;

        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.dataset.original = submitBtn.innerHTML;
            submitBtn.innerHTML = '<i class="ti ti-loader"></i> Обработка...';
        }
        
        document.querySelectorAll('.error-inline, .error-server').forEach(el => el.remove());

        const formData = new FormData(this);
        const csrf = document.querySelector('[name=csrfmiddlewaretoken]')?.value;

        try {
            const res = await fetch(this.action, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrf || '',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: formData
            });

            const text = await res.text();
            let data;
            
            try {
                data = JSON.parse(text);
            } catch (e) {
                showFieldErrors({'__all__': ['Неверный логин или пароль']});
                return;
            }

            if (res.ok && data.redirect) {
                window.location.href = data.redirect;
            } else {
                showFieldErrors(data.errors || data.error || {'__all__': ['Ошибка валидации']});
            }
        } catch (err) {
            showFieldErrors({'__all__': ['Неверный логин или пароль']});
        } finally {
            if (submitBtn) {
                submitBtn.disabled = false;
                submitBtn.innerHTML = submitBtn.dataset.original || submitBtn.innerHTML;
            }
        }
    }); {% endcomment %}
    
    window.togglePassword = function(inputId, btn) {
        const input = document.getElementById(inputId);
        const icon = btn?.querySelector('i');
        if (!input || !icon) return;
        
        if (input.type === 'password') {
            input.type = 'text';
            icon.classList.replace('ti-eye', 'ti-eye-off');
        } else {
            input.type = 'password';
            icon.classList.replace('ti-eye-off', 'ti-eye');
        }
    };
});