# IMPORTANT! 
Anto : PULL dulu kak, baru kita push perubahan ta' :)
Risal : Ok sudah, untuk mysql ada sudah saya masukkan, coba saja import nanti
Anto: Project saya running di dbsqlite3 kak, folder /aam /acd/ saya gitignore dulu, saya pull model baru ta, dan sy tidak push /aam sama /acd

# Cara Pull
`git pull origin main` 

# Cara Push
`git add .`
`git commit -m "message"`
`git push origin main`

# MODAL 

```html
<div id="nomorsurat" class="modal-edit">
	<div class="modal-content-edit">
		<span class="close" onclick="closeModal('nomorsurat')">&times;</span>
		<h2>Perihal dan Tujuan</h2>
		<form method="post" enctype="multipart/form-data">
			{% csrf_token %}
		<div class="form-group">
			<label style="text-align: left;">Perihal</label>
			{{ form.perihal }}
		</div>
		<div class="form-group">
			<label style="text-align: left;">Tujuan</label>
			{{ form.tujuan }}
		<button type="submit" class="btn primary">
			<i class="ri-save-line"></i>
			Update Data
		</button>
	</form>
	</div>
</div>
```

```js
<script>
    function openModal(modalId) {
        var modal = document.getElementById(modalId);
        modal.style.display = "block";
    }

    function closeModal(modalId) {
        var modal = document.getElementById(modalId);
        modal.style.display = "none";
    }

    window.onclick = function(event) {
        var modals = document.getElementsByClassName('modal-edit');
        for (var i = 0; i < modals.length; i++) {
            if (event.target == modals[i]) {
                modals[i].style.display = "none";
            }
        }
    }
</script>
```


# folder css 
- main/styles.css


# Dokumentasi SetUP Git to collaborate with my team
- `git config --list`
- `git checkout main`
- `git fetch origin` 
- `git pull origin main`
- `git checkout your-branch-name`
- `git merge main`
- `git pull origin main` 
- `git add .`
- `git commit -m "Merge main and resolve conflicts"`

# 