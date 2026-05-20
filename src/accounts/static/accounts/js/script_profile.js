document.addEventListener('DOMContentLoaded', function() {
        const form = document.querySelector('.auth-card form');
        const msgBox = document.querySelector('.auth-messages');
        const submitBtn = form?.querySelector('button[type="submit"]');
        const avatarInput = document.getElementById('avatarInput');
        const avatarPreview = document.getElementById('avatarPreview');

        if (avatarInput && avatarPreview) {
            avatarInput.addEventListener('change', function(e) {
                const file = e.target.files[0];
                if (file && file.type.startsWith('image/')) {
                    const reader = new FileReader();
                    reader.onload = function(evt) {
                        if (avatarPreview.tagName === 'IMG') {
                            avatarPreview.src = evt.target.result;
                        } else {
                            avatarPreview.innerHTML = `<img src="${evt.target.result}" style="width:100%;height:100%;object-fit:cover;border-radius:50%;">`;
                        }
                    };
                    reader.readAsDataURL(file);
                }
            });
        }

        function showErrors(errors) {
            if (!msgBox) return;
            msgBox.innerHTML = '';
            const errorList = [];
            
            if (errors.__all__) errorList.push(...errors.__all__);
            for (const field in errors) {
                if (field !== '__all__') errorList.push(...errors[field]);
            }
            
            errorList.forEach(err => {
                const p = document.createElement('p');
                p.className = 'message error';
                p.textContent = err;
                p.style.cursor = 'pointer';
                p.onclick = function() { this.remove(); };
                msgBox.appendChild(p);
            });

            setTimeout(() => {
                msgBox.querySelectorAll('.message').forEach(m => {
                    m.style.opacity = '0';
                    m.style.transform = 'translateY(-10px)';
                    setTimeout(() => m.remove(), 300);
                });
            }, 5000);
        }
    });
