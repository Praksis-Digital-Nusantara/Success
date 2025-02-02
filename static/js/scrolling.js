// Event untuk scroll
window.addEventListener('scroll', function() {
    var scroll = window.scrollY; // Mendapatkan nilai scroll
    console.log(scroll);

    // Ambil elemen dari DOM
    var myBody = document.getElementById("myBody");
    var myNav = document.getElementById("myNav");

    if (myBody) {
        // Ubah margin top sesuai scroll
        myBody.style.marginTop = (-400 - 0.5 * scroll) + "px";
    }

    if (myNav) {
        // Tambahkan atau hapus kelas "bg-dark" pada navigasi
        if (scroll >= 300) {
            myNav.classList.add("bg-dark");
        } else {
            myNav.classList.remove("bg-dark");
        }
    }
});

// Event untuk tombol scroll ke "myBody"
document.getElementById("btnHome").addEventListener("click", function() {
    var myBody = document.getElementById("myBody");

    // Periksa apakah elemen "myBody" ada
    if (myBody) {
        myBody.scrollIntoView({
            behavior: "smooth", // Animasi smooth scroll
            block: "start" // Posisikan elemen di bagian atas viewport
        });
    }
});
