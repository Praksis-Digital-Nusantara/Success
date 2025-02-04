
			const navToggle = document.querySelector('.nav-toggle');
			const navLinks = document.querySelector('.nav-links');
			const searchToggle = document.querySelector('.mobile-search-toggle');
			const searchContainer = document.querySelector('.search-container');
			const searchOverlay = document.querySelector('.search-overlay');
		
			navToggle.addEventListener('click', () => {
				// Close search if it's open
				if (searchContainer.classList.contains('active')) {
					searchContainer.classList.remove('active');
					searchOverlay.classList.remove('active');
					searchToggle.querySelector('i').classList.remove('ri-close-line');
					searchToggle.querySelector('i').classList.add('ri-search-line');
				}
				// Toggle nav menu
				navLinks.classList.toggle('active');
				navToggle.querySelector('i').classList.toggle('ri-menu-line');
				navToggle.querySelector('i').classList.toggle('ri-close-line');
			});
		
			searchToggle.addEventListener('click', () => {
				// Close nav menu if it's open
				if (navLinks.classList.contains('active')) {
					navLinks.classList.remove('active');
					navToggle.querySelector('i').classList.remove('ri-close-line');
					navToggle.querySelector('i').classList.add('ri-menu-line');
				}
				// Toggle search
				searchContainer.classList.toggle('active');
				searchOverlay.classList.toggle('active');
				searchToggle.querySelector('i').classList.toggle('ri-search-line');
				searchToggle.querySelector('i').classList.toggle('ri-close-line');
			});
		
			searchOverlay.addEventListener('click', () => {
				searchContainer.classList.remove('active');
				searchOverlay.classList.remove('active');
				searchToggle.querySelector('i').classList.remove('ri-close-line');
				searchToggle.querySelector('i').classList.add('ri-search-line');
			});

